<!-- upstream: INDEX.md -->
---
style: descriptive
---

# engagements

## Purpose

One directory per client engagement. This is the unit of work: an engagement starts, it ends, and it
belongs to one client — so it is filed as a unit and can be deleted as a unit when the relationship ends.

## Inventory

| Item | What it is | Class |
|---|---|---|
| `example-client/` | An empty engagement with the six subdirectories in place. Environment Setup copies it, then creates the engagement's notes and decision register | Mutable |

## The six subdirectories

| Directory | What lands there |
|---|---|
| `interview/` | Transcripts, session notes, the pre-session note, the discovery record, the ambiguity list |
| `process/` | The reconstructed process, its boundaries, its exceptions, what happens when it breaks |
| `spec/` | The signed PRD, automation decision brief and technical specification under construction |
| `deliverable/` | The agreed client-operated files, canonical deployment/operations instructions and known defects; one agent skill is the common default |
| `handover/` | The owner-facing account, client package manifest and final versioned handoff archive |
| `verification/` | Internal Validator reports, source map, comprehension and operational-acceptance records, candidate manifest and permitted evidence; never included in the client package |

## Freshness

| Item | Last updated | Class | Status |
|---|---|---|---|
| `example-client/` | 2026-08-15 | Mutable | empty directory template with internal verification boundary; root control files are created per engagement |

## Conventions

Directory name is the client slug in kebab-case. Nothing about one client goes in another client's
directory, and nothing shared across clients goes in either — that belongs in `reference/`.
