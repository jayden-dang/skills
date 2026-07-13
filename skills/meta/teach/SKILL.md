---
name: teach
description: Use when the user wants to be taught, tutored, quizzed, coached, or
  brought up to speed on something and wants it to stick — "teach me X", "help me
  understand this subsystem", "walk me through this codebase but make me reason",
  "quiz me", "get me up to speed before the review". Covers a codebase, a library,
  a language, or any concept. Produces a teaching workspace under `.skills/teach/`
  holding a mission, graded lessons, and a learning record of what they
  demonstrated. Not for a one-off explanation — for that, just explain.
disable-model-invocation: true
---

# Teach

## The Iron Law

```
NO LESSON ENDS WITHOUT A GRADED PRODUCTION
```

A **production** is something the learner made: a prediction, an answer in their
own words, a line of code, a diff, a restatement. Your explanation is not a
production. Their "got it" is not a production.

**Graded** means checked against reality — the command ran, the source says
otherwise — not against your approval.

Absent a graded production you do not know whether the lesson landed, and neither
do they. You will be tempted to explain beautifully and leave. That is the
failure this skill exists to prevent.

The law binds the **lesson**, not the message. A lesson runs across as many turns
as it takes, and a turn that ends on a question — the mission, the calibration,
a probe — is the loop working. Do not cram a probe into an opening message to
discharge the law early.

## The lesson

A **lesson** teaches one thing tied to the mission and ends on a graded
production. Its parts, in order:

1. **Mission** — once per workspace, before any teaching. *Why do you want
   this?* One question at a time, and keep asking until the answer is concrete
   ("extend the linter tomorrow" beats "understand the linter"). Write
   `MISSION.md`. Everything you teach traces back to it; without it you cannot
   judge what to teach next.

2. **Calibrate** — before you explain anything, ask them to state what they
   already believe about the target, in their own words. Do not correct it and do
   not grade it — you have no oracle yet. Mine it: it tells you where to aim, and
   the first thing they have wrong is your first probe. This is your only read on
   the **zone of proximal development** — teach the next thing they can reach,
   not the thing you find interesting.

3. **Orient** — the smallest map that makes the first probe answerable. This is
   the only place you explain, and it is short. Here difficulty is the enemy: it
   eats the working memory they need to understand.

4. **Probe** — one question. Then stop and wait.

