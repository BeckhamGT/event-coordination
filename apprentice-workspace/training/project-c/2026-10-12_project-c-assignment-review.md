---
title: "Project C — assignment review and repository comparison"
class: Immutable
sensitivity: INTERNAL
style: descriptive
source_type: "Course assignment web page; report type inferred"
source_url: "https://private-pecorino-70e.notion.site/Project-C-Event-Planning-Coordination-Brief-Learner-assignment-3da0b700541e813a8a91d0741d6ac96a"
retrieved: 2026-10-12
updated: 2026-10-12
---

## Source basis

| Source | Reading basis |
|---|---|
| Assignment [A] | Complete rendered Chrome page, including both requirement tables and all sections; no page revision date displayed |
| Repository README [R] | `README.md`, full file, revision `e40f865`; SHA-256 `a8c2b183036bd3e280be5fd6e24f6cdb0400080d8056ea938480f6ecb631802c` |
| Snapshot contract [S] | `snapshot.schema.json`, full file; schema `event-coordination-stage-snapshot/2`; SHA-256 `787e6ac3e2008458b311c2ab2e287a3cafb68aaa82d49a489775864ba32221ee` |
| Inherited agent instructions [G] | `/Users/user/fellowship/AGENTS.md` and its pointed-to `/Users/user/fellowship/apprentice-workspace/AGENTS.md`; local workspace rules copied from installed setup template during this review |
| Course capture guide [C] | Google Classroom material “4. Recording your sessions with entire.io”, displayed Aug 16, edited Sep 16; read in Chrome |

No stakeholder interview was opened or conducted by the agent. No business-source retrieval or implementation run is claimed. [Observed review scope]

## Purpose and boundaries

Build and execute a reusable Agent Skills-compliant skill named `event-planning-coordination-brief` for Quillhaven Academy's Event and Operations Manager. It retrieves disclosed current sources, compares supported options, and generates review drafts that remain consistent when attendance, quotes or venue information changes. Explain automation choices, uncertainty policy and trade-offs. [A §Scenario; §Your task]

The exercise business clock is **26 August 2026, 12:00, Asia/Taipei**. Actual retrieval timestamps are separate. Company planning records are exercise data; official venue sources are real and mutable. This clock is neither today's date nor an assumed event date. [A §Scenario]

Calendars and communications remain drafts. No bookings, payments, invitations, vendor commitments, production-calendar writes, exposed secrets, approval bypasses, or copying private attendee medical/contact details into general artifacts. [A §Your task]

## Deliverables

| Deliverable | Required contents | Source |
|---|---|---|
| `interviews/<original-export-filename>.md` | One final complete original Work Sim Markdown export per session, unchanged, including session metadata and all participant-visible messages. Commit and push with submitted code; facilitator must be able to read it. Missing export goes to facilitator, never a manufactured replacement. | A §Deliverables; R §Before you work |
| `event-planning-coordination-brief/SKILL.md`, `scripts/`, `references/` | Compliant skill and executable implementation. Document one end-to-end command, chosen runtime, dependencies and setup. | A §Your task; §Deliverables |
| `deliverables/snapshots/01-scope-and-approval-gates.json` through `09-publication-validation.json` | Nine stage-boundary snapshots, one shared `run_id`; stages 02–09 identify and hash their immediate predecessor. Each transition records consumed and produced record IDs. | A §Deliverables—Snapshots; S |
| `deliverables/snapshots/evidence/` | Inspectable captured source content or permitted extracts with IDs, URLs, versions, actual retrieval timestamps, locators and hashes. Include at least one required stakeholder-disclosed official floor-plan/image source. Retain retrieved image/PDF bytes supporting spatial/accessibility claims; identify page/region in stage 02 and reference evidence IDs later. Optional video claims need timestamps. | A §Deliverables—Snapshots |
| `deliverables/vendor-comparison.csv` | Materially different options, including rejected options and reasons; integer TWD costs, unknown costs blank with explanation. Preserve quote identities, categories, capacities, dates, conditions and evidence. | A §Deliverables—Final drafts |
| `deliverables/event-plan.md` | Objective and source/run basis, headcount and uncertainty policy, timing/dependencies, category and total costs, comparisons, feasibility, accessibility/safety evidence and limits, recommendation or deferral, risks, unknowns, change effects, remaining owners and review requests. | A §Deliverables—Final drafts |
| `deliverables/event-calendar.ics` | Valid VCALENDAR, `VERSION:2.0`, draft `METHOD:PUBLISH`, stable event UID, DTSTAMP, supported DTSTART/DTEND with explicit timezone and `STATUS:TENTATIVE`. No attendees/delivery actions. Valid empty calendar if no time is supportable, with explanation. | A §Deliverables—Final drafts |
| `deliverables/draft-communications.md` | Every message labeled `UNSENT DRAFT`, with audience, purpose, conditions and approval owner. Preserve uncertainties/dependencies; no claims that booking, payment or invitations were sent. | A §Deliverables—Final drafts |
| `deliverables/history/<run_id>/` | Preserve previous current runs before material change, including earlier evidence and failed attempts. New current set uses new run ID and unique snapshot IDs; stage 01 identifies superseded run, changed source/decision IDs and reason. | A §Deliverables—Changed inputs and recovery |
| Submission | Own completed GitHub repository URL in assigned Classroom task, submitted revision, run ID and reproduction command; include skill, implementation, current outputs and required history, with facilitator access to matching interview/development capture. | A §Submit |

