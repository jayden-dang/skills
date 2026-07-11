# `amend`

> The iteration lane for an already-shipped, spec'd feature. A fast lane, not a gate bypass — every path still exits through `tdd`, and anything with real design questions escalates to `brainstorm`.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `docs/specs/INDEX.md` (to find the feature's spec), the feature's `requirements.md` / `design.md` sections the change touches |
| **Writes** | nothing directly — it produces a tier decision and routes; edits land in the lane it hands to |
| **Calls** | [`tdd`](tdd.md) (tier 0 and every exit), [`write-requirements`](write-requirements.md) (tier 1 mini-spec), [`brainstorm`](brainstorm.md) (new scope), [`sync-spec`](sync-spec.md) (if the triad was touched) |
| **Called by** | the user asking for a small in-scope change to a shipped feature |

## When it fires

When an already-shipped, spec'd feature needs a small in-scope change — a recolor, a copy edit, a tweak, a follow-up add-on to existing behavior — and running the full greenfield cycle through [`brainstorm`](brainstorm.md) would be overkill.

It sits between its neighbors, and the boundaries are sharp:

- Brand-new capability, no spec yet — [`brainstorm`](brainstorm.md), not amend.
- Behavior that is broken — [`debug`](debug.md), not amend.
- A spec that has drifted from the code — [`sync-spec`](sync-spec.md), not amend.

The feature must already have an approved spec and working code. "Small" is a claim you **verify against the existing spec**, not a feeling.

The skill has a shape: ground the change in the spec, classify it out loud into one of three cases, route it to the lightest lane that still keeps the spec and the tests true, and keep the trace honest on the way out. The classification is the load-bearing step — everything after it follows from which case you named.

## 1. Ground the change in the existing spec

Find the feature's spec — `docs/specs/<date>-<feature>/{requirements,design,tasks}.md` via [`docs/specs/INDEX.md`](../concepts/artifacts.md) — and read the requirements the change touches plus the design section that owns them.

If the feature has **no** spec at all, amend is the wrong skill: a brand-new capability is [`brainstorm`](brainstorm.md), a break is [`debug`](debug.md).

**Done when** you can name the requirement IDs the change affects.

## 2. Classify the change — out loud

State which of three cases this is and why, the same way [`brainstorm`](brainstorm.md) names a tier:

| Case | What it means | Where it routes |
|---|---|---|
| **Tier 0 — no behavior change** | A recolor, an icon, a label, a copy edit; every existing acceptance criterion still reads true unchanged | [`tdd`](tdd.md) — assert the visual/behavioral change at its seam. No spec edit beyond fixing a criterion whose wording is now stale |
| **Tier 1 — changes or extends existing spec'd behavior, ≤ ~half a day** | The change modifies what an existing requirement already promises, or adds a small follow-on to it | Mini-spec: amend or add the requirement plus a `... SHALL CONTINUE TO ...` guard, via [`write-requirements`](write-requirements.md), then [`tdd`](tdd.md) |
| **Genuinely new scope** | New behavior the spec never covered, a real UX or design decision with live alternatives, more than ~half a day, or it spans subsystems | STOP amending. Escalate to [`brainstorm`](brainstorm.md) — this earns the full cycle |

The honest test for the escalation:

> Does the existing spec's intent already cover this behavior? If you are inventing what it should do, it is new scope.

Hand new scope up; do not shape big new work inside this skill.

The tell for each case is concrete. Tier 0 is where *every existing acceptance criterion still reads true unchanged* — you are altering how something looks or reads, not what it does. Tier 1 is where you are modifying what a requirement already promises, or bolting a small follow-on onto it, and a mini-spec plus a `SHALL CONTINUE TO` guard is enough to pin down the change and protect what must keep working. New scope is anything that introduces behavior the spec never described, opens a real design decision with live alternatives, runs past roughly half a day, or crosses subsystem boundaries. When two of those signals fire, treat it as new scope.

**Done when** the tier is stated out loud and the case is chosen.

## 3. Keep the trace honest

