# `assess-milestone`

> Did the milestone actually deliver what it promised? Judged once, recorded permanently, and never closed on a model's say-so.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/assess-milestone` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/roadmap/INDEX.md`, `docs/specs/INDEX.md`, `docs/product/vision.md`, each member's `requirements.md`, `git`, `templates/roadmap-findings.md`, and any existing assessment |
| **Writes** | `docs/roadmap/assessments/<MILE-N>.md` — and nothing else, ever |
| **Calls** | [`plan-milestones`](plan-milestones.md) with a verified handoff. Names [`sample-attention`](sample-attention.md), [`status-roadmap`](status-roadmap.md) and [`publish-issues`](publish-issues.md) for the user |
| **Called by** | nobody — it is user-invoked. [`status-roadmap`](status-roadmap.md) names it in ladder row 8 |

## The other half of the close

[`status-roadmap`](status-roadmap.md) answers whether a milestone's **structure** is sound: is every item bound, does every status agree, is anything dangling. It deliberately refuses to answer whether the milestone *worked* — that judgment depends on the reader, and a check whose result depends on the reader is not a check.

This skill answers the second question. A milestone can pass every structural test and still have missed: every member shipped, every status green, and the `Outcome:` sentence still not true. Nothing else in the set can see that gap.

## Two halves, drawn deliberately

```
MECHANICAL — reproducible, no judgment      JUDGED — one reading, never terminal alone
scope · bindings · baseline · candidate     outcome · goals · deferrals
structural preconditions                    ↓
↓                                           a human disposes of it
close eligibility (non-overridable)         ↓
                        both must hold → the close may proceed
```

The split is what keeps `ARCH-1` intact. Everything on the left is an exact `grep`/`git` pass — two agents on the same repo resolve identical values. The one judged thing on the right is never terminal by itself, because a human accepts, overrides, or defers it first.

That is also why the milestone's committed baseline is resolved with a pickaxe query rather than from the commitment date: two milestones committed the same day share a date and not a SHA.

## The disposition, and why it is yours

The agent writes an evidence-backed draft verdict. You dispose of it. Both are recorded, separately and permanently.

| Disposition | Terminal | Effective verdict | Close |
|---|---|---|---|
| `Pending` | no | none | withheld |
| `Deferred` | no | none | withheld |
| `Accepted` | yes | the agent's verdict | `Close` → eligible · `Hold` → withheld |
| `Overridden` | yes | your replacement verdict | `Close` → eligible · `Hold` → withheld |

`Deferred` is deliberately not terminal: "not yet" stays reversible, while "yes" and "no but close anyway" do not. Accepting proves adoption, not authorship — an override leaves the agent's reasoning intact beside your replacement, because an overridden judgment is evidence about the judgment, not a mistake to erase.

If you never answer, the assessment stays `Pending` and the close stays shut. Silence is never consent.

## A missed outcome can still close

When every member shipped and the outcome still was not achieved, you can dispose `Close` anyway. Shipping more code cannot fix a wrong premise, and a milestone left open forever makes the roadmap lie by omission. The roadmap then reads closed; the assessment file records what closing it actually meant.

## Append-only, because the history is the point

One file per milestone, `## Assessment <N>` blocks, earlier ones byte-identical forever. A further block is appended only when the **requested closing revision** changes or material evidence does — a disposition arriving late is neither, so it completes the block already written by appending to its dated `History:`.

Commits landing on `HEAD` afterwards do not stale an assessment. Validity is SHA equality, not recency: the assessment is about a revision, not about being the newest thing in the repo.

## What it will not do

- **Write the roadmap.** `docs/roadmap/INDEX.md` belongs to [`plan-milestones`](plan-milestones.md). This skill hands it a verified handoff; that skill re-derives every value from the assessment file and refuses on any mismatch.
- **Run `/sample-attention` or `/status-roadmap`.** Both are user-invoked. It names them.
- **Forecast.** Plan-accuracy counts are recorded as observed facts, with no velocity, capacity, estimate, or projected date derived from them.
- **Hold an action-item list.** Every finding carries exactly one destination: `amend-feature`, `reroute-plan`, `plan-milestones`, `define-domain`, or `/publish-issues`.
- **Run a team retrospective.** What went well, what went badly, who did what — not this skill. It assesses an outcome against a written intent.

## One consequence worth knowing

After this feature, [`plan-milestones`](plan-milestones.md) **cannot close a milestone without an assessment handoff** — in any repository, including one that has never run this skill. That is deliberate. A gate you can skip is not the reason a closed milestone means anything.
