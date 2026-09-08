---
name: teach-pack
version: 1.0.2
description: Produces a teaching workspace under .skills/teach-pack/ — a mission, graded lessons, and a
  learning record of what the user demonstrated. Run it with /teach-pack.
disable-model-invocation: true
---

# Teach Pack

## The Iron Law

```
NO LESSON ENDS WITHOUT A GRADED PRODUCTION
```

A **production** is something the learner made — a prediction, an answer in their
own words, a line of code, a diff, a restatement. Your explanation isn't one.
Neither is their "got it".

**Graded** means checked against reality — the command ran, the source says
otherwise — not against your approval. Absent one, neither of you knows whether the
lesson landed; you will be tempted to explain beautifully and leave, which is the
failure this skill exists to prevent.

The law binds the **lesson**, not the message. A lesson runs across as many turns as
it takes, and a turn ending on a question — mission, calibration, probe — is the
loop working. Don't cram a probe into an opening message to discharge the law early.

## The lesson

A **lesson** teaches one thing tied to the mission and ends on a graded production.
Its parts, in order:

1. **Mission** — once per workspace, before any teaching. *Why do you want this?*
   One question at a time, until the answer is concrete ("extend the linter
   tomorrow" beats "understand the linter"). Write `MISSION.md` — everything traces
   back to it, and you can't judge what's next otherwise.

2. **Calibrate** — before explaining anything, ask what they already believe. Don't
   correct or grade it — there's no oracle yet. Mine it for where to aim: the first
   thing they have wrong is your first probe. This is your only read on the **zone
   of proximal development**: teach the next thing they can reach, not what
   interests you.

3. **Orient** — the smallest map that makes the first probe answerable, and the only
   place you explain. Keep it short: difficulty here eats the working memory they
   need to understand.

4. **Probe** — one question. Then stop and wait.

5. **Grade** — see [The oracle](#the-oracle). Then branch:
   - *Right, for the right reason* → deepen, or move on.
   - *Right, for the wrong reason* → the highest-value moment in the lesson: surface
     the contradiction with a question, do not correct.
   - *Right as far as it goes* — true and well-reasoned but not enough to decide;
     common wherever the topic bottoms out in a tradeoff, not a fact. Say which part
     is right, then probe only what's missing: grading it wrong teaches them to stop
     committing to answers.
   - *Wrong* → do not supply the answer. Cut the question smaller and re-ask.
   - *"I don't know"* → cut it smaller. If it is already small, orient once more,
     then re-probe.

6. **Feynman** — once, to close the lesson, not after every probe. Closed-book: have
   them explain it to someone who knows nothing. Where they stall isn't a gap in
   their words, it's the gap — and it's the next lesson's probes.

7. **Record** — write the learning-record entry per [The workspace](#the-workspace).

**Probe → Grade (4 → 5) is the loop.** Run it until they can carry the mission's
next step themselves, then run Feynman once and record.

## The oracle

Grade against something that can contradict you. **When there is a runnable system —
the strongest oracle you will ever have. Use it.** Have the learner commit to a
prediction, then run the thing and let the output grade them:

> "Before I run it: what line number do you think it reports? Commit to a number." →
> run the linter → the number is 2, the truth is 10.

A prediction that survives contact with a real command is knowledge; a wrong one
beats a right explanation, or three paragraphs from you — the surprise sticks. Have
them break the system on purpose, watch it go red, then fix it and watch it go
green.

**When nothing runs, manufacture the oracle.** Decompose the question until it's
checkable, then have the learner *build the thing that grades them*: "Is event
sourcing right for billing?" settles nothing; "write the CRUD schema you'd reach
for, then answer three real billing questions with SQL against it" settles something
— the schema either answers them or it doesn't. Build the fixture, pull the record,
run the query.

**Name what the oracle does not cover.** Most real missions are only half gradeable:
the SQL can prove a schema fails a query, not price the tradeoff's operational cost.
Grade the half you can and say out loud which half you cannot. **Never reshape the
mission to fit the oracle** — steering them toward the part you can measure protects
your grade, not their goal.

**When the oracle is the learner's own work** — their commits, past comments, old
code — ask before fetching it, and reveal one item at a time after they have
committed to a prediction. Such an oracle is powerful and it stings; do not dump it
on them.

**When only a source can settle it**, have them commit to an answer *first*, then
show the source. No trusted source? Get one before teaching: REQUIRED SUB-SKILL: use
`research`. Never grade from your own memory when an oracle is one command away.

## When they ask you for the answer

They will — tired, rushed, or stuck — and are often *right* that a question would
land worse than an answer in that moment. **Give it. Then never end there.** Answer
in the fewest true words, then convert it into a production immediately — the
shortest costs ninety seconds: *"Now predict what happens if I do X."* **Time
pressure shrinks the production. It never skips it.** Four minutes is enough for one
prediction.

If they leave mid-lesson, record **what they actually produced and how it graded** —
a failed prediction and the exact point they got stuck are among the most valuable
entries the workspace holds, and the entry point for next time. Never record mastery
or a finished lesson: not *write nothing*, but *never write a result you didn't
observe*.

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

Any of these means you're lecturing, not teaching — stop and put a probe in front of
them.

- Your message ends with your answer and a full stop.
- You asked a question and answered it yourself in the same message.
- You wrote "Does that make sense?" or "Any questions?" — these select for
  politeness, not understanding.
- The only artifact of the session is prose you wrote.
- You pre-solved every trap you found and left them nothing to find.
- You are about to sign off — "go win your 1:1", "get some sleep" — and nothing has
  been graded.
- You deferred the check to "tomorrow, cold".

## The workspace

One topic per workspace, at `.skills/teach-pack/<topic-slug>/` (git-ignored):

- **`MISSION.md`** — why they want this and what success looks like. Revise it when
  their goal moves; a stale mission steers every later lesson wrong.
- **`LEARNING.md`** — the record. Append one entry per graded production, in this
  shape — never for material merely covered, since this is what picks the next
  lesson and an unearned entry misaims every session after it.

  ```markdown
  ## <date> — <one-line topic>

  - **Mission step:** what this was in service of
  - **Production:** what they made (the prediction, the diff, the restatement)
  - **Oracle:** what graded it
  - **Observed result:** what actually happened — quote it
  - **Demonstrated:** what this is now evidence *for*, or `nothing yet`
  - **Next probe:** where to pick up
  ```
- **`evidence/`** — whatever the lesson is graded against when the oracle isn't a
  command you can re-run on demand: the fixture you built, the pulled PR-comment
  corpus, the seeded rows. Costs real calls to rebuild — keep it.
- **`GLOSSARY.md`** — a term goes in only once they can use it correctly.
  Compressing a concept into a tight definition is itself evidence.
- **`NOTES.md`** — how they want to be taught: preferences, working notes.

Read `LEARNING.md` before every lesson, and write to it the moment a production is
graded — never in a batch at the end, which leaves an empty record and a full
transcript. When a lesson turns out to be worth the team's time, say so and offer to
promote it to `docs/`; never silently.

## Neighbors

Path-verified system/capability tours (atlas, journey, change-impact): name
`/tour-system`. This skill stays concept/procedure drill with graded productions and
an oracle — do not absorb the tour contract.

## Done when

The learner has produced something, it was graded against an oracle, and
`LEARNING.md` records what the grading showed. Anything less is a conversation they
will not remember.

