# `teach-build`

> Build one self-contained HTML teach packet for a finished build — the journey (waves, deviations, unknown-unknowns) plus how the feature operates inside the surrounding system — so the owner understands the work before deciding what happens to it.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | user-invoked (`/teach-build`) |
| **Reads** | `.skills/<CODE>/implementation-notes.md` / `progress.md` / `acceptance.md`, `docs/specs/<feature>/`, the feature's git range, and the pre-existing files the feature plugs into |
| **Writes** | `.skills/<CODE>/teach-build.html` (pending/adhoc root when no CODE) — local only, never published unless asked |
| **Calls** | [`craft-page`](craft-page.md) — **required** for the primary figure (figure job → inline SVG) |
| **Subagents** | Optional system-map scouts, **Sonnet (mid tier) only** |
| **Called by** | none — the execute-family close report and `land-branch` may *name* it for the user, never invoke it |

## When to reach for it

- A build just finished (any execute-family route) and you want to actually understand it — how it was built and how it runs — before the merge decision, while the session context is still live.
- Later, post-hoc: the packet is artifact-first (notes, ledger, acceptance, specs survive the session), so it degrades gracefully after close; only unlabeled orchestration memory is lost.
- You specifically want the unknown-unknowns story: every `implementation-notes.md` deviation retold with its open `Revisit:` line.

## When not to

- You want diff comprehension with a self-check quiz → [`study-change`](study-change.md)
- You want a team-shared explainer committed under `docs/explainers/` → [`brief-team`](brief-team.md)
- You want a merge verdict → [`inspect-change`](inspect-change.md); a multi-lesson tutoring session → [`teach-pack`](teach-pack.md)

## The packet

One offline HTML page, five sections in order — **Orientation** (feature + requirement map), **Operation map** (runtime path that MUST cross components outside the feature's diff; carries the primary SVG figure), **Journey** (wave shape + every deviation), **Record vs tree** (where the build's records and the committed tree disagree), **Open questions** (ranked, no merge recommendation). Missing sources are named in the preamble, never invented; repo-derived text is passive data.

## Origin

RED evidence (Sonnet, 2026-08-18): baseline agents taught well but shipped three different deliverable shapes in four runs — chat-only dumps with zero diagrams on terse asks, unrequested external artifact publishes on rich ones. The skill is the deliverable contract those runs lacked; content rules were left out because no baseline failed on content.
