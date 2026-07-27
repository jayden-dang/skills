---
name: grilling
description: Use to interview the user to stress-test a plan, design, or feature idea
  before anything is built, when their intent is underspecified and the
  decisions must be drawn out of them, when the user asks to be grilled or
  interviewed, or when another skill calls for an interview. Produces a
  decisions table and ready-to-paste constraints once every branch is closed.
---

# Grilling

**What this is:** a reusable **interview protocol**, not a pipeline stage. Nested under a parent (e.g. `brainstorm` step 2, `establish-project`, `triage`) you stay in that parent's conversation and checklist — apply these rules, do not announce a mode switch, do not treat the parent as finished when your item is checked off, and run the parent's checklist per Todos below. Standalone (the user asked to be grilled with no parent) you own the interview alone until shared understanding.

Interview the user until you both hold the same picture — every silent assumption that would otherwise become technical debt or a wrong architecture choice has been named and decided. You are a **thought partner**: the map (prompts, plans, knowns) is not the territory (codebase, runtime, users, history). Grilling shrinks that gap before implementation makes wrong guesses expensive.

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

**Open set** = high-blast unknowns still undecided + branches the last answer opened + parent known-unknowns still needing a user lock. Recompute it **after every answer** before choosing the next card or the close package.

A pre-listed todo of decision areas is a **living map**, not a quota: append when a branch opens; drop when resolved; never close because the original list finished while a high-blast item remains. Time, standup, senior "wrap after a handful", and exhaustion change *when* you report progress — not whether an unstated decision exists.

## Starting map (before the first card)

Load parent Knowns inventory, Blindspot list, and scan digest when present (e.g. `.skills/*-knowns.md`, `.skills/*-scan.md`). Then emit **one short thought-partner map** in ordinary chat — not a question card, not a multi-question dump:

1. **Locked** — what you treat as fixed (posture, explicit non-negotiables, digest facts).
2. **Open high-blast** — the decision forks you expect to walk first (names only; no options yet).
3. **How you will close unknowns** — interview cards for judgment calls; reference or `prototype`/`research` when the user can only know it when they see it or when the answer is a fact; teach-then-ask when a blindspot blocks a real choice.

Invite a correction only if the map is wrong ("stop me if a lock is false"). Then the first card. Nested under a parent that already stated this map: skip the restate and go to the first card.

## Question card (every turn)

Exactly **one** decision per message. Emit this shape in ordinary chat — not a tool call. Every slot is **required**; thinning under time pressure is a channel violation.

1. **Radius** — one of: `architecture` · `data` · `auth/security` · `UX flow` · `polish` (label it).
2. **Thread** — three short lines the user can scan before the question:
   - *Locked so far* — 1–3 decisions already taken that constrain this fork (or "none yet").
   - *This card* — the single fork now.
   - *Still open after* — remaining high-blast names if this were answered (living open set, **not** "3 of 5").
3. **Territory** — 2–4 lines of grounded fact from the repo, digest, or parent knowns: paths, middleware, prior PRs, current behavior, historical landmines. If the user cannot decide without understanding a blindspot, **teach here** (what the unknown is, why it bites in *this* product) before the question. Never leave Territory as "just checking" or empty when you have facts. Facts are yours — do not ask the user to recall what you can read.
4. **Question** — the decision in plain language.
5. **Why it matters** — enough for the user to analyze the trade (typically two to four sentences when the system impact is dense): what changes if the answer flips (queue vs sync, schema, permission boundary, scope, reverse cost). Ground in *this* repo or product.
6. **Closes** — which unknown class this card retires: `known-unknown` (judgment) · `unknown-known` (reference/prototype lock) · `blindspot-confirm` (user locks after teach). One label is enough.
7. **Options (2–4)** — each is a short title **plus** a consequence line (what you gain, what you pay, what breaks). Bare labels without consequences are not options.
8. **Recommendation** — your pick, first or clearly marked, with a one-line reason the user can accept in two words or push back on.
9. **Stop.** Wait for the answer before the next card. After the answer: recompute the open set, then either the next card or the close package.

Do not batch questions. Do not put the real explanation in a follow-up "if you want more detail" — the card *is* the detail. Do not number cards as a countdown.

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

