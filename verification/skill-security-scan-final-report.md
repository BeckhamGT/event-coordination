# Agent Skill Security Scan Report

**Skill:** event-planning-coordination-brief
**Directory:** /Users/user/fellowship/event-coordination/event-coordination/event-planning-coordination-brief
**Status:** [OK] SAFE
**Max Severity:** MEDIUM
**Scan Duration:** 0.34s
**Timestamp:** 2026-10-15T02:57:47.888181+00:00

## Summary

- **Total Findings:** 4
- **Critical:** 0
- **High:** 0
- **Medium:** 3
- **Low:** 0
- **Info:** 1

## Findings

### MEDIUM Severity

#### [MEDIUM] Undeclared network usage

**Severity:** MEDIUM
**Category:** unauthorized_tool_use
**Rule ID:** TOOL_ABUSE_UNDECLARED_NETWORK
**Location:** event-planning-coordination-brief/SKILL.md

**Description:** Skill code uses network libraries but doesn't declare network requirement

**Remediation:** Declare network usage in compatibility field or remove network calls

#### [MEDIUM] Outbound network request primitives that can transmit data externally

**Severity:** MEDIUM
**Category:** data_exfiltration
**Rule ID:** DATA_EXFIL_NETWORK_REQUESTS
**Location:** scripts/sources.py:92

**Description:** Pattern detected: urllib.request.Request(

**Code Snippet:**
```
request = urllib.request.Request(url, data=data, headers={"User-Agent": "ProjectC-EvidenceReader/1.0", "Content-Type": "application/json"})
```

**Remediation:** Ensure network operations are necessary and document allowed destinations

#### [MEDIUM] Outbound network request primitives that can transmit data externally

**Severity:** MEDIUM
**Category:** data_exfiltration
**Rule ID:** DATA_EXFIL_NETWORK_REQUESTS
**Location:** scripts/sources.py:93

**Description:** Pattern detected: urllib.request.urlopen(

**Code Snippet:**
```
with urllib.request.urlopen(request, timeout=25) as response:
```

**Remediation:** Ensure network operations are necessary and document allowed destinations

### INFO Severity

#### [INFO] Skill does not specify a license

**Severity:** INFO
**Category:** policy_violation
**Rule ID:** MANIFEST_MISSING_LICENSE
**Location:** SKILL.md

**Description:** Skill manifest does not include a 'license' field. Specifying a license helps users understand usage terms.

**Remediation:** Add 'license' field to SKILL.md frontmatter (e.g., MIT, Apache-2.0)

## Analyzers

The following analyzers were used:

- static_analyzer
- bytecode
- pipeline

