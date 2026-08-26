# `frame-change` — knowns inventory + blindspot (unknowns loop)

## Baseline already strong (no-op if re-stated alone)

| Scenario | Result |
|---|---|
| S-BS-U1 over-specified architecture + time | 2/2 challenged `OAuthProvider`/`AuthService` against existing seams |
| S-BS-U2 unfamiliar module | Territory traps surfaced before preference Q |
| S-BS-U3 taste / feel | Multi-variant run-spike before lock |
| S-BS-U5 authority “don’t open src/auth” | Disobeyed; behavioral requirements only |

Do **not** delete those behaviors; they are pre-existing.

## RED — S-BS-STRUCT (technique / omission)

**User.** Second auth provider; low module familiarity. Complete step 1 only.

**Observed.** Rich scan with traps in prose; **no** named Knowns inventory;
**no** required Blindspot section title; step-1 user text = "what exists".

**Failure class.** Omits handoff-shaped elements from an already-good step 1.

## GREEN — same, upgraded skill

**Observed (1/1).**
- Scan digest includes **Blindspot**
- `.skills/*-knowns.md` with locks / known unknowns / unknown knowns / assumptions
- STEP1_OUTPUT surfaces blindspot for low familiarity

**Artifacts (run):** `/tmp/bs-struct-green-56143/.skills/github-auth-knowns.md`,
`github-auth-scan.md`, `STEP1_OUTPUT.md`

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Scan MUST include **Blindspot** | RED missing named section; GREEN present |
| Knowns inventory REQUIRED before step 2 | RED missing; GREEN four bullets |
| Assumptions ≠ locks | GREEN inventory separates solution shape from locks |

## Multi-rep (3/3)

Unfamiliar module + step 1 only. **3/3:** Blindspot in scan; knowns file;
locks vs assumptions.

## Neighbor skills

- `clarify-decisions` — blast-radius first already held under "ask color first" authority;
  explicit sentence added for connectivity, not a new RED failure.
- `run-spike` / `research` — remain detours for unknown knowns / known unknowns.
- `interpret-session` — map/territory technique pass (with skill): challenged OAuthProvider
  against `providers.ts`, stance lead, locks vs assumptions.

## Edit — reverse-track before load-subgraph (v1.1.0)

**Roster:** grok-4.6, grok-4.5. Scenario:
`.skills/_pending-reconcile/red-wire-fc-scenario.md`. Pressures: time +
"always just frame-change" + pragmatic.

**RED (v1.0.0), 2/2.** Both models: step 1 REQUIRED SUB-SKILL only
`load-subgraph`; `INVOKED_RECONCILE: no` despite post-pull `ORIG_HEAD≠HEAD`
and missing `.skills/reverse-features/state.json`.

**Failure class:** omits an element / conditional hand-off missing.
Form: observable conditional + REQUIRED SUB-SKILL `reconcile-features`
before `load-subgraph`.

**GREEN (v1.1.0), 2/2.** Both models: `INVOKED_RECONCILE: yes`;
`reconcile-features` before `load-subgraph`; pending OBS/known-impact
surfaced before neighbor cards.

## Edit — query-first catalog context (v1.2.0)

**Roster:** grok-4.6, grok-4.5. Scenario:
`.skills/_pending-reconcile/red-catalog-fc-scenario.md` (120-row flat INDEX).

**RED (v1.1.0), 2/2.** Both: `FULL_INDEX_IN_CONTEXT: yes`,
`CODES_IN_CONTEXT_COUNT: 120` — skill said INDEX is small / read directly.

**Failure class:** output/context has the wrong shape (unbounded ingest).
Form: positive recipe via `catalog-query.md` + replace the “small” sentence.

**GREEN (v1.2.0), 2/2.** Both: `FULL_INDEX_IN_CONTEXT: no`. Caps applied
(`DOMAINS_MAX` 2 / `DIRECT_CARDS_MAX` 4); 4.6 kept 4 cards, 4.5 kept 0
concrete CODEs (fixture path absent) but refused full ingest.
