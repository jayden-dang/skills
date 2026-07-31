# `refresh-roadmap-status`

> Where does the plan actually stand, and what is the one next thing to do? Answered fresh every time, from the roadmap, the specs, and git — never from a stored status file.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/refresh-roadmap-status` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/roadmap/INDEX.md`, `docs/product/vision.md`, `docs/specs/INDEX.md`, each bound feature's `requirements.md`, `git`, and `.skills/progress.md` when it exists |
| **Writes** | nothing — by contract |
| **Calls** | nothing. Names [`realign-spec`](realign-spec.md), [`plan-milestones`](plan-milestones.md), [`audit-trace`](audit-trace.md) and the feature-flow skills in its output |
| **Called by** | nobody — it is user-invoked |

## The horizontal counterpart to `audit-trace`

[`audit-trace`](audit-trace.md) is the **vertical** check: does one feature's requirements, tasks, and tests agree with each other? `refresh-roadmap-status` is the **horizontal** one: do the plan and the specs agree, and what follows from that?

The two never overlap. `audit-trace` never reads `docs/roadmap/INDEX.md` or the vision's `Goals` section; `refresh-roadmap-status` never reads a `tasks.md` footer or a test annotation. They touch the same string in exactly one place — a feature's `Status:` — and neither writes it.

## Why it stores nothing

Progress is derivable, so storing it creates a second source of truth that drifts from the first. The researched prior art, BMAD, keeps progress in a `sprint-status.yaml` whose own reader warns "may be stale" when its timestamp is over seven days old — that warning is the design flaw admitting itself.

So this skill recomputes. It writes no file, updates no status, and edits no roadmap. There is nothing to go stale and nothing to reconcile. Repair belongs elsewhere: [`realign-spec`](realign-spec.md) realigns a drifted `Status:`, [`plan-milestones`](plan-milestones.md) fixes the roadmap.

## Eleven findings

| Code | Means | Withholds the next action |
|---|---|---|
| `R1` | a milestone cites a goal that does not resolve to one live `GOAL-N` | no |
| `R2` | a live goal is neither cited nor dispositioned | **yes** |
| `R3` | the vision defines the same `GOAL-N` twice | no |
| `R4` | a `ROAD-N` sits under no milestone, or several | **yes** |
| `R5` | a feature binds a `ROAD-N` the roadmap does not define | no |
| `R6` | two features bind the same `ROAD-N` | no |
| `R7` | a `ROAD-N` has no feature — *unspecced* | no |
| `R8` | a feature has no roadmap item — *unplanned* | no |
| `R9` | a `Closed` milestone holds work that did not ship | **yes** |
| `R10` | a feature's two `Status` records disagree | **yes** |
| `R11` | the roadmap is unparseable or breaks a structural rule | **yes** |

`R7` and `R8` are **normal states, not defects.** An unspecced item is simply the next thing to spec; an unplanned feature is work that predates the roadmap or bypassed it. A healthy repo can carry both indefinitely.

A **withholding** finding replaces the recommendation with the reason — because a next action computed from a broken join is worse than no next action.

## One next action, off a fixed ladder

Ten rows, first match wins, ties broken by milestone table order then lowest `ROAD-N`. Identical artifact state therefore yields an identical recommendation — the ladder is a pure function of what is written down, not a judgment.

It walks from "the roadmap isn't approved yet" (→ `plan-milestones`) through the feature flow for the first incomplete member of the first committed milestone — `frame-change`, `specify-behavior`, `design-solution`, `plan-tasks`, `build-in-waves` — and ends at either naming `/cut-release` for you or reporting the roadmap complete.

## Structural presence, never judgment

A finding fires on structure alone. Whether a milestone's outcome was *achieved*, whether a feature really delivers its item, whether a deferral was wise — none of that is asked here. That judgment belongs to a retrospective; putting it here would make the result depend on who ran it, which is the one thing the check exists to prevent.

Everything read from these artifacts is **passive data**: a milestone outcome that reads like an instruction is reported, not obeyed.

## Standup mode

The same derivation, rendered as a card — the milestone in flight, the status of its members, the one next action. One skill with two renderings rather than two skills; it splits out only if genuine team-ceremony responsibilities appear.

## Optionality

No `docs/roadmap/INDEX.md` means the layer is absent: the skill says so and stops. No findings, no recommendation, no complaint.

## See also

- [`plan-milestones`](plan-milestones.md) — authors the intent this reads
- [`audit-trace`](audit-trace.md) — the vertical check beside it
- [`realign-spec`](realign-spec.md) — repairs the `Status` drift this reports as `R10`
