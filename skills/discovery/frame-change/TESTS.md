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

## Quality pass (v1.2.1) — author-skills wording sweep

Description gains outcome noun; reverse-track BEFORE catalog-query; predicate
uses checkpoint/`HEAD` (not sticky ORIG_HEAD); catalog-query pointed not
restated. No new behavior beyond recorded sequencing intent.

## Edit — reverse-track names map-features (v1.3.0)

**Roster:** control-current-skills (RED vs desired), then v1.3.0 text.

**Desired failure of v1.2.x:** auto-invokes `reconcile-features` on reverse
predicate (R1/R2 in map-features TESTS.md v2 RED).

**GREEN (v1.3.0):** WHEN predicate holds → **name** `/map-features` only; never
invoke reconcile-features (removed) or auto-invoke map-features; load-subgraph
still runs for overlap.

## Edit — todo gate is portable (v1.5.0)

**Roster:** Sonnet only. Harness under test: a Claude Code build with **no `TodoWrite`** —
verified absent from the direct tool list, absent from the deferred list, and a `ToolSearch`
for "todo list task checklist write" returns CronList / TaskOutput / TaskStop / browser
tools and no todo tool.

**The false fact.** v1.4.0 line 44 read: "create the todo list … via your harness's todo
tool (**`TodoWrite` in Claude Code**; the equivalent in Kimi, Codex, or wherever this runs).
… **Do not proceed until the list exists**." The parenthetical asserts a fact this build
falsifies, so the gate's closing condition was unsatisfiable — the skill's first hard gate
could not fire, and no skill in the set defined a fallback.

**Fixture.** OrderFlow repo plus `docs/specs/INDEX.md` + `catalog/orders.md` (ORD-100,
ORD-120) so the catalog query resolves, and the full skills tree under `skillref/`. Ask:
"add order status change notifications — when an order moves to `shipped` or `cancelled`,
the customer gets told."

**RED — v1.4.0, 5 observations, 2 shapes, gate lost in 3:**

| Rep | Behavior |
|---|---|
| fc-solo | **No list, no mention.** Opens "Step 1 (project context) is done." |
| fc-1 | **No list, no mention.** Opens "Step 1 done." |
| fc-3 | **No list, no mention.** Opens "Step 1 findings before moving to the interview." |
| fc-4 | Visible inline checklist — "six steps, todo-tracked (no TodoWrite tool in this environment, so I'm tracking it inline)" |
| field report | Visible inline checklist, same explicit note; and the tier read came *before* step 1, where this skill puts the provisional call after step 1 |

Per `pressure-testing.md`, variance this wide means the form is not binding. The majority
outcome is the gate evaporating, taking with it the mechanism that keeps the six steps
ordered and forces each **Done when** check.

**GREEN — v1.5.0.** Form: a conditional keyed to an observable predicate (does the harness
expose a todo tool), not an unconditional rule plus an exemption. Both branches close on one
observable — *the list exists and the user can see it* — so the gate is satisfiable in every
harness. The tool-name assertion is deleted: naming one harness's tool is the kind of fact
that rots, and it did. Red flag added: "narrating step 1 before the six-step list is
visible."

**Same false fact fixed in the same pass:** `write-flow-guide` §Todos (v2.1.0) and
`execute-common` §Todos (v2.3.0), neither of which carried even a portability clause.
`TodoWrite` no longer appears anywhere in `skills/`, `docs/`, or `templates/`.

**GREEN result — v1.5.0, 2 reps: PARTIAL, and converged.** Both produce the six-step list,
visible, with per-item status markers (`1. ✅ Explore project context` / `2. ⏳ Interview` /
`3. ⬜ …`). The total loss seen in 3 of 5 RED reps is gone. Both emit it *after* step 1's
findings rather than first, tripping this edit's own new red flag. So the fallback branch
binds; its **placement** does not. Two reps, one shape — the form is binding, just to the
wrong position.

(A third rep was discarded as contaminated: it spanned the moment the fixture's skill copy
was swapped to v1.5.1, so it cannot be attributed to either version.)

### Rejected REFACTOR — v1.5.1 placement wording (do not retry as written)

Hypothesis: name the position and placement follows. The fallback branch was rewritten to
"the six-step checklist **is the first block of your first reply**, above any findings", with
the gate's closing observable changed to "the list is visible before the first step's output
is" plus a sentence explaining that a late checklist is a summary, not a plan.

**Result — 2 reps: worse than v1.5.0.** Rep 1 produced **no list at all** — the RED failure
mode returning. Rep 2 produced a late list, as before. Two reps, two shapes: where v1.5.0
converged, v1.5.1 diverged, so by `pressure-testing.md`'s variance rule the rewrite is
strictly the weaker text. Reverted; `main` keeps v1.5.0.

**Likely mechanism, unconfirmed (n=2).** The edit replaced an imperative with a copula —
"**write** the six steps as a checklist" became "the six-step checklist **is** the first
block". Chasing the placement detail deleted the verb that made the line an instruction,
which is the "positive recipe" rule in `author-skills` inverted. A future attempt should keep
the imperative *and* add the position, not trade one for the other.

**Placement stays open, and not because nobody has tried.** These reps run headless
(`claude -p`), where the agent composes one reply per turn — a good probe of whether the list
exists, a poor one for "first action". Two wording attempts have not moved it against this
measurement. The next attempt should be an interactive-session rep, not a third rewrite
scored the same weak way.

**What the original bug hid.** In a harness *with* a todo tool the tool call is inherently
first, so position was enforced by the harness, never by this text. Removing the tool exposed
that the skill had been leaning on the harness for half the rule.

**Change class:** portability fix to an existing gate. Checklist steps, tier rules, HARD-GATE,
and terminal states untouched.
