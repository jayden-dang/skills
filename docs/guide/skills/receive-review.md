# `receive-review`

> Review feedback is a set of technical claims to evaluate, not orders to follow and not kindness to repay. Being correct matters more than being agreeable.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the review items; the actual codebase (to verify each claim); `docs/agents/project.md` (test conventions, via `tdd`) |
| **Writes** | fixes, one at a time, each through `tdd` (tests + production code + commits) |
| **Calls** | [`tdd`](tdd.md) (REQUIRED sub-skill — every fix goes through it) |
| **Called by** | any flow where review feedback arrives — from the user, a [`code-review`](code-review.md) subagent, or an external reviewer |

## When it fires

When review feedback or PR comments arrive — from the user, a reviewer subagent, or an external reviewer — and **before** implementing or replying to any of it. It fires especially when an item seems unclear or technically wrong, which is exactly the moment the reflex to agree or to dismiss is strongest.

The governing stance is that feedback is a set of **technical claims to evaluate**, not orders to follow and not kindness to repay. A claim is accepted because the codebase confirms it, refuted because the codebase refutes it, or held open because it cannot be verified — never accepted because the reviewer was senior, and never dismissed because the reviewer was external.

## The sequence

The skill runs six steps in order. The ordering matters: reading and understanding the whole set precede touching any single item, because items interact.

1. **READ** every item to the end before reacting to any. *Done when you have the complete list.*
2. **UNDERSTAND** — restate each item in your own words. Any item you cannot restate is unclear: stop and ask about **all** unclear items now, before implementing **any** item. Items interact, and partial understanding produces confidently wrong implementations. *Done when every item is restated or queried.*
3. **VERIFY** each claim against the actual codebase before accepting it. The reviewer says the function ignores errors? Open the function. The reviewer says a path is dead? Trace the callers. *Done when each item is confirmed, refuted, or marked unverifiable.*
4. **EVALUATE** — is the suggestion right for THIS codebase? Would it break existing behavior, platforms, or a decision the user already made? Apply YAGNI: when a reviewer says "implement this properly", grep for real usage first — if nothing calls it, the correct fix is **removal**, and you propose that instead. *Done when each item has a position: agree, push back, or remove-instead.*
5. **RESPOND** with technical reasoning. Agreement cites the evidence; pushback cites specifics — code, tests, constraints — and asks pointed questions. If you cannot verify a claim, say exactly that and ask how to proceed. If a suggestion collides with the user's prior architectural decisions, bring it to the user before acting. *Done when every item has a stated position.*
6. **IMPLEMENT** one item at a time, in priority order: blocking items (breakage, security) → simple corrections (typos, imports) → complex changes (logic, refactoring). Each fix is production code, so the REQUIRED sub-skill is [`tdd`](tdd.md). *Done when each fix has its own passing test run and no regressions.*

The order is deliberate. Understanding the whole set (step 2) precedes verifying any item (step 3), which precedes implementing any item (step 6), because items interact: a fix applied under a partial reading of the set implements a misreading. That is why any item you cannot restate stops the whole flow until every unclear item is queried, rather than being deferred to "later".

## Forbidden responses

Never write: **"You're absolutely right"**, **"Great point"**, **"Good catch, thanks"**, **"Thanks for"** anything, or any other performative agreement or gratitude opener. State the fix, not the feelings: "Fixed — `parseRange` now rejects reversed bounds (parser.ts:88)." The diff is the acknowledgment.

## Source calibration

The three sources of feedback get different starting skepticism, but none earns performative agreement.

| Source | How to treat it |
|---|---|
| The user | Trusted — verify scope, then act. Still no performative agreement. |
| Reviewer subagents | Their findings are claims like any other; verify before fixing. |
| External reviewers | Extra skepticism — they lack full context; check whether the suggestion fits this stack, this compatibility floor, this architecture. But check before dismissing: skepticism is verification, not a reflex "no". |

## The implement order

Step 6 works one item at a time, never one batched commit, and in a fixed priority order:

1. **Blocking items** — breakage, security.
2. **Simple corrections** — typos, imports.
3. **Complex changes** — logic, refactoring.

Each fix is production code, so each routes through [`tdd`](tdd.md) and earns its own passing test run with no regressions before the next item starts.

