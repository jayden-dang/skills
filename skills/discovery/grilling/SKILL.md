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

Interview the user until you both hold the same picture — every silent assumption that would otherwise become technical debt or a wrong architecture choice has been named and decided.

## The Iron Law — channel

```
EVERY QUESTION IS INLINE CHAT WITH FULL CONTEXT.
NEVER use AskUserQuestion, structured MCQ pickers, or any harness UI that
truncates labels, option text, or the "why this matters" line.
```

A tap-friendly UI that strips consequences is not faster — it is a different, worse interview. "House style prefers the picker", "standup in five minutes", "the lead said use the structured UI", and "the option description field is long enough" are not exceptions.

## Question card (every turn)

Exactly **one** decision per message. Emit this shape in ordinary chat — not a tool call:

1. **Radius** — one of: `architecture` · `data` · `auth/security` · `UX flow` · `polish` (label it).
2. **Question** — the decision in plain language.
3. **Why it matters** — one or two sentences: what changes in the system if the answer flips (queue vs sync, schema, permission boundary, scope). Ground it in *this* repo or product when you have territory facts; never leave it as "just checking".
4. **Options (2–4)** — each option is a short title **plus** a consequence line (what you gain, what you pay, what breaks). Bare labels without consequences are not options.
5. **Recommendation** — your pick, first or clearly marked, with a one-line reason the user can accept in two words or push back on.
6. **Stop.** Wait for the answer before the next card.

Do not batch questions. Do not put the real explanation in a follow-up "if you want more detail" — the card *is* the detail.

### Worked shape

```
**architecture** · Question 1

Where should export generation run?

↳ This decides whether we need a job queue, a ready-notification path, and
  an artifacts bucket — or none of those. Large reviews will blow a 30s
  gateway timeout if we stay on the request thread.

- **Sync in the API request** — simplest; a 400-comment export times out.
- **Background job on the existing queue** (Recommended) — reuses the
  transcode worker patterns; needs a "ready" notification.
- **Client-side only** — zero backend; caps formats and helps support less.

Recommended: background job — export size is unpredictable with drawings.
```

## Order and coverage

- **Blast-radius first.** Prefer the next question whose answer can change architecture, data model, public API, auth/security boundary, UX flow, or implementation scope over cosmetic or copy questions — **even when the user asks to start with polish**.
- **Walk every branch.** Decisions depend on each other; resolve in dependency order. An early answer opens some branches and closes others — walk the opened sub-branch before returning to the trunk. Done only when no unexplored branch remains.
- **Facts are yours; decisions are the user's.** Look up codebase and docs yourself — never ask the user to recall what you can read. Judgment calls go to the user, one card at a time.
- **Right-size to posture.** When the parent supplies it, or `docs/agents/project.md` has **Project posture**, prune branches that do not apply: skip data migration / backward compatibility / deprecation on Prototype · Research · Learning; press them on Released · Scaling · Maintenance. Absent posture, walk every branch. Posture and Team **band** are orthogonal.
- **Package to team band.** When `## Team` has a non-empty roster or a Workflow band override, read band and packaging from that section. Small/Multi: add optional ownership/reviewer probes when relevant. Solo or Team absent: no multi-person assignee theater. Never invent a team; never hard-fail for missing Team.

## Unknowns the interview must close

The map (prompts, plans) is not the territory (codebase, runtime, users, history). Grilling exists to shrink that gap before implementation makes wrong guesses expensive.

- **Load what the parent already found.** When a parent left a Knowns inventory, Blindspot list, or scan digest (e.g. `.skills/*-knowns.md`, `.skills/*-scan.md`), read them before the first card. Turn high-blast blindspots into decision cards or explicit locks the user confirms — do not re-ask trivia the digest already settled as fact.
- **Prefer territory-grounded forks.** Prefer questions where a wrong default creates real debt: dual-write traps, middleware bypass templates, flag-skew between environments, registration steps that compile but never surface, permission egress via share links, historical reverts that still apply. Generic product taste questions wait until the landmines are decided.
- **Unknown knowns → reference or prototype, not more adjectives.** When the user can only "know it when they see it," do not grind abstract preference cards. Offer a **reference path** (point at a folder, module, prior PR, or external component and lock to its semantics after you restate them) or hand off to the parent's `prototype` / `research` detour — then resume with one card on the resulting decision.
- **"Just make something sensible" is not a decision.** Inventing industry defaults while a concrete in-repo reference exists is a fact failure. Surface the reference; restate its semantics; ask the user to accept, adapt, or reject.

## Close package (required)

When no unexplored branch remains — and **before** returning control to a parent or claiming shared understanding — emit:

1. **Decisions table** — rows: radius · topic · decision (user's words).
2. **Constraints block** — a short ready-to-paste list the next stage can treat as fixed (architecture and data locks first; polish last). Flag any lower-radius answer that conflicts with a higher-radius lock.
3. **Explicit confirmation** — ask whether this is the shared picture. Only an affirmative on **this package** counts.

Not confirmation: "any other questions?", "we're aligned, skip the table", "just go write requirements", senior pressure to skip ceremony, or silence. If they correct a row, edit the package and re-confirm.

**Do not enact anything** — no production code, no scaffolding, no plan execution — until that confirmation lands. (Glossary/`CONTEXT.md` updates owned by `domain-modeling` as a passive side effect are allowed when a term settles mid-interview.)

## Todos

This skill does **not** own a todo list when nested. You are running *inside* the parent's checklist — keep that list live. The interview is one item on the parent's list; mark it in-progress while you grill and check it off only once the close package is confirmed. As branches resolve, that progress belongs to the parent's list, not a new one.

Invoked standalone: a short todo list of the decision areas you plan to walk is fine — still one card per message. If a parent skill is already in flight, never open a second channel.

## Rationalizations

| Thought | Reality |
|---|---|
| "House style / the lead said use AskUserQuestion" | Channel is the Iron Law. Inline cards are the interview; pickers truncate the why and the consequences. |
| "Standup in five minutes — short labels only" | A truncated decision is slower than one clear card. Time pressure changes *when* you report, not what a decision needs. |
| "Option description field is long enough" | If the tool caps text, it is the wrong channel. Full context goes in chat. |
| "I'll AskUserQuestion and also paste context" | Dual channel. One inline card; no picker. |
| "Recommended + one-line reason is enough" | Without consequences per option, the user cannot push back on merits — only accept a default. |
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
- A question with no "why it matters" grounded in system impact
- Leading with polish while architecture / data / auth branches remain open
- Closing with "any other questions?" instead of the decisions package
- Handing back to the parent or starting requirements without an explicit yes on the package
- Asking the user for a fact present in the repo or the parent's scan digest
