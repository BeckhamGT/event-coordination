# Runtime, source access and reproduction

The submitted live run used Python 3.9.6 in `.venv`. A clean Python 3.13 environment was also installed and tested independently during verification. Python 3.13 is the documented bootstrap choice; `requirements.txt` pins direct runtime dependencies and `requirements.lock.txt` pins the tested complete environment, including optional PyYAML for skill authoring validation. No API key is required for these disclosed public source routes.

From the repository root:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python event-planning-coordination-brief/scripts/pipeline.py
```

The final line is the single end-to-end reproduction command. The default mode retrieves the disclosed Notion brief, four Google Sheets XLSX exports, official TICC index and exact required PDF. Notion's public HTML can be a JavaScript shell; the adapter preserves that failed attempt and uses the same disclosed page identity through its read-only page API. Google export responses and original PDF bytes are saved. Transport endpoints and mutable public sources can change; a future run must report its own outcomes rather than promise the submitted result.

Every actual stage is written immediately, with a unique snapshot ID, shared run ID and exact predecessor hash. The original interview and schema hashes are checked before use. Prior current drafts/evidence are byte-verified into history before replacement. Historical root-relative paths resolve through each history manifest's original-to-archived path map. Source failures retain supported work and identify dependent claims/owners. Catastrophic failures write `deliverables/failure.json`; process exit 0 alone is not proof of complete planning—inspect `deliverables/run.json`.

The optional `--source-bundle PATH` is explicitly an audit/test of already-observed source bytes with original retrieval timestamps and matching registry hashes. It is not a remote retrieval or an automatic fallback for failed network access. Tests use it in temporary roots; the submitted current run uses live retrieval.

## Verification commands

```sh
.venv/bin/python -m pip check
.venv/bin/python -m unittest discover -s tests -v
entire status
entire doctor
entire session current --json
entire checkpoint list --json
```

Entire 0.11.3 has Codex hooks installed and approved. Actual transcript-marker checks—not only the enabled flag—are recorded in `verification/final-setup-and-capture-check.json`. Raw transcripts stay outside ordinary project commits; Entire's checkpoint storage retains development capture. Commit hooks add the checkpoint trailer and push capture with the project revision. Verify the resulting commit/checkpoint association and remote revision after pushing.

The facilitator's clarification removes the previous sign-off gate: onboarding covers identity and remaining technical setup is self-checked. No facilitator approval record is created. Actual plan, venue/date and category spending approvals remain pending. All communications and calendar artifacts are unsent drafts.

The pinned local skill scanner was installed with the user's authorization, using Homebrew pipx and Python 3.13. Scanner dependencies are isolated from project dependencies. The local-only report and manual dispositions are under `verification/`; a clean high-severity count is not a safety certification.
