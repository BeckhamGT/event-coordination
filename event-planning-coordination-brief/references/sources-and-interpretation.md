# Sources and interpretation

Read this reference when capturing sources, assigning meaning to fields or resolving a changed record. `project.json` holds executable configuration; the retrieved records remain the source of current amounts, capacities, dates and status.

## Disclosed source routes and ownership

| Role | Disclosed identity / intended route | Interpretation and resolution owner |
|---|---|---|
| Event brief and venue note | [Notion page](https://app.notion.com/p/3ba0b700541e81d0af55dc1a8f49f5af), page ID `3ba0b700541e81d0af55dc1a8f49f5af` | Operations owns objective, room allocation, business clock, readiness and programme clarifications. Preserve the distinct versions `EVENT-BRIEF-2026-08-26`, `VEN-2026-08-26`, `VEN-2026-08-26-R2`, `PROG-2026-08-26-R3`. |
| Attendee signals | [Google Sheet](https://docs.google.com/spreadsheets/d/1IXAEAFsZM6Q9IZZ_9pGqbFQ7l2ikr-oThqrEKudHwIU), `Attendee Signals` | Learner Experience owns the population and needs signals. `signal_id` is identity; `source`, `segment`, `signal`, `value`, `unit`, `observed_at`, `confidence` give meaning and uncertainty. |
| Budget | [Google Sheet](https://docs.google.com/spreadsheets/d/1Cxo7CvcgImz9HbT8PThZyvaTuyd44ug7w5rBA1z5qlM), `Budget` | Each row's named owner controls its category. Distinguish `planned_amount_twd`, `approval_limit_twd`, `committed_amount_twd` and `record_version`. |
| Calendar constraints | [Google Sheet](https://docs.google.com/spreadsheets/d/1f_i6tUCHbJV-Ug_j6U3T4LEZ3yAr2ucdBnID-4C_-8s), `Calendar Constraints` | Operations and Programme own timing; use row `owner`, `constraint_id`, `constraint_type`, `start_at`, `end_at`, `priority`, `notes`, `record_version`. |
| Vendor register | [Google Sheet](https://docs.google.com/spreadsheets/d/1cULbGrOQS-vuj862nV2EWND4oe0H5kf-smJ85VZegko), `Vendor Quotes` | Operations with Programme owns quotes and availability. `quote_id` is identity; package scope, category, amount, capacity, date, expiry, status and notes all constrain use. |
| Official accessibility index | [TICC index](https://www.ticc.com.tw/wSite/lp?ctNode=398&mp=2&xq_xCat=6) | Official public route to the required diagram; preserve relevant links, response metadata and bytes. Operations resolves any mismatch with exercise claims. |
| Required official 4F plan | [TICC PDF](https://www.ticc.com.tw/wSite/public/Attachment/f1710485827023.pdf) | Save actual successful PDF bytes. Inspect the complete page visually and record page/region locators. Distinguish visible layout/symbols from case assumptions and current operating conditions. |

Each retrieval records actual timestamp, source identity and URL, transport/result, content type, provider/version metadata when available, raw bytes, SHA-256, local reference and observations. Preserve failed attempts alongside a subsequent successful route. Authentication pages and HTML error bodies are not successfully retrieved business records. An unavailable source leaves its dependent claims unverified; continue only independent work supported by other evidence.

An explicit audit/test use of an archived source bundle must identify the originating retrieval time/hash and mark the run mode. It is never a fresh remote retrieval. Avoid undisclosed local substitutes. For a browser/connector-only source, preserve that route's actual captured result and limits rather than inventing a generic HTTP success.

The CLI's sole optional workflow flag is `--source-bundle PATH`. Use it only when deliberately auditing/testing previously observed source bytes and their `source-registry.json`; default execution performs live reads. Both modes are valid per-invocation choices with materially different provenance, so the audit branch cannot be inferred from ordinary configuration. Check the requested bundle's recorded identities/hashes before use. Never add the flag just to conceal an outage in a live run.

## Evidence hierarchy and conflict handling

- The learner's original Work Sim export establishes stakeholder statements and field meanings; preserve it unchanged. The skill must not conduct or script another interview.
- Retrieved source rows establish current supplied exercise facts. Compare them with interview statements by stable ID, not row position. Preserve disagreement with both locators, affected outputs and the source owner; a later clarification needs its own provenance.
- Learner planning choices select how to handle uncertainty and trade-offs. They grant neither Operations approval nor spending approval.
- Assumptions are planner choices unsupported by an explicit source; label their rationale, impact and resolution owner. Never transform a missing hard constraint into a favorable assumption.
- Newly authored exercise clarifications may postdate the simulated clock. Their explicit clock override permits case evaluation; their metadata remains actual and they do not establish a historical retrieval or real-world venue condition.

## Population and service basis

The interview defines separate populations: fellows, partners, staff, speakers and forecast walk-ins. The supplied baseline is `148 + 32 + 18 + 12 + 35 = 245`; the 35 walk-ins have medium confidence and are already included. Wheelchair spaces, companions, captions, hearing loops, quiet-room requests and dietary needs overlap those people. The interview's quiet-room basis is nine simultaneous users. The 80% target applies to 180 registered fellows/partners, so the success threshold is 144 check-ins; service capacity remains 245.

The learner chose no additional attendance margin, Q-003 as preliminary preference and Q-004 as a capacity alternative. Test attendance above 260: Q-003 then fails capacity; Q-004 remains capacity-supported only through 300 and subject to all other constraints. Updated signals require recalculation rather than preserving 245 by decree.

## Costs, conditions and approvals

All supplied quotes are flat packages. Charge each selected quote once, not once per person. Keep the TWD 25,000 communications and TWD 40,000 contingency allowances. Existing commitments count toward the ceiling and require explicit treatment to avoid double-counting already committed scope. Record an allocation variance separately from an approval-limit breach.

For the supplied zero-commitment rows, the two base bundles use Q-001, Q-005, Q-006, Q-009, Q-010 and either Q-003 or Q-004. Expected totals are TWD 494,000 and 512,000, **including** contingency. Remaining ceiling headroom is separately TWD 26,000 and 8,000. Security's TWD 28,000 exceeds its TWD 25,000 allocation but remains below its TWD 35,000 approval limit. These are baseline checks, not constants to reuse after a source change.

Q-007 lacks the hearing loop; the baseline cannot silently substitute it for Q-006. Q-008 adds TWD 55,000: production becomes TWD 133,000 and total TWD 549,000/567,000, exceeding the TWD 100,000 production limit and TWD 520,000 overall ceiling. Keep livestream rejected with both financial reasons and its unresolved network test/venue confirmation. Category approval cannot override the overall ceiling. `held`, `available` and `conditional` describe quotes, never authorization.

Operations approves the plan, date and venue; named category owners approve spending. The fictional readiness R2 supplies exercise schedule feasibility for either base catering bundle, including pre-opening readiness and teardown. Feasibility does not imply a real test, reservation or approval. Record actual later decisions only with actor, subject, plan revision, timestamp, outcome and reasons.

## Schedule and visual evidence

Preserve the October 17 access window 07:30–18:30, programme 09:30–17:00 and keynote 10:00–11:00 in Asia/Taipei. Twelve named team demos each need ten minutes plus a separate three-minute changeover: 156 minutes total, independent of attendee/speaker counts. Include opening, lunch, two catering breaks, pre-opening readiness and teardown without programme conflicts. The planner chooses compatible times; identify those allocations as planner choices.

Retain the decision deadline September 4 at 17:00, hold expiry September 5, September 25 14:00–16:00 walkthrough after venue confirmation, and October 16 15:00–18:00 rehearsal (remote backup acceptable). Represent all calendar source records with their constraint roles; a containing event window is not a simultaneous activity conflict. October 24 loses the keynote and is not an equivalent feasible fallback.

The official PDF supports room locations, facility symbols and spatial observations. The fictional venue note supplies 500 usable audience places including six wheelchair spaces, quiet-room occupancy 20, step-free case coordination and separation. The supplied plan does not establish current elevator operation, obstruction-free routes, exact usable seating or acoustic performance. Record visible page/region evidence and exercise facts separately; current real-world confirmation would remain with Operations for any actual deployment.