After the change lands through [`tdd`](tdd.md), its new or changed requirement carries its ID into the test tag and the commit trailer like any other. If the edit touched the triad, run [`sync-spec`](sync-spec.md) to realign `Status:` and the trace. [`check-trace`](../resources/scripts.md#check-trace) stays clean, or the change is not done.

Concretely, before the amend is done:

- The changed behavior has a test you watched fail first, written at an agreed seam through [`tdd`](tdd.md).
- The new or changed requirement's ID is in the test tag and in the commit trailer.
- Any tier-1 requirement carries its `SHALL CONTINUE TO` guard, and the guard has a test.
- If the triad moved, [`sync-spec`](sync-spec.md) has realigned `Status:` and `INDEX.md`.
- [`check-trace`](../resources/scripts.md#check-trace) is clean.

**Done when** the change is implemented test-first, its requirement ID traces end to end, and `check-trace` is clean.

## Red flags — you are in the wrong lane

Any of these means stop and re-route before writing code:

- You are inventing behavior the spec never described — that is [`brainstorm`](brainstorm.md), not amend.
- The "small" change grew a design decision with real alternatives — escalate; do not decide it by feel here.
- You are about to change code without touching a test — that is [`tdd`](tdd.md), always.
- The feature was never spec'd, or it is simply broken — [`brainstorm`](brainstorm.md) (new) or [`debug`](debug.md) (broken), not amend.
- You are splitting one request into a trivial part and a new-behavior part — route each half separately: the tweak stays here, the new behavior goes to [`brainstorm`](brainstorm.md).

## Worked example

A shipped feature whose code is `SHELL` renders the active module's name in the header. The user asks: "make the header label bold, and while you're at it let it also show the module's unread count."

**Ground it.** [`docs/specs/INDEX.md`](../concepts/artifacts.md) points to `docs/specs/2026-05-02-shell/`. The header is governed by `SHELL-3.1` ("the shell SHALL display the active module's name in the header"), and reading the triad confirms there is no requirement about unread counts anywhere in it. So one half of the request lands on an existing requirement and the other half lands on empty spec.

**Classify — out loud.** This request splits cleanly into two cases:

- Bolding the label is **Tier 0**: no acceptance criterion changes, the name is still displayed, only its weight differs. It routes to [`tdd`](tdd.md) — one test asserting the header renders the label with the bold style at the header seam.
- Showing an unread count is **genuinely new scope**: the spec's intent never covered surfacing per-module counts, and it raises live questions (counts from where? zero-state? overflow past 99?). Applying the honest test — the existing spec does not describe this behavior, so you would be inventing what it should do. It escalates to [`brainstorm`](brainstorm.md).

The two halves route separately: the bold tweak stays in this lane, the count feature is handed up.

**Land the tweak.** [`tdd`](tdd.md) drives the bold change test-first. The Tier-0 label edit does not touch the triad, so no `write-requirements` and no `sync-spec` are needed here — but if the `SHELL-3.1` criterion's wording had implied a specific style, you would fix that stale wording. The commit carries the guard trailer:

```
style(shell): render the active-module header label in bold

Guards: SHELL-3.1
```

[`check-trace`](../resources/scripts.md#check-trace) stays clean, and the tweak is done — while the unread-count half is off in [`brainstorm`](brainstorm.md) earning its own requirements.

## Why it is written the way it is

`amend` exists because the greenfield cycle is the right amount of ceremony for new behavior and the wrong amount for a copy edit — and an agent under pressure will happily route a genuinely-new feature through a "quick tweak" to skip the gate. So the skill makes the classification the load-bearing act: it must be stated out loud, tested against the spec's actual intent, and it has exactly one escape hatch (new scope → [`brainstorm`](brainstorm.md)) that cannot be argued around by calling the work small. Every legitimate case still exits through [`tdd`](tdd.md), so "fast lane" never means "no test". That is why the red-flags list is framed as *you are in the wrong lane*: the failure this skill guards against is not doing the work badly, it is doing it in a lane that skips a gate the work actually needed.

## See also

- [`brainstorm`](brainstorm.md) — where genuinely new scope escalates to
- [`tdd`](tdd.md) — the gate every amend path exits through
- [`sync-spec`](sync-spec.md) — realigns the triad when an amend touched it
- [Ceremony tiers](../methodology/ceremony-tiers.md) — the tier vocabulary this skill classifies into
- [`debug`](debug.md) — where a broken (not small) change belongs instead
