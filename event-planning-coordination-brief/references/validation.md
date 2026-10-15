# Validation and evaluation

Read when checking a run or investigating a regression. The canonical pair in `eval/` defines expected invariants. Keep a concise record containing check ID, source/method, actual result, correction and remaining uncertainty. Planned checks have a planned status; only executable or directly inspected evidence can establish a pass.

For authoring validation, the system skill creator's `quick_validate.py` requires the optional development dependency `PyYAML==6.0.3`. This is not a pipeline runtime dependency. The skill takes no mandatory invocation arguments; configuration is read from `references/project.json`. The optional `--source-bundle PATH` explicitly selects audit/test provenance, as described in the source reference.

## Checks for each run

| Area | Independent method and acceptance |
|---|---|
| Source integrity | Rehash actual evidence bytes; compare XLSX parsing with an independent representation/extract where available. Check successful response is the expected business content, not a login/error document. |
| Interpretation | Compare interview definitions with actual rows by stable IDs. Record both sides of disagreement; use owner-backed clarification rather than silently choosing a value. |
| Attendance | Recalculate only separate population rows. Check overlapping need rows were excluded, confidence retained and service capacities tested against the full chosen basis. |
| Budget | Sum underlying selected packages and allowances independently. Include commitments, distinguish contingency already included from headroom, and compare category amount against both allocation and approval limit. |
| Dates and conditions | Compare expiry and hold dates to the exercise clock; preserve actual retrieval timestamps. Check service date, quote status and every conditional note. |
| Programme | Parse the generated programme/calendar; verify required windows, keynote, all twelve demos exactly once, ten-minute presentation plus three-minute changeover, meals/breaks, readiness, teardown and dependencies. Check activity overlaps while allowing explicitly labelled containing constraint windows. |
| Accessibility | Inspect the actual official PDF page beside venue text. Verify six wheelchair spaces, nine quiet-room concurrent users against 20, captioning/hearing-loop/staffing basis, and distinct official versus fictional claims. |
| Four drafts | Cross-check option IDs, totals, headcounts, dates, capacities, contingency/headroom, programme and approval states across CSV, Markdown plan, ICS and communications. Parse ICS, preserve `Asia/Taipei` plus `VTIMEZONE`, `TENTATIVE` VEVENTs and the deadline VTODO's `DUE`/`NEEDS-ACTION` without fabricated duration; all communications must be unsent drafts. |
| Snapshots | Validate nine files against the unchanged schema with format checking; verify unique IDs, run binding, evidence locators, consumed/produced identities, exact predecessor hashes and final artifact hashes against actual bytes. |
| Privacy and submission | Inspect tracked files and staged diff for credentials, tokens, attendee contacts and personal medical data. Confirm remote repository and pushed revision, then verify matching Entire checkpoint/capture evidence. |

## Meaningful failure and recovery tests

Run `.venv/bin/python -m unittest discover -s tests -v` and inspect its actual report. Test fixtures and isolated output directories must remain visibly separate from remote-source retrieval evidence. A test that injects a transport failure proves handling of that failure; it does not establish current source availability.

- Reorder records and columns and add unrelated columns: totals and semantic results remain stable.
- Raise population to 261: Q-003 capacity fails and Q-004 is reevaluated, with consistent drafts. Test a value above 300 as well; inventing another package is not a recovery.
- Change a price or committed amount: costs, allocation variance, approval-limit result, ceiling headroom and recommendation all update. Preserve the prior run.
- Inject unavailable/malformed input: retain the failure, identify affected claims/owner and continue only supported work. Exercise duplicate identities and ambiguous/missing required fields.
- Expire a quote relative to the business clock, or move its date: the option cannot remain silently feasible.
- Remove/corrupt an output or predecessor: validation detects it; recovery creates a traceable replacement and rechecks hashes and consistency.

Source outages observed in a real run are recorded as actual access results. Synthetic outages and changed-input tests are labelled test scenarios. Never describe a future test plan or expected baseline as a passed test.
