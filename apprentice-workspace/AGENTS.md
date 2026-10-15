# How to work in the apprentice workspace

Read this before doing anything else in this folder. It is the agent's operating instruction and the
fellow's too.

This folder, `apprentice-workspace/`, is the AI Fellowship apprentice workspace for the repository it
sits in. The `setup` skill of the `apprentice-workspace` plugin created it. **Every path in this file,
and every `engagements/`, `training/` or `reference/` path in a playbook, template or skill, is inside
this folder:** `engagements/acme/interview/` means `apprentice-workspace/engagements/acme/interview/`.
Never create those three folders at the repository root.

## Where `library/` is

`library/` is not in this repository. It is the library of the installed `apprentice-workspace`
plugin: the skills, playbooks, personas, SOPs, templates, renderers and reference notes. Every
`library/…` path in a skill, playbook or template means a file there. To find it, take the folder of
any apprentice-workspace skill you were given (it holds that skill's `SKILL.md`) and go up two
folders: a skill at `…/library/skills/onboarding/SKILL.md` has the library at `…/library/`.

## The one rule that is not negotiable

**`library/` is read-only.** You may read it, run it and copy from it. You may not edit it, and that
includes the installed copy of the plugin on this machine. Every file in it is recorded, with a hash,
in a provenance manifest kept in the plugin's own repository; editing a file breaks that record
silently, and the next plugin update overwrites the edit anyway.

If a library file is wrong, report it. Do not repair it in place.

## Where things go

| You are doing | It goes in |
|---|---|
| Anything for a specific client | `engagements/<client-slug>/` |
| Current engagement decisions, unresolved decision areas and stage gates | `engagements/<client-slug>/decision-register.md` |
| Coursework, exercises, practice interviews — anything with no client | `training/<module-id>/` |
| Interview notes, transcripts, session records | `engagements/<client-slug>/interview/` |
| The reconstructed process, its boundaries, its exceptions | `engagements/<client-slug>/process/` |
| The specification you are building | `engagements/<client-slug>/spec/` |
| The implementation and canonical deployment/operations instructions you hand over | `engagements/<client-slug>/deliverable/` |
| The owner-facing account, and the file the owner opens | `engagements/<client-slug>/handover/` |
| Internal validation reports, manifests and permitted evidence | `engagements/<client-slug>/verification/` — never include the directory itself in the client package |
| Something you will reuse on the next client — a question stem, a self-audit line | `reference/` |
| Something you were told must not leave the business | keep it out of git entirely: name the file `*.local.*`, which this folder's `.gitignore` already excludes, and record in the process notes that it exists and where it is |

The six engagement subdirectories are named for six kinds of engagement material, not
for a sequence — a session fills `interview/` and `process/` in the same afternoon, and `interview/`
receives more material after `process/` has. File as you go; an engagement you file at the end is an
engagement you reconstruct from memory.

## Every work area carries an INDEX.md

Every layer of this folder, engagement root, six structural engagement directories and independently
navigated human-maintained work area carries one: **Purpose** in one or two sentences, an **Inventory**
table listing every item with a one-line description, and a **Freshness** table. When you create a file
or directory, update the governing `INDEX.md` in the same operation. A sweep to fix this later is a
sweep that does not happen.

Companion implementation directories such as `references/`, `scripts/`, `assets/` and `eval/`, and
generated/session/evidence bundles, do not need a nested INDEX when their complete contents are
inventoried by the nearest governed parent or component entrypoint. Give one its own INDEX as soon as it
becomes an independently navigated work area. This exception avoids recursive manifest paperwork; it
does not permit an unlisted directory.

Spoke manifests declare their parent on line 1: `<!-- upstream: path/to/parent/INDEX.md -->`, with the
path written from this folder (`INDEX.md` is this folder's own manifest).

## Naming

| Casing | Meaning |
|---|---|
| `UPPERCASE.md` | A file a workflow requires structurally — `INDEX.md`, `CLAUDE.md` |
| `lowercase.md` | Content — notes, records, research |

Directories are kebab-case. Content files are snake_case or kebab-case, consistently within a directory.

## How to write

`library/sops/working-standards.md`. Four rules, one page. The one people break first: a code never
stands alone — write the thing, and bracket the code after it if it helps with filing.

## What the agent has

The skills of the `apprentice-workspace` plugin (in the ChatGPT app type `@` and pick one; in Claude
Code type `/apprentice-workspace:` and its name; ask `workspace-help` for the current list rather than
trusting a count — the skill list a session starts with leaves out the skills that start only when
the apprentice names them, so it is never the whole plugin), document shapes in `library/templates/`, the renderers that turn finished work into
a file the owner opens in `library/renderers/`, the plugins `library/sops/agent-settings.md` asks you
to install yourself, three MCP servers in the base set and three more you connect per engagement with
the client's own credentials — never ours. The full list with
reasons: `library/reference/tool-inventory.md`.

## When you finish an engagement

`engagements/<client-slug>/` is deletable as a unit, and that is deliberate: when a client relationship
ends, the material for that client goes with it. Anything worth keeping across clients is not client
material and belongs in `reference/`.
