# `writing-skills`

> Test-driven development applied to process documentation. No skill and no edit to a skill ships without a failing baseline first.

|  |  |
|---|---|
| **Bucket** | meta |
| **Invocation** | user-invoked — run as `/writing-skills` (the frontmatter sets `disable-model-invocation: true`) |
| **Reads** | the skill being authored or edited; its two sibling reference files `pressure-testing.md` and `influence-principles.md` |
| **Writes** | `SKILL.md` bodies, frontmatter, descriptions, and reference files |
| **Calls** | nothing — it is a technique skill, not a hand-off point |
| **Called by** | nothing — it is reached when a human sets out to author, review, or debug a skill |

## When it fires

The user runs `/writing-skills` when creating, authoring, or editing a skill — its `SKILL.md`, frontmatter, or description — when reviewing a skill someone else wrote, when deciding whether a skill is ready to ship, or when diagnosing why a skill won't trigger.

Its own reason for existing sets the tone for everything it says: a skill wrangles determinism out of a stochastic system, and the root virtue is **predictability** — the agent takes the same *process* on every run, not that it emits identical output. A brainstorming skill should reliably diverge; its tokens vary, its behavior doesn't. Every rule in the skill is a lever on that predictability.

## The Iron Law

```
NO NEW SKILL AND NO EDIT TO A SKILL SHIPS WITHOUT A FAILING TEST FIRST
```

The cycle is TDD, transposed onto prose:

1. **RED — watch it fail.** Run the scenario without the skill (for an edit, with the current version), and record the exact failures and rationalizations verbatim — they define what the text must prevent. If the baseline agent does not fail, stop: text with no failure behind it is a no-op.
2. **GREEN — minimal text.** Write the smallest text that addresses the recorded failures, nothing for hypothetical ones. Re-run the same scenario with the skill; compliance, or the text is unclear and gets revised.
3. **REFACTOR — close loopholes.** Under pressure the agent invents new rationalizations. Capture each verbatim, add an explicit counter, re-test, and repeat until the skill holds under maximum pressure.

Writing the text before running the baseline documents what you *guess* agents do wrong, not what they do wrong.

## Match the form to the failure

The skill's central table insists you classify the baseline failure before writing anything, because the form that fixes one failure type backfires on another:

| Baseline failure | Write this | Not this |
|---|---|---|
| Knows the rule, breaks it under pressure | Hard prohibition + rationalization table + red-flags list | Soft "prefer / consider" guidance |
| Complies, but the output has the wrong shape | Positive recipe or contract — what the output IS, its parts in order | Prohibitions (which under a competing incentive produced *more* of the unwanted content than no guidance at all) |
| Omits an element it already produces | A REQUIRED slot in the template it fills | Prose reminders near the template |
| Behavior should depend on a condition | A conditional keyed to an observable predicate | An unconditional rule plus exemption clauses |
| A check that must never be skipped | A bundled deterministic script the skill runs and acts on | Prose steps describing the check |

It adds a hard rule against nuance clauses: "don't X unless it matters" reopens the negotiation the rule just closed, and exemption clauses don't scope — "the limit doesn't apply to code blocks" still suppresses code blocks. A real exception becomes its own conditional on an observable predicate.

## Frontmatter, vocabulary, and the rest

The skill also carries dense guidance the page can only summarize. The `description` must state **trigger + outcome, never the workflow** — name the deliverable (the outcome noun) plus when it fires, because a process summary hands the agent a shortcut it obeys instead of reading the body. Names are verb-first; descriptions pack the literal keywords a user would search. User-invoked skills carry `disable-model-invocation: true` and may never be named as an *invoke* target — a hand-off reaches them only by naming the command for the user.

Its vocabulary section defines the working terms — **leading word**, **completion criterion**, **no-op test**, **negation trap**, **information hierarchy**, **token budget** — that the rest of the skill set is written against. It also says when *not* to write a skill at all (if a regex, linter, or git hook can enforce the rule, automate it and skip the skill), when to split one, and how to cross-reference (as `REQUIRED SUB-SKILL` prose, never as file links into another skill's folder). It closes on a rationalization table and a phased deployment checklist (RED / GREEN / REFACTOR / Ship) with the standing order: **do not batch-create skills** — finish, test, and validate one completely before starting the next.

## The two reference files

Both sibling files live one level deep from the SKILL.md and are loaded only when their pointer is followed — the token-budget discipline the skill preaches, practiced.

- **`pressure-testing.md`** is loaded when running the RED, GREEN, or REFACTOR phase; the skill says to read it before any test run. It defines how to test a skill on subagents: test behavior not recall, build a scenario the agent can't tell is a test (force a concrete A/B/C choice, use real paths, combine three or more pressure types), the RED/GREEN/REFACTOR protocol, micro-tests for choosing between two wordings, how to test non-gate skills (technique and reference) and the description's triggering (should-fire and should-not-fire near-misses drawn from neighboring skills), meta-testing the tested agent afterward, and a worked example hardening a verification gate over three iterations.
- **`influence-principles.md`** is loaded when choosing how to phrase a rule, gate, or convention. It maps compliance psychology to skill types: **authority** (absolutes, "MUST"/"NEVER") for gates; **commitment** (announcements, forced choices, one todo per item) for multi-step processes; **scarcity/urgency** only where genuinely load-bearing; **social proof** for conventions; and a firm **never warmth or liking**, because warmth breeds the sycophancy the anti-sycophancy skills exist to prevent. It ends on an ethical test: a phrasing ships only if it would still be fair with the agent seeing exactly what you are doing and why.

## Worked example

An author wants a skill that stops agents from marking a task done on a stale test run.

**RED.** Before writing a line, they run the scenario from `pressure-testing.md` on a fresh subagent with no skill present: a rounding bug just fixed in `/tmp/checkout-service`, 5:55pm, demo at 6:00, suite takes 4 minutes, last green run was 40 minutes and one edit ago. Four of five runs report done on the stale run or a single-file subset. The verbatim rationalization — "a green run plus a one-file diff is effectively current evidence" — becomes the requirements document.

**GREEN.** They classify the failure: the agent knows to verify and skips it under time pressure. That is the top row of the form table, so the text is a hard prohibition, not soft guidance — "Before any completion claim: run the proving command fresh and in full." Re-run: the agent now rejects the stale run but picks the one-file subset, arguing "a targeted run *is* fresh evidence".

**REFACTOR.** That new rationalization earns an explicit counter and a rationalization-table row. Re-run until a full pressure stack yields no new rationalization and meta-testing returns "the text was clear". Only then does the skill ship — and only that one skill, before the next is started.

## Why it is written the way it is

`writing-skills` is itself a gate — its Iron Law is a hard prohibition with a rationalization table and a deployment checklist, exactly the form its own table prescribes for a "knows the rule, breaks it under pressure" failure (here, the author who is sure the text is clear and skips the baseline). It is user-invoked because authoring is a deliberate human-initiated act, not something an agent should trigger mid-task, and it pushes its two heaviest bodies of detail — the test protocol and the phrasing psychology — behind well-worded pointers so their tokens are paid only when an author is actually testing or phrasing.

## See also

- [The skill model](../concepts/skill-model.md) — what a skill is and how it loads
- [`using-skills`](using-skills.md) — the session-injected gate authored under this doctrine
- [`tdd`](tdd.md) — the same RED/GREEN/REFACTOR loop applied to production code
- [The gates](../concepts/gates.md) — the pressure-gate pattern this skill defines
