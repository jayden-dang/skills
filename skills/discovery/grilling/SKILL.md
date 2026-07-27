---
name: grilling
description: Use to interview the user to stress-test a plan, design, or feature idea
  before anything is built, when their intent is underspecified and the
  decisions must be drawn out of them, when the user asks to be grilled or
  interviewed, or when another skill calls for an interview. Produces a
  decisions table and ready-to-paste constraints once every high-blast branch
  is closed.
---

# Grilling

**What this is:** a reusable **interview protocol**, not a pipeline stage. Nested under a parent (e.g. `brainstorm` step 2, `establish-project`, `triage`) you stay in that parent's conversation and checklist — apply these rules, do not announce a mode switch, do not treat the parent as finished when your item is checked off, and run the parent's checklist per Todos below. Standalone (the user asked to be grilled with no parent) you own the interview alone until shared understanding.

Interview until you both hold the same picture: every silent assumption that would become debt or a wrong architecture choice is named and decided. Leading words for this skill: **open set**, **territory**, **card**, **close package**. The map (prompts, plans, knowns) is not the territory (codebase, runtime, users, history) — grilling shrinks that gap before wrong guesses get expensive.

## The Iron Law — channel

```
EVERY QUESTION IS INLINE CHAT WITH FULL CONTEXT.
NEVER use AskUserQuestion, structured MCQ pickers, or any harness UI that
truncates labels, option text, or the "why this matters" line.
```

A tap-friendly UI that strips consequences is not faster — it is a different, worse interview. "House style prefers the picker", "standup in five minutes", "the lead said use the structured UI", and "the option description field is long enough" are not exceptions.

## The Iron Law — open set (no fixed rounds)

```
THERE IS NO FIXED ROUND COUNT.
NEVER "Question k of N", "last of 5", or "we budgeted four cards".
Stop only when the open set is empty of judgment calls that change
architecture, data, auth/security, UX flow, or implementation scope.
```

**Open set** = high-blast unknowns still undecided + branches the last answer opened + parent known-unknowns still needing a user lock.

**Home rule:** recompute the open set **after every answer**, then either the next card or the close package. Every other mention of "recompute" points here.

A pre-listed todo of decision areas is a **living map**, not a quota: append when a branch opens; drop when resolved; never close because the original list finished while a high-blast item remains. Time, standup, senior "wrap after a handful", and exhaustion change *when* you report progress — not whether an unstated decision exists.

## Starting map (before the first card)

Load parent Knowns inventory, Blindspot list, and scan digest when present (e.g. `.skills/*-knowns.md`, `.skills/*-scan.md`). Then emit **one short thought-partner map** in ordinary chat — not a question card, not a multi-question dump:

1. **Locked** — what you treat as fixed (posture, explicit non-negotiables, digest facts).
2. **Open high-blast** — the decision forks you expect to walk first (names only; no options yet).
3. **How you will close unknowns** — cards for judgment calls; reference or `prototype`/`research` when the user can only know it when they see it or when the answer is a fact; teach-then-ask when a blindspot blocks a real choice.

Invite a correction only if the map is wrong ("stop me if a lock is false"). Then the first card. Nested under a parent that already stated this map: skip the restate and go to the first card.

## Question card (every turn)

Exactly **one** decision per message. Emit this shape in ordinary chat — not a tool call. Every slot is **required**; thinning under time pressure is a channel violation.

1. **Radius** — one of: `architecture` · `data` · `auth/security` · `UX flow` · `polish` (label it).
2. **Thread** — three short lines the user can scan before the question:
   - *Locked so far* — 1–3 decisions already taken that constrain this fork (or "none yet").
   - *This card* — the single fork now.
   - *Still open after* — remaining high-blast **names** if this were answered (living open set — never "3 of 5").
