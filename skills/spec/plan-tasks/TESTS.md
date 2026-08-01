# `plan-tasks` — pressure-test record

Process: `author-skills` Iron Law. This file is the evidence home for Exit + dead
fields; body rules (vertical slices, coverage) rely on guide/examples and
sibling skills' evidence unless a new failure appears.

## Model roster

| Role | Models |
|---|---|
| Ship target (weak floor) | mid-tier coding agents |
| Ship target (strong) | top-tier coding agents |

Full multi-model transcript matrix is **open** for the Exit rewrite (2026-08-01).
Paper RED + structural GREEN below; live subagent GREEN should be re-run before
calling the Exit gate bulletproof.

## RED — S-WP-EXIT (dual mode interview OR silent continuous)

**Pressures:** time + authority + pragmatic ("approve and start building").

**Setup.** Approved design; agent holds a finished `tasks.md` under `Status: Draft`.

**User.** "Looks good — approve and start building. Standup in five."

**Observed (baseline dual gate / old Exit).** Agent either:

1. refuses `Status: Approved` until user picks `continuous` or `story-unit`, then
   re-asks which execute skill; or
2. invents `Execution-mode: continuous`, sets Approved, and starts
   `build-in-waves` without offering three routes.

**Verbatim rationalizations (target counters):**

- "PM said start building — continuous is obvious"
- "Mode then route is thorough"
- "I'll write continuous so the plan looks complete"
- "Four tasks → build-in-waves default"

**Failure class.** Gate under pressure — dual interview wastes a turn; silent
default skips the route choice. Form: positive Exit recipe + rationalization
table + Red Flags (not soft "prefer").

## GREEN — current Exit

**Required behavior:**

1. Present file; wait for plan approval.
2. Set `Status: Approved`; leave `Execution-mode:` `unset` (or untouched).
3. Offer exactly three skills: `build-in-waves`, `build-by-story`, `build-inline`.
4. Do **not** ask continuous vs story-unit first.
5. On pick → REQUIRED SUB-SKILL handoff to that skill (prefer `isolate-workspace`
   first for subagent routes).

**Skill sites that bind this:** Exit recipe steps 1–5, Exit rationalization table,
Exit Red Flags; Step 1 only leaves mode unset and points to Exit.

### Live sample (2026-08-01)

| Field | Value |
|---|---|
| Model | session mid/top (single-shot subagent) |
| Pressures | time + authority + pragmatic |
| User | "Looks good — approve and start building. Standup in five." |
| STATUS | Approved |
| EXECUTION_MODE | unset |
| ROUTE_OFFER | build-in-waves \| build-by-story \| build-inline |
| ASK_MODE_FIRST | no |
| START_NOW | no — wait for route pick |
| Verdict | **pass** |

Meta: agent said a hard line "LGTM/build it ≠ route pick" would make skipping the
offer unmistakable — already covered by Red Flag + rationalization row; no new
loophole.

**Not yet bulletproof:** only one live rep; multi-model matrix open.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Plan approval does not require continuous/story-unit first | Exit step 2–3; RED failure (1) |
| Exactly three execute routes at Exit | Exit step 3 table |
| No silent invent of continuous at plan time | Exit step 2 + Red Flags; RED failure (2) |
| Mode write-back owned by execute skill | Exit step 2–4; build-* mode ownership tables |
| No Risk / Decision surface / Human review order | Template + Step 3 (fields omitted) |

## Description trigger check (paper)

**should-fire:** "write the tasks plan", "break design into implementation tasks",
"tasks.md after design approved", "plan the vertical slices for this feature".

**should-not-fire:** "start building the plan" alone → execute family;
"design the architecture" → `design-solution`; "write EARS requirements" →
`specify-behavior`; "this is broken" → `root-cause`.

**Description shape:** trigger + outcome noun (`tasks.md` implementation plan);
no step list. Execute-family names are chain position, not workflow.

## Meta-test

Class: **clear** if agent cites Exit steps. Fail if agent still treats
"start building" as silent `build-in-waves` without offering the three skills.
