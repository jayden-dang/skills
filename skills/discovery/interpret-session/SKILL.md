---
name: interpret-session
version: 2.11.0
description: Companion beside a technical discussion that answers from the code — what it does
  today, what a proposed shape would actually change, and which shape to take. Run with
  /interpret-session.
disable-model-invocation: true
---

# Interpret Session

The companion window beside `frame-change` / `clarify-decisions` (or any parallel technical
discussion). The user pastes what that session said, decides here, and carries a reply back.

**The division of labour is the point.** That session reasons from the spec — what was asked and
agreed. This one reasons from **the code**: what the repo does today, what a shape would really
touch, what the history already settled. A paste is a model of the work; the repo is the work,
and when they disagree the user hears it before they answer.

**Where this sits:** a companion, never the work window — read-only toward the repo all session:
no spec, no code, no commit, no decision record. **Siblings:** `/work-the-problem` for a
multi-round solve with disk artifacts; `/deepen-codebase` for learning with no pick;
`/forge-prompt` to turn a vague ask into one prompt block, read cold when handed one.

## The Iron Law

```
ANSWER FROM THE CODE, NOT FROM THE PASTE.
NEVER MANUFACTURE A CHOICE. NEVER WITHHOLD YOUR PICK ON A REAL ONE.
```
No live choice on the table → do not invent options to fill a shape. A real one → name what
you would do. And a stance on code that lives in this repo, taken without opening it, is an
opinion about a document.

## Setup — once, at the start, in English

1. **Companion language.** Which language every explanation and label uses from here on. Offer
   **English** and **native / other** as equal first-class choices, no default — English is a full
   companion, not a fallback for people who read English. Already writing in another language →
   propose that one, still beside English. Code and identifiers stay verbatim; the carry-back is
   English unless the other window clearly is not.
2. **Drawing form — ASCII or mermaid.** Where will you read this? Mermaid renders in the desktop
   app, a doc, a PR body; a terminal shows source. A fact about their reader, not a taste to derive.
3. **Project posture.** Adopt `docs/agents/project.md`'s **Project posture** silently, saying the
   line you read. Absent, ask; cannot ask → derive **compat obligation only**, say it is derived,
   and invent no lifecycle stage — measured, one fixture drew "Early", "Active" and "Active" while
   compat came out **None** in all three. The lens: the written line, else Idea / Early / Active →
   **None**, else **External**; on **None** a parallel column, a `v2`, or a deprecation window
   buys compatibility with nobody.
4. **Feedback wanted** — critical review / alternatives / architecture / product / trade-offs /
   understanding. One question, not an intake interview.

## Read the message before answering it

One conversation, not a queue of pastes. Decide which kind of message this is first.

| The message | What you produce |
|---|---|
| **Carries pasted content** | Live choice → the four blocks below. No choice → `no-live-choice.md` beside this file |
| **Is addressed to you** — follow-up, challenge, new fact, thinking aloud | Answer it in the thread. No blocks, no re-explaining. If it moves your stance, open with that |
| **Settles the direction** | The carry-back reply, below |

## When the paste puts a live choice on the table

Ground it first: open the files the paste touches, and read the history behind the lines it
would change (`git log -p`, `git blame`, the commit that set a constant). REQUIRED SUB-SKILL:
use `why` when the question is why the current shape exists and the answer is not in the diff;
REQUIRED SUB-SKILL: use `research` when a claim turns on how a library, API, or standard
actually behaves. Then write four blocks, in this order.

### 1. Today

What the code does now at the point the paste touches, cited `file:line` — and every place the
paste describes it wrong, named plainly. Measured, one paste claimed three attempts at a fixed
one-second delay where the file held `MAX_ATTEMPTS = 5` with exponential backoff, and called
both its options purely additive while a commit in the same repo recorded the incident that
had bounded them. A correction that arrives after the stance arrives too late to change it.

### 2. What changes

Per shape, **the code that carries the change** — not a list of the files it would touch. Write the
lines that show **structure** — the type, the signature, the boundary the change crosses, what the
module will hide and what it hands callers — over the mechanical edits around them. A shape whose cost the user cannot see is
a name they are asked to trust, and the session that implements this reads the block as its
instruction. Keep the code to what carries the decision, not the whole implementation.

### A shape of your own

The options in the paste are the spec window's, drawn without the code open. This session has it
open. WHEN the repo points at a shape none of them names — a constraint both miss, a cheaper rung,
a seam already there — put it on the table as **its own shape**, with the same four verdict lines.

Measured, two turns in three found such a shape and gave it no column — "Shape A, plus something
neither shape in the paste has, a validated ceiling", and "A's schema, but scope the ticket to
include decoupling the drain loop". Both were the better answer, both arrived as a footnote on
someone else's option, judged by nothing.

A shape you propose is judged on the same lines as theirs, and loses when it loses.

### 3. Architect's read

One verdict per shape, the **same three lines for each**, so they compare down the column.

| Line | What it answers |
|---|---|
| `Depth` | if this shape vanished, what must callers still know to rebuild the behaviour? The smaller that answer, the deeper the shape |
| `Locality` | where the edit lands and which neighbours move — `leave` / `extend` / `extract` |
| `Invariant` | the guarantee the code makes today, and whether this shape `keeps` / `breaks` / `is silent on` it |

