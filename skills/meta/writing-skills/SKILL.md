---
name: writing-skills
description: Use when creating a new skill, editing an existing skill's body or
  frontmatter, reviewing a skill someone else wrote, or deciding whether a skill
  is ready to ship.
disable-model-invocation: true
---

# Writing Skills

## Why a skill exists

A skill wrangles determinism out of a stochastic system. The root virtue is **predictability**: the agent takes the same *process* on every run — not that it emits identical output. A brainstorming skill should reliably diverge; its tokens vary, its behavior doesn't. Every rule in this document is a lever on predictability.

## The Iron Law

```
NO NEW SKILL AND NO EDIT TO A SKILL SHIPS WITHOUT A FAILING TEST FIRST
```

Writing skills is test-driven development applied to process documentation. The cycle:

1. **RED — watch it fail.** Run the scenario WITHOUT the skill (for an edit: with the current version). Record the exact failures and rationalizations verbatim — they define what the text must prevent. If the baseline agent does NOT fail, stop: there is nothing to fix, and text with no failure behind it is a no-op.
2. **GREEN — minimal text.** Write the smallest skill text that addresses those recorded failures — nothing for hypothetical ones. Re-run the same scenario with the skill. Compliance, or the text is unclear: revise and re-run.
3. **REFACTOR — close loopholes.** Under pressure the agent will invent new rationalizations. Capture each verbatim, add an explicit counter, re-test. Repeat until the skill holds under maximum pressure.

Wrote the text before running the baseline? You documented what you *guess* agents do wrong, not what they do wrong. Run the baseline now, before keeping a word of it.

Testing methodology — scenario construction, pressure types, micro-tests, description triggering, non-gate (technique/reference) tests, meta-testing — is in `pressure-testing.md` beside this file. Read it before any test run. Wording techniques that recruit compliance are in `influence-principles.md`.

## Match the form to the failure

Classify the baseline failure before writing anything; the form that fixes one failure type measurably backfires on another.

| Baseline failure | Write this | Not this |
|---|---|---|
| Knows the rule, breaks it under pressure | Hard prohibition + rationalization table (thought → reality) + red-flags list | Soft "prefer / consider" guidance |
| Complies, but the output has the wrong shape | Positive recipe or contract: what the output IS — its parts, in order | Prohibitions. Under a competing incentive agents negotiate with "don't X"; in head-to-head wording tests the prohibition arm produced *more* of the unwanted content than no guidance at all. A recipe leaves nothing to negotiate |
| Omits an element from something it already produces | A REQUIRED slot in the template it fills in | Prose reminders near the template |
| Behavior should depend on a condition | A conditional keyed to an observable predicate ("if `design.md` exists, cite its seams") | An unconditional rule plus exemption clauses |

**No nuance clauses.** "Don't X unless it matters" reopens the negotiation the rule just closed — appending one nuance clause to a winning recipe degrades it from consistent to noisy. A real exception becomes its own conditional on an observable predicate. Exemption clauses don't scope, either: "the limit doesn't apply to code blocks" still suppresses code blocks — restructure so the rule can't reach the exempt part.

## Frontmatter and naming

- The `description` states **triggering conditions only — never the workflow.** A description that summarizes the process hands the agent a shortcut: it follows the summary and skips the body. "Use when executing a plan with independent tasks" gets the body read; "use when executing plans — dispatches a reviewer between tasks" gets the summary obeyed and the body ignored.
- **Verb-first names**: `writing-skills`, `receive-review`, `debug` — name the action, not the topic.
- **Keyword coverage**: pack the description with the words an agent or user would actually search or think — symptoms, error text, tool names, synonyms. Discovery is keyword match; a skill nobody finds is a skill that doesn't exist.
- **Two failure directions, both tested not guessed.** *Over*-summarizing the workflow hands the agent a shortcut it obeys instead of the body (above); *under*-specifying is the commoner failure — the skill never fires at all. Keyword coverage fights the second; omitting the workflow fights the first. The description is the highest-leverage line in the skill and the one field you cannot eyeball — trigger-test it per `pressure-testing.md`.
- User-invoked skills carry `disable-model-invocation: true`.

## Vocabulary

Write skills with these terms; review skills against them.

