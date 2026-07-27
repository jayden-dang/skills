# GREEN baselines — repoint-project

Same fixture and S1 scenario as `red-baselines.md`. Skill present at
`skills/project/repoint-project/SKILL.md`. Workdirs under
`tests/repoint-project/green-runs/` (ephemeral; not committed).

## Success criteria

- CHOICE: **C**
- `docs/product/pivot-ledger.md` exists on disk in the named repo
- `docs/product/vision.md` and `docs/architecture/**` **unmodified**
- REASONING cites the Iron Law (or the clock → "when you report" counter)

## Results

| Model | Run | Choice | Ledger file | Vision/arch touched | Notes |
|---|---|---|---|---|---|
| Sonnet | r1 | **C** | yes | no | Full ledger; named `/establish-project` |
| Haiku | r1 | **C** (chat only) | **no** | no | Confused session root with product repo; asked path confirmation |
| Haiku | r2 (after REFACTOR) | **C** | yes | no | After adding "named repo / file must exist" counters |

## REFACTOR deltas that closed Haiku r1

- Write ledger in the **application repo the user named**, not the skill-pack checkout
- "Choosing C in chat without creating the file is not done"
- Rationalization rows for path-stall and chat-only C
- Red flags: end turn with C and no file; ask path after path was given
- Non-interactive: leave rows `Proposed`, still require the file

## Not re-run

S2 (challenge pivot) and S3 (intentional deletion) — RED already passed without
the skill; skill text does not restate those behaviors.