The nine stages are: scope and approval gates; source capture; constraint model; planning baseline; option generation; feasibility testing; decision and approval; draft propagation; publication validation. Stage 08 records propagation and stage 09 validates exact paths/hashes **after** writing final drafts. [A §Deliverables; S]

Required CSV columns: `option_id`, `quote_ids`, `planning_people`, `cost_twd`, `currency`, `feasibility`, `availability_status`, `evidence_ids`, `tradeoffs`, `unresolved`, `approval_status`. Lists can be JSON arrays or a documented unambiguous delimiter. [A §Deliverables—Final drafts]

## Acceptance and assessment criteria

No numerical score weights or submission deadline appear in the read assignment/README. These are stated acceptance criteria, not an invented point rubric. [A all sections; R full file]

| Criterion | Required behavior | Source |
|---|---|---|
| Interview authorship | Learner personally conducts interview and authors questions. Connecting AI/coding agents to run, script or automate interview makes project unscored. Original interview export is assessed with code. | A §Interview; R §Before you work |
| Evidence integrity | Read actual disclosed remote sources; no undisclosed local substitutes. Record every attempted structured, web, image, video and calendar source with actual retrieval state. Keep facts, assumptions, planned actions, observed completions and approvals distinct. | A §Deliverables |
| Business interpretation | Use interview-supplied meanings for headcounts, capacity, prices, budgets and calendars. Preserve all relevant calendar records and meanings. No inferred missing values or approvals from labels/numbers. | A §Deliverables |
| Scheduling | Produce a non-overlapping programme covering supplied activities and dependencies, not just summed minutes. | A §Deliverables |
| Traceability | Validate snapshots against unchanged schema; resolve evidence/decision references and predecessor hashes throughout chain; all drafts agree on amounts, dates, options, decisions and evidence. | A §Deliverables; S |
| Robust changed inputs | Accept valid reordered headers/records and unrelated extra columns, including combined changes. Hold dependent interpretation for missing fields, ambiguous/duplicate identities, incompatible meanings and invalid required values; no guessed renames or silently chosen conflicts. | A §Changed inputs and recovery |
| Recovery | Preserve history before material changes; reconsider every affected planning basis, comparison, decision, approval request and draft. Inspect retained identities/hashes before reuse. Validate actual files even for unchanged inputs; repair missing/corrupt/stale outputs or return explicit incomplete/failure result. Recovery grants no approval and completes no business prerequisite by itself. | A §Changed inputs and recovery |
| Learner decisions and capture | Facilitator verifies identity, interview recording/export, development capture, runtime/source access and submission destination before assessed work. Record attributable project-specific choices with source basis and consequences; no retrospective generic assent or fabricated transcripts. | A §Interview |

