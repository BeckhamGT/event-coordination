#!/usr/bin/env python3
"""Execute the nine observed boundaries; default is live public-source reads."""
import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from jsonschema import Draft202012Validator, FormatChecker
from planning import FIELDS, KEYS, SOURCE_IDS, aware, build_model, build_programme, date_only, generate_options, programme_checks, rec
from rendering import ARTIFACTS, render, validate_outputs
from sources import InputError, capture, digest, now, parse_table, write_json

STAGES = ("scope-and-approval-gates", "source-capture", "constraint-model", "planning-baseline", "option-generation", "feasibility-testing", "decision-and-approval", "draft-propagation", "publication-validation")


def configuration():
    return json.loads((SCRIPT_DIR.parent/"references/project.json").read_text())


def archive_current(root):
    directory = root/"deliverables"
    if directory.is_symlink():
        raise InputError("Symlinked deliverables directory is unsafe")
    if directory.exists() and any(p.is_symlink() for p in directory.rglob("*")):
        raise InputError("Symlinked generated/history member is unsafe")
    meta = next((p for p in (directory/"run.json", directory/"preparation-run.json") if p.is_file()), None)
    if meta is None:
        return None, {}, []
    old = json.loads(meta.read_text())["run_id"]
    if not isinstance(old, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,120}", old):
        raise InputError("Unsafe prior run identity")
    destination = directory/"history"/old
    if destination.exists():
        raise InputError("History already exists for current run; refusing overwrite:"+old)
    previous_sources, anomalies = {}, []
    registry = directory/"snapshots/evidence/source-registry.json"
    if registry.exists():
        try:
            previous_sources = {s["id"]: s.get("content_hash") for s in json.loads(registry.read_text()).get("sources", [])}
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            anomalies.append("Invalid prior source registry; old hashes unavailable: " + type(error).__name__)
    members = [p for p in directory.iterdir() if p.name != "history"]
    destination.mkdir(parents=True)
    preserved = []
    for member in members:
        target = destination/member.name
        if member.is_dir():
            shutil.copytree(member, target)
        else:
            shutil.copy2(member, target)
        for saved in ([target] if target.is_file() else sorted(target.rglob("*"))):
            if saved.is_file():
                original = directory/saved.relative_to(destination)
                if saved.read_bytes() != original.read_bytes():
                    raise InputError("Archive copy mismatch")
                preserved.append({"original_path": str(original.relative_to(root)), "archived_path": str(saved.relative_to(root)), "sha256": digest(saved.read_bytes())})
    # Validate actual old output hashes before trusting historical success; preserve failures too.
    final = directory/"snapshots/09-publication-validation.json"
    if final.exists():
        try:
            try:
                _chain_check(root)
            except Exception as chain_error:
                anomalies.append("Invalid prior snapshot/source chain:"+str(chain_error))
            for artifact in json.loads(final.read_text())["state"]["artifacts"]:
                if artifact["path"] not in {"deliverables/"+name for name in ARTIFACTS}:
                    raise InputError("Unsafe prior artifact path")
                path = root/artifact["path"]
                if not path.exists() or digest(path.read_bytes()) != artifact["sha256"]:
                    anomalies.append("Missing/corrupt prior output:"+artifact["path"])
        except Exception as error:
            anomalies.append("Invalid prior stage09:"+type(error).__name__)
    write_json(destination/"history-manifest.json", {"run_id": old, "retained_at": now(), "files": preserved, "observed_anomalies": anomalies, "path_resolution": "Resolve original_path through explicit archived_path; do not follow old root paths into new current run"})
    # Reversible removal: every byte was verified in history first. Only generated
    # deliverables are touched; canonical interview/source config is never moved.
    for member in members:
        if member.is_dir():
            shutil.rmtree(member)
        else:
            member.unlink()
    return old, previous_sources, anomalies


