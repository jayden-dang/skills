# `explain-change`

> Team-shared post-implementation brief. One pitch-and-map HTML packet under
> `docs/explainers/` so people who did not author the change can understand it
> without reading specs as human prose.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | user-invoked (`/explain-change`) |
| **Reads** | git range (required); optional specs, implementation-notes, grilling locks |
| **Writes** | `docs/explainers/<slug>.html` (overwrite) + `docs/explainers/INDEX.md` upsert |
| **Calls** | — |
| **Called by** | named (never invoked) from `finish-branch` when multi-task / risk-glob hit / architecture-affecting |

## When to run it

After a **large** or **architecture-affecting** change, before or during PR review,
when the team needs a shared mental model. Not every PR. Not a merge gate.

For **author** self-check with a quiz, use [`comprehend-change`](comprehend-change.md)
instead (outside the repo).

## What you get

A single offline HTML file with:

1. What changed for users  
2. Decisions and locks  
3. What can break  
4. How to verify in ~5 minutes  
5. System intuition (+ figure when complex)  
6. Seams and files touched  

Plus a derived-from header (range, generated time, REQ IDs when known).

Re-runs **overwrite** the canonical slug; git keeps history. `INDEX.md` lists current explainers.

## What it is not

- Not a quiz or pass/fail gate  
- Not a reason to withhold merge/PR  
- Not a full dump of the requirements triad  
- Not a replacement for `CONTEXT.md` or specs (those remain agent maps)

## See also

- [`comprehend-change`](comprehend-change.md) — author self-check + quiz  
- [`finish-branch`](finish-branch.md) — may name this skill optionally  
- [`grilling`](grilling.md) — pre-impl close package feeds decisions when present  