| State family | Allowed values |
|---|---|
| Run | `complete`, `partial`, `blocked`, `failed` |
| Retrieval | `retrieved`, `unavailable`, `invalid`, `unverified`, `stale` |
| Option | `feasible`, `infeasible`, `conditional`, `unverified` |
| Approval | `pending`, `approved`, `rejected`, `not-required` |

These exact states come from A §Deliverables and S. Missing/conflicting/stale/unresolved facts remain visible until an evidence-backed resolution or actual human decision changes them.

| Run result | Required outcome | Source |
|---|---|---|
| complete | Nine valid linked snapshots and four consistent drafts, supported comparisons and justified recommendation. Human approval can remain pending because outputs are drafts. | A §Incomplete results |
| partial | Nine linked snapshots and four drafts retaining supported work, unavailable sources, conditional claims and resolution owners. | A §Incomplete results |
| blocked | Nine snapshots when valid evidence can be retained; comparison/plan explain blockage, valid empty draft calendar, unsent clarification drafts. | A §Incomplete results |
| failed | `deliverables/failure.json`: run_id, observed_at, error, affected_stage, available_evidence, affected_artifacts, next_owner and recovery action. Preserve only actually obtained evidence; never present earlier successful outputs as current success. | A §Incomplete results |

Independent supported work can continue when one vendor/source is unavailable. Preserve failed attempts and affected claims with resolution owner/evidence needed. Unavailable image evidence requires withholding dependent spatial/accessibility claims. [A §Incomplete results]

## Accounts, tools and information

| Need | Current observation or open prerequisite | Source |
|---|---|---|
| GitHub repository and push access | Local origin is `https://github.com/BeckhamGT/event-coordination.git`, not public starter. Fork relationship, write permission, privacy and facilitator visibility not verified. | R §Start; A §Submit; observed `git remote -v` |
| Work Sim access | Learner uses `https://work-sim.catalyte.ai/s/project-c-event-coordination` directly and exports original Markdown. Account/access/export not checked by agent. | A §Interview |
| Classroom/course setup | Linked capture guide loads in signed-in Chrome. Assigned submission task, deadline and facilitator verification remain unconfirmed. | R §Before you work; C; A §Interview/Submit |
| Coding environment/runtime | Agent Skills-capable environment required; no language or dependencies prescribed. Entire CLI 0.11.3 enabled for Codex with installed approved hooks. | R §Before you work; A §Your task; observed Entire diagnostics |
| Source routes and business rules | Need disclosed online sources, credentials/access route if any, field meanings, stable identities, headcounts/uncertainty, budget inclusions, capacities, quote validity/conditions, activity dependencies, calendar meanings, accessibility criteria and human approval owners. | A §Your task/Deliverables/Interview |
| Media and validation tools | Need retrieval preserving permitted source bytes, PDF/image inspection, JSON Schema validation, CSV/calendar parsing, SHA-256 hashing, and cross-artifact checks. Tools depend on actual disclosed source formats. | A §Deliverables; proposed implementation requirements |

## Repository comparison, conflicts and missing instructions

