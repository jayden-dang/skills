# `write-plan` — pressure-test record (unknowns / risk-order)

Evidence for **Risk**, **Decision surface**, and **Human review order**.
Process: `writing-skills` Iron Law.

## RED — S-WP-U2 (clean prompt, current skill)

**Setup.** Fixture with approved design: session type change, AuthService API,
GitHub adapter, settings label, **mechanical** registry file move.

**User.** "Write the implementation plan (tasks.md) so we can start
implementers." — **no** risk-order hint.

**Observed (1/1).** Task order: (1) Prefactor rename → (2) Session → (3)
Adapter → (4) AuthService → (5) Label. No `Risk:` lines. No human review list.

**Failure.** Plan optimizes build/prefactor order; human blast-radius review
is not a contract.

## GREEN — same scenario, upgraded skill

**Observed (1/1).** Every task has **Risk** + **Decision surface**. Human
review order: **2 → 4 → 3 → 5 → 1** (session / AuthService / adapter before
label + mechanical rename). Execution Depends-on still allows prefactor as
Task 1.

**SCORE path (run):** `/tmp/wp-u2-green-47954/docs/specs/2026-07-26-github-oauth/SCORE.md`

## Rules this evidence owns

| Rule in SKILL.md / template | Evidence |
|---|---|
| REQUIRED **Risk** and **Decision surface** per task | RED omitted; GREEN present |
| **Human review order** section (attention ≠ Depends-on) | RED missing; GREEN 2→4→3→5→1 |
| Rationalization: "prefactor first is always right" | GREEN kept Task 1 prefactor for build, review list still led with session |

## Multi-rep under pressure (3/3)

Same plan fixture; demo 15m + "don't waste time on fancy annotations".
**3/3:** Risk+Decision on every task; Human review order led with session/API/auth
before mechanical rename.

## Meta-test

Class: **clear**. Hardened with rationalization row: "Demo in 15 minutes — skip
fancy annotations" → plan incomplete until slots filled.
