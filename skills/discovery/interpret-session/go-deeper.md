# Go deeper

The menu that ends every live-choice turn, and every turn that answers a pick
from it. Two engineering hops, then carry-back. A message the user wrote
themselves ends without it, even one asking for what a hop would have offered;
so does a carry-back.

**Contents:** [The menu](#the-menu) · [Hop 1](#hop-1--deeper) · [Hop 2](#hop-2--lowest) ·
[After a hop](#after-a-hop)

## The menu

Last thing in the turn, under a fixed `Go deeper` header, labels in the companion
language:

```
**Go deeper**
1 · Deeper — <this turn's technical overview>
2 · Lowest — <this turn's file:line walk>
───
0 · Write the carry-back
```

Always these two hops, in this order. Each label names **this turn's** target —
the graph, the file, the guarantee — not a generic "technical overview". A number
answers the menu, never the paste: a bare `1` is hop 1 even when the paste has an
Option 1. `0` always writes the carry-back. A number with no matching line is not
the carry-back.

Number this menu from this file, not from a previous turn or another agent's
session. A five-line menu that ends `5 · Write the carry-back` with labels
*Explain again* / *Walk it* / *Impact* is the retired form — measured, a resumed
session copied it. A menu of Walk / Challenge / Stress / Verify is the v2.16 form;
this file replaced it.

Do not offer "the card, plainly" or Explain — turn 1 already spent those.

## Hop 1 — Deeper

The whole system, still in sentences. Render from `grounding.md`: **Today** (what
the code does, every paste-vs-repo miss with `file:line`) and the Architect
comparison on Depth / Locality / Invariant, in ordinary sentences, not as the
turn-1 table. A **middle diagram** of the same neighborhood, one grain finer than
turn 1 — still the system, not the options. Read `diagrams.md`.

Two to four **pressure-test** questions may close this hop — weakest assumption,
irreversible cost, likely future requirement, failure mode. Not a menu of
directions.

Do not re-render turn 1. Do not write a carry-back.

## Hop 2 — Lowest

One concrete case through `file:line → file:line`, today and under the pick, with
numbers derived from the code. Close on the **Invariant**. Show the **code that
carries the change** (the What-changes fragments). A **low diagram** if hop 1's
picture cannot carry the walk. Run the stance's **What would flip me** if a check
is in reach; otherwise name the smallest probe, where it runs, and the result
that flips the pick.

Do not re-render turn 1 or hop 1. Do not write a carry-back.

## After a hop

End with the menu again. If hop 1 was taken, hop 1 may drop (number unused) and
hop 2 stays `2`. If hop 2 was taken, both hops may drop; `0` remains. Labels
copied from the previous menu are a failure.

**0 · Write the carry-back.** Read `deciding.md`. No shape named with the pick →
the stance's pick.