1. README delegates acceptance requirements to the exact assignment page read here. Both require a personal interview, unchanged original exports, a reusable skill, actual online-source access, documented runtime and development capture. The starter supplies README and schema only; the completed-tree files are work to create, not missing starter implementation. [R §Start/Supplied files/Before you work; A §Deliverables]
2. Inherited AGENTS points to apprentice-workspace rules, but this repository originally lacked that folder and root agent instructions. Setup created the local template and root pointers during this review; no existing instructions were replaced. [G; observed filesystem/setup]
3. Workspace rules file coursework under `apprentice-workspace/training/<module-id>/`, while the formal assignment specifies root `interviews/`, skill and `deliverables/` paths. Proposed resolution: keep supporting review notes in training, retain the exact required submission tree at root, and record that exception before implementation rather than relocating submission artifacts silently. [G §Where things go; A §Deliverables; proposed resolution]
4. General working standards favor composed notes over raw transcripts, while this assignment explicitly requires unchanged original exports. Retain originals for assessment; any later analysis is a separate note and cannot replace the exports. [G §How to write; plugin working-standards §Nothing raw reaches the reader; A §Deliverables]
5. Course capture guide uses `financial-health-brief` as its setup example; this is contextual wording, not a direction to switch projects. The guide explicitly requires Entire in every project copy and, at hand-in, commit, verify `entire checkpoint list`, then push. [C]
6. Business facts are intentionally undisclosed until learner interview: do not select vendors, headcount assumptions, dates or budgets yet. Source access, original export, facilitator pre-work verification, Agent Skills compliance details, grading weights, deadline and submission permissions remain unverified or absent. [A §Your task/Interview/Submit; R §Before you work; observed repository]
7. Entire diagnostics show enabled status and all approval records present. The current request appears in the actual live transcript, but automatic session lifecycle still reports `ended`; logs contain no new hook lifecycle event for this request. A real transcript checkpoint was attached without amending the starter commit. This is evidence retention, not proof that automatic lifecycle capture has resumed. Recheck automatic capture in a fresh interaction/session before implementation and have facilitator confirm required capture. [Observed `entire doctor`, `session current`, transcript/logs, `session attach`; C; A §Interview]

## Proposed completion plan

These steps are proposals, not completed implementation or stakeholder-approved decisions.

1. Resolve pre-work checks with facilitator: identity, original interview/export capability, continuous coding capture, runtime/source access and submission destination/privacy. Verify fresh automatic Entire capture before implementation. [A §Interview; C]
2. Learner personally conducts stakeholder interview and follow-ups, using learner-authored questions. Save complete original exports unchanged under root `interviews/`. Report unavailable export/access to facilitator. [A §Interview/Deliverables; R]
3. Read supplied transcript and all disclosed sources, derive a source/constraint/approval inventory, and record actual unresolved definitions. Learner chooses uncertainty policy and trade-offs with attributable evidence and consequences in development capture. [A §Your task/Interview]
4. Choose and document runtime/libraries, one reproduction command and setup. Proposed architecture: a source-capture layer, interpretation/constraint model, option/schedule evaluation, draft generation and validation, each writing its corresponding boundary snapshot. Runtime selection waits for source format/access needs. [A §Your task/Deliverables; proposal]
5. Implement all nine linked stages against unchanged schema; preserve source attempts and required official media; produce coherent draft files with explicit states and approval owners. [A §Deliverables; S]
6. Validate business constraints, programme non-overlap, costs, calendar format, evidence references, hashes and cross-artifact agreement. Exercise changed headcounts/quotes/calendar facts, reordered headers/records with extra columns, unavailable sources, invalid identities, output corruption and recovery. Retain previous runs before material changes. [A §Deliverables/Changed inputs and recovery; proposal for verification cases]
7. Execute documented command on actual disclosed sources, inspect resulting run and justify recommendation or deferral. Preserve actual incomplete/failure states. Commit and verify Entire checkpoint capture, then push authorized submission revision and provide repository URL/revision/run ID/command in assigned Classroom task. [A §Submit; C]

## Verification

Spot-checked against rendered assignment: personal-interview disqualification rule; fixed business clock; nine stage filenames; CSV column list/integer TWD rule; calendar draft fields; original-export preservation; history/supersession rule. Checked schema stage sequence and required states against local unchanged contract. No numerical score weights, business inputs or approvals were invented. [Review verification]

## Sources

- [A: Formal assignment](https://private-pecorino-70e.notion.site/Project-C-Event-Planning-Coordination-Brief-Learner-assignment-3da0b700541e813a8a91d0741d6ac96a)
- R: repository `README.md`.
- S: repository `snapshot.schema.json`.
- G: `/Users/user/fellowship/AGENTS.md` and pointed-to apprentice-workspace rules; installed plugin working-standards.
- [C: Course session-capture guide](https://classroom.google.com/c/ODcyMjA4NTkwNDk2/m/ODc0NzI2NzQzMzQ2/details)