def _record_decisions(config):
    return [dict(rec("D-L-01", "Use245 baseline,no extra margin;forecast35 medium-confidence walk-ins already included", ["E-LEARNER"]), rationale="User recorded this choice in actual captured conversation", tradeoffs=["Q-003 has15 spare at245;attendance above260 requires reevaluation"]), dict(rec("D-L-02", "CompareQ-003/Q-004;retain communications25000 and contingency40000;Q-003 preliminary preference", ["E-LEARNER"]), rationale="Baseline covered with greater headroom;keep extra-capacity alternative", tradeoffs=["Contingency included;remaining headroom counted separately"]), dict(rec("D-L-03", "Exclude livestream from base;retain rejected alternative", ["E-LEARNER"]), rationale="Over overall ceiling and production limit;network test uncompleted", tradeoffs=["No category approval can override total ceiling"]), dict(rec("D-L-04", "Use Python pipeline,nine boundaries,independent validation and recovery", ["E-LEARNER"]), rationale="User accepted design and requires actual cross-checks", tradeoffs=["No planned test reported as passed;source failures remain traceable"])]


def _chain_check(root, expected=9):
    schema = json.loads((root/"snapshot.schema.json").read_text())
    fc = FormatChecker()
    @fc.checks("date-time")
    def dt(value):
        if not isinstance(value, str):
            return True
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
        except ValueError:
            return False
    validator = Draft202012Validator(schema, format_checker=fc)
    records, run_id, identifiers = set(), None, set()
    registry = json.loads((root/"deliverables/snapshots/evidence/source-registry.json").read_text())
    evidence = {s["id"] for s in registry["sources"]} | {"E-LEARNER", "E-INTERVIEW", "E-CLARIFICATION"}
    snapshots = sorted((root/"deliverables/snapshots").glob("[0-9][0-9]-*.json"))
    if len(snapshots) != expected:
        raise InputError("Unexpected snapshot count")
    for index, path in enumerate(snapshots):
        data = json.loads(path.read_text())
        validator.validate(data)
        run_id = data["run_id"] if run_id is None else run_id
        if data["run_id"] != run_id or data["snapshot_id"] in identifiers or data["stage"] != STAGES[index]:
            raise InputError("Snapshot identity/run/sequence binding failure")
        identifiers.add(data["snapshot_id"])
        if not set(data["consumed_record_ids"]) <= records:
            raise InputError("Unresolved consumed record references")
        if index:
            previous = data["predecessor"]
            prior = snapshots[index-1]
            if previous["path"] != str(prior.relative_to(root)):
                raise InputError("Unsafe or incorrect predecessor path")
            if digest(prior.read_bytes()) != previous["sha256"] or json.loads(prior.read_text())["snapshot_id"] != previous["snapshot_id"]:
                raise InputError("Predecessor binding failure")
        def check(value):
            if isinstance(value, dict):
                if not set(value.get("evidence_ids", [])) <= evidence:
                    raise InputError("Unresolved evidence reference")
                for sub in value.values():
                    check(sub)
            elif isinstance(value, list):
                for sub in value:
                    check(sub)
        check(data)
        records.update(data["produced_record_ids"])
    for source in registry["sources"]:
        if source.get("content_hash") and source.get("local_reference"):
            relative = Path(source["local_reference"])
            if relative.is_absolute() or ".." in relative.parts or relative.parts[:3] != ("deliverables", "snapshots", "evidence"):
                raise InputError("Unsafe source reference path")
            if digest((root/source["local_reference"]).read_bytes()) != source["content_hash"]:
                raise InputError("Source hash mismatch:"+source["id"])
    return {"valid": True, "checks": ["Schema/date-time validation", "Unique snapshot IDs and one run", "Immediate predecessor bytes,IDs and hashes", "Consumed/produced records and evidence references", "Actual retained source hashes"]}


