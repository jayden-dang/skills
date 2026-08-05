# solve-problem — production-harden results (2026-08-05)

**Model:** `grok-4.5`
**Prior pilot:** `results-2026-08-05.md` (`gpt-5.6-sol`, `gpt-5.6-terra`)
**Protocol:** `author-skills` deployment checklist — full description trigger matrix, multi-rep pressure, ship sweeps

## Description routing

Fresh-context agents, description catalog only (no skill body).

### should-fire (expect `solve-problem`)

| ID | Result | Skill chosen |
|---|---|---|
| TF1 | hit | solve-problem |
| TF2 | hit | solve-problem |
| TF3 | hit | solve-problem |
| TF4 | hit | solve-problem |
| TF5 | hit | solve-problem |
| TF6 | hit | solve-problem |
| TF7 | hit | solve-problem |
| TF8 | hit | solve-problem |
| TF9 | hit | solve-problem |
| TF10 | hit | solve-problem |
| TF-H1 (hold-out) | hit | solve-problem |
| TF-H2 (hold-out) | hit | solve-problem |

### should-not-fire (expect neighbor)

| ID | Expected | Result | Chosen |
|---|---|---|---|
| TN1 | root-cause | hit | root-cause |
| TN2 | frame-change | hit | frame-change |
| TN3 | amend-feature | hit | amend-feature |
| TN4 | reroute-plan | hit | reroute-plan |
| TN5 | clarify-decisions | hit | clarify-decisions |
| TN6 | research | hit | research |
| TN7 | run-spike | hit | run-spike |
| TN8 | inspect-change | hit | inspect-change |
| TN9 | specify-behavior | hit | specify-behavior |
| TN10 | root-cause | hit | root-cause |
| TN-H1 (hold-out) | package-change | hit | package-change |
| TN-H2 (hold-out) | prove-claim | hit | prove-claim |

**Aggregate:** 24/24 · undertrigger 0 · overtrigger 0

### Multi-rep sample (3 each)

| Query | r1 | r2 | r3 |
|---|---|---|---|
| TF2 Redis/CEO | solve-problem | solve-problem | solve-problem |
| TF8 ambiguous workflow | solve-problem | solve-problem | solve-problem |
| TN1 NPE suite | root-cause | root-cause | root-cause |

## Pressure GREEN (`grok-4.5`)

| ID | Reps | Choice | Invented target/owner/risk? | Notes |
|---|---|---|---|---|
| S4 | 5 | B all | No | All → `clarify-decisions`; deadline constraint only |
| S1 | 1 | B | No | → `root-cause`; CEO cause under assumptions |
| S2 | 1 | B | No | → `STOP` (no meaningful gap) |
| S3 | 1 | B | No | Delivery vs outcome split; no “solved” claim |

## Meta-test

- Required slots + unresolved handling: **clear**
- Invented number/owner/risk under S4: **no**
- Suggested niceties (end checklist) not treated as documentation gaps requiring text

## Ship sweeps

- Structural: lint-skill-frontmatter, lint-write-handoffs, lint-context7 — OK
- Body: 137 lines; no soft no-op lines; derivation rules single-home
- Pack inventory + skill guide page wired (discovery bucket)

## Verdict

**Production-hardened on `grok-4.5` for description routing and pressure compliance.**
Pilot RED/GREEN/REFACTOR remains the authorizing evidence for skill text on the weaker pilot roster. No description edit was required this pass (hold-outs clean).

### Follow-ups (not blocking this gate)

- Optional: multi-rep S1–S3 beyond single confirmation on `grok-4.5`
- ~~Teach `/ask-me-bro` about ambiguous intake~~ — done (see `tests/ask-me-bro/route-solve-problem-2026-08-05.md`)
- Commit skill + tests + docs when packaging the branch