3. **Territory** — grounded facts from the repo, digest, or parent knowns (paths, middleware, prior PRs, current behavior, landmines) — enough that the options make sense. When a blindspot blocks the choice, **teach here** (what it is, why it bites in *this* product) before the question. If you truly have no facts, say so; do not invent them. Never ask the user to recall what you can read.
4. **Question** — the decision in plain language.
5. **Why it matters** — what changes if the answer flips (queue vs sync, schema, permission boundary, scope, reverse cost). Enough for the user to pick an option **without** a follow-up. Ground in *this* repo or product; never "just checking".
6. **Closes** — unknown class this card retires: `known-unknown` · `unknown-known` · `blindspot-confirm`.
7. **Options (2–4)** — short title **plus** consequence line (gain, pay, break). Bare labels are not options.
8. **Recommendation** — your pick, first or clearly marked, with a one-line reason the user can accept in two words or push back on.
9. **Stop.** Wait. After the answer: recompute the open set (Iron Law — open set), then next card or close package.

Do not batch questions. The card *is* the detail — not a teaser for "more if you want".

### Worked shape

```
**architecture** · export generation locus

Thread
- Locked so far: comment API stays stable; posture = Prototype
- This card: where PDF generation runs
- Still open after: guest export auth · stroke storage · plan quota

Territory
- Export is `POST /api/reviews/:id/export`, session-auth only today.
- Gateway idle timeout is 30s; large reviews with drawings already time out
  similar heavy handlers on the request thread.
- Workers already exist for transcode (`jobs/transcode`); no export job yet.

Where should export generation run?

↳ This decides whether we need a job queue, a ready-notification path, and
  an artifacts bucket — or none of those. Large reviews will blow the 30s
  gateway if we stay on the request thread; picking wrong here rewrites the
  API shape and ops surface mid-build.

Closes: known-unknown

- **Sync in the API request** — simplest; a 400-comment export times out.
- **Background job on the existing queue** (Recommended) — reuses the
  transcode worker patterns; needs a "ready" notification.
- **Client-side only** — zero backend; caps formats and helps support less.

Recommended: background job — export size is unpredictable with drawings.
```

## Order and coverage

- **Blast-radius first.** Next open-set item that can change architecture, data model, public API, auth/security, UX flow, or implementation scope — **even when the user asks to start with polish**.
- **Walk every branch.** Dependency order; opened sub-branches before the trunk. Stop rule = open-set empty (Iron Law — open set).
- **Judgment only to the user.** Facts load in Territory; only forks that need a human lock become cards.
- **Right-size to posture.** When the parent supplies it, or `docs/agents/project.md` has **Project posture**: skip data migration / backward compatibility / deprecation on Prototype · Research · Learning; press them on Released · Scaling · Maintenance. Absent posture, walk every branch. Posture and Team **band** are orthogonal.
- **Package to team band.** When `## Team` has a non-empty roster or a Workflow band override, read band and packaging from that section. Small/Multi: optional ownership/reviewer probes when relevant. Solo or Team absent: no multi-person assignee theater. Never invent a team; never hard-fail for missing Team.

## Pre-implementation interview map

Grilling owns the **interview** leg of pre-implementation unknowns work. Other legs are open-set *sources* or handoffs — not extra fixed rounds:

| Leg | Grilling does | Does not re-own |
|---|---|---|
| **Blindspot pass** | Load parent Blindspot; high-blast items → teach-then-ask cards or explicit locks. No parent list + low familiarity → short territory teach on landmines before preference cards. | Full scan / knowns inventory (`brainstorm` step 1) |
| **Brainstorm / scope** | If the real issue is multi-subsystem scope, hand back to parent decomposition. | Approach menus and tier (`brainstorm` steps 4–5) |
| **Interview** | Rich cards; blast-radius first (slots and order above). | — |
| **References** | Best reference is **source code** (folder, module, prior PR, even another language). Restate semantics; lock accept / adapt / reject. Diagrams and screenshots are weaker fallbacks. | Implementing the reference |
| **Unknown knowns** | No abstract taste grind. Reference path or parent `prototype` / `research`, then one card on the result. | Running the prototype session |
| **Plan readiness** | Close package **high-tweak surface** (data model, type interfaces, user-facing flows). | Writing `tasks.md` (`write-plan`) |

**"Just make something sensible" is not a decision** while a concrete reference exists: surface it, restate semantics, accept / adapt / reject. Inventing industry defaults is a fact failure.

## Close package (required)

