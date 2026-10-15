<!-- upstream: engagements/example-client/INDEX.md -->
---
style: descriptive
---

# verification

## Purpose

Internal evidence for the exact candidate and handoff package that were checked. Validator A writes the
delivery manifest, report and permitted reproducible evidence here. Validator B writes the handoff
report here. This directory is part of the engagement record, not the client delivery boundary.

## Inventory

Empty. Validator A may create:

```text
deliverable-report.md
deliverable-manifest.tsv
evidence/
  commands/
  fixtures/
  observed-results/
```

Validator B may add `handoff-report.md`; the post-B client deployment and independent owner run add
`operational-acceptance.md`. Evidence stored here must obey the engagement Data & Credential Boundary;
use an access-controlled pointer when the evidence itself cannot be retained safely.

Output Phraser and the comprehension gates may also create:

```text
handoff-source-map.md
persona-preflight.md
owner-acceptance.md
```

The source map traces material `HC-*` claims without exposing those internal identifiers to the client.
The persona report records its restricted prior knowledge; the owner record names the exact package and
owner-facing hashes accepted or rejected. Operational acceptance names the same B-passed package and
records whether it was deployed and operated independently in the intended client environment.

The paths above are the **current** records. Before replacing one, snapshot the complete mutable run set
it cites — not only the report — under `history/<stage>-<YYYYMMDDTHHMMSSZ>/`, retaining every copied
artifact's original engagement-relative path. Verification artifacts therefore land in that snapshot's
`verification/` child; cited `spec/`, `process/` or other engagement authorities keep those paths too.
For Validator A this includes its report, deliverable manifest and cited evidence; for later gates it
includes the report or acceptance record plus the source map, package hashes and every otherwise
mutable local authority needed to resolve its retained pointers. If the Data & Credential Boundary
forbids copying an authority, record a durable, immutable, access-controlled external pointer instead.
Hash and inventory the snapshot in `history/INDEX.md`. Put the full engagement-relative archived record
path, for example
`verification/history/validator-a-20260815T041500Z/verification/deliverable-report.md`, in the new
record's `supersedes` field. Never edit an archived run or a failed/passed current run into a different
verdict. Run directories are evidence bundles inventoried by `history/INDEX.md`; they do not each need
another nested INDEX.

Treat each `history/<stage>-<timestamp>/` directory as a synthetic engagement root. An
engagement-relative pointer retained inside an archived report, such as
`verification/deliverable-manifest.tsv`, resolves below that snapshot root, never against the current
engagement files. Put `snapshot-manifest.tsv` at the snapshot root with the original
engagement-relative path, archived path and SHA-256 for every copied artifact; inventory that manifest
in `history/INDEX.md`. A reviewer starts from the archived record named by `supersedes`, finds its
snapshot root, verifies `snapshot-manifest.tsv`, and resolves all retained pointers inside that root.

Do not put this directory, either validation report or internal evidence into the client package.

## Freshness

| Item | Last updated | Class | Status |
|---|---|---|---|
| — | 2026-08-15 | Mutable | empty; populated by Phraser, comprehension gates, Validator A/B and operational acceptance |
