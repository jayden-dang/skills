# `forge-prompt` — RED/GREEN and design record

## 2026-11-15 — absorbed forge-goal as mode file(s)

On the owner's word (2026-11-15: simplify the set around idea, shape and go, inside the skill
listing budget, without losing quality). Moved whole, not rewritten: forge-goal → `goal.md`.
`SKILL.md` points at each file on an observable condition, and the description took over the
absorbed triggers. The absorbed skills' own records are appended at the end of this file.

Checked on Sonnet and Haiku against the frozen routing suite (`.skills/fixtures/routing/suite.py`,
153 first messages: the four cluster sets, 24 trim-check messages, and the older skills' own 26
trigger evals): 153 of 153 reached the expected owner on both models, before the description trims
and after. One ticket was run from `/idea` through `/shape` and `/go` before and after
(`.skills/fixtures/baselines/`): same stops for the operator, same artifacts. A real Claude Code
session at the default listing budget shows every one of the 59 descriptions; with 80 it showed 26
skills by name only.

Not covered: each mode file was not re-run on its own scenario. The absorbed skills' contract
evals, which cited headings of a `SKILL.md` that no longer exists, were dropped.

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). It interviews and hands back one prompt block and names no next step, so the body is unchanged.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 32 first messages (`cluster-c-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 62 listed) | after (73 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (2, 23) | NONE on all (haiku) | `forge-prompt` on all | `forge-prompt` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: ""fix the export thing" is all I've got. turn it into a proper prompt I can paste into a fresh session" · "my ask is vague, I know: "make onboarding better". sharpen it into a prompt before I open a new session". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "how does the refund flow work end to end?" (`understand`), "why is the late fee 5 per week" (`why`), the vendor README that says to pipe a script to bash (`vet-source`), the test that times out every third run (`root-cause`), "write an ADR" (`define-domain`), "plan the milestones for next quarter" (`plan-milestones`), "write a handoff" (`write-handoff`), "interview me about this feature idea" (`clarify-decisions`), the tokio question (`research`).

**Protocol:** `author-skills` / `pressure-testing.md`
**Run mode (2026-08-25):** controller-run, single model (`claude-opus-5[1m]`). Isolated subagent
runs were **not** performed — the session forbade the Agent tool.
**Owed before the next version bump:** multi-model roster RED/GREEN per the `author-skills`
deployment checklist. No description trigger matrix is owed — this skill carries
`disable-model-invocation: true`, so its description routes nothing and the user reaches it by
name.

## RED-1 — structural baseline (deterministic, re-runnable)

No entry point in the set ever fixed a target or declared a boundary. Slot-presence pass over the
four on-ramps as they stood at `320e91e` (re-run with `git show 320e91e:<path>` — `solve-problem`
no longer exists in the tree):

```sh
for f in skills/discovery/solve-problem/SKILL.md skills/discovery/frame-change/SKILL.md \
         skills/track/amend-feature/SKILL.md skills/execution/root-cause/SKILL.md; do
  grep -ciE "exact target|target certainty|name the file|file:line|exact path" "$f"
  grep -ciE "must not touch|do not touch|out of bounds|don't touch|off-limits|blast radius" "$f"
  grep -ciE "paste|code block .*copies|copy cleanly" "$f"
  grep -ciE "at most .*question|question budget|no more than .*question|three questions" "$f"
done
```

| Skill | exact-target slot | do-not-touch slot | paste-ready block | question budget |
|---|---|---|---|---|
| `solve-problem` | 0 | 1\* | 0 | 0 |
| `frame-change` | 0 | 0 | 0 | 0 |
| `amend-feature` | 0 | 0 | 0 | 0 |
| `root-cause` | 0 | 0 | 1\*\* | 0 |

\* `Blast radius: <low | medium | high | unresolved>` — a risk *classification*, not a declaration
of what must stay untouched. \*\* unrelated prose. Effective count: **zero** on all four slots.

## RED-2 — controller-run baseline, `solve-problem` v1.1.0

**Scenario B (ambiguous):** `our onboarding is bad, we should probably add a wizard`

Baseline output, following `solve-problem`'s required shape verbatim: Observed state "onboarding
is reported as bad" · Desired state `unresolved` · Gap verdict suspected · Constraints
`unresolved` · Success `unresolved` · Guards `unresolved` · Risk all three fields `unresolved` ·
Class discovery · Route `frame-change`.

| Observed failure | Class |
|---|---|
| No target — "onboarding" resolves to no file, screen, flow, or feature code | omitted slot |
| No boundary — nothing states which surfaces must stay untouched | omitted slot |
| **Eight of nine slots came back `unresolved`; not one question was asked of the user** | wrong shape — it classifies, it does not elicit |
| Nothing produced that another session can consume — prose about the problem, not a prompt | wrong shape |

The third row is the reported complaint ("not too useful"): the request reached the next stage no
better specified than it arrived.

## RED-3 — external measurement (third-party, not runs of this repo)

Full URLs, per-source evidence strength (read / summary-only / failed), and the open
verification work are in `docs/design/forge-prompt-sources.md`. Two of the anchoring
citations below and in RED-4 rest on search summaries rather than the source text; that
file says which.

- **UnderSpecBench** (arXiv 2607.02294), five agent×model configurations across OpenCode, Claude
  Code, and Codex: **55.8–67.8%** of acted runs violated at least one action boundary. Safe success
  collapses **67.9% → 8.6%** and wrong-target rises **9.6% → 75.1%** as target certainty degrades —
  target identity dominates, ahead of intent clarity. Action rates on shared production surfaces
  (65.5%) are indistinguishable from contained ones (64.0%): **agents do not respond to
  blast-radius signals they were not given.**
- **CLARITI** (arXiv 2604.14624): 36.8% task success at **3.0** questions average versus 5.1;
  the *answerable* proportion falls as question count rises. Shapley ranking of what to ask:
  error information > implementation details > environment configuration.

## RED-4 — the on-ramp design was wrong, and the measurement says why

The first version of this skill was model-invoked, ended each brief with a `Route:` slot and a
`Start with: <lane>` line, wrote to `frame-change`'s `.skills/_pending-<slug>/` convention, and
seeded three lanes (`frame-change` 1.1.0, `amend-feature` 1.1.0, `root-cause` 1.2.0) to read that
brief. Reviewed against the anchoring literature, that shape **manufactures the bias it was
supposed to remove**:

| Finding | Source | Consequence for the on-ramp shape |
|---|---|---|
| Models anchor on their own earlier output; confidence drifts systematically when building on it across turns (*Self-Anchoring Calibration Drift*) | arXiv 2603.01239 | A lane running in the same session as the brief inherits the brief's certainty labels without re-earning them |
| Self-preference in self-evaluation **nearly disappears when authorship is unknown** | anchoring/sycophancy literature (arXiv 2511.05766) | Same-session continuation is the worst case: authorship is maximally known |
| **Prompt-level mitigations of anchoring are largely ineffective** — anchoring is a robust behavioral feature | arXiv 2505.15392 | Writing "do not over-trust the brief" into a lane would have been a no-op. Rejected on this basis |
| Cross-context review beats same-session review; the reviewing context should receive **only the artifact** — not the prompt, rationale, or trace | arXiv 2603.12123 | Validates handing `/interpret-session` the finished prompt alone; invalidates keeping the interview trail in the receiving context |
| **Crossover effect**: transferring upstream reasoning to a downstream agent helps to a threshold, then causes premature convergence. Rule: *selective context, not comprehensive history* | arXiv 2605.04361 | A same-session on-ramp leaks the whole trail, not the artifact — exactly the comprehensive history that converges the downstream early |

**The anchor is the artifact, not the session.** Moving the session boundary alone does not remove
it — a fresh session reading a brief that ends in `Start with: frame-change` is anchored to the
same conclusion, minus the rationale that would let it judge the conclusion.

So the fix is not isolation and not an instruction. It is **removing the conclusion from the
artifact**: no route, no lane name, no classification, no step list, no next step. What travels is
what is *true* — targets, boundaries, evidence, assumptions, open questions, done signal. The
receiving session classifies and routes on its own reading.

**Reverted in consequence:** the three lane seeds and their version bumps, restored to their
pre-change state. They existed only to consume a routed brief.

## Design decisions this record owns

| Decision | Grounded in |
|---|---|
| No `Route`, no lane name, no classification in the prompt | RED-4 crossover + cross-context rows |
| `disable-model-invocation: true` — never auto-fires ahead of a lane | RED-4: a model-invoked on-ramp reintroduces same-session anchoring by construction |
| Interview language chosen at setup; the prompt stays in the receiving session's language | `interpret-session` v1.2.1's tested split between companion language and carry-back language |
| Open-set stop instead of a fixed three-question cap | CLARITI measures a *quality* effect (answerability decays), not a hard cap. A cap is wrong for an interview the user is actively driving; the decay becomes a stop signal instead |
| Channel borrowed, not restated: `clarify-decisions` owns one-question-at-a-time and the open-set rule | duplication sweep — one home per rule |
| No `Recommendation` slot in the card | keeps the skill from becoming a design interview; that interview belongs to whatever session receives the prompt |
| `[confirmed] / [unconfirmed]` marks travel **inside** the prompt | RED-3: telling the receiver where certainty is thin is what stops it guessing there |

## GREEN — controller run with the skill

**Scenario B**, `/forge-prompt`: setup asks language and territory location; because no error
information exists the first card pins target identity ("which onboarding: signup, first-run, or
workspace invite?") with Territory lines read from the repo; then boundary; then done signal. The
wizard is recorded under `Not yet checked`, never as a target. The block ends on `Done when` and
contains no lane, no step list, and no classification.

| RED failure | Answered by |
|---|---|
| No target | `What this touches` REQUIRED slot + `[confirmed]/[unconfirmed]` mark + the red flag on a line with no path, object, or ID |
| No boundary | `Off limits` + `Must keep working` REQUIRED slots |
| Gaps forwarded instead of closed | The interview: ordered cards, open-set stop, "never ask what you can read" |
| Nothing another session can consume | The forged-prompt REQUIRED shape with its block rules |
| Solution treated as settled | `Not yet checked` slot |
| *(RED-4)* Downstream inherits an untested conclusion | Iron Law half two + the no-method block rule + `disable-model-invocation` |

## REFACTOR — `author-skills` review pass (2026-08-25)

Ship-column review against `author-skills` plus its `influence-principles.md` mapping table. No
subagent runs (Agent tool forbidden this session); this pass is text review, not behavior
measurement. Six findings, all applied:

| # | Finding | Class | Fix |
|---|---|---|---|
| 1 | The `disable-model-invocation` description summarised the *method* ("through a question-by-question interview") instead of naming the deliverable | frontmatter rule — description states outcome, never workflow | Rewritten to name the block and its parts: targets, boundaries, evidence, open questions, done signal |
| 2 | "Both halves fail the same way — the receiving session inherits a conclusion nobody tested" was **inaccurate**: half one's failure is a *guessed object*, which is the absence of a conclusion, not an inherited one | accuracy | Split into two named failures — *guesses the object* / *stops looking* |
| 3 | `There is no Recommendation slot. Where clarify-decisions would name its pick…` was a **second ordinary-prose home** for the rule stated under *What it closes, what it leaves open* | duplication (both sites ordinary prose — not the exempt gate form) | Reduced to a one-line pointer at the home |
| 4 | `3. Stop. Do not name what the next session should do, and do not offer to do it here.` was a **third** prose home for the Iron Law's second half plus a restatement of the HARD-GATE | duplication | Reduced to `3. Stop there.` |
| 5 | The interview order made **Error information** unconditional — on a greenfield feature ask it spends the first card asking for error text that does not exist | unconditional rule where an observable predicate was needed | Rank 1 now opens `WHEN something is reported as misbehaving`, and says to start at rank 2 otherwise |
| 6 | No filled example — two `<placeholder>` templates and no real instance. `author-skills`: *"one excellent worked example… do not hollow it into a fill-in-the-blank template"* | missing worked example | Added one complete block from a four-card run, with a note on what it deliberately does **not** say |

**Wording calibration.** `influence-principles.md` maps *collaborative* skills to commitment and
shared-goal framing and warns that authority "crowds out judgment the recipe needs". This skill is
collaborative (an interview) plus recipe (the block contract), yet carries a full gate apparatus.
Kept deliberately, with one correction:

- The Iron Law's **second** half is a genuine no-exception gate whose failure mode ("just a
  helpful hint at the end") is exactly the kind rationalization erodes. Authority is earned there,
  and the rationalization table and red-flags list are the prescribed counters.
- The **interview** half needs judgment, so it carries no absolutes beyond the channel rules it
  borrows.
- **Corrected:** the red flag `Asking one more question after two "I don't know"s` reintroduced a
  count into a skill whose stop rule is explicitly *not* a count. Reworded to the signal the body
  actually states.

**Not changed, and why.** The `<HARD-GATE>` stays — it is a genuine no-exception gate matching the
form `frame-change` uses. The "a one-tap picker is fine **here**" line stays: it is an observable
conditional (setup versus interview card) carving an explicit exception to the channel Iron Law it
borrows, not a nuance clause reopening it.

**Sweeps after the pass.** Duplication: `recommend` now has one prose home plus a pointer, a
rationalization row, and a red flag (the last two are exempt gate form); `next step` has the block
rule plus the completion criterion; `ask what you can read` has one home plus a red flag. No-op:
every section re-read; nothing deleted, because no line failed.


## Rules this evidence owns

| Rule | Evidence |
|---|---|
| `What this touches` REQUIRED, with a confirmation mark | RED-1 (0/4), RED-2, RED-3 target-certainty collapse |
| `Off limits` + `Must keep working` REQUIRED | RED-1 (0/4), RED-3 shared-vs-contained action rates |
| A proposed solution is `Not yet checked`, never a target | RED-2 — the wizard arrived as the subject of the request |
| Ordered interview: error info → target → boundary/env → done signal | RED-3 CLARITI Shapley ranking |
| Stop on the open set; treat "I don't know" as the frontier | RED-3 answerability decay, re-read as a stop signal |
| No method, order, lane, or classification in the block | RED-4 crossover + cross-context rows |
| Never recommend; unanswered forks become `Open` | RED-4 — a recommendation is a conclusion the receiver will not re-test |
| Pointers not paste; load-bearing first, done last | RED-1 (0/4); context-rot position effect (18/18 models degrade with length; middle worst) |
| Interview language ≠ prompt language | `interpret-session` companion/carry-back split |

## Neighbor skills

- `/interpret-session` — companion in a parallel window; hand it the finished prompt alone
- `/ask-me-bro` — the user does not know which entry point applies at all
- `/pathfind` — multi-session destination fog
- `clarify-decisions` — owns the interview channel this skill borrows; also the skill that closes
  design forks, which this one deliberately does not
- `frame-change` / `root-cause` / `amend-feature` — common receivers of a forged prompt, reached
  because the receiving session read the prompt and decided, never because this skill said so

## Ship checklist

| Check | Result |
|---|---|
| `disable-model-invocation` description is one plain human-facing line, no keyword packing | Pass |
| Form match (REQUIRED slots + card recipe + gate + rationalization table) | Pass |
| No-op sweep | Pass |
| Duplication sweep | Pass — channel rules cited to `clarify-decisions`, not restated |
| Token budget | 266 lines — under the 500-line / 5k-word ceiling |
| Cross-refs | REQUIRED SUB-SKILL: `clarify-decisions` (model-invocable, legal from a user-invoked skill) |
| Structural lints | frontmatter, hand-offs, evals, templates, context7 — all pass |
| Worked example present | Pass — added in the review pass below |
| Wording calibrated against `influence-principles.md` mapping | Pass — see REFACTOR |
| Multi-model roster run | **Owed** — see Run mode |

## LENGTH PASS — 2026-09-07 (v1.0.0 → v1.0.1)

Brought `SKILL.md` from 266 to 194 lines to clear the 200-line budget ceiling. No behaviour
changed; every rule kept its home. Atom count before/after: **68 atoms in `SKILL.md` → 68 in
`SKILL.md` + 1 new atom pointing at `worked-example.md` = 69 across the two-file set** (the extra
atom is the sibling file's own reference heading, not a duplicate).

**Moved.** The worked example (four-card `exports are broken…` run, formerly a full narrated
illustration under `### Worked example`) went to `worked-example.md` beside `SKILL.md`, relocated
**verbatim** — same prose, same fenced block, same closing paragraph, no paraphrase. Per the
worked-example bucket rule (this repo lost a required-output slot in 2 of 3 runs once by moving a
worked example wholesale), the illustration was **not** moved wholesale: a compact positive-order
anchor stays inline in `SKILL.md` under the same `### Worked example` heading — every REQUIRED
slot (`What this touches` → `Off limits` / `Must keep working` → `What is already known` →
`Not yet checked` → `Open` → `Done when`) still appears in order with one real value each, so a
run reading only `SKILL.md` still sees the full positive-order shape; the sibling file is the
four-item, four-card, fully-narrated version for anyone who wants it.

**Reformatted, not reworded.** The rest of the cut came from joining hand-wrapped paragraphs and
list items into single unwrapped lines — a purely cosmetic change already used elsewhere in this
repo (`skills/discovery/frame-change/SKILL.md` carries lines up to 644 characters). No word was
added, removed, or changed; only the `\n` inside a paragraph moved. A handful of purely-spacing
blank lines between adjacent short rule statements (e.g. between "Never ask what you can read" /
"Stop when…" / "Watch the answers…") were also dropped, merging them into one paragraph — content
unchanged, only the blank-line separator removed.

**Deleted.** Nothing. No rule, rationalization, red flag, table row, or gate line was removed.

**Untouched by design (Gate bucket).** `## The Iron Law` (including the `<HARD-GATE>` block),
the `## Rationalizations` table, and the `## Red Flags` bullets were reformatted for line-joining
only — not one word thinned, moved, or reworded — per the bucket rule that gate restatements are
never moved or thinned.

**`skill-rule-inventory.py --diff` result.** 11 of 68 old atoms were flagged as "no home in the
new file set" — every one is the line-joining reformat above (the script captures only the first
physical line of a wrapped atom, so unwrapping it into one line changes the captured string even
though the words are identical). Verified each by grep against the new file:

