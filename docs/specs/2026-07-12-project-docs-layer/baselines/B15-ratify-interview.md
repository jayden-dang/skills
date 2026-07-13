# B15 — evidence-seeded, ratification-gated interview

Covers: `[PROJDOC-1.8]` `[PROJDOC-1.9]`

**Scenario:** (fixtures described in-scenario, not committed as real repos, per B04's
convention)

- **(a) Brownfield fixture with a completed scan digest.** Same brownfield fixture as
  B14(a) — `src/app.py` beneath a detected `src/` root — Step 1 has already dispatched
  the scan and written a complete `.skills/<slug>-scan.md` digest with all four grouped
  headings populated: **Product-scope facts** ("a CLI that syncs local files to a remote
  bucket" — observation, `README.md:3`), **Glossary terms** ("Bucket: the remote storage
  target" — observation, `src/app.py:12`), **Architecture invariants** ("every write goes
  through `src/sync.py`'s `atomic_write`" — inference, pattern across `src/sync.py`,
  `src/cli.py`), **Engineering guidelines** ("every public function has a docstring" —
  inference, pattern across `src/*.py`). Running `establish-project` create mode Step 2:
  the `grilling` interview must present these four grouped candidates to the user as
  evidence for the vision / glossary / invariant / guideline decisions it draws out.
  `[PROJDOC-1.8]`
- **(b) Same fixture and digest as (a); the user ratifies some candidates and declines
  others.** During Step 2's `grilling` interview the user: ratifies the product-scope
  candidate and one glossary term ("Bucket"), ratifies the architecture-invariant
  candidate, but explicitly declines the engineering-guideline candidate ("no, we don't
  actually enforce docstrings, drop it") and declines a second glossary term the digest
  proposed but the interview never confirms. Steps 3–5 (and the passive `domain-modeling`
  glossary write from Step 2) then run to completion. Assert: the ratified product-scope
  fact appears in `docs/product/vision.md`; the ratified "Bucket" term appears in
  `CONTEXT.md`; the ratified invariant appears in `docs/architecture/` as a fresh
  `**ARCH-N**`; the declined docstring guideline never appears in
  `docs/product/guidelines.md`; the declined/unconfirmed second glossary term never
  appears in `CONTEXT.md`. Only ratified candidates are written; the digest itself stays
  ephemeral (never copied verbatim into any durable file). `[PROJDOC-1.9]`

**Walk (verify):** — executed against the edited `SKILL.md` Create Step 2 and Steps 3–5
sections:

- **(a)** Step 2 now reads: "WHERE a brownfield scan digest exists, present its grouped
  candidates (product-scope facts, glossary terms, architecture invariants, engineering
  guidelines) to the user as evidence for the invariant / vision / glossary / guideline
  decisions this interview makes." The fixture's digest exists and is complete (per B14a),
  so this consult fires: the `grilling` interview is required to surface all four groups
  from the digest as evidence before/while drawing out each decision — matching the
  fixture's four populated headings exactly. Expected = observed. `[PROJDOC-1.8]` **PASS.**
- **(b)** The gate clause appears once per durable-write step, each scoped to that step's
  own artifact: Step 3 — "A scan-derived candidate becomes content in `vision.md` only
  after the user ratifies it in the `grilling` channel; unratified candidates are
  discarded with the ephemeral digest." Step 4 — the same gate scoped to
  `docs/architecture/`. Step 5 — the same gate scoped to `guidelines.md`. Step 2's
  `domain-modeling` side-effect note carries the same gate scoped to `CONTEXT.md`: "a
  scan-derived candidate becomes a `CONTEXT.md` glossary entry only after the user
  ratifies it in the `grilling` channel; unratified candidates are discarded with the
  ephemeral digest." Walking the fixture: the ratified product-scope fact, "Bucket" term,
  and invariant each cleared their gate (ratified in the `grilling` channel) and are
  written to `vision.md`, `CONTEXT.md`, and `docs/architecture/` respectively in Steps
  3/4/2-side-effect. The declined docstring guideline never clears Step 5's gate, so it is
  never written to `guidelines.md`. The declined/unconfirmed second glossary term never
  clears Step 2's gate, so it is never written to `CONTEXT.md`. No step copies the digest
  file itself into any durable location — the digest at `.skills/<slug>-scan.md` remains
  the sole, ephemeral record of the unratified candidates. Expected = observed.
  `[PROJDOC-1.9]` **PASS.**
- **ARCH-2 no-op check (both sub-scenarios' complement):** re-reading Step 2 and Steps
  3–5 with no digest present (the B02/B14(b) greenfield case) — the added Step 2 sentence
  is itself a `WHERE a brownfield scan digest exists` consult, so it does not fire and
  the interview proceeds exactly as before; the added Steps 3–5 / domain-modeling gate
  sentences are each conditioned on "a scan-derived candidate" existing, and with no
  digest there is no such candidate, so the sentences are vacuously satisfied and impose
  no new blocker on the normal (non-brownfield) flow. Every other word in Step 2 and
  Steps 3–5 is byte-identical to before this task. Expected = observed. **PASS.**

**Result:** PASS — both sub-scenarios verified by direct reading of the edited
`skills/project/establish-project/SKILL.md` Create Step 2 and Steps 3–5 sections; both
requirement IDs covered; the ARCH-2 no-digest no-op confirmed by inspection of the same
sections' unconditioned prose.