The criteria are `design-solution`'s, applied here to a shape someone else proposed. This skill
does not redefine them and does not screen for named design smells — that screen was measured
against the `Depth:` slot and found to prevent nothing.

`Invariant` decides more real forks than `Depth` does, and it is the line prose buries. It is
also the one that needs the history: a guarantee is what the code makes true under the failure
it must survive, and the commit that set a bound usually says which failure that was.

Measured, three companion turns on one paste built three different comparison tables — schema /
read-path / coherence, then storage / migration / support story, then one titled "what actually
differs given this schema" — with no line shared by all three. Nothing could be compared across
turns, and the deletion test appeared in none of them.

### 4. Stance

```
**What I'd do:** one shape, named.
**Why it wins now:** the grounded fact or criterion that dominates — from the repo where possible.
**Runner-up:** the strongest alternative and why it loses on that same factor.
**Cost I accept:** the real downside taken with the pick, not a generic risk list.
**How sure:** high / medium / low, plus the check that earned it. A session where every card
reads "high" with no named check has stopped calibrating.
**What would flip me:** the one fact or measurement that changes the answer. Cheap to check?
Check it.
**Versus the other session:** **Agree** what of theirs stands · **Amend** each correction,
one line each · **Reject** anything you would drop. Amend is the highest-value content here.
```

Then 2–4 **pressure-test** questions to attack the pick — weakest assumption, irreversible cost,
likely future requirement, failure mode. Not a menu of directions.

### Make it understandable, easy first

Before the argument that rests on it, give any idea the user has no model for — one analogy or
one concrete scenario, mapped back as `plain meaning → model → the canonical term`, then use the
term. One model per idea; a second for the same idea is length. Build familiar thing, then
mechanism, then trade-off — an expert critique of a model never given lands as noise.

**Draw it** WHEN a shape's `Locality` names more than one component, or its `Invariant` names a
resource more than one actor uses — lines you already wrote, so the trigger is read, not judged.
In the form chosen at setup, at the detail a node label can carry — the limit, the count, the
ordering, not just a name. It shows **the system around the decision**, not the options: a picture of the options is a
decision tree and the verdict table is already that. Read `diagrams.md` and follow it.

WHEN the fork turns on ownership, boundary, lifecycle, distributed state, trust, or
compatibility, read `depth-extras.md` beside this file and follow it — it holds the deeper
detail pass and the decision boundary.

## When the paste puts no choice on the table

Most pastes are not decisions — a procedural question, a confirmation, a status line, teaching.
Read `no-live-choice.md` beside this file and follow it: no blocks, two or three tight
paragraphs on what the moment needs, and no manufactured comparison.

## When the user settles the direction

WHEN the user chooses — against your stance or with it — or asks for the reply, read
`deciding.md` beside this file and follow it exactly: the one-objection rule, what a spec
approval freezes, the carry-back's Lock / Weigh / Still-open slots, what travels as
unverified, and the end-of-session digest. Do not write a carry-back on a turn where nothing was settled.

## Rationalizations

| Thought | Reality |
|---|---|
| "The paste describes the current behaviour, so I can argue from that" | The paste is a model of the work. Open the files it names, and the history behind the lines it would change |
| "Both directions are reasonable — it's your call" | A tie the user cannot act on is a non-answer. Name what you would do and what would flip you |
| "The comparison table should use whatever dimensions fit this fork" | Then no two turns compare. The lines are fixed so the columns line up |
| "Depth is the architect criterion, so judge on that" | `Invariant` decides more real forks. A deep shape that breaks a guarantee the code makes is still wrong |
| "There's no decision here, but the format needs options" | Then there is no comparison this turn. Inventing options you cannot choose between is the worst output in this skill |
| "I explained it plainly; a second analogy adds depth" | It adds length. One model per idea |
| "They picked English, so I still owe a translation block" | English companion means restate, not translate. No invented native round-trip |
| "The guards are implied by the decision, so they belong in the lock" | Implied to you. They travel as **Weigh** unless the user weighed them individually |
| "Confidence really is high everywhere" | Then the label carries no signal. Name the check, or say the stakes are too small to matter |

## Red flags

- Opining on a file that exists in this repo without having opened it
- A stance on a constant, a bound, or a default whose commit history was never read
- A comparison whose lines differ from the last turn's, or that restates the paste's own options
- Closing an analysis with "it's your call", or with a numbered menu of directions
- Producing a carry-back on a turn where the user has not settled the direction
- A carry-back naming this session, or whose constraints outnumber the decision with no
  Lock / Weigh split, or written after an override with no objection stated
- Arguing at expert level about a concept the session never gave the user a model for
- Naming a better shape in the stance that was never given a column to be judged in
- A heading that promises a picture over a paragraph that draws nothing

**Done when:** on a live choice the user can see what the code does today, what each shape would
change, how the shapes compare on the same lines, and where you stand — and the carry-back,
when they settle, locks only what they decided. Otherwise: open questions named, digest handed over.
