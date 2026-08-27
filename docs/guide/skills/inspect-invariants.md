# `inspect-invariants`

> `audit-trace` proves a `Respects: ARCH-N` citation points at a live invariant. This proves the design actually honors it — the semantic judgment `audit-trace` refuses to make.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `docs/architecture/` (the spine); a feature `design.md` or a diff |
| **Writes** | nothing — it returns verdicts |
| **Calls** | nobody |
| **Called by** | [`inspect-change`](inspect-change.md), [`build-in-waves`](build-in-waves.md) (task review), [`define-project`](define-project.md) (validate mode) |

## When it fires

When a design or diff cites architecture invariants (a `Respects: ARCH-N` line, or a change in a repo that has `docs/architecture/`) and someone needs to know whether it **actually conforms**. If there is no `docs/architecture/` spine, it says so once and stops — it only runs where a project has opted into the architecture layer.

## The judgment

For each cited invariant (and each clearly-relevant uncited one), it reads the rule, reads what the design or diff does, and returns one verdict with a one-line rationale:

| Verdict | Meaning |
|---|---|
| **respects** | consistent with the invariant |
| **violates** | does something the invariant forbids, or omits something it requires |
| **unclear** | neither clearly honors nor clearly breaks it — a human should look |

## Why it is separate from `audit-trace`

The audit-trace check is deterministic — `grep` and set-difference — and it is deliberately kept that way (**ARCH-1**). "Does this design *truly* respect ARCH-2?" is a judgment, so it cannot live inside `audit-trace` without making the result depend on the reader. `inspect-invariants` is that judgment, split out: **advisory**, LLM-judged, and never a hard merge gate. `inspect-change` surfaces its verdicts in a separate advisory lane; `audit-trace` keeps checking only existence and liveness (E4/E5/W3).

## See also

- [`audit-trace`](audit-trace.md) — the deterministic referential-integrity counterpart (E4/E5/W3)
- [`inspect-change`](inspect-change.md) — runs this as an advisory third lane
- [`define-project`](define-project.md) — runs it in validate mode
- [`design-solution`](design-solution.md) — produces the `Respects: ARCH-N` citations it judges
