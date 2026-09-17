# Go deeper

The menu that ends every live-choice turn, and every turn that answers a pick from it. It is the
user's way to go further without having to phrase the ask — and the loop that sharpens the card
before a carry-back leaves. A message the user wrote themselves, and a carry-back, end without it.

## The menu

Last thing in the turn, labels in the companion language under a fixed `Go deeper` header:

```
**Go deeper**
1 · The card, plainly: what <the fork> decides for <the feature>, and why <the pick>
2 · Explain again: <the idea this turn leaned on hardest>
3 · Walk it: <one concrete case> through <file:line → file:line>, today and under <shape>
4 · Impact: assume <shape> shipped and broke — <the guarantee at stake>, and what it locks
5 · Verify: <the stance's What would flip me, as a check>
───
6 · Write the carry-back
```

Every label names **this turn's** target — the fork, the idea, the file, the guarantee. Line 1
is the whole card from above; lines 2–5 go into one part of it. Line 5 is always the stance's own
**What would flip me**; a platform question that surfaced along the way goes in *Questions this
opens*, not here. Renew the labels from what the latest turn found; a line with nothing real left
to name is dropped (a check already run and settled is not offered again, and line 1 once given
returns only when the stance has moved since). A number belongs to its line: a dropped line leaves
its number unused, so `6` always writes the carry-back.
Measured, a menu rendered after an impact turn copied the previous turn's labels word for word,
and never offered the gap that turn had just found: the on-call runbook had no reason to look in
the new policy table.

## What each pick does

Picks 1–5 end with the menu again, renewed.

**1 · The card, plainly.** The card again from above, for a user who has not yet held all of it —
nothing the card did not already establish, no four blocks re-rendered. Four parts, in this order:

- **What is being decided** — two or three plain sentences: the feature, the question in front of
  it, why it came up now.
- **What it does to the feature** — per shape, one or two lines on what someone using or running
  the feature would notice. Not the code; `What changes` already holds that.
- **The pick** — the stance's shape, named.
- **Why, ranked** — three to five reasons, one or two lines each, each resting on a fact the card
  cites. Rank by how far the pick would move if that reason were false: reason 1 is the stance's
  **Why it wins now**, and a reason whose loss would not move the pick is not a reason. Fewer than
  three real ones → give those and say the pick rests on them alone.

**2 · Explain again.** Re-explain that one idea in two paragraphs: one model mapped part by part
(*the cashier is `drain()`, the line is the 100-row batch*), then the point where the model stops
holding. Then **Questions this opens** — three to five, one or two lines each, spread across the
idea itself, the platform around it, the card or the idea being framed, and which of 3 / 4 / 5
would sharpen the card and why. The user answers any, all, or none. Measured, an unprompted re-explanation ran about 600 words with no model, and all
three of its questions were about the mechanism — none about the card, none pointing at a next
pick. With "short" as the only bound, two more ran 650 and 750 words.

**3 · Walk it.** The state at each step — values, rows, elapsed time — today and under the shape,
with numbers derived from the code rather than restated. Close on one line naming the invariant
the walk shows.

**4 · Impact.** Assume the shape shipped and broke. What failed, traced through `Invariant` and
the history behind it; what the failure does **not** reopen; what the pick locks.

**5 · Verify.** Run the check. Report the stance as held, changed, or unresolved — and when the
check cannot run from here, name the one that would close it and where it runs.

**6 · Write the carry-back.** Picking it is asking for the reply: read `deciding.md` beside this
file and follow it. No shape named with the pick → the stance's pick.
