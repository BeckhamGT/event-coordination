# Runtime and reproduction

Python3.9 or newer is required. All implementation dependencies are pinned in `requirements.txt`.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python event-planning-coordination-brief/scripts/pipeline.py
```

The last command will be the single end-to-end command once implementation is complete. It must attempt the disclosed remote sources and write each snapshot when its stage is reached. It will retain real retrieval failures and valid partial work. It will not send messages or publish to calendars.

Development capture is Entire for Codex. Run `entire status`, `entire doctor` and `entire session current --json` to inspect it. Checkpoint/remote verification belongs to the submitted revision; a local enabled flag alone is insufficient.

Facilitator clarification: onboarding covers identity; remaining setup is self-checked, with no facilitator sign-off. Actual Operations and spending approvals remain pending. This document records a technical setup procedure, not an approval.
