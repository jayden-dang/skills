# Go deeper

The menu that ends every live-choice turn, and every turn that answers a pick from it. It is the
user's way to go further without having to phrase the ask — and the loop that sharpens the card
before a carry-back leaves. A message the user wrote themselves ends without it, even one asking
for what a line would have offered; so does a carry-back.

**Contents:** [The menu](#the-menu) · [The moves](#the-moves) · [Choosing this round's lines](#choosing-this-rounds-lines) ·
[What each pick does](#what-each-pick-does)

## The menu

Last thing in the turn, under a fixed `Go deeper` header, kinds and labels in the companion language:

```
**Go deeper**
1 · <kind> · <this turn's target>
2 · <kind> · <this turn's target>
3 · <kind> · <this turn's target>
───
0 · Write the carry-back
```

Three to five lines, numbered from 1 in the order of the moves table below — Overview, Explain, Walk,
Challenge, Stress, Verify — so the easiest move is always line 1. Every label names **this turn's**
target — the fork, the idea, the file, the line of the stance. A number
answers the menu, never the paste: a bare `1` is menu line 1 even when the paste has an Option 1, and
`0` always writes the carry-back. Measured, a bare `1` after a menu whose line 1 was the card was read
as "Option 1" and a carry-back went out that the user never asked for.

## The moves

| Kind | Moves | Needs |
|---|---|---|
| **Overview** | *The card, plainly* — the whole card from above · *Where we are* — what this session has locked, what is open, where this fork sits · *What this round changed* — the earlier lock or stance line this round touches | nothing |
| **Explain** | One idea the turn leaned on, through one model · two ideas or shapes easy to confuse, told apart | an idea the user has no model for yet |
| **Walk** | One concrete case through `file:line → file:line`, today and under a shape · the commit or incident that bounded this code | shapes whose behaviour a trace can tell apart |
| **Challenge** | One named line of the stance, attacked — a cost accepted, the Why · the runner-up at its strongest · what the other window takes for granted | a stance |
| **Stress** | Assume the shape shipped and broke, through `Invariant` · the requirement most likely to arrive next, and what each shape pays to absorb it | a stance, and a pick that is costly to reverse |
| **Verify** | The stance's **What would flip me**, as a check · when no check in reach decides it, the smallest probe that would | a flip fact |

## Choosing this round's lines

Read the round before writing the menu. The kinds follow what this round is, not the last menu:

| This round | Lead with | Leave out |
|---|---|---|
| A fork that is costly to reverse — schema, public contract, a resource several actors share | Walk, Stress, Verify | — |
| A fork that is cheap to reverse | Overview, Verify | Stress |
| Scope or framing — what belongs in this feature, whether this is the problem | Overview (*What this round changed* or *Where we are*), Challenge the framing | Walk, unless the scope turns on the code |
| No fact in reach decides it — the numbers do not exist yet | Verify as the smallest probe, Challenge, Stress | — |

Then the user's own messages this session: asked what something means → keep one Explain; argued
with the mechanism or the pick → no Explain, and when this stance still rests on the point they
disputed, a Challenge aimed at it. A second round or later offers *Where we are* or *What this
round changed* whenever the round touches something an earlier round locked. One line per kind; Verify whenever the stance has a flip fact.
A line with nothing real left to name is not offered — a check already run, an idea already given
a model — and *The card, plainly* returns only when the stance has moved.

Measured on a seven-turn session with four kinds of round, every one of nine menus drew the same
five kinds: a scope question was offered a code walk and a pre-mortem, a user who had just argued
the mechanism was offered the idea explained again, and no menu attacked a line of the stance or
said where the session stood. The only adaptation seen was dropping lines.

## What each pick does

Picks other than `0` end with the menu again, chosen afresh from what this turn found. Labels copied
from the previous menu are a failure: measured, a menu after an impact turn repeated its
predecessor word for word and never offered the gap that turn had just found.

**The card, plainly.** Nothing the card did not already establish, no four blocks re-rendered.
Four parts, in order: **What is being decided** — two or three plain sentences: the feature, the
question, why it came up now. **What it does to the feature** — per shape, one or two lines on what
someone using or running it would notice, not the code. **The pick** — named. **Why, ranked** —
three to five reasons, one or two lines each, each resting on a fact the card cites, ranked by how
far the pick would move if the reason were false; reason 1 is the stance's **Why it wins now**.
Fewer than three real ones → give those and say the pick rests on them alone.

**Where we are.** Three short lists from the thread alone: **Locked** — each with the round it came
from; **Open** — each with who holds the answer; **This fork** — which of those it depends on or
would reopen.

**What this round changed.** Each earlier lock or stance line this round touches — held, needs
amending, or reopened — with the fact that decides which.

**Explain.** Two paragraphs: one model mapped part by part (*the cashier is `drain()`, the line is
the 100-row batch*), then where the model stops holding. Then **Questions this opens** — three to
five, one or two lines each, across the idea, the platform around it, the card, and which next line
would sharpen the card. The user answers any, all, or none. Measured, an unbounded re-explanation
ran about 600 words with no model, and all its questions were about the mechanism.

**Walk.** The state at each step — values, rows, elapsed time — today and under the shape, with
numbers derived from the code rather than restated. Close on the invariant the walk shows.

**Challenge.** Argue against the named line as hard as the repo allows, or make the runner-up's best
case and the condition under which it wins. End on the stance — held, changed, or now resting on
something narrower — and say which.

**Stress.** Assume the shape shipped and broke: what failed, traced through `Invariant` and the
history behind it; what the failure does **not** reopen; what the pick locks. For the next
requirement: name it, and what each shape pays to take it in.

**Verify.** Run the check. Report the stance as held, changed, or unresolved — and when the check
cannot run from here, name the smallest one that would close it, where it runs, and the result that
flips the pick.

**0 · Write the carry-back.** Picking it is asking for the reply: read `deciding.md` beside this file
and follow it. No shape named with the pick → the stance's pick.