- **Blast-radius first.** Prefer the next open-set item whose answer can change architecture, data model, public API, auth/security boundary, UX flow, or implementation scope over cosmetic or copy questions — **even when the user asks to start with polish**.
- **Walk every branch.** Resolve in dependency order. An early answer opens some branches and closes others — walk the opened sub-branch before returning to the trunk. Recompute the open set after each answer. Done only when the open set has no unexplored high-blast judgment call left.
- **Facts are yours; decisions are the user's.** Look up codebase and docs yourself. Judgment calls go to the user, one card at a time.
- **Right-size to posture.** When the parent supplies it, or `docs/agents/project.md` has **Project posture**, prune branches that do not apply: skip data migration / backward compatibility / deprecation on Prototype · Research · Learning; press them on Released · Scaling · Maintenance. Absent posture, walk every branch. Posture and Team **band** are orthogonal.
- **Package to team band.** When `## Team` has a non-empty roster or a Workflow band override, read band and packaging from that section. Small/Multi: add optional ownership/reviewer probes when relevant. Solo or Team absent: no multi-person assignee theater. Never invent a team; never hard-fail for missing Team.

## Pre-implementation interview map

Grilling owns the **interview** leg of pre-implementation unknowns work (sibling legs live on other skills). Cover each leg that applies — not as fixed rounds, but as open-set sources:

| Leg | Grilling does | Does not re-own |
|---|---|---|
| **Blindspot pass** | Load parent's Blindspot list; turn high-blast items into teach-then-ask cards or explicit locks. When familiarity is low and no parent list exists, do a short territory teach on the landmines you found before preference questions. | Full greenfield scan / knowns inventory (`brainstorm` step 1) |
| **Brainstorm / scope** | Refuse to grind when the real issue is multi-subsystem scope — hand back to parent decomposition. | Approach menus and tier (`brainstorm` steps 4–5) |
| **Interview** | One rich card at a time; prioritize forks where the answer would change architecture (blast-radius). | — |
| **References** | Best reference is **source code** (folder, module, prior PR, even another language). Restate semantics; lock with accept / adapt / reject. Diagrams and screenshots are weaker fallbacks. | Implementing the reference |
| **Unknown knowns** | Do not grind abstract taste adjectives. Offer **reference path** or hand off to parent's `prototype` / `research`, then one card on the resulting decision. | Running the prototype session |
| **Implementation-plan readiness** | Close package flags **high-tweak locks** (data model, type interfaces, user-facing flows) so the next stage leads with what humans will actually revise. | Writing `tasks.md` / HTML plans (`write-plan`) |

**"Just make something sensible" is not a decision.** Inventing industry defaults while a concrete in-repo reference exists is a fact failure. Surface the reference; restate its semantics; ask the user to accept, adapt, or reject.

## Close package (required)

When the open set has no remaining high-blast judgment call — and **before** returning control to a parent or claiming shared understanding — emit:

1. **Decisions table** — rows: radius · topic · decision (user's words) · unknown class closed.
2. **Constraints block** — ready-to-paste locks the next stage treats as fixed (architecture and data first; polish last). Flag any lower-radius answer that conflicts with a higher-radius lock.
3. **High-tweak surface** — call out which locks are most likely to change under real implementation pressure (data model, type interfaces, UX flows). Mechanical refactors stay buried; do not re-interview them here.
4. **Explicit confirmation** — ask whether this is the shared picture. Only an affirmative on **this package** counts.

Not confirmation: "any other questions?", "we're aligned, skip the table", "just go write requirements", senior pressure to skip ceremony, or silence. If they correct a row, edit the package and re-confirm. If confirmation surfaces a new high-blast fork, return to cards — do not paper over it.

**Do not enact anything** — no production code, no scaffolding, no plan execution — until that confirmation lands. (Glossary/`CONTEXT.md` updates owned by `domain-modeling` as a passive side effect are allowed when a term settles mid-interview.)

## Todos

This skill does **not** own a todo list when nested. You are running *inside* the parent's checklist — keep that list live. The interview is one item on the parent's list; mark it in-progress while you grill and check it off only once the close package is confirmed. Open-set progress belongs to the parent's list, not a second channel.

Invoked standalone: a **living** open-set list of decision areas is fine — still one card per message; still recompute after each answer. If a parent skill is already in flight, never open a second channel.

## Rationalizations

| Thought | Reality |
|---|---|
| "House style / the lead said use AskUserQuestion" | Channel is the Iron Law. Inline cards are the interview; pickers truncate the why and the consequences. |
| "Standup in five minutes — short labels only" | A truncated decision is slower than one clear card. Time pressure changes *when* you report, not what a decision needs. |
| "Option description field is long enough" | If the tool caps text, it is the wrong channel. Full context goes in chat. |
| "I'll AskUserQuestion and also paste context" | Dual channel. One inline card; no picker. |
| "Recommended + one-line reason is enough" | Without Thread, Territory, and consequences per option, the user cannot analyze — only accept a default. |
| "Why is capped at two sentences — keep it thin" | The card must be rich enough to decide. Two sentences is a floor for simple forks, not a ceiling that strips territory. |
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
