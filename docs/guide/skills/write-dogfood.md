# `write-dogfood`

> Dogfood a finished feature: a person drives the real app through every
> user-facing ability and judges what they see. The deliverable is a **run
> file**, a **rendered HTML guide** from a checked-in shell, and an
> **independent review** of that guide by a reviewer with a clean context — not
> a chat message and not a bespoke CSS page every time.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the spec triad — `requirements.md`, `design.md`, `tasks.md`; the source (theme tokens, CSS, keyword and label definitions); `docs/agents/project.md` (the `## Run locally (dev)` command) |
| **Writes** | `.skills/<CODE>/dogfood.json` (cases + verdicts), `.skills/<CODE>/dogfood.html` (rendered guide), `.skills/<CODE>/review-brief.md`, and — through the reviewer — `.skills/<CODE>/dogfood-review.md` |
| **Calls** | the `dogfood` CLI (`scripts/dogfood render`); a fresh read-only **reviewer subagent** right after the run file exists; [`craft-page`](craft-page.md) **only** when the user asks for custom craft |
| **Called by** | [`validate-feature`](validate-feature.md), [`prove-claim`](prove-claim.md); hands off to [`run-dogfood`](run-dogfood.md) only after a clean review |

## When it fires

When a finished feature needs a hands-on pass from the user's seat, case by
case, over every user-facing ability — including the visuals, feel, and edge
cases a human must eyeball. Also when an existing guide needs re-reviewing for
missing situations.

It complements [`validate-ui`](validate-ui.md), which automates flows into
tests. To **execute** a written guide in the browser (with backend probes and a
fix loop), use [`run-dogfood`](run-dogfood.md).

## 1–4. Scope, ground, boot, write

- **Coverage gate:** every user-facing ID has ≥1 case; every ability area has a
  `happy` **and** a non-happy kind (or a greppable *Coverage exception*);
  Out-of-Scope gets `nonbehavior` when a user can attempt it; persistence
  claims get `persist`. Kinds: `happy` | `edge` | `error` | `nonbehavior` |
  `persist` | `visual` | `journey`.
- **Ground** each Expect in the real source (labels, theme tokens). **Boot** via
  `## Run locally (dev)`; behaviors with no UI get an honest observation point.
- **Write** the run file — eight slots per case: `id`, `req`, `kind`, `title`,
  `setup`, `try`, `expect`, `backend` — and render it:

```bash
python3 <write-dogfood-skill-root>/scripts/dogfood render .skills/<CODE>/dogfood.json \
  -o .skills/<CODE>/dogfood.html
```

Schema: `references/cases-schema.md` beside the skill.

## 5. Independent review, then hand over

The author cannot see what their own cases miss. Right after the run file and
HTML exist, the skill fills `references/review-brief.md` (paths only) and
dispatches a **fresh, read-only subagent**. The reviewer reads
`references/review.md` — the author never loads it — opens the product code,
maps every user-observable path and state against the cases, and writes
`dogfood-review.md` with code-grounded missing-situation findings (`VFG-N`).

- **Clean report** → name `run-dogfood` to drive the cases.
- **Open findings** → patch the run file, re-render, dispatch a **new**
  reviewer; at most 2 re-review cycles, then stop for the human
  (`references/review-fix-loop.md`).
- **No subagents** → the author states `AUTHORING CLOSED` and runs the review
  recipe inline.

Offer `dogfood serve` when the person will also test by hand; their ticks are
recorded, never a `pass`.

## Why it is written this way

The review used to be its own skill, always called right
after authoring. Loading a second 195-line skill into the author's context cost
tokens on every run and put the reviewer's doctrine where the author could lean
on it. Now only the reviewer subagent reads its recipe, and the author's
context carries a one-page brief.

## See also

- [`run-dogfood`](run-dogfood.md) — drive the cases with the ledger CLI; gated on a fresh clean review
- [`validate-ui`](validate-ui.md) — automated sibling
- [`validate-feature`](validate-feature.md) — orchestrator
- [`prove-claim`](prove-claim.md) — names a dogfood pass for "the feature works"
