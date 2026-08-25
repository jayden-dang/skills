# `draft-ux`

> Requirements do not imply an interaction. Two runs on the same Approved requirements built opposite flows, each certain the requirements forced it — so the shape of the interaction is a decision, and this skill makes it the user's, felt in the browser before it is spec'd.

|  |  |
|---|---|
| **Bucket** | craft |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the feature's requirements; the locked `ui-brief.md` when one exists; the repo's existing components |
| **Writes** | 2–3 runnable takes + switcher (deleted at the lock); a `## Interaction` section inside `ui-brief.md` |
| **Calls** | — (borrows `draft-ui` §2's switcher mechanics; no hand-off) |
| **Called by** | — reached on what the user says |

## When it fires

"What happens when you hit Send?", "undo or a confirm dialog?", "what does a slow call feel like?", "make it clickable so I can feel it" — the behavior question, once the look is settled or irrelevant. `draft-ui` decides what a surface *looks* like; this decides what it *does*.

## The workflow

1. **List the moments** — one line per action whose outcome is not implied, each carrying its branches: instant, in-flight, success, failure, way back. Written where the user can read it.
2. **Diverge on when the world changes** — 2–3 named takes of the same flow: commit-on-click with a way back, hold-until-confirmed with a busy state, ask-first. Same markup, same components, same look. Latency is simulated with a named constant; the failure branch gets a hook you can flip.
3. **Every number is a decision** — each delay and window carries a reason and an answer for the call that outruns it. A constant justified by the prototype itself is a prototype artifact about to be spec'd.
4. **Show, recommend, wait for the go** — hand over the URL plus what each take *costs the user*, and a recommendation. An instruction to decide is an instruction to recommend, never authority to lock; an absent user is the case that rule exists for, not an exception to it.
5. **Lock** — after the go, `## Interaction` goes into this feature's `ui-brief.md`, one `###` per moment in the same five slots the visual sections use, plus Decision, Grounding, Timings, Amendments. Not a sibling file, not a commit message, not a pointer bolted onto an Approved `requirements.md`.
6. **Delete the prototype** — losing takes *and* the winner, switcher, simulated delays, failure hooks; production files restored. A bug found while prototyping is reported, not fixed there.

## Downstream

[`design-solution`](design-solution.md) Step 2b lifts `## Interaction`'s per-moment slots alongside the visual ones; Decision, Timings, and Amendments stay in the brief, which the design cites. The build rewrites the flow from the brief under [`test-first`](test-first.md).
