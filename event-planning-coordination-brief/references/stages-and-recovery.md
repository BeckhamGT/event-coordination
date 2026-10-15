# Stage boundaries and recovery

Read before execution, changed-input handling or output repair. The public `snapshot.schema.json` is authoritative and remains unchanged. Emit each snapshot when its work finishes; preserve its observed creation time and results. A historical observation cannot be reconstructed afterward and presented as contemporaneous evidence.

## Nine boundaries

| Sequence | Stage | State that must exist at this boundary |
|---:|---|---|
| 01 | `scope-and-approval-gates` | Objective, decision deadline, owners, genuine approval requirements, actual self-check status and learner choices. There is no facilitator sign-off gate. |
| 02 | `source-capture` | Actual per-source retrieval outcomes, versions, timestamps, raw evidence hashes, locators, media observations and access failures. |
| 03 | `constraint-model` | Hard constraints, preferences, assumptions, unknowns and conflicts, each linked to evidence and responsible owner. |
| 04 | `planning-baseline` | Recalculated headcount and overlap rules, scheduling dependencies, commitments/allocations/limits and accessibility basis. |
| 05 | `option-generation` | Materially different bundles and early rejections with reasons. Preserve alternatives honestly when fewer than two remain feasible. |
| 06 | `feasibility-testing` | Per-option capacity, time, budget, quote validity, availability and accessibility results, plus unresolved hard conditions. |
| 07 | `decision-and-approval` | Supported recommendation or deferral, trade-offs, learner decisions and revision-specific stakeholder approval requirements. |
| 08 | `draft-propagation` | Four draft files and hashes, affected dependencies, source/run bindings and unresolved items. |
| 09 | `publication-validation` | Actual inspected artifacts and hashes, checks performed, discrepancies and `validated`, `blocked` or `failed` publication status. Publication here means the draft package, not real-world sending. |

Every stage has a unique snapshot ID and shared run ID; sequences 02–09 reference the exact predecessor ID, repository-relative path and SHA-256. Consumed record IDs resolve to prior produced records; evidence IDs resolve to captured sources or explicit decision/self-check evidence. Use `partial`, `blocked` or `failed` when required work lacks support. A schema-valid placeholder is not a completed stage.

The draft calendar keeps source constraints distinct from activity blocks. Preserve explicit `Asia/Taipei` timezone identity with `VTIMEZONE`. Use `TENTATIVE` VEVENTs for positive intervals and a `NEEDS-ACTION` VTODO with `DUE` for the exact decision deadline; it has no invented duration. Never add attendees, invitations or production writes.

## Change and recovery procedure

1. **Preserve** the current run's snapshots, drafts, evidence and manifest in a uniquely identified history directory before a material replacement. Retain preparation stages 01–04 and earlier history as recorded; a clarification or correction is a new record, not a silent edit to the old observation.
2. **Identify** the trigger, original run, changed or missing input/output, old/new hash, earliest affected stage and dependent artifacts. Create a new run ID and actual timestamps; record the causal relationship to its predecessor run.
3. **Retrieve** changed remote inputs through their disclosed routes. Record outages, invalid records and changed content. An explicit archived-bundle audit/test run keeps its archived provenance and does not claim current remote access.
4. **Recompute** from the earliest affected basis through every dependent output. Reuse unaffected captured evidence only with its original retrieval metadata and an explicit reuse record. New IDs and predecessor hashes must describe the new chain.
5. **Validate** repaired files, source links, semantic consistency and hashes. Preserve a failed attempt and its error before recovery. Report exactly what recovered, which tests ran and which issues remain.

Attendance changes revisit baseline and capacities; quote or budget changes revisit validity, commitments, feasibility and recommendation; date changes revisit the entire schedule and every dated service; accessibility changes revisit room/service feasibility and programme readiness. A missing or corrupt output requires regeneration and independent output checks, not only copying its old hash into a new manifest.

## Failure states

For unavailable source data, retain transport details and owner, mark affected claims unverified and continue independent stages where supported. For missing/ambiguous required columns, duplicate stable identities, invalid units or malformed amounts/dates, hold the affected data for resolution. Reordered rows/columns and unrelated extra columns are valid and must preserve semantic results.

If timing cannot be supported, create a valid empty draft calendar and explain the missing basis. If a remaining dependency is a hard requirement, classify the option conditional/unverified rather than feasible. All human approvals stay pending unless a real, revision-matching decision is supplied.