def run(root, config=None, source_bundle=None):
    root = Path(root).resolve()
    config = copy.deepcopy(config or configuration())
    # Policy dictionaries can be supplied for controlled tests; defaults remain
    # the actual recorded user choices, never a facilitator-approval gate.
    policy = config.setdefault("policy", configuration()["policy"])
    schema = root/"snapshot.schema.json"
    expected_hash = config.get("expected_schema_sha256", configuration()["expected_schema_sha256"])
    if hashlib.sha256(schema.read_bytes()).hexdigest() != expected_hash:
        raise InputError("Supplied schema changed; refusing execution")
    previous, old_sources, old_anomalies = archive_current(root)
    prior_scope, prior_failures = {}, []
    if previous:
        history = root/"deliverables/history"/previous
        try:
            scope_path = history/"snapshots/01-scope-and-approval-gates.json"
            if scope_path.exists():
                prior_scope = json.loads(scope_path.read_text()).get("state", {})
                if not isinstance(prior_scope, dict):
                    raise InputError("Prior scope state is not an object")
            prior_registry = history/"snapshots/evidence/source-registry.json"
            if prior_registry.exists():
                prior_failures = [s["id"] for s in json.loads(prior_registry.read_text()).get("sources", []) if s["retrieval_status"] != "retrieved"]
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            prior_scope, prior_failures = {}, []
            old_anomalies.append("Prior change provenance unavailable after verified archival: " + type(error).__name__)
    prior_policy = prior_scope.get("policy")
    decision_fields = {
        "D-L-01": ("baseline_people", "extra_margin_people"),
        "D-L-02": ("communications_allowance_twd", "contingency_allowance_twd", "preferred_caterer"),
        "D-L-03": ("livestream_in_base",),
    }
    changed_decisions = list(policy["decision_ids"]) if not previous else [] if not isinstance(prior_policy, dict) else [identity for identity, fields in decision_fields.items() if any(prior_policy.get(key) != policy.get(key) for key in fields)]
    if prior_scope.get("facilitator_signoff_required") is True:
        changed_decisions.append("D-CLARIFICATION")
    implementation_hashes = {str(p.relative_to(SCRIPT_DIR.parent)): digest(p.read_bytes()) for p in sorted(SCRIPT_DIR.parent.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}
    run_id = "run-"+datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    directory = root/"deliverables"
    evidence = directory/"snapshots/evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    mode = "live remote retrieval" if source_bundle is None else "explicit observed-source audit/test;original retrieval metadata retained"
    decisions = _record_decisions(config)
    stages, pending = [], []
    active_stage = 1

    def snapshot(number, state, produced, status=None):
        nonlocal active_stage
        active_stage = number
        status = status or ("partial" if pending else "complete")
        predecessor = None
        if stages:
            p = directory/"snapshots"/(str(number-1).zfill(2)+"-"+STAGES[number-2]+".json")
            predecessor = {"snapshot_id": stages[-1]["snapshot_id"], "path": str(p.relative_to(root)), "sha256": digest(p.read_bytes())}
        record = {"schema_version": "event-coordination-stage-snapshot/2", "snapshot_id": run_id+"-"+str(number).zfill(2), "run_id": run_id, "stage": STAGES[number-1], "sequence": number, "created_at": now(), "status": status, "predecessor": predecessor, "consumed_record_ids": stages[-1]["produced_record_ids"] if stages else [], "produced_record_ids": produced, "state": state, "unresolved": copy.deepcopy(pending), "decisions": decisions}
        path = directory/"snapshots"/(str(number).zfill(2)+"-"+STAGES[number-1]+".json")
        write_json(path, record)
        stages.append(record)
        return record
    try:
        interview = root/config.get("interview", configuration()["interview"])
        interview_hash = config.get("interview_sha256", configuration()["interview_sha256"])
        if not interview.is_file() or hashlib.sha256(interview.read_bytes()).hexdigest() != interview_hash:
            raise InputError("Original interview missing/changed")
        write_json(evidence/"learner-choice-basis.json", {"id": "E-LEARNER", "policy": policy, "decisions": decisions, "source": "Actual user choices in recorded Codex conversation;see committed preparation record", "clarification": "Onboarding covers identity;remaining checks are self-checks,no facilitator sign-off", "clarification_type": "User-reported facilitator process clarification,not approval"})
        snapshot(1, {"objective": "Produce consistent review-ready Quillhaven Demo Day planning drafts", "decision_deadline": config["decision_deadline"], "owners": ["Operations", "Learner Experience", "Programme", "Communications", "Category budget owners"], "approval_gates": ["Operations reviews plan,date and venue", "Category owners approve spending/threshold exceptions subject to overall ceiling", "No bookings,payments,sends or production-calendar changes"], "business_clock": config["business_clock"], "facilitator_signoff_required": False, "clarification": "Onboarding covers identity;technical setup self-checked;not an approval record", "supersedes_run_id": previous, "changed_decision_ids": changed_decisions, "changed_source_ids": [], "change_detection": "Fresh reads follow;actual changed source hashes recorded at02 without backfilling01. Unchanged recorded choices are not new decisions.", "sources_to_revalidate": [s["id"] for s in config["sources"]], "prior_failed_source_ids": prior_failures, "reason": "Retry recorded source failures and revalidate using current implementation" if prior_failures else "Verify source and output integrity with current implementation and preserved learner choices", "implementation_hashes": implementation_hashes, "mode": mode, "policy": policy, "prior_output_anomalies": old_anomalies, "interview": {"path": str(interview.relative_to(root)), "sha256": digest(interview.read_bytes())}}, ["SCOPE", "E-INTERVIEW", "E-LEARNER", "E-CLARIFICATION"]+[d["id"] for d in decisions])
        active_stage = 2
        # Reads are independent; interpretation waits for every observed result.
        with ThreadPoolExecutor(max_workers=7) as workers:
            sources = list(workers.map(lambda spec: capture(spec, evidence, config["visual_review"], source_bundle), config["sources"]))
        tables = {}
        for source, spec in zip(sources, config["sources"]):
            if spec["name"] in FIELDS and source["retrieval_status"] == "retrieved":
                try:
                    table = parse_table(evidence/spec["filename"], FIELDS[spec["name"]], KEYS[spec["name"]])
                    build_model({spec["name"]: table}, policy, "", include_programme=False)
                    if spec["name"] == "vendor-register":
                        for row in table:
                            date_only(row["available_date"])
                            date_only(row["valid_until"])
                    tables[spec["name"]] = table
                    source["version_metadata"]["record_versions"] = sorted({r["record_version"] for r in table if "record_version" in r})
                    source["record_ids"] = [row[KEYS[spec["name"]]] for row in table]
                except Exception as error:
                    source["retrieval_status"] = "invalid"
                    source["interpretation_error"] = str(error)
            if source["retrieval_status"] != "retrieved":
                pending.append(rec("U-"+source["id"], "Source "+source["retrieval_status"]+";dependent claims withheld:"+str(source.get("interpretation_error", "see actual attempt records")), [source["id"]], "Operations / source owner"))
        write_json(evidence/"source-registry.json", {"run_id": run_id, "mode": mode, "sources": sources, "additional_evidence": {"E-LEARNER": "deliverables/snapshots/evidence/learner-choice-basis.json", "E-CLARIFICATION": "deliverables/snapshots/evidence/learner-choice-basis.json", "E-INTERVIEW": str(interview.relative_to(root))}})
        changed = [s["id"] for s in sources if old_sources.get(s["id"]) != s.get("content_hash")]
        snapshot(2, {"sources": sources, "changed_source_ids": changed, "mode": mode, "interpretation_not_yet_completed": True}, [s["id"] for s in sources]+[identity for s in sources for identity in s.get("record_ids", [])])
        active_stage = 3
        brief_source = next(s for s in sources if s["id"] == "E-BRIEF")
        brief = (evidence/"event-brief-and-venue-note.txt").read_text() if brief_source["retrieval_status"] == "retrieved" else ""
        model = build_model(tables, policy, brief, include_programme=False)
        floor = next(s for s in sources if s["id"] == "E-FLOOR")
        index = next(s for s in sources if s["id"] == "E-ACCESS")
        model["media_verified"] = floor["retrieval_status"] == "retrieved" and floor.get("visual_review_verified_by_hash", False) and index["retrieval_status"] == "retrieved"
        model["source_failures"] = [s["id"] for s in sources if s["retrieval_status"] != "retrieved"]
        model["business_clock"] = config["business_clock"]
        if not model["media_verified"]:
            model["unknowns"].append(rec("U-VISUAL", "Official media is unavailable/changed/unreviewed; dependent spatial claims withheld", ["E-FLOOR", "E-ACCESS"], "Operations"))
        pending.extend(model["unknowns"])
        model["programme"] = []
        snapshot(3, {"hard_constraints": [rec("HC-CEILING", "Total ceiling520000;categoryapprovalcannotraiseit", ["E-BUDGET", "E-LEARNER"]), rec("HC-ACCESS", "Step-free access,wheelchair seating,captions,hearing-loop request,staffedquietroom", ["E-BRIEF", "E-ATTENDEES"]), rec("HC-SCHEDULE", "Source programme/window/dependencies preserved;no inferred completedprerequisite", ["E-CALENDAR", "E-BRIEF"])], "preferences": [rec("P-Q003", "Learner preliminarily prefersQ-003,comparisonretainsQ-004", ["E-LEARNER"])], "assumptions": [rec("A-ALLOCATION", "Planner allocates meal/break and setup/check sequence within supported aggregatewindows;not vendor-mandated durations", ["E-BRIEF", "E-LEARNER"])], "unknowns": copy.deepcopy(pending), "conflicts": [u for u in pending if "CONFLICT" in u["id"] or "CHANGE" in u["id"]], "learner_policy": policy}, ["HC-CEILING", "HC-ACCESS", "HC-SCHEDULE", "P-Q003", "A-ALLOCATION"]+[u["id"] for u in pending])
        model["programme"] = build_programme(model)
        snapshot(4, {"headcount_basis": [rec("B-HEADCOUNT", "Separate populations summed;needs overlap;registered success target doesnot reduce servicecapacity", ["E-ATTENDEES", "E-INTERVIEW", "E-LEARNER"])], "schedule_dependencies": [rec("B-SCHEDULE", "Actual calendar retained;walkthrough awaitsvenueconfirmation;12 explicitdemo slots notpeoplecounts", ["E-CALENDAR", "E-BRIEF"])], "budget_baseline": [rec("B-BUDGET", "Commitments,allocations,approval limits,totalceiling and included contingency kept separate", ["E-BUDGET", "E-LEARNER"])], "accessibility_baseline": [rec("B-MEDIA", "Official visual observations require retainedhashmatchingreview;fictional capacities/readiness are not realcertification", ["E-FLOOR", "E-BRIEF"])], "model": model}, ["B-HEADCOUNT", "B-SCHEDULE", "B-BUDGET", "B-MEDIA"])
        active_stage = 5
        candidates = [("BASE-260", ["Q-001","Q-003","Q-005","Q-006","Q-009","Q-010"]), ("BASE-300", ["Q-001","Q-004","Q-005","Q-006","Q-009","Q-010"]), ("LIVESTREAM", ["Q-001","Q-003","Q-005","Q-006","Q-008","Q-009","Q-010"]), ("BASIC-AV", ["Q-001","Q-003","Q-005","Q-007","Q-009","Q-010"]), ("FALLBACK", ["Q-002","Q-003","Q-005","Q-006","Q-009","Q-010"])]
        snapshot(5, {"options": [rec(identity, "Unevaluated candidate package", ["E-VENDORS", "E-LEARNER"], quote_ids=ids) for identity,ids in candidates], "rejected_early": [], "source_quote_records": model["quotes"], "feasibility_not_yet_tested": True}, [identity for identity,ids in candidates])
        active_stage = 6
        options = generate_options(model)
        schedule_errors = programme_checks(model)
        snapshot(6, {"option_results": options, "unresolved_conditions": copy.deepcopy(pending)+[rec("COND-"+o["option_id"], ";".join(o["unresolved"]), o["evidence_ids"], "Operations / relevant source owner") for o in options if o["unresolved"]], "programme": model["programme"], "programme_checks": {"performed": bool(model["programme"]), "errors": schedule_errors, "demo_count": len(model["demo_ids"]), "demo_total_minutes": len(model["demo_ids"])*(model["demo_minutes"]+model["changeover_minutes"]) if model["demo_minutes"] else None}, "cost_and_capacity_checks": "Calculated each quote package,applicable population/category,commitments,allowances,expiry,date,status,limits and overallceiling"}, ["TEST-"+o["option_id"] for o in options]+["TEST-PROGRAMME"])
        feasible = [o for o in options[:2] if o["feasibility"] == "feasible"]
        selected = next((o["option_id"] for o in feasible if policy.get("preferred_caterer", "Q-003") in o["quote_ids"]), feasible[0]["option_id"] if feasible else None)
        approvals = [dict(rec("AP-OPERATIONS", "Review proposedplan,dateandvenue", ["E-INTERVIEW", "E-BRIEF"], "Operations"), status="pending")]+[dict(rec("AP-"+row["category"], "Reviewspendingandallocation/limitstatusfor"+row["category"], ["E-BUDGET", "E-VENDORS"], row["owner"]), status="pending") for row in model["budget"]]
        final_status = "complete" if len(feasible) == 2 and not model["source_failures"] and not pending else "partial"
        if not tables.get("calendar-constraints") and not tables.get("vendor-register"):
            final_status = "blocked"
        snapshot(7, {"recommendation": selected, "tradeoffs": [rec("TRADE-"+o["option_id"], o["tradeoffs"]+";"+str(o["headroom_twd"])+"ceilingheadroom;contingencyincluded", o["evidence_ids"]) for o in options], "learner_decisions": decisions, "approval_requirements": approvals, "selection_rationale": "PreferQ-003onlyafterhardconstraintpasses;otherwise supported feasiblealternativeor deferral", "run_status": final_status}, ["RECOMMENDATION"]+[r["id"] for r in approvals], final_status)
        active_stage = 8
        write_json(evidence/"planning-state.json", {"run_id": run_id, "model": model, "options": options, "selected_option": selected})
        artifacts = render(root, run_id, model, options, selected, mode)
        snapshot(8, {"artifact_drafts": artifacts, "affected_dependencies": [rec("PROPAGATION", "Samecurrentmodel,headcount,quotes,categories,decisionsandcalendarfedallfour drafts", ["E-LEARNER", "E-ATTENDEES", "E-VENDORS"])], "unresolved_items": copy.deepcopy(pending), "observed_completion": "Four fileswritten;not messages sent orcalendarpublication"}, [a["id"] for a in artifacts], final_status)
        active_stage = 9
        validation = validate_outputs(root)
        chain = _chain_check(root, expected=8)
        actual_hashes = [{**a, "sha256": digest((root/a["path"]).read_bytes()), "validation_status": "valid" if validation["valid"] else "invalid"} for a in artifacts]
        snapshot(9, {"artifacts": actual_hashes, "validation_checks": [rec("CHECK-OUTPUTS", json.dumps(validation), ["E-LEARNER"]), rec("CHECK-CHAIN", json.dumps(chain), ["E-LEARNER"])], "publication_status": "validated" if validation["valid"] else "failed", "publication_meaning": "Draftfilesvalidated;noexternalcalendarwrite,bookingorcommunication", "recommendation": selected}, ["VALIDATION-CURRENT"], final_status if validation["valid"] else "failed")
        chain = _chain_check(root)
        result = {"run_id": run_id, "status": final_status if validation["valid"] else "failed", "selected_option": selected, "validation": {**validation, "chain": chain}, "source_mode": mode, "observed_at": now(), "source_failures": model["source_failures"], "supersedes_run_id": previous, "stakeholder_approvals": "pending"}
        write_json(directory/"run.json", result)
        return result
    except Exception as error:
        failure = {"run_id": run_id, "observed_at": now(), "error": type(error).__name__+":"+str(error), "affected_stage": active_stage, "available_evidence": sorted(str(p.relative_to(root)) for p in evidence.glob("*") if p.is_file()), "affected_artifacts": ["deliverables/"+x for x in ARTIFACTS], "next_owner": "Operations / maintainer", "recovery_action": "Inspect preserved actualattempts/history,resolve error,reruncommand;never useoldsuccessfuloutputsascurrent", "status": "failed"}
        write_json(directory/"failure.json", failure)
        write_json(directory/"run.json", {"run_id": run_id, "status": "failed", "error": failure["error"], "observed_at": now()})
        return {"run_id": run_id, "status": "failed", "error": failure["error"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-bundle", type=Path, help="Explicit audit of already-observed source bytes with original registry metadata;not live retrieval")
    args = parser.parse_args()
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    result = run(root, source_bundle=args.source_bundle)
    print(json.dumps(result, indent=2))
    return 1 if result["status"] == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
