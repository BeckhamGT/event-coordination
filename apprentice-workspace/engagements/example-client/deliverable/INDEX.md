<!-- upstream: engagements/example-client/INDEX.md -->
---
style: descriptive
---

# deliverable

## Purpose

The agreed deliverable the business receives. The default implementation is an agent-executable
`skill.md`; adapt the inventory when the signed specification requires a larger package. Every shape
also carries canonical deployment and operations instructions. Non-blocking findings from an applicable
reviewer are written down here, not dropped.

## Inventory

Empty. **The interview playbook does not fill this directory either.** In the default shape, `skill.md`
is written from the specification in `../spec/`, using `create-skill`, and then attacked with the
`adversarial-reviewer` persona before it goes anywhere near the owner. A larger solution keeps the same
traceability and records each delivered component in this INDEX.

Every populated deliverable includes:

- `deployment.md`, copied from `library/templates/deliverable-deployment.md`: prerequisites,
  installation, configuration, start, verification, upgrade or replacement, rollback and uninstall
  where applicable; and
- `operations.md`, copied from `library/templates/deliverable-operations.md`: normal use, monitoring,
  failure response, recovery, credential rotation or revocation, maintenance and escalation.

These files, not a handover summary, are the canonical operating instructions. Add a client-runnable
smoke or health check when practical and inventory it here.

`known-defects.md` sits beside it and holds every non-blocking finding the reviewer raised. Deferring
a defect in writing is delivery; leaving it out is not.

## Freshness

| Item | Last updated | Class | Status |
|---|---|---|---|
| — | 2026-08-15 | Mutable | empty; required delivery contracts defined |