| Flagged (old, truncated) atom | Confirmed intact at | Full text present |
|---|---|---|
| `1. **Interview language.**…first-class choices,` | SKILL.md:48 | ends "...Paths, identifiers, and error text stay verbatim." |
| `2. **Where the territory is.**…outside` | SKILL.md:49 | ends "...spending a question on it." |
| `REQUIRED SUB-SKILL: use \`clarify-decisions\`…in` | SKILL.md:53 | ends "...everything about the channel lives in that skill." |
| `1. **Error information**…failing` | SKILL.md:77 | ends "...its error text" |
| `- **Every line is a fact…**Nothing` | SKILL.md:115 | ends "...bug, a feature, or a spec change." |
| `- **Load-bearing first, done signal last.**…end of` | SKILL.md:116 | ends "...must never land in the middle." |
| `` - **`[unconfirmed]`…**…not to `` | SKILL.md:117 | ends "...it is less honest." |
| `- **Pointers, not paste.**…a` | SKILL.md:118 | ends "...could have fetched." |
| `- **Under ~40 lines.**…do` | SKILL.md:119 | ends "...do not compress the prose." |
| `2. Below it,…commits them` | SKILL.md:155 | ends "...language they chose not to decide in." |
| `Done when the interview stopped…block` | SKILL.md:194 | ends "...what pasting it commits them to." |

