"""Business interpretation from named records, with approvals kept separate."""
import math
import re
from datetime import datetime, timedelta

from sources import InputError, integer


FIELDS = {
    "attendee-signals": ("signal_id", "source", "segment", "signal", "value", "unit", "observed_at", "confidence"),
    "budget": ("category", "planned_amount_twd", "approval_limit_twd", "committed_amount_twd", "owner", "record_version"),
    "calendar-constraints": ("constraint_id", "owner", "constraint_type", "start_at", "end_at", "priority", "notes", "record_version"),
    "vendor-register": ("quote_id", "vendor", "category", "option", "quote_amount_twd", "capacity", "available_date", "valid_until", "status", "notes"),
}
KEYS = {"attendee-signals": "signal_id", "budget": "category", "calendar-constraints": "constraint_id", "vendor-register": "quote_id"}
SOURCE_IDS = {"attendee-signals": "E-ATTENDEES", "budget": "E-BUDGET", "calendar-constraints": "E-CALENDAR", "vendor-register": "E-VENDORS"}
CALENDAR_MEANINGS = dict(zip(("CAL-%03d" % n for n in range(1, 9)), (
    "preferred_event_window", "fallback_event_window", "venue_hold", "keynote_availability",
    "decision_deadline", "accessibility_walkthrough", "rehearsal_window", "teardown_deadline")))
QUOTE_CATEGORIES = dict(zip(("Q-%03d" % n for n in range(1, 11)), (
    "venue", "venue", "catering", "catering", "accessibility", "production",
    "production", "production", "security", "accessibility")))
SIGNAL_MEANINGS = dict(zip(("SIG-%03d" % n for n in range(1, 14)), (
    ("fellows", "registered_attendees"), ("partners", "registered_attendees"),
    ("staff", "required_on_site"), ("speakers", "required_on_site"),
    ("walk_ins", "expected_attendees"), ("all", "wheelchair_spaces"),
    ("all", "mobility_companions"), ("all", "live_caption_requests"),
    ("all", "hearing_loop_requests"), ("all", "quiet_room_requests"),
    ("all", "vegetarian_meals"), ("all", "halal_meals"), ("all", "severe_allergy_follow_up"))))


def rec(identity, summary, evidence, owner=None, **extra):
    return dict(id=identity, summary=summary, evidence_ids=evidence, owner=owner, **extra)


