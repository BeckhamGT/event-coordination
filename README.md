# Event Planning & Coordination — Project C

Reusable skill and Python implementation for evidence-backed event options and consistent planning drafts. This repository is the learner's submission fork, [BeckhamGT/event-coordination](https://github.com/BeckhamGT/event-coordination).

## Reproduce the planning package

Use Python 3.13 and install the pinned dependencies in a virtual environment:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
```

Run this single end-to-end command from the repository root:

```sh
.venv/bin/python event-planning-coordination-brief/scripts/pipeline.py
```

The default command reads all seven disclosed remote sources, writes each of nine snapshots at its actual stage boundary, and generates four draft files. It archives the previous current run before replacement, including failed attempts. It never sends communications or writes calendars externally. The exercise clock is **2026-08-26 12:00 Asia/Taipei**; retrieval timestamps remain actual UTC observations.

Before assessed work, verify active Entire capture and the unchanged interview export. Setup is self-checked: the facilitator clarified that onboarding covers identity and there is no facilitator sign-off. Operations and spending approvals remain pending. See [runtime and capture](RUNTIME.md), the [skill entrypoint](event-planning-coordination-brief/SKILL.md), and [performed verification](verification/implementation-verification.md).

## Current draft package

Live run `run-20261015T030818Z-00ca2bd3` retrieved all seven sources, validated all nine linked snapshots and recommends Q-003 for review. Both catering variants remain in the comparison. Q-003 totals TWD 494,000 with TWD 26,000 remaining ceiling headroom; Q-004 totals TWD 512,000 with TWD 8,000 headroom. Both include communications TWD 25,000 and contingency TWD 40,000. Feasible exercise drafts are not bookings or approvals.

| Artifact | Purpose |
|---|---|
| [Vendor comparison](deliverables/vendor-comparison.csv) | Both catering variants and rejected alternatives, evidence and approval states |
| [Event plan](deliverables/event-plan.md) | Attendance, costs, full programme, evidence limits and pending owners |
| [Calendar](deliverables/event-calendar.ics) | Tentative source records and activities; exact decision deadline as unsent VTODO |
| [Communications](deliverables/draft-communications.md) | Unsent review, attendee and vendor drafts |
| [Run receipt](deliverables/run.json) / [snapshots](deliverables/snapshots/) | Actual source outcomes, nine-stage chain and actual-file validation |
| [History](deliverables/history/) | Original preparation, updated stages 01–04 and actual blocked run |

Run the independent regression suite after setup:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

The tests use clearly labelled synthetic changes in temporary roots and actual archived source fixtures. They do not replace live retrieval evidence. Reordered fields/records, changed attendance/prices/commitments, unavailable or invalid sources, missing required calendar meanings, and missing/corrupt outputs and predecessors are covered. See the verification record for actual results, corrections and unresolved limitations.

## Original assignment and interview rules

1. Read the [formal assignment](https://private-pecorino-70e.notion.site/Project-C-Event-Planning-Coordination-Brief-Learner-assignment-3da0b700541e813a8a91d0741d6ac96a?source=copy_link) for the work and acceptance requirements.
2. Create your own repository from [this starter](https://github.com/GitRollTraining/event-coordination) using **Fork**, then clone your copy and work there.

## Supplied files

| File | Purpose |
|---|---|
| `README.md` | Starting instructions and links. |
| `snapshot.schema.json` | Public snapshot contract; keep it unchanged. |

Create the Skill, implementation and outputs described in the formal assignment. This starter supplies no business workflow implementation.

## Before you work

**Interview rule.** You conduct the stakeholder interview yourself, and the questions are yours. Do not connect a coding agent or any other AI to the interview to run, script, or automate it. The interview transcript is assessed together with the code; a project whose interview was run by an agent is not scored.

- Export your interview as the original Work Sim Markdown, save one final complete file per session under `interviews/`, and commit and push it with your code. Do not rewrite the export. If the export is unavailable, contact the facilitator.

- Use an Agent Skills-capable coding environment. Choose and document your implementation runtime and dependencies; no runtime or install command is supplied here.
- Follow the [shared course guide for session capture](https://classroom.google.com/c/ODcyMjA4NTkwNDk2/m/ODc0NzI2NzQzMzQ2/details) and verify capture is active before implementation. Keep credentials out of the repository.
- Meet the [stakeholder](https://work-sim.catalyte.ai/s/project-c-event-coordination) to understand the work and relevant business sources. Read those online sources through their intended access route; an unavailable source is not permission to substitute repository data.
