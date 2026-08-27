# Handoff capsule

## Contents

- [When](#when)
- [Routing](#routing)
- [Capsule fields](#capsule-fields)

## When

| Gap | Behavior |
|---|---|
| Non-blocking `open_gap` | Ledger entry; **continue** tour |
| Blocking gap / need foundation or drill | **Stop** checkpoint; write claim + evidence + scope + `next_probe`; emit **one** capsule |

Never explain-then-reprobe inline. Never auto-invoke a user-invoked skill.

## Routing

Name **exactly one** primary route:

| Situation | Name |
|---|---|
| Missing mental model / foundation / repo structure | `/deepen-codebase` |
| Need procedure/prediction practice until they can do it | `/teach-pack` |
| Focus is a **resolved range** and user wants a comprehension **packet** | `/study-change` (coexistence — **not** a remediation route) |

Optional: repeated misconception → prefer naming `/teach-pack`.

## Capsule fields

focus/CODE · checkpoint id · ledger path · learner claim · observed evidence ·
gap kind · blocking reason · next_probe · suggested route

Do not dump raw personal notes or full handoff history into chat beyond the capsule.
