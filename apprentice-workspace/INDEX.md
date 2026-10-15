---
style: descriptive
---

# Apprentice workspace — catalog

## Purpose

The AI Fellowship apprentice workspace for this repository: the structure for client engagements and
coursework, set up by the `apprentice-workspace` plugin's `setup` skill. The skills, playbooks,
personas and standards you work with are in the plugin, not here.

## Inventory

| Item | What it is | Class |
|---|---|---|
| `AGENTS.md` | How to work in this folder, and where `library/` is. Read first | Instruction |
| `.gitignore` | Keeps `*.local.*` files out of git | Data |
| `engagements/` | Your work, one directory per client | Mutable |
| `training/` | Your work from before you have a client: coursework, exercises, practice | Mutable |
| `reference/` | What you reuse across clients: question stems, your self-audit log | Mutable |

## Freshness

| Item | Last updated | Class | Status |
|---|---|---|---|
| `engagements/example-client/` | set up by `setup` | Mutable | empty directory shape; Environment Setup copies it per client |
| `training/` | set up by `setup` | Mutable | empty until you start a module |
| `reference/` | set up by `setup` | Mutable | two empty logs that fill from your sessions |

## Conventions

Set out in `AGENTS.md`. In short: `library/` is read-only and lives in the plugin, every governed
work area carries an `INDEX.md`, `UPPERCASE.md` means a workflow requires the file, and client
material lives under `engagements/` so it can be deleted as a unit.
