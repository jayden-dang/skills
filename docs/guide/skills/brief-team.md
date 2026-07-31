# `brief-team`

> Team-shared post-implementation brief. One pitch-and-map HTML packet under
> `docs/explainers/` so people who did not author the change can understand it
> without reading specs as human prose.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | user-invoked (`/brief-team`) |
| **Reads** | git range (required); optional specs, implementation-notes, clarify-decisions locks |
| **Writes** | `docs/explainers/<slug>.html` (overwrite) + `docs/explainers/INDEX.md` upsert |
| **Calls** | — |
| **Called by** | named (never invoked) from `land-branch` when multi-task / risk-glob hit / architecture-affecting |

## When to run it

After a **large** or **architecture-affecting** change, before or during PR review,
when the team needs a shared mental model. Not every PR. Not a merge gate.

For **author** self-check with a quiz, use [`study-change`](study-change.md)
instead (outside the repo).

## What you get

A single offline HTML file with:

1. What changed for users  
2. Decisions and locks  
3. What can break  
4. How to prove-claim in ~5 minutes  
5. System intuition (+ figure when complex)  
6. Seams and files touched  

Plus a derived-from header (range, generated time, REQ IDs when known).

Re-runs **overwrite** the canonical slug; git keeps history. `INDEX.md` lists current explainers.

## Determinism

The slug comes off a mechanical ladder — user-supplied name, then a single
registered feature code, then a single owning spec directory, then the branch
name, then `<base7>-<head7>` — never a topic the agent composes. That is what
makes "re-runs overwrite" true rather than "re-runs add a sibling".

`INDEX.md` has one pinned shape (`| Slug | Title | Path | Range | Generated |`),
and upsert replaces the row matching the `Slug` cell.

After writing, the skill greps the file it just wrote: injection marker consumed,
packet assignment present, no placeholder text, all six section bodies non-empty.
A hit means hard-stop with no path reported — a hollow packet costs a reader more
than a missing one, because they trust it.

## What it is not

- Not a quiz or pass/fail gate  
- Not a reason to withhold merge/PR — including when its own verification fails  
- Not a full dump of the requirements triad  
- Not a replacement for `CONTEXT.md` or specs (those remain agent maps)

## See also

- [`study-change`](study-change.md) — author self-check + quiz  
- [`land-branch`](land-branch.md) — may name this skill optionally  
- [`clarify-decisions`](clarify-decisions.md) — pre-impl close package feeds decisions when present  