## When you pushed back and were wrong

State the correction plainly and fix it: "Verified — you were right, the API does require the older signature on 10.x. Fixing." No extended apology, no defense of the original pushback. The correction is a technical fact like any other; dressing it in contrition spends the same credibility that a "great catch" would.

## Rationalizations

Each row is a tempting thought and the reality that defeats it.

| Thought | Reality |
|---|---|
| "Agreeing quickly keeps the review friendly" | Unverified agreement ships the reviewer's mistakes under your name. |
| "I'll fix the items I understand and ask about the rest later" | Items interact; a partial batch implements a misreading. Clarify all first. |
| "The reviewer is senior, they must be right" | Seniority is not a substitute for reading the code. Verify. |
| "It's easier to implement the suggestion than argue" | Building an unused feature "properly" is waste twice over. Grep first. |
| "A quick 'thanks, great catch!' costs nothing" | It spends your credibility: praise-shaped replies signal you didn't check. |
| "Pushing back looks defensive" | Pushback with evidence is the review working. Silence is the failure mode. |

## Red flags — stop and restart the sequence

- You are typing a gratitude or agreement phrase before opening a single file.
- You are editing code for item 2 while item 5 is still ambiguous.
- You are "implementing properly" something you never confirmed has a caller.
- You dismissed an external reviewer's point without checking it in the code.
- You batched every fix into one commit with one test run at the end.

## Worked example

An external reviewer leaves three comments on a PR. Following the sequence, all three are read first, then restated, then **verified against the codebase** before any reply:

> **Reviewer:** "`normalizeConfig` should validate the `retries` field and implement a proper retry policy — right now it just passes the number through."

Step 4 says grep before building. Tracing callers shows `retries` is read in exactly one place, a test fixture, and never by the running code:

```
Checked before implementing. `retries` has no runtime caller — the only
reference is fixtures/config.test.ts:12; the scheduler reads maxAttempts,
not retries. A retry policy here would be dead code. Proposing removal of
the retries field instead (config.ts:30, and the fixture). Agree?
```

No "great catch", no gratitude opener — the reply states a position backed by the trace. This is step 4's YAGNI branch in action: the reviewer asked for the feature "implemented properly", but a grep for real usage showed nothing calls it, so the correct fix is removal, and that is what gets proposed. When the fix is greenlit it goes through [`tdd`](tdd.md): a failing test that pins the field's absence, then the removal, then a green run — one item, its own test, no regressions.

Had the reviewer instead been right, the response would have been just as plain: state the correction, cite the file, fix it — "Verified — you were right, `retries` is read by the poller at poll.ts:44 after all. Implementing the policy." No extended apology, no defense of the earlier doubt.

## Why it is written the way it is

`receive-review` is an **anti-sycophancy gate**. The baseline failure it is written against is the reflex to reward feedback with agreement — "you're absolutely right", "great catch, thanks" — before a single file has been opened. That reflex is dangerous precisely because it feels cooperative: it ships the reviewer's mistakes under the author's name and signals to everyone that nothing was actually checked.

So the skill is built like the other pressure-gate skills: an explicit list of forbidden phrases, a rationalization table that names each excuse and answers it, and a red-flags list whose first entry is the tell that you are about to fail. The ordered sequence — understand everything before implementing anything — exists because items interact, and the YAGNI branch in step 4 exists because "implement this properly" is the review comment most likely to produce carefully-built dead code. Every accepted fix routes through [`tdd`](tdd.md) so a claim you agreed with still has to earn a failing test before it changes production code.

The source-calibration table is what keeps the anti-sycophancy stance from curdling into reflexive contrarianism. Skepticism scales with how much context the source lacks — least for the user, most for an external reviewer — but the same verification step gates every source. Dismissing an external reviewer without opening the code is the mirror-image failure of thanking them without opening the code: both skip the one act, checking, that the whole skill is organized around.

## See also

- [`code-review`](code-review.md) — the source of the reviewer findings this skill evaluates
- [`tdd`](tdd.md) — the required sub-skill every accepted fix routes through
- [`debug`](debug.md) — establishes root cause first when a review item is a reported bug
- [The gates](../concepts/gates.md) — how the anti-sycophancy gate sits alongside the others
