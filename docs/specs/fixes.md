# Fixes

Tier-1 mini-spec fixes and small in-scope extensions that no feature spec owns.
Each `## N.` section is one fix, its criteria IDed `**FIX-N.M**`, appended over
time. IDs are immutable once Approved; retire by strikethrough, never renumber.
Verification in this repo is the baseline-scenario convention (no automated test
runner; `trace`'s E2 is documented-exempt — the tagged baseline is the covering
evidence). "THE SYSTEM" means the skill set — the agent executing these SKILL.md
files.

Code: FIX

## 1. Non-functional requirements as a first-class category

Status: Approved
Date: 2026-07-13

Extends `write-requirements` (`skills/spec/write-requirements/SKILL.md`) so quality
attributes — performance, security, reliability, accessibility — are captured as
first-class, traceable acceptance criteria rather than left implicit, riding the
same requirement-ID → task → test/baseline trace spine as behavioral criteria.

- **FIX-1.1** WHEN `write-requirements` authors a feature's acceptance criteria THE
  SYSTEM SHALL consider the non-functional quality attributes performance, security,
  reliability, and accessibility, capturing each one that applies as a non-functional
  requirement instead of leaving it implicit.
- **FIX-1.2** WHERE a non-functional requirement is captured THE SYSTEM SHALL write it
  as an EARS-style criterion that names a measurable-or-checkable target and its
  verification method, carrying a hierarchical ID `**CODE-N.M**` that traces through
  tasks and tests exactly like a behavioral criterion.
- **FIX-1.3** IF a quality attribute does not apply to the feature THEN THE SYSTEM
  SHALL record it as explicitly none (e.g. write `None`) rather than silently omitting
  it, so a skipped attribute is a visible decision, not an oversight.
- **FIX-1.4** (guard) WHEN a feature declares no applicable non-functional requirements
  THE SYSTEM SHALL CONTINUE TO produce behavioral EARS criteria
  (WHEN/WHILE/IF/WHERE/ubiquitous), the existing `requirements.md` structure, and both
  the tier-1 mini-spec and new-feature modes unchanged — the NFR category is additive
  and never a new mandatory approval gate.