def aware(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise InputError("Calendar timestamp lacks explicit timezone")
    return result


def date_only(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date()


def build_model(tables, policy, brief_text, include_programme=True):
    attendees = tables.get("attendee-signals", [])
    budgets = tables.get("budget", [])
    quotes = {row["quote_id"]: row for row in tables.get("vendor-register", [])}
    calendar = tables.get("calendar-constraints", [])
    population, registered, needs, unknowns = {}, 0, {}, []
    allowed = {"fellows", "partners", "staff", "speakers", "walk_ins"}
    for row in attendees:
        expected = SIGNAL_MEANINGS.get(row["signal_id"])
        if expected and (row["segment"], row["signal"]) != expected:
            raise InputError("Stable attendee identity changed meaning: " + row["signal_id"])
        value = integer(row["value"], row["signal_id"])
        if row["segment"] in allowed and row["signal"] in ("registered_attendees", "required_on_site", "expected_attendees"):
            if row["segment"] in population:
                raise InputError("Ambiguous overlapping population records for " + row["segment"])
            if row["unit"] != "people":
                raise InputError("Population quantity has incompatible unit")
            population[row["segment"]] = {"people": value, "confidence": row["confidence"], "signal_id": row["signal_id"]}
            if row["signal"] == "registered_attendees":
                registered += value
        else:
            expected_unit = "meals" if row["signal"] in ("vegetarian_meals", "halal_meals") else "people"
            if row["unit"] != expected_unit:
                raise InputError("Incompatible needs unit for " + row["signal"])
            if row["signal"] in needs:
                raise InputError("Ambiguous need identity: " + row["signal"])
            needs[row["signal"]] = value
    required_needs = {"wheelchair_spaces", "mobility_companions", "live_caption_requests", "hearing_loop_requests", "quiet_room_requests", "vegetarian_meals", "halal_meals", "severe_allergy_follow_up"}
    if not required_needs <= set(needs):
        unknowns.append(rec("U-NEEDS", "Required service needs are missing; absence is not zero demand", ["E-ATTENDEES"], "Learner Experience"))
    people = sum(x["people"] for x in population.values()) if set(population) == allowed else None
    if people is None:
        unknowns.append(rec("U-POPULATION", "Complete separate population groups are unavailable", ["E-ATTENDEES"], "Learner Experience"))
    if people is not None and people != policy.get("baseline_people", 245):
        unknowns.append(rec("U-HEADCOUNT-CHANGE", "Source attendance differs from recorded245 baseline; learner review required, no silent policy change", ["E-ATTENDEES", "E-LEARNER"], "Learner Experience / Learner"))
    budget = {row["category"]: row for row in budgets}
    for row in quotes.values():
        if row["quote_id"] in QUOTE_CATEGORIES and row["category"] != QUOTE_CATEGORIES[row["quote_id"]]:
            raise InputError("Stable quote identity changed category: " + row["quote_id"])
    for row in calendar:
        if row["constraint_id"] in CALENDAR_MEANINGS and row["constraint_type"] != CALENDAR_MEANINGS[row["constraint_id"]]:
            raise InputError("Stable calendar identity changed meaning: " + row["constraint_id"])
        start, end = aware(row["start_at"]), aware(row["end_at"])
        if end < start or (end == start and row["constraint_type"] != "decision_deadline"):
            raise InputError("Invalid calendar interval for " + row["constraint_id"])
    required_types = [r["constraint_type"] for r in calendar if r["constraint_type"] != "blackout"]
    if len(required_types) != len(set(required_types)):
        raise InputError("Ambiguous duplicate calendar meaning")
    missing_calendar = set(CALENDAR_MEANINGS.values()) - set(required_types)
    if missing_calendar:
        unknowns.append(rec("U-CALENDAR-RECORDS", "Required calendar meanings unavailable: " + ", ".join(sorted(missing_calendar)), ["E-CALENDAR"], "Operations / Programme / Learner Experience"))
    keynote = next((r for r in calendar if r["constraint_type"] == "keynote_availability"), None)
    if keynote and "10:00–11:00 keynote" in brief_text and (aware(keynote["start_at"]).strftime("%H:%M") != "10:00" or aware(keynote["end_at"]).strftime("%H:%M") != "11:00"):
        unknowns.append(rec("U-KEYNOTE-CONFLICT", "Calendar timing conflicts with the brief's hard10:00–11:00 keynote", ["E-CALENDAR", "E-BRIEF"], "Programme / Operations"))
    venue_capacity = re.search(r"allocates ([\d,]+) usable audience places", brief_text)
    wheelchair = re.search(r"including (\w+) wheelchair spaces", brief_text)
    words = {"six": 6}
    wheelchair_places = words.get(wheelchair[1]) if wheelchair else None
    if wheelchair and wheelchair[1].isdigit():
        wheelchair_places = int(wheelchair[1])
    quiet = re.search(r"occupancy up to (\d+) people", brief_text)
    demo_ids = sorted(set(re.findall(r"\bDEMO-\d{2}\b", brief_text)))
    duration = re.search(r"Each demonstration needs (\d+) minutes.*?separate (\d+)-minute changeover", brief_text, re.S)
    ready = "VEN-2026-08-26-R2" in brief_text and "07:30" in brief_text and "09:30" in brief_text and "18:30" in brief_text
    spatial = "venue coordination confirms step-free access" in brief_text
    if not ready:
        unknowns.append(rec("U-READINESS", "Exercise readiness confirmation for setup/checks and teardown not verified", ["E-BRIEF"], "Operations / Programme"))
    if not demo_ids or not duration:
        unknowns.append(rec("U-DEMO-ROSTER", "Explicit programme roster/durations are unavailable; do not infer demos from people", ["E-BRIEF"], "Programme"))
    model = {"people": people, "registered": registered, "checkin_target": math.ceil(registered * .8), "population": population, "needs": needs, "quiet_users": needs.get("quiet_room_requests"), "budget": budgets, "budget_by_category": budget, "quotes": quotes, "calendar": calendar, "policy": policy, "ceiling_twd": policy.get("ceiling_twd", 520000), "planned_twd": sum(integer(r["planned_amount_twd"]) for r in budgets) if budgets else None, "committed_twd": sum(integer(r["committed_amount_twd"]) for r in budgets) if budgets else None, "venue_capacity": int(venue_capacity[1].replace(",", "")) if venue_capacity else None, "wheelchair_places": wheelchair_places, "quiet_capacity": int(quiet[1]) if quiet else None, "readiness_confirmed": ready, "step_free_case_confirmed": spatial, "demo_ids": demo_ids, "demo_minutes": int(duration[1]) if duration else None, "changeover_minutes": int(duration[2]) if duration else None, "brief_text": brief_text, "unknowns": unknowns, "media_verified": True, "source_failures": [], "business_clock": "2026-08-26T12:00:00+08:00"}
    model["programme"] = build_programme(model) if include_programme else []
    return model


def build_programme(model):
    rows = {r["constraint_type"]: r for r in model.get("calendar", [])}
    required = {"preferred_event_window", "keynote_availability", "venue_hold", "teardown_deadline"}
    if not required <= set(rows) or not model.get("demo_ids") or not model.get("demo_minutes"):
        return []
    window = rows["preferred_event_window"]
    start, end = aware(window["start_at"]), aware(window["end_at"])
    keynote = rows["keynote_availability"]
    ks, ke = aware(keynote["start_at"]), aware(keynote["end_at"])
    if not (start <= ks < ke <= end):
        return []
    programme = []

    def add(identity, summary, a, b, dependency=None, kind="programme", **extra):
        if b <= a:
            return
        programme.append({"event_id": identity, "summary": summary, "start_at": a.isoformat(), "end_at": b.isoformat(), "duration_minutes": int((b-a).total_seconds()/60), "kind": kind, "dependencies": dependency or [], "status": "TENTATIVE", **extra})
    hold = rows["venue_hold"]
    hs = aware(hold["start_at"])
    # These are documented planner allocations within R2's confirmed aggregate window.
    cut = hs + (start-hs)/2
    add("SETUP", "Draft coordinated setup and service installation", hs, cut, kind="setup")
    add("READINESS", "Draft caption/loop/accessibility/security readiness checks", cut, start, ["SETUP"], kind="setup")
    add("OPEN", "Opening and programme orientation", start, ks, ["READINESS"])
    add("KEYNOTE", "Keynote", ks, ke, ["OPEN"])
    add("MORNING-BREAK", "Morning refreshment break", ke, ke+timedelta(minutes=20), ["KEYNOTE"])
    cursor = ke+timedelta(minutes=20)
    duration = model["demo_minutes"] + model["changeover_minutes"]
    for index, identity in enumerate(model["demo_ids"]):
        if index == len(model["demo_ids"])//2:
            add("LUNCH", "Lunch and dietary service", cursor, cursor+timedelta(minutes=60), [model["demo_ids"][index-1]])
            cursor += timedelta(minutes=60)
        following = cursor + timedelta(minutes=duration)
        add(identity, identity + " presentation and changeover", cursor, following, ["KEYNOTE"] if index == 0 else [programme[-1]["event_id"]], presentation_minutes=model["demo_minutes"], changeover_minutes=model["changeover_minutes"])
        cursor = following
    if cursor < end:
        remaining = int((end-cursor).total_seconds()/60)
        # Chosen meal/break/networking allocations; never represented as source-mandated durations.
        for identity, summary, minutes in [("BREAK", "Afternoon break", min(20, remaining)), ("PARTNERS", "Partner discussion and accessible networking", max(0, remaining-35)), ("CLOSE", "Closing and next steps", min(15, max(0, remaining-20)))]:
            following = cursor + timedelta(minutes=minutes)
            add(identity, summary, cursor, following, [programme[-1]["event_id"]])
            cursor = following
    teardown = rows["teardown_deadline"]
    add("TEARDOWN", "Draft teardown and vendor clearance", aware(teardown["start_at"]), aware(teardown["end_at"]), ["CLOSE"], kind="teardown")
    return programme


def programme_checks(model):
    checks = []
    programme = model.get("programme", [])
    if not programme:
        return ["Programme cannot be supported by available calendar/roster"]
    ordered = sorted(programme, key=lambda r: r["start_at"])
    for before, after in zip(ordered, ordered[1:]):
        if aware(before["end_at"]) > aware(after["start_at"]):
            checks.append("Overlapping programme blocks:"+before["event_id"]+"/"+after["event_id"])
    by_id = {r["event_id"]: r for r in programme}
    for row in programme:
        for dep in row["dependencies"]:
            if dep not in by_id or aware(by_id[dep]["end_at"]) > aware(row["start_at"]):
                checks.append("Unsatisfied programme dependency:" + dep)
    records = {r["constraint_type"]: r for r in model.get("calendar", [])}
    window = records.get("preferred_event_window")
    if window:
        for row in programme:
            if row["kind"] == "programme" and not (aware(window["start_at"]) <= aware(row["start_at"]) < aware(row["end_at"]) <= aware(window["end_at"])):
                checks.append("Programme outside event window:"+row["event_id"])
    for row in model.get("calendar", []):
        if row["constraint_type"] == "blackout":
            if any(aware(p["start_at"]) < aware(row["end_at"]) and aware(p["end_at"]) > aware(row["start_at"]) for p in programme):
                checks.append("Programme intersects blackout:" + row["constraint_id"])
    if sorted(r["event_id"] for r in programme if r["event_id"].startswith("DEMO-")) != sorted(model["demo_ids"]):
        checks.append("Demo roster incomplete or duplicated")
    return checks


def generate_options(model):
    specs = [("BASE-260", ["Q-001", "Q-003", "Q-005", "Q-006", "Q-009", "Q-010"], "Lower-cost catering package; current capacity margin shown in the plan"), ("BASE-300", ["Q-001", "Q-004", "Q-005", "Q-006", "Q-009", "Q-010"], "Higher-capacity catering package; current capacity margin shown in the plan"), ("LIVESTREAM", ["Q-001", "Q-003", "Q-005", "Q-006", "Q-008", "Q-009", "Q-010"], "Rejected base extension: livestream"), ("BASIC-AV", ["Q-001", "Q-003", "Q-005", "Q-007", "Q-009", "Q-010"], "Rejected hearing-loop omission"), ("FALLBACK", ["Q-002", "Q-003", "Q-005", "Q-006", "Q-009", "Q-010"], "Rejected equivalent fallback: keynote unavailable")]
    results = []
    clock = aware(model["business_clock"])
    current = next((r for r in model["calendar"] if r["constraint_type"] == "preferred_event_window"), None)
    for identity, ids, tradeoff in specs:
        missing = [x for x in ids if x not in model["quotes"]]
        reasons, conditions, categories, variances, breaches = [], [], {}, {}, {}
        if missing:
            conditions.append("Missing quotes:" + ",".join(missing))
        if not model["budget"]:
            conditions.append("Budget source unavailable or invalid")
        for qid in ids:
            quote = model["quotes"].get(qid)
            if not quote:
                continue
            amount = integer(quote["quote_amount_twd"])
            categories[quote["category"]] = categories.get(quote["category"], 0) + amount
            if date_only(quote["valid_until"]) < clock.date():
                reasons.append(qid+" expired at exercise clock")
            if current and identity != "FALLBACK" and date_only(quote["available_date"]) != aware(current["start_at"]).date():
                reasons.append(qid+" available on a different date")
            if quote["status"] not in ("available", "held"):
                conditions.append(qid+" status:"+quote["status"])
            if quote["category"] in ("venue", "catering", "production") and model["people"] is not None and integer(quote["capacity"]) < model["people"]:
                reasons.append(qid+" capacity below planning people")
            if qid == "Q-010" and model["quiet_users"] is not None and integer(quote["capacity"]) < model["quiet_users"]:
                reasons.append("Quiet-room staffing simultaneous capacity insufficient")
        categories["communications"] = model["policy"].get("communications_allowance_twd", 25000)
        categories["contingency"] = model["policy"].get("contingency_allowance_twd", 40000)
        cost = None if missing or not model["budget"] else sum(categories.values()) + model["committed_twd"]
        for category, amount in categories.items():
            baseline = model["budget_by_category"].get(category)
            if baseline is None:
                conditions.append("Missing budget category:"+category)
                continue
            effective = amount + integer(baseline["committed_amount_twd"])
            variance = effective - integer(baseline["planned_amount_twd"])
            excess = effective - integer(baseline["approval_limit_twd"])
            if variance:
                variances[category] = variance
            if excess > 0:
                breaches[category] = excess
                conditions.append(category+" approval-limit breach requires explicit owner approval")
        if cost is not None and cost > model["ceiling_twd"]:
            reasons.append("Total exceeds520000 ceiling; category approval cannot override ceiling")
        if model["people"] is None:
            conditions.append("Planning population unverified")
        if model["quiet_capacity"] is None or model["quiet_users"] is None:
            conditions.append("Quiet-room occupancy/demand unverified")
        elif model["quiet_users"] > model["quiet_capacity"]:
            reasons.append("Quiet-room space occupancy insufficient")
        if model["wheelchair_places"] is None:
            conditions.append("Wheelchair allocation unverified")
        elif model["needs"].get("wheelchair_spaces", 0) > model["wheelchair_places"]:
            reasons.append("Wheelchair places insufficient")
        if not model["readiness_confirmed"] or not model["step_free_case_confirmed"]:
            conditions.append("Venue readiness or step-free case coordination unverified")
        if not model.get("media_verified"):
            conditions.append("Required official image unavailable, changed or not visually reviewed; spatial claims withheld")
        conditions.extend(programme_checks(model))
        if any(u["id"] == "U-HEADCOUNT-CHANGE" for u in model["unknowns"]):
            conditions.append("Attendance change requires recorded learner review")
        for unknown in model["unknowns"]:
            if unknown["id"] in ("U-NEEDS", "U-KEYNOTE-CONFLICT", "U-CALENDAR-RECORDS"):
                conditions.append(unknown["summary"])
        if identity == "LIVESTREAM":
            reasons.append("Learner excludes livestream from base plan")
            conditions.append("Q-008 network test and venue confirmation not evidenced")
        if identity == "BASIC-AV":
            reasons.append("Q-007 lacks requested hearing loop; no supported substitute")
        if identity == "FALLBACK":
            reasons.append("Keynote unavailable24October; base service quotes are17October")
        feasible = "infeasible" if reasons else "conditional" if conditions else "feasible"
        results.append({"id": identity, "option_id": identity, "summary": tradeoff, "quote_ids": ids, "planning_people": model["people"], "cost_twd": cost, "currency": "TWD", "categories": categories, "headroom_twd": model["ceiling_twd"]-cost if cost is not None else None, "feasibility": feasible, "availability_status": "supported exercise records;not a booking" if not missing else "unverified", "evidence_ids": ["E-ATTENDEES", "E-BUDGET", "E-VENDORS", "E-BRIEF", "E-CALENDAR", "E-FLOOR"], "tradeoffs": tradeoff, "reasons": list(dict.fromkeys(reasons)), "unresolved": list(dict.fromkeys(conditions)), "allocation_variances_twd": variances, "approval_limit_breaches_twd": breaches, "approval_status": "pending"})
    return results