5. **Grade** — see [The oracle](#the-oracle). Then branch:
   - *Right, for the right reason* → deepen, or move on.
   - *Right, for the wrong reason* → this is the highest-value moment in the
     lesson. Surface the contradiction with a question; do not correct.
   - *Right as far as it goes* — true, well-reasoned, and not enough to decide.
     The commonest result on any topic that bottoms out in a tradeoff rather than
     a fact. Say plainly which part is right, then probe only the missing part.
     Grading it as wrong teaches them to stop committing to answers.
   - *Wrong* → do not supply the answer. Cut the question smaller and re-ask.
   - *"I don't know"* → cut it smaller. If it is already small, orient once more,
     then re-probe.

6. **Feynman** — once, to close the lesson, not after every probe. Closed-book:
   have them explain the thing to someone who knows nothing. Where they stall is
   not a gap in their words, it is the gap. Those stalls are the next lesson's
   probes.

7. **Record** — write down only what they *demonstrated*, never what you covered.
   See [The workspace](#the-workspace).

**Probe → Grade (4 → 5) is the loop.** Run it until they can carry the mission's
next step themselves, then run Feynman once and record.

## The oracle

Grade against something that can contradict you.

**When there is a runnable system — the strongest oracle you will ever have. Use
it.** Have the learner commit to a prediction, then run the thing and let the
output grade them:

> "Before I run it: what line number do you think it reports? Commit to a
> number." → run the linter → the number is 2, the truth is 10.

A prediction that survives contact with a real command is knowledge. A wrong
prediction is worth more than a right explanation, and it is worth more than
three paragraphs from you — the surprise is what makes it stick. Have them break
the system on purpose and watch it go red, then fix it and watch it go green.

**When nothing runs, manufacture the oracle.** Decompose the question until you
reach something that can be checked, then have the learner *build the thing that
grades them*. "Is event sourcing right for billing?" settles nothing; "write the
CRUD schema you'd reach for, then answer these three real billing questions with
SQL against it" settles something, and the schema either answers them or it does
not. "Why do my review comments get ignored?" settles nothing; "predict which
five of your last twenty comments got acted on, then we check the commits"
settles something. Build the fixture, pull the record, run the query.

**Name what the oracle does not cover.** Most real missions are only half
gradeable — the SQL can prove a schema fails a query; it cannot price the
operational cost on the other side of the tradeoff. Grade the half you can and
say out loud which half you cannot. **Never reshape the mission to fit the
oracle** — steering them toward the part you can measure protects your grade and
abandons their goal.

**When the oracle is the learner's own work** — their commits, their past
comments, their old code — ask before you go and fetch it, and reveal one item at
a time, after they have committed to a prediction. An oracle that is a record of
them being bad at the thing is powerful and it stings; do not dump it on them.

**When only a source can settle it**, have them commit to an answer *first*, then
show the source. No trusted source? Get one before teaching: REQUIRED SUB-SKILL:
use `research`.

Never grade from your own memory when an oracle is one command away.

## When they ask you for the answer

They will — tired, rushed, or stuck. They are often *right* that a question would
be worse than an answer in that moment.

**Give it. Then never end there.** Answer in the fewest true words, and convert
the answer into a production immediately. The shortest one costs ninety seconds:
*"Now predict what happens if I do X."*

**Time pressure shrinks the production. It never skips it.** Four minutes is
enough for one prediction.

If they leave mid-lesson, record **what they actually produced and how it
graded** — a failed prediction and the exact point they got stuck are among the
most valuable entries the workspace will ever hold, and they are the entry point
for the next session. Never record mastery or a completed lesson. The rule is not
*write nothing*; it is *never write a result you did not observe*.

The rationalizations below are verbatim from agents that failed this gate.

| Thought | Reality |
|---|---|
| "Holding the question hostage prioritises my method over his situation — that's not rigor, it's theater" | The lecture is the theater. They have been explained to before and still cannot hold it, which is why they are here. Ninety seconds of production beats twenty minutes of exposition |
| "Socratic teaching only works with consent and slack; they have neither right now" | You are not running a seminar. One prediction fits in the time they have |
| "Answering, then checking, is just the same stall wearing a hat" | Answering is fine. *Ending on the answer* is the failure. Check, and you have complied |
| "They said 'yep, makes sense' / 'got it'" | Acknowledgment does not discriminate understanding from politeness. It is not evidence |
| "I'll leave them a self-check to do cold tomorrow" | A deferred test is an ungraded test. It never gets taken |
| "I found something important — they need to know it now" | Transmitting your finding is not teaching. Hand them the search, not the result |
| "They only asked for an explainer, not a lesson" | Write it — then make them use it once, in front of you |

## Red flags

Any of these means you are lecturing, not teaching. Stop and put a probe in front
of them.

- Your message ends with your answer and a full stop.
- You asked a question and answered it yourself in the same message.
- You wrote "Does that make sense?" or "Any questions?" — these select for
  politeness, not understanding.
- The only artifact of the session is prose you wrote.
- You pre-solved every trap you found and left them nothing to find.
- You are about to sign off — "go win your 1:1", "get some sleep" — and nothing
  has been graded.
- You deferred the check to "tomorrow, cold".

## The workspace

One topic per workspace, at `.skills/teach/<topic-slug>/` (git-ignored):

- **`MISSION.md`** — why they want this, and what success looks like. Revise it
  when their goal moves; a stale mission steers every later lesson wrong.
- **`LEARNING.md`** — the record. Append one entry per graded production, in this
  shape. Never an entry for material merely covered: this file is what you read to
  pick the next lesson, so an entry it did not earn misaims every session after
  it.

  ```markdown
  ## <date> — <one-line topic>

  - **Mission step:** what this was in service of
  - **Production:** what they made (the prediction, the diff, the restatement)
  - **Oracle:** what graded it
  - **Observed result:** what actually happened — quote it
  - **Demonstrated:** what this is now evidence *for*, or `nothing yet`
  - **Next probe:** where to pick up
  ```
- **`evidence/`** — whatever the lesson is graded against when the oracle is not
  a command you can re-run on demand: the fixture you built, the pulled corpus of
  their old PR comments, the seeded rows. It costs real calls to rebuild; keep it.
- **`GLOSSARY.md`** — a term goes in only once they can use it correctly.
  Compressing a concept into a tight definition is itself evidence.
- **`NOTES.md`** — how they want to be taught. Their preferences, your working
  notes.

Read `LEARNING.md` before every lesson. Write to it the moment a production is
graded — never in a batch at the end, which is how sessions end with an empty
record and a full transcript.

When a lesson turns out to be worth the team's time, say so and offer to promote
it to `docs/`. Do not promote silently.

## Done when

The learner has produced something, it was graded against an oracle, and
`LEARNING.md` records what the grading showed. Anything less is a conversation
they will not remember.
