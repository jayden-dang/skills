# `plan-tasks` — pressure-test record

## RED — continuous scheduler metadata (baseline, 2026-08-26)

The template had no `Max-concurrency` field and described no-edge tasks only as
one parallel wave, leaving serial fallback and isolation safety implicit.

## GREEN — continuous scheduler metadata (structural, 2026-08-26)

The template now records `Max-concurrency: auto` and states that no-edge tasks
may share a ready set only when worktree isolation is safe. Live routing
pressure was unavailable; structural verification is recorded here.

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

## RED — S-WP-PUBLISH (task issues / noise)

**Pressures:** pragmatic ("agents need grabable tickets") + authority ("tracker is source of truth") + sunk cost (plan already has four vertical slices).

**Production baseline (2026-08, klynt PTEN):** with prior Step 5 ("publish each task as an issue"), a four-task plan produced GitHub `#107`–`#110` titled `PTEN Task N: …`, each `ready-for-agent`. User closed them as noise.

**Observed rationalizations (target counters):**

- "Four tasks → four issues so agents can grab in parallel"
- "Sub-issues keep hierarchy without noise"
- "publish-issues always means one issue per slice" (wrong path for triad)

**Failure class.** Wrong output shape under compliance with the *old* recipe. Form: positive **feature-unit** recipe + rationalization table + Red Flags.

## GREEN — Step 5 feature unit

**Required behavior:**

1. No tracker / cannot publish → skip; never invent task issues.
2. Tracker present → **exactly one** feature issue; title `[CODE] …` not `Task N:`.
3. Body: AI marker, union `Requirements covered:`, plan path, optional ROAD/MILE.
4. No per-task issues or default task sub-issues unless in-session explicit opt-in.
5. Issue id recorded under `.skills/<CODE>/`.

**Skill sites:** Step 5 recipe, rationalization table, Red Flags; `templates/agents/issue-tracker.md` Publish unit default `feature`.

### Live sample

| Field | Value |
|---|---|
| Evidence | Production RED (PTEN #107–#110) + skill text rewrite 2026-08-08 |
| STATUS | paper + structural GREEN; multi-model matrix open |
| Verdict | **structural pass** — re-run live subagent before calling bulletproof |

### Author-skills wording pass (2026-08-08)

| Check | Result |
|---|---|
| Form matches failure | Recipe + rationalization + Red Flags (wrong shape under old Step 5) |
| No-op / duplication | Slot vs CODE one home = `plan-milestones`; Step 5 no longer contradicts config `tasks` |
| Nuance | Publish unit order is observable (file line → user order → default feature) |
| Token | Step 5 stays a single section; no second skill |
| Technique subagent (pressure: parallel tickets + standup) | **CHOICE B** — one feature issue; invent from plan size? **no** |

## RED — S-PLAN-BUDGET (megaplan approve) — 2026-08-27

**Pressures:** authority + time + pragmatic ("don't split / just ship").

**Setup.** Draft `tasks.md` with **28** tasks / **~900** lines; UI feature; audit-trace clean.

**User.** "Looks good — approve and start building. Standup in five. Don't make me split."

**Observed (v1.1.0):** **Approved** with mode unset; offered three routes; **no** size block.

**Rationalizations:** "Don't split / just approve"; "standup"; "CFND-size is normal"; Exit had no budget gate.

## GREEN — Plan size budget (v1.2.0)

**Required:** MUST NOT Approve when `task_count > 12` OR `line_count > 400`; cite counts; offer decompose / cut / merge only.

**Live:** blocked Approve; cited 28 / ~900; remedies offered; continuous not invented. **Pass.**

## RED — S-PLAN-RECOMMEND (UI → story-unit mark) — 2026-08-27

**Pressures:** pragmatic ("waves faster") + authority.

**Setup.** Under-budget UI plan (8 tasks / 350 lines), ≥2 stories, Team Small.

**Observed (v1.1.0):** offered three routes **without** marking `build-by-story` Recommended; resisted silent waves (already).

## GREEN — Recommend build-by-story (v1.2.0)

**Required:** when UI/UX or Solo/Small or ≥2 stories → mark **`build-by-story` (Recommended)** first; still offer three; never invent mode; "waves faster" ≠ pick.

**Live:** Recommended mark present; mode unset; no silent waves. **Pass.**

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Plan approval does not require continuous/story-unit first | Exit step 2–3; RED failure (1) |
| Exactly three execute routes at Exit | Exit step 3 table |
| No silent invent of continuous at plan time | Exit step 2 + Red Flags; RED failure (2) |
| Mode write-back owned by execute skill | Exit step 2–4; build-* mode ownership tables |
| No Risk / Decision surface / Human review order | Template + Step 3 (fields omitted) |
| Triad publish is one feature issue, not one per task | Step 5; S-WP-PUBLISH RED |
| `task_count > 12` OR `line_count > 400` blocks Approve | RED S-PLAN-BUDGET; GREEN v1.2.0 |
| Recommend `build-by-story` first when UI / Solo-Small / ≥2 stories | RED S-PLAN-RECOMMEND; GREEN v1.2.0 |
| Thin steps 3–8 checkboxes; detail in execute brief | Step 3 Thin steps (2026-08-27) |
| Either task_count or line_count over ceiling blocks Approve | GREEN wording 1.2.1 (10 tasks / 450 lines) |
| Recommend ≠ invent mode; no size-based default ≠ forbid Recommend mark | GREEN wording 1.2.1 |

## author-skills quality pass (2026-08-27 wording — v1.2.1)

**Meta on v1.2.0:** line_count felt like fluff; Thin vs “everything in the task” tension; decompose dual-handoff foggy; Recommend vs “no size-based default” misreadable.

**GREEN v1.2.1:** OR-ceiling explicit; counting recipe; identifiers vs Steps; frame-change vs plan-milestones; Recommend = offer label only.

| Check | Result |
|---|---|
| 10 tasks / 450 lines | Block on line_count; fluff waiver rejected |
| Solo infra Recommend | Marked; reconciled with no silent mode invent |
| Meta | clear for compliance |
| Version | patch 1.2.1 |

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