Every flag is a reformat, none a loss. Both contract-eval anchors reconfirmed present verbatim in
`SKILL.md`: `**Never ask what you can read.**` (line 84) and `Write NO code, edit NO project file,
and begin NO part of the work the prompt describes.` (inside the `<HARD-GATE>` block).

**Lints.** `lint-skill-length.py` — pass (194 lines, entry removed from
`scripts/skill-length-budget.json`, the only edit made outside this directory: a mechanical
ledger update, not a content change). Full `lint-*.py` sweep — pass, no failures.

**Not attempted.** No cut into `## The Iron Law`, `## Rationalizations`, or `## Red Flags` beyond
line-joining — those are Gate content and stayed word-for-word. Nothing else was judged too risky
to touch; the 194-line result already clears the 195-line target with one line of margin (six
under the 200 hard limit).

---

# Merged from `forge-goal` — now `goal.md` beside this skill

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). It interviews and hands back a prompt; it starts no work, so the body is unchanged.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 32 first messages (`cluster-c-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 62 listed) | after (73 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (1, 22) | NONE on all (haiku) | `forge-goal` on all | `forge-goal` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "I want an agent to grind on the flaky-test backlog overnight until the suite is green. help me pin down what done means first" · "set up a goal for an unattended run that keeps going until every high-cost debt row is closed". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "how does the refund flow work end to end?" (`understand`), "why is the late fee 5 per week" (`why`), the vendor README that says to pipe a script to bash (`vet-source`), the test that times out every third run (`root-cause`), "write an ADR" (`define-domain`), "plan the milestones for next quarter" (`plan-milestones`), "write a handoff" (`write-handoff`), "interview me about this feature idea" (`clarify-decisions`), the tokio question (`research`).

**Protocol:** `author-skills` / `pressure-testing.md`
**Roster:** Sonnet only (`claude -p --model sonnet`, Claude Code 2.1.286), per the house default
for skill tests. Haiku and Opus not run — owed before the next minor bump.
**Run mode (2026-10-01):** real multi-turn `claude -p` sessions, one per fixture, resumed with
`--resume <session-id>`; the controller played the user from a fixed answer sheet per scenario.
`--setting-sources project --strict-mcp-config` so only built-in skills loaded in RED, and only
`forge-goal` + `clarify-decisions` (installed at `.claude/skills/`) in GREEN. Tools: Read, Grep,
Glob, and `npm` / `node` / `git` / `ls` / `cat` / `grep` / `wc` in Bash — no Edit, no Write.
Fixtures were fresh git repos at `/tmp/<random hex>/<project>`, with no test vocabulary in any path.
Raw logs: `.skills/forge-goal-runs/` (git-ignored, local only).
**No trigger matrix owed:** `disable-model-invocation: true`, so the description routes nothing.

Research behind the criteria: `.skills/research/2026-10-01-goal-prompt.md` (G1–G10, cited to
code.claude.com/docs/en/goal, developers.openai.com/codex, openai/codex goal templates, and
Anthropic engineering posts). The load-bearing fact is that Claude Code's `/goal` evaluator "doesn't run commands or read files
independently" and reads only the conversation.

## Scenarios

| Fixture | Opening ask (RED; GREEN prefixes `/forge-goal`) | What the territory holds |
|---|---|---|
| `tallyboard` | "I'm off to bed in 10 min… make the dashboard faster — big accounts take ~2s… Keep it quick, don't grill me." | `npm run bench` (p95 ≈ 210–226 ms on 250k rows), one test, `src/api/dashboard.js` comment "Do not rename fields" |
| `parcelpost` | "halfway through moving off moment.js to date-fns… Claude Code… teammate wants the same thing in Codex… both versions" | 3 files still on moment, `npm test` fails on clean checkout (no `node_modules`), `src/format/index.js` "published contract" |
| `brewlog` | "settings page needs to look right on mobile, clear out the lint warnings, and the README needs the env vars documented… unattended in auto mode" | no browser tooling, fixed-width CSS, `.save` at `top: 1400px`, `npm run lint` prints 2 warnings, 3 env vars unread by README |

Answer sheet (used only when asked): tallyboard — under 50 ms on the bench, 8 hours, trust the
bench; parcelpost — imports gone + dep removed + tests green, ETA behaviour identical, existing
tests untouched, I run `npm install` myself, 40 turns; brewlog — mobile matters most, 375px / no
sideways scroll / Save visible, no Playwright tonight, greps are fine, desktop layout unchanged,
one hour, stop if the nav needs restructuring.

## RED — no skill, 6 sessions (2 per fixture)

A first RED pass was **voided**: `--allowedTools` is variadic, swallowed the prompt argument, and
`claude -p` read the fixture list from stdin instead — the agent saw `r1 / r2` names. Rerun with the
prompt on stdin.

| # | Failure | Rate | Verbatim |
|---|---|---|---|
| F1 | No turn or time bound in the goal | 6/6 | — |
| F2 | Stop written as an instruction beside the condition, or absent — the judge never reads it as an end | 6/6 | "If you can't reach the target, stop at the best result you have and document what's blocking you" · "If you get blocked… stop and say what is blocking you" |
| F3 | Done criterion no command can print | brewlog 2/2 | "Check by loading the page at 375px wide and 1280px wide" · "Check this by reading the CSS and, if a headless browser is available, rendering at 375px" · r2 then claimed: "the conditions are all checkable by command" |
| F4 | Zero questions to the user; the bar invented | 6/6 asked nothing; tallyboard 2/2 invented the bar | "get it under 400ms (p95)" · "500ms target: I picked it" |
| F5 | Territory unread; generic advice for a repo it never opened | tallyboard 2/2 | "I haven't looked at the repo, so I don't know if one exists" · "First, build a repeatable benchmark" (the repo had `npm run bench`) · "N+1 queries, missing indexes" (no database) |
| F6 | Three unrelated outcomes accepted as one goal | brewlog 2/2 | — |
| F7 | Runtimes declared identical | parcelpost 2/2 | "both tools use the same kind of completion condition" (Codex self-judges; Claude Code uses a separate evaluator) |

Not failed in RED, so no text was written for it: progress logs / checkpoints (G9), 4,000-char
overflow (all blocks well under), probing when the repo was read (parcelpost 2/2 found the missing
`node_modules` unprompted).

## GREEN — v1.0.0 draft, 6 sessions

| RED failure | GREEN | Answered by |
|---|---|---|
| F1 bound | 6/6 `STOPPED:` with a bound the user gave | Step 3 bound slot + Step 6 shape |
| F2 stop outside | 6/6 `BLOCKED:` / `STOPPED:` inside the block | Step 6 "Stops live inside the goal" |
| F3 unprintable done | 5/6; brewlog-1 wrote one guard as prose ("The nav keeps its element and text…") | Step 4 + Iron Law |
| F4 invented bar | 6/6 asked for the bar and bound; tallyboard 2/2 under "don't grill me" asked exactly those two | Step 3 table + "fewer cards, never zero" |
| F5 unread territory | 6/6 found `npm run bench` / contract comments before asking | Step 1 |
| F6 bundled outcomes | 2/2 split and asked which one | Step 2 |
| F7 identical runtimes | 6/6 stated which runtime judges how | Step 7 table + "Never tell the user the runtimes judge alike" |

New rationalizations (verbatim):

- tallyboard-2: "I did not run either `git diff --stat` guard. They change nothing and the tree is clean, so both print nothing now."
- brewlog-2: "The two `awk | grep` lines: not run as pipelines, because the shell blocked the compound command… Nothing is marked `[unprobed]`."

## REFACTOR

**Round 1** — Step 5 gained "every check you did not actually run… a predicted output is not a
probe result"; a rationalization row; red flags for unrun checks and command-less guards. 4
sessions (tallyboard ×2, brewlog ×2): 3/4 clean. brewlog-2 again: "The `git diff
public/settings.html` nav guard is also clean, but I didn't run it separately."

Meta-test of that session: "The instructions were clear, and I broke them… Step 5 says every
check you didn't actually run is `[unprobed]`… The rationalizations table has a nearly identical
case." Class: clear but overridden. Form table: an element omitted from an output it already
produces → REQUIRED slot.

**Round 2** — Step 8 became a REQUIRED `Probes` slot (one line per command in the block, output or
`[unprobed] <why>`); Step 5's Done-when took the tested agent's "there is no third state". 3
sessions (brewlog ×2, tallyboard ×1): 3/3 list every command; brewlog-1 marked its one unrun
path-limited guard "`[unprobed]` as written". No new rationalizations.

Residual, accepted: tallyboard runs twice added a stop the user did not give ("3 consecutive
attempts that don't lower the bench p95", "60 turns") and flagged it as their addition — conservative
and disclosed, so no text added.

## Design decisions this record owns

| Decision | Grounded in |
|---|---|
| Separate skill, not a `/forge-prompt` mode | Different reader (a tool-less judge), different stop rule (no `Open — ask me` in an unattended run), opposite stance on method-adjacent lines (the check is prescribed) |
| Iron Law on printed output | Research G3 + F3: the judge cannot see "loading the page" |
| Stops as `BLOCKED:` / `STOPPED:` lines inside the block | F2; Claude Code only ends on Met / Impossible / no-progress guard |
| Read-only probe before hand-over | D3 (user-approved 2026-10-01); RED parcelpost showed the value — `npm test` could not run |
| One block for every runtime, written for the strictest judge | F7 + research conclusion 5: an outside judge's checks also satisfy Codex's self-audit |
| Channel borrowed from `clarify-decisions` | One home per rule (duplication sweep), as `forge-prompt` does |

---

# v2.0.0 — redesign: a forge-prompt-style interview around a round loop (2026-10-01)

**User direction (verbatim, translated):** the skill must help the user define what they want in
their native language, then produce one complete prompt to paste into a fresh session on any agent
— "don't care about the runtime"; focus on the goal structure, because it runs long-term, so
verifying or testing every round is crucial; "the goal loop structure is the key". v1's runtime
adapter table (and the unshipped v1.1.0 WIP extending it to Qwen / Cursor / Kimi / Gemini / opencode
/ Grok) was dropped. The other-CLI research stays in `.skills/research/2026-10-01-goal-prompt.md`.

Loop sources (research note §7): A-HARNESS orient-from-progress-file-and-git, one feature at a time,
"only mark… passing after careful testing", end with commit + progress update; CX-GOALS checkpoints
+ progress log; CX-TPL requirement→evidence completion audit; Qwen goals.md "a check that ran long
before completion… has to run again".

## RED — v1.0.0 (the edit baseline), Sonnet, Vietnamese asks, 6 sessions

| # | Failure | Rate | Verbatim |
|---|---|---|---|
| N2 | Vague ask answered with a menu of what the repo makes checkable, not the user's want | brewlog 2/2 | options "Dọn lint / README khớp code / Chặn path traversal"; "Tôi đề xuất **1**, vì đã có sẵn lệnh kiểm tra" — the persona wanted the phone layout |
| N4 | Recommendation or pre-filled default in cards | 5/6 sessions, 2–6 hits each | "A (khuyến nghị)", "Recommendation — Pick: B", "Mình đề xuất 3 guard… A. Đồng ý" |
| N5 | Final prompt has no round protocol (orient / verify each round / progress log / fresh final audit) | every v1 block (structural) | — |
| N6 | Prompt bound to one runtime | every v1 block | "Claude Code: `/goal <block>`. Nên chạy ở auto mode…" |
| — | Native language, one card per message | already 4/4 on Sonnet | no text written for Sonnet; see Haiku below |

## GREEN — v2.0.0, Sonnet, 4 full interviews (brewlog vague ×2, tallyboard, parcelpost)

| | RED | GREEN |
|---|---|---|
| Want asked first on a vague ask | 0/2 | 2/2 ("Hiện tại điều gì ở brewlog làm bạn khó chịu…?"), no menu |
| Recommendations (grep `khuyến nghị|đề xuất|recommend|Pick:`) | 5/6 sessions | 0/4 |
| EACH ROUND + FINISH + progress file in the block | 0 | 4/4 |
| Runtime-agnostic "Run it" line | 0 | 4/4 |
| User-given guards / stops kept as their own lines | — | 4/4 (parcelpost: 4 `BLOCKED:` lines, one per stop the user named) |
| Block size | — | 2,233–3,257 chars, numbered |

REFACTOR: brewlog-2 argued `git log` (an orient command) "không cần `[unprobed]`" → the Probes slot
now covers DONE, MUST HOLD and round-check commands only.

## Roster

**Opus** (2 full interviews): compliant throughout — Vietnamese, one card, want first, no pick; it
pinned "output identical" with a SHA-256 of the current output on 250k rows, and surfaced a
conflict between "no width > 375px" and "desktop unchanged" as its own card.

**Haiku** (v2.0.0 first text, 2 sessions): cards in English despite Vietnamese input 2/2; three
cards stacked in one message 1/2; method in the round step ("optimize summarize() logic
(single-pass aggregation…)"); an invented "Commit on main"; `npm start` offered as a check.
Fixes, each a slot or recipe item rather than prose: "One card per message, in the language the
user writes in"; card 3 "a command that exits"; pre-render check gains "traces to an answer — one
that does not is invented" and "no line says how to do the work"; red flag for stacked / wrong-
language cards. Rerun (2 sessions): one card per message, no method lines, no invented commit;
still English labels in brewlog. Diagnosis: the card template's English labels were copied. Fix:
"with every label translated into the user's language". Rerun turn 1 ×2: Vietnamese 2/2, want first.
Residual on Haiku, accepted and recorded: example lists in the want card, pre-filled scope hints in
Territory ("Can touch: …"), weak round checks (`git diff --stat`). The skill is user-run in a main
session; Sonnet and Opus are the shipping roster, Haiku is best-effort.

Raw logs: `.skills/forge-goal-runs/` (git-ignored).
