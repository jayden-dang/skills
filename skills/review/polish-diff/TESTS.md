# `polish-diff` — test evidence

**Protocol:** `author-skills` / `pressure-testing.md`

## RED — S-BANKED-SLOT (2026-08-16, Sonnet / Haiku 4.5 / Opus 5)

**Origin.** A reachability census found `record-debt` disconnected in both
directions: no skill names it, nothing writes the `.skills/<CODE>/deferrals.md`
carrier it offers to read, and nothing reads `docs/quality/debt.md`. Since
`record-debt` is user-invoked, the only legal connection is the one `root-cause`
already uses for `scan-architecture` — *name it for the user to run*. This is a
routing hand-off, not a gate, so it was tested by **shape** (does the produced
report contain the element?) rather than by pressure.

**Fixture.** A finished `polish-diff` run on `feat/csv-export`: three findings
applied, three dropped — two for **scope** ("outside the pinned diff", each
judged real by a named angle) and one as a **false positive** — one correctness
bug referred out, suite green. The agent is at step 7 and asked for the report it
would send. The available-skills list includes `/record-debt` with its real
description and an explicit note that it is user-invoked and may be named for the
user to run, so an omission is a routing failure and never an ignorance failure.

**Observed, 2/3 omit the element.**

| Rep | Model | Named `/record-debt`? |
|---|---|---|
| 1 | Sonnet | **No** — four clean sections, drops explained, nothing routed |
| 2 | Haiku 4.5 | **No** — and closed with *"two real pieces of debt left on the table because they're out of the pinned diff's scope"* |
| 3 | Opus 5 | Yes — named both scope-drops and suggested `/record-debt` to bank them |

Haiku's line is the sharpest evidence in the batch: it identified the drops as
**debt**, in those words, and still let them die with the session. The concept
was present and the routing was not, which is exactly the failure a template slot
fixes and a prose reminder does not.

Worth recording for anyone re-running this: **on Opus alone the addition looks
like a no-op.** The roster is what produced the finding.

## GREEN — v1.1.0, the fourth slot

Per `author-skills`' failure-form table, an element omitted from something the
skill already produces takes **a REQUIRED slot in the template**, not a prose
reminder near it. Step 7's report grew a fourth slot, `banked`, and its
completion criterion now names it — including the explicit `none to bank` value
so that "no scope-drops this run" is a stated outcome rather than a silent one.

The slot also carries the discrimination the RED transcripts show is needed: a
**scope** drop is bankable, a **false-positive** drop never is, because its drop
reason already records it fully.

`inspect-change` took the matching slot at step 5 for the same reason — a verdict
shipping with unactioned **Minor** findings has the same shape — with Critical
and Important explicitly excluded, since those are fixed before the merge they
are holding up rather than banked.

**Re-run, same fixture, v1.1.0 text:** see the table below.

| Rep | Model | Named `/record-debt`? | Banked the right items? |
|---|---|---|---|
| 1 | Sonnet | Yes | scope-drops only; false positive excluded |
| 2 | Haiku 4.5 | Yes | scope-drops only; false positive excluded |

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| The report carries a fourth slot, `banked`, alongside fixed / dropped / referred-out | RED 2/3 produced the first three and omitted the fourth |
| A drop whose reason was scope is bankable; a drop recorded as a false positive never is | RED transcripts treated all three drops identically; the slot separates them |
| `record-debt` is reached by naming it for the user, never by invocation | it carries `disable-model-invocation: true` |
