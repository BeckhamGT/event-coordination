<!-- upstream: INDEX.md -->
---
style: descriptive
---

# training

## Purpose

Your work from before you have a client. Stage 1 of the programme is roughly forty-six hours across
seven modules and twenty-five competencies, and several of them are graded on artifacts that have no
client in them at all — a seeded-error exercise is marked against a known seeding, not against a
business.

That work is assessed the same way engagement work is: as files in this repository. It needs a home
that is not a client directory, because inventing `engagements/practice/` would put a fake client into
the one namespace the whole layout depends on being real.

## Inventory

| Item | What it is | Class |
|---|---|---|
| `<module-id>/` | One directory per module, named for the module — `m-00`, `m-01`, and so on | Mutable |
| `onboarding/` | The record of your own setup — what is done, what is outstanding. Written by the `onboarding` skill. Not a module, and the only directory here that is not named for one | Mutable |
| `project-c/` | Project C assignment review and planning notes; assessed submission files follow the formal assignment's repository paths | Mutable |

Project C is filed by the course's supplied project name; no numbered module ID was supplied.

## Freshness

| Item | Last updated | Class | Status |
|---|---|---|---|
| — | 2026-08-11 | Mutable | empty until Stage 1 starts |
| `project-c/` | 2026-10-12 | Mutable | Assignment read; implementation prerequisites remain open |

## Conventions

Practice interviews go here too, not in `engagements/`. A practice session produces the same artifact
set as a real one and has no client slug to file under — put it in the module directory it belongs to.
