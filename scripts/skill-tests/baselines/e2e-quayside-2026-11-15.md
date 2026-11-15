# End-to-end baseline: idea → shape → go (2026-11-15, commit 2c0d503, Sonnet subagent)

Fixture: `make-quayside.sh` with all 80 skills in `.claude/skills/` and `INDEX.md` (the listing). One
agent, three operator turns (Lan), no subagents or tmux available to it.

| Turn | Operator sends | Agent stops at | Tracker | Cumulative tokens / tool calls / seconds |
|---|---|---|---|---|
| 1 | `/idea` + the zero-payment report | ticket #14 filed, framed, card written, two questions | `bug` + `status:shaping`, lan | 40k / 11 / 45 |
| 2 | answers + `/shape #14` | cause and PAY-1.4/1.5 drafted, waits for approval | unchanged, one comment | 51k / 17 / 88 |
| 3 | approval + `/shape #14` + `/go #14` | built, reviewed on both axes, PR not opened | `status:ready` then `status:building`; `Requirements covered:` on the body | 76k / 30 / 158 |

Artifacts: branch `fix/pay-zero` off `dev`, two commits (spec approved; fix), `src/payments.js` one
condition, two new tests, red watched first (`actual: 500, expected: 400`), `npm test` 11/11,
`.skills/PAY/tickets.md`. No code before approval. No approval supplied by the agent.

Fixture limits, not skill results: `bin/gh` has no `pr create` and the repo has no remote, so the run
ends before `in-review`; the two-axis review was done inline because the agent cannot dispatch.

Use: rerun after any consolidation. Same stops, same artifacts, tokens and tool calls not higher.

## After the merges (same day)

| Set | Turn 1 `/idea` | Turn 2 `/shape` | Turn 3 `/shape` + `/go` | Artifacts |
|---|---|---|---|---|
| 80 skills, commit 2c0d503 (baseline) | 40k / 11 / 45s | 51k / 17 / 88s | 76k / 30 / 158s | 2 commits, 11 tests, ticket `status:building`, no receipt |
| 80 skills, commit 2c0d503 (baseline, second run) | 46k / 8 / 38s | 58k / 14 / 76s | 90k / 26 / 146s | 3 commits, 11 tests, ticket `status:building`, no receipt |
| 62 skills, commit 3eef518 (15 merges + trims) | 46k / 8 / 38s | 58k / 14 / 65s | 89k / 31 / 133s | 2 commits, 11 tests, ticket `status:building` |
| 59 skills (build family merged, final trims) | 45k / 9 / 41s | 53k / 14 / 74s | 90k / 29 / 146s | 2 commits, 10 tests, ticket `status:building`, `close-receipt.md` written |

Figures are cumulative tokens / tool calls / seconds. Same three stops for the operator in all
three; no production code before approval; no approval supplied by the agent; red watched first.
The 59-skill run added one test, not two (the guard is covered by the two existing payment tests),
and was the only one to write the close receipt. The two baseline runs on the same 80-skill commit spread from 76k to 90k tokens, and both
later runs (89k, 90k) fall inside that spread: the merges neither cost nor saved tokens that this
table can show.
