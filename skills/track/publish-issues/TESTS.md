# TESTS.md — publish-issues

## 2026-11-01 — follow the repo's issue format (1.0.0 → 1.1.0)

Design: `docs/design/2026-11-01-issue-format.md`. Fixture: a generated repo with an in-repo tracker CLI
and the new `Issue format` seed. Prompt: two approved slices, the second blocked by the first. Scored
from the tracker's JSON.

**RED, 1.0.0** (sonnet 1 and haiku 1 with a blocking relation, haiku 1 without).
- Format: 3/3 followed the seed over the skill's own template and marker line, and each said so: "the
  repo's rule wins". The format itself did not fail, so nothing new was written for it. The
  duplicate templates and the marker line were deleted, since they contradict the seed.
- No blocking relation: 1/1 left the blocked slice with `enhancement` alone. "I used `needs-triage`
  nowhere so triage doesn't pick #2 up." That breaks the one-state rule.

**Form.** An observable rule: every slice takes the same state role, and the edge holds it back.

**GREEN, 1.1.0.**
- No blocking relation, sonnet 1 and haiku 1: 2/2 gave both slices `ready-for-agent` with a `Blocked by: #1` line.
- With a blocking relation, haiku 1: both slices `ready-for-agent`, the edge in the tracker's field, and the requester's plan left out.
- Not yet approved, haiku 1: stopped at the breakdown and created nothing.