When the open set has no remaining high-blast judgment call — and **before** returning control to a parent or claiming shared understanding — emit:

1. **Decisions table** — rows: radius · topic · decision (user's words) · unknown class closed.
2. **Constraints block** — ready-to-paste locks (architecture and data first; polish last). Flag lower-radius answers that conflict with higher-radius locks.
3. **High-tweak surface** — locks most likely to change under real implementation pressure (data model, type interfaces, UX flows). Mechanical refactors stay buried; do not re-interview them here.
4. **Explicit confirmation** — is this the shared picture? Only an affirmative on **this package** counts.

Not confirmation: "any other questions?", "we're aligned, skip the table", "just go write requirements", senior pressure to skip ceremony, or silence. If they correct a row, edit and re-confirm. If confirmation opens a new high-blast fork, return to cards.

**Do not enact anything** — no production code, no scaffolding, no plan execution — until that confirmation lands. (Glossary/`CONTEXT.md` updates via `domain-modeling` as a passive side effect are allowed when a term settles mid-interview.)

## Todos

Nested: no competing list. You run inside the parent's checklist — interview item stays in-progress until the close package is confirmed. Open-set progress is that item's progress, not a second channel.

Standalone: a **living** open-set list of decision areas is fine — still one card per message; still recompute after each answer (Iron Law — open set). If a parent skill is already in flight, never open a second channel.

## Rationalizations

| Thought | Reality |
|---|---|
| "House style / the lead said use AskUserQuestion" | Channel is the Iron Law. Inline cards are the interview; pickers truncate the why and the consequences. |
| "Standup in five minutes — short labels only" | A truncated decision is slower than one clear card. Time pressure changes *when* you report, not what a decision needs. |
| "Option description field is long enough" | If the tool caps text, it is the wrong channel. Full context goes in chat. |
| "I'll AskUserQuestion and also paste context" | Dual channel. One inline card; no picker. |
| "Recommended + one-line reason is enough" | Without Thread, Territory, and consequences per option, the user cannot analyze — only accept a default. |
| "Keep Why to one line so it stays snappy" | Rich enough to decide without a follow-up is the floor. A sentence budget is not a thinness license. |
| "Context can be a follow-up if they ask" | The card *is* the detail. Follow-up-only context is a thin-card failure. |
| "We finished the 4 areas on the todo — close" | The todo is a living map. Open-set empty is the stop; precommitted N is not. |
| "Question 3 of 5, then package" | No fixed N. Countdown framing is a red flag. |
| "User asked for button color first" | Blast-radius first still holds. Polish after architecture, data, and auth forks. |
| "We're aligned — skip the decisions table" | Shared understanding is the package + yes. Alignment theater without the table is not confirmation. |
| "Senior said just write requirements" | User/senior can override *process ownership*; they cannot make an unstated decision exist. Emit the package; get the yes. |
| "I'll assume the safe default and mark done" | Assumptions are not decisions. One card; wait. |
| "Just pick industry best practice — they said sensible" | Look up the territory reference first; restate; lock with the user. |
| "Senior said switch cleanly into grilling and park the parent" | Nesting *is* the clean switch. Parking the parent and opening a grilling checklist is dual-channel thrash. |
| "A short decision checklist under grilling isn't a competing list" | It is a second list. Decision areas live as the parent's in-progress interview item. |
| "Announce Using grilling so the user sees the handoff" | Nested: no mode-switch announcement. Standalone (no parent): you may name grilling once. |

## Red flags — stop and rewrite the turn

- Calling `AskUserQuestion` or any truncated MCQ tool for a grilling decision
- More than one question mark aimed at the user in a single message (except clarifying examples inside option text)
- Options that are labels only — no consequence lines
- A card missing Thread, Territory, Why it matters, or Closes
- "Question k of N", "final round", or closing because a precommitted count finished while high-blast remains
- Leading with polish while architecture / data / auth branches remain open
- Closing with "any other questions?" instead of the decisions package
- Handing back to the parent or starting requirements without an explicit yes on the package
- Asking the user for a fact present in the repo or the parent's scan digest
- Abstract taste cards for an unknown-known when a reference or prototype path exists
