# Unknowns-loop skill upgrade program

Source: Thariq Shihipar — *A Field Guide to Fable: Finding Your Unknowns*
Process: `author-skills` Iron Law — one skill at a time; no text without RED failure.

## Order (serial) — status 2026-07-26

| # | Skill | Status |
|---|---|---|
| 1 | frame-change | GREEN — knowns + Blindspot (F4); many behaviors already baseline-pass |
| 2 | clarify-decisions | Explicit blast-radius line; baseline already preferred high-blast Qs |
| 3 | interpret-session | Map/territory + knowns sketch + criteria (lighter evidence — no full RED) |
| 4 | plan-tasks | GREEN — Risk, Decision surface, Human review order (F1) |
| 5 | build-in-waves + implementer-prompt | GREEN — implementation-notes (F2); controller hook |
| 6 | research | GREEN — evaluation literacy under pressure (F3) |
| 7 | run-spike | No edit — multi-variant already baseline-pass |
| 8 | wiring | AGENTS.md unknowns loop; write-handoff knowns/deviations; land-branch names `/study-change` |

Evidence: `tests/unknowns/RED-FINDINGS.md`, `HARDENING.md`, per-skill `TESTS.md`,
`INTEGRATION.md`.

Hardening (session 2): multi-rep 3/3 all core skills; meta → research override
wording; controller → reroute-plan path verified; interpret-session technique pass.

## Shared vocabulary (introduced as each skill ships)

Leading words used consistently across the set (not a new skill):

- **map** — prompts, specs, plans, what the human said
- **territory** — codebase, runtime, users, history, real constraints
- **known known** / **known unknown** / **unknown known** / **unknown unknown**
- **lock** — hard constraint the agent must not treat as optional
- **assumption** — preferred solution that may be false until checked
- **blindspot pass** — surface questions the human did not know to ask
- **deviation** — mid-build departure from plan, logged with cause
- **evaluation criteria** — standards needed before choosing among options

Connectivity rule: each skill hand-off uses `REQUIRED SUB-SKILL:` for
model-invocable targets only; user-invoked skills are named for the user.

## Per-skill evidence

Each upgraded skill gets `skills/.../<name>/TESTS.md` (or `tests/unknowns/<name>.md`
if the skill folder must stay lean). Every rule row cites a RED scenario ID.
