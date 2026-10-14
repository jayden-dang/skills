# TESTS.md — refresh-roadmap-status

## 2026-10-14 — R11 covers S8 (1.1.0 → 1.2.0)

Template sync from plan-milestones 1.2.0: the roadmap gained the `After:` item-order
field and structural rule `S8` (a dangling or self `After:` target, or a cycle).
`R11` now names `S8`, so this check withholds its next action on a cyclic or
dangling `After:`. RED/GREEN evidence for the field itself is in plan-milestones'
TESTS.md (2026-10-14); nothing in this skill's own text changed except the rule
range `S1`–`S8`.
