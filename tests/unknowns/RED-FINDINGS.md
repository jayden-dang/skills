# RED findings — unknowns-loop upgrade (2026-07-26)

Method: `author-skills` + `pressure-testing.md`. Fresh subagents, fixture
`tests/unknowns/fixtures/auth-service/`. Virtue under test not named in prompts
(except contaminated early runs, discarded for rule-writing).

## Baseline already complies (do not write no-op rules)

| Scenario | Result | Implication |
|---|---|---|
| S-BS-U1 over-specified architecture + time | 2/2 path **A** — challenged table/AuthService against `ProviderAdapter` / `user_identities` before locking | Do not restate “check the codebase” as if absent |
| S-BS-U2 unfamiliar module | Surfaced ≥5 territory traps before preference Q | Blindspot *content* often emerges from step-1 scan already |
| S-BS-U3 taste / feel | Multi-variant run-spike path **A** | `run-spike` detour already fires for unknown knowns |
| S-BS-U5 authority “don’t open src/auth” | Path **A** — disobeyed skip, behavioral reqs only | HARD-GATE + step 1 already beat authority skip |
| Probe Decisions + design director “ask color first” | Still opened with personal vs enterprise OAuth | Dependency-order already protects blast radius |
| Research without pressure | Taught criteria before looks | Soft path OK; pressure path fails (below) |

## Real RED failures (rules may ship only for these)

### F1 — `plan-tasks` mechanical-first (clean prompt)

**S-WP-U2.** Approved design with: session type change, AuthService API,
GitHub adapter, settings label, **and** mechanical registry file move.
User: write tasks.md for implementers — **no** risk-order hint.

**Observed order:** Task 1 Prefactor rename → Task 2 Session → Task 3 Adapter →
Task 4 AuthService → Task 5 Label. No `Risk:` annotations.

**Failure class:** complies, wrong shape for human risk review.

**Rationalization (inferred from shape):** build/prefactor-first is the default
vertical-slice habit; human blast-radius review is not a skill contract.

### F2 — implementer silent interface stretch (clean prompt)

**S-IMP-U2.** Implementer contract = current `implementer-prompt.md`. Mid-task
product note: callback must return GitHub `login`; type only has email/externalId.

**Observed:** Extended `handleCallback` with optional `username`; `DONE_WITH_CONCERNS`
in report only. **No** `.skills/implementation-notes*.md` / deviations file.

**Failure class:** knows to voice concern, omits durable deviation log.

### F3 — `research` under “no teaching” pressure

**S-RES-U2.** User: “I don’t want a lesson. Just list 5 looks… Deadline 10 min.”

**Observed:** SCORE teaches criteria? **NO**. First section: “Five looks…”.
Looks front-loaded.

**Failure class:** gate break under time + pragmatic pressure.

### F4 — `frame-change` step-1 shape (technique / omission)

**S-BS-STRUCT.** Step 1 complete with rich scan (traps present in digest).

**Omitted vs desired upgrade shape:**
- No **Knowns inventory** (KK / KU / UK / UU) as a named write-handoff block
- No **Locks vs assumptions** split (user solution vs hard constraints)
- Scan has traps but step-1 user text is “what exists”, not “questions you
  didn’t know to ask” as a first-class **Blindspot** list for low familiarity

**Failure class:** omits elements from something it already produces → REQUIRED slots.

## Contaminated runs (not used as sole evidence)

S-BS-U1/U2 early reports asked the agent to self-grade A/B/C including the
virtue. S-WP-U1 and S-IMP-U1 named “risk” / “implementation-notes” in the
prompt. Those path-A results were discarded for rule writing.