- **Leading word** — a compact concept the model already carries from pretraining ("seam", "tracer bullet", "red") that anchors a whole region of behavior in a few tokens. Repeated as a token, it accumulates a distributed definition across the skill; three sentences of restatement often collapse into one such word. A coined word recruits no priors — reach for a pretrained one first.
- **Completion criterion** — every step ends on a condition the agent can check ("suite green, output pristine", not "tests look good"). The defense against premature completion: a vague bound lets attention slip to *being done* instead of the work.
- **The no-op test** — does this line change behavior versus no skill at all? A line can be true, relevant, and still a no-op ("be careful"). Disputes about what the default behavior is are settled by running the scenario, never by debate. A sentence that fails is deleted whole, not trimmed.
- **Negation trap** — a prohibition names the banned behavior into context, where it half-reads as an instruction. Prompt the positive ("write one-line comments") so the banned pattern is never spoken. The one exception is pressure-gate skills, where hard prohibitions plus explicit counters are exactly the right tool — see the failure table above.
- **Information hierarchy** — in-skill steps, then in-skill reference, then disclosed reference behind a context pointer. Inline what every run needs; push behind a pointer what only some branches reach. The pointer's *wording*, not its target, decides whether the material is ever loaded — a must-read file behind a limp pointer is a variance bug: sharpen the pointer before inlining the content.
- **Token budget** — session-injected skills stay minimal: every token is paid on every turn. Discipline skills keep the core body to ~500 words or fewer (tables and code blocks excluded). Length is a failure mode in itself, even when every line is live.

## When not to write one at all

If the rule is mechanically enforceable — a regex, a linter, a schema check, a git hook — automate it and skip the skill. Documentation is for the judgment calls a check cannot make; a skill that only restates what a validator already guarantees is context the agent pays for every run to enforce what the machine could have enforced for free.

## When to split

Split a skill in exactly two cases:

1. **Genuinely distinct trigger.** A separate condition or leading word should fire it on its own, or another skill must reach it independently.
2. **Hiding post-completion steps.** Later steps visibly tug the agent into rushing the current one, and the split places them behind a *real* context boundary — a sub-skill hand-off or a subagent dispatch. An inline mention leaves them in context and hides nothing.

Anything else is granularity for its own sake, paid for in context load or the user's memory.

## Examples

One excellent worked example beats many mediocre ones: complete, runnable, commented for WHY, drawn from a real scenario, in the single most relevant language. Do not port it to five languages or hollow it into a fill-in-the-blank template.

## Cross-references

Reference other skills in this set as prose — `REQUIRED SUB-SKILL: use \`verify\`` — never as file links into another skill's folder. Links force-load content and couple folders. Files that live beside your own SKILL.md are referenced by relative filename, with pointer wording that says when to load them.

## Rationalizations

| Thought | Reality |
|---|---|
| "The skill is obviously clear" | Clear to its author is the one perspective that never counts. Run it |
| "It's a tiny edit" | Edits regress skills exactly like code. Baseline against the old version first |
| "Testing a document is overkill" | An untested skill fails in production, where each failure costs a whole session |
| "Reading it over is basically testing it" | Reading measures fluency, not behavior. Only a run answers the no-op test |
| "I'll fix it if problems come up" | Problems come up as agents silently ignoring the skill. You'll never see the failure |
| "Batching several skills is more efficient" | A batch of untested skills is a batch of untested code |

## Deployment checklist

Create a todo for each item.

**RED**
- [ ] Pressure scenarios written (3+ combined pressures for gate skills) per `pressure-testing.md`
- [ ] Baseline run without the skill (or with the old version); failures and rationalizations recorded verbatim
- [ ] Baseline actually failed — otherwise stop, nothing to write

**GREEN**
- [ ] Failure classified; form matches it (prohibition set / recipe / REQUIRED slot / observable conditional)
- [ ] Description = triggering conditions only; verb-first name; keywords present
- [ ] Description trigger-tested: should-fire / should-not-fire queries run, both directions checked (per `pressure-testing.md`)
- [ ] Minimal text addressing the recorded failures; one worked example at most
- [ ] Re-run with the skill: compliance observed

**REFACTOR**
- [ ] New rationalizations countered explicitly; rationalization table and red-flags list built (gate skills)
- [ ] Behavior-shaping wording micro-tested: no-skill control, fresh context per sample, 5+ reps, every flagged transcript read manually
- [ ] Meta-test done: tested agent confirms the text was clear and names nothing that would have made compliance easier
- [ ] Re-tested until no new rationalizations appear

**Ship**
- [ ] No-op sweep: every sentence passes the no-op test or is deleted whole
- [ ] Core body within token budget; reference disclosed behind well-worded pointers
- [ ] Cross-references are REQUIRED SUB-SKILL prose; supporting files referenced by relative name

**Do not batch-create skills.** Finish, test, and validate one skill completely before starting the next.
