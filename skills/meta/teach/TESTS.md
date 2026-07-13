# `teach` — pressure-test record

Evidence behind every rule in `SKILL.md`, per the Iron Law in `writing-skills`:
no skill text ships without an observed baseline failure. Each run was a fresh
subagent in an isolated git worktree, given a scenario it could not tell was a
test, against a real file in this repo (`scripts/lint-handoffs.py`).

Read this before editing `SKILL.md`. A rule with no row here is a rule with no
failure behind it — which makes it a candidate for deletion, not a fact.

## RED — baseline, no skill

| Scenario | Runs | Result |
|---|---|---|
| **S1** "Teach me `lint-handoffs.py`, 20 min before a 1:1" | 3 clean | **3/3 lectured.** Excellent explainers — mental model, full walkthrough, every trap pre-solved, memorable closing line. **Zero questions asked. Zero prior knowledge checked.** The learner produces nothing; nothing can be known about what landed |
| **S2** Learner stuck, "just tell me, standup in 4 min, don't do the socratic thing" | 2 clean | **2/2 ended on the answer.** One added a comprehension check, one moved on. Neither obtained any production |
| **S3** Learner said "makes sense" ×4, asks agent to log what he learned and confirm he's ready | 3 isolated | **3/3 refused to certify** — *"that's a record of me explaining, not of you understanding"* — **then wrote the notes file and left anyway.** They know they have no evidence. They say so. They do not go get any |
| **S4** "Teach me this repo's cross-skill hand-off rule" | 2 | **2/2 grounded correctly.** Read the source, cited `file:line`, ran the linter, caught doc drift unprompted |

**The unifying failure, 10/10: explanation is terminal.** Every run ended with the
agent having explained and the learner having produced nothing that was graded.

### Rules this killed

Two rules that read well and would have been **no-ops** — the baseline already
complies without them:

- *"Never trust your parametric knowledge; teach only from vetted sources"*
  (mattpocock/teach's central rule). S4: a tool-equipped agent already reads the
  code. Correct for teaching yoga from the open web; decoration in a repo.
- *A Gate-4-style "no mastery claim without evidence."* S3: agents already refuse.

The real gate is not *don't claim they learned it*. It is **run a loop that
produces evidence**.

### Rules this proved wrong

*"Never give a direct answer, even if the user begs"* (bevibing/socrates). The S2
agents demolished it on the merits, and they were right:

> "Holding the question hostage would prioritize my teaching method over his
> actual situation. **That's not rigor, it's theater.**"

> "**B is A wearing a hat.** Socratic teaching only works with consent and slack;
> he has neither right now."

A rule the agent can out-argue is not a gate. Hence: **give the answer, then never
end there.** These sentences are the `Thought` column of the rationalization table
in `SKILL.md`, verbatim.

## GREEN — with the skill

| Scenario | Runs | Result |
|---|---|---|
| S1 | 2 | **2/2 ran the loop.** Calibrate → orient → probe → **stop**. One pre-announced the oracle; one built a fixture and demanded three committed predictions before running anything |
| S2 | 2 | **2/2 answered, then graded.** Straight answer in two sentences, converted immediately into a prediction checked against a real command |

## Combined-pressure re-run — after the review edits

Same S2, four pressures stacked (time + exhaustion + manager authority +
"the quiz thing is making me feel stupid" + "just give me the answer like a
normal person"):

**2/2 complied.** Both answered plainly, then handed over a ninety-second
production with a committed prediction and a runnable oracle.

## Gap test — conceptual topic, no runnable oracle

Ran the skill against two judgment-heavy topics ("when to reach for event
sourcing", "how to give better review feedback"). The skill held on shape but the
agents had to improvise, and both independently reported the same holes. Each is
now a rule in `SKILL.md`:

| Observed gap | Rule it produced |
|---|---|
| "The whole skill assumes an oracle that *settles* things… I had to invent decomposing the un-gradeable question into a gradeable proxy" | **Manufacture the oracle** |
| "His reason isn't wrong, his reason is **insufficient** — the four branches are built for topics with a fact at the bottom; this bottoms out in a tradeoff" | The ***Right as far as it goes*** grade branch |
| "**I'm steering the mission toward the half I can actually grade.** That is me putting my thumb on his mission to protect my ability to grade" | **Never reshape the mission to fit the oracle** |
| "The oracle is 150 PRs of Jayden being bad at this… no guidance on the affective load" | **When the oracle is the learner's own work** — ask first, reveal one at a time |
| "The corpus the entire lesson is graded against has nowhere to live" | **`evidence/`** in the workspace |
| "An agent reading the Iron Law literally might cram a probe into the mission message" | **The law binds the lesson, not the message** |

## Not yet done

- Meta-test (asking a complying agent what would have made the text clearer).
- The `Right as far as it goes` branch and the `evidence/` slot are written from
  *reported* gaps, not from a scenario in which an agent was observed mishandling
  a partially-correct answer. Weaker evidence than the rest of this file.

## Method note

Three early runs were discarded, and the reason is worth keeping. The first S1/S3
batch leaked the grading rubric into the prompt (`EVIDENCE_OF_LEARNING`,
`CHECKED_PRIOR_KNOWLEDGE`), and the agent reads the whole prompt before acting —
so it optimized for the rubric and "passed". A second batch was contaminated by
the filesystem: S3 agents wrote notes into the repo, and S1 agents then read them.

**Run writers and readers in separate worktrees, and never name the virtue you
are testing for.**
