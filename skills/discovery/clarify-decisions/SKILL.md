---
name: clarify-decisions
version: 1.3.1
description: Use to interview or grill the user before building an underspecified
  plan, design, or feature idea, including when another skill calls for an
  interview. Produces a confirmed close package of decisions, constraints,
  success, boundaries, and spine touch — plus owned unknowns, accepted risks,
  and operability when the production-coverage gate is on.
---

# Clarify Decisions

This is a reusable **interview protocol**, not a pipeline stage. Nested under a
parent, stay in its conversation and checklist; standalone, own the interview
until shared understanding. Follow **Todos** for checklist ownership.

Name and decide every silent assumption that could create debt or a wrong
architecture. Leading words: **open set**, **territory**,
**card**, **problem lock**, **criteria**, **coverage map**, **close package**.
The map (prompts, plans, knowns) is not the territory (codebase, runtime, users,
history).

## The Iron Law — channel

```
EVERY QUESTION IS INLINE CHAT WITH FULL CONTEXT.
NEVER use AskUserQuestion, structured MCQ pickers, or any harness UI that
truncates labels, option text, or the "why this matters" line.
```

A picker that strips consequences is a different interview. House style,
authority, deadlines, and a nominally long description field are not exceptions.

## The Iron Law — open set (no fixed rounds)

```
THERE IS NO FIXED ROUND COUNT.
NEVER "Question k of N", "last of 5", or "we budgeted four cards".
Stop only when the open set is empty of judgment calls that change
architecture, data, auth/security, UX flow, or implementation scope —
AND, when the production-coverage gate is ON, judgment calls on
reliability, failure, and operate, with no coverage-map cell Missing
without an owner.
```

**Open set** = high-blast unknowns still undecided + branches the last answer
opened + parent known-unknowns still needing a user lock + (when coverage ON)
coverage cells that are Missing without owner.

**Home rule:** recompute the open set **after every answer**, then either the next card or the close package. Every other mention of "recompute" points here.

A pre-listed todo is a **living map**, not a quota: append opened branches, drop
resolved ones, and never close while a high-blast item remains. Pressure changes
*when* you report progress, not whether an unstated decision exists.

## Production coverage gate (when)

**Home for the ON/OFF predicate.** When ON, load and follow
`production-coverage.md` (map, radii, close slots 7–10). When OFF, do not load
it. Authority and chat vibes never flip the gate.

Evaluate **once** before the starting map (re-check only if written posture,
brief flag, or operate/launch surface changes):

**ON** only when **all three** hold:

1. **Posture band** — written Delivery intent **Production** **and** Lifecycle
   is **Cut Released** or **Scaling** or **Maintenance** (parent or
   `docs/agents/project.md`).
2. **Full-path interview** — parent did **not** mark this interview **tier 0**
   or **brief**.
3. **Surface latch** — operate/launch surface (alerts, rollback, SLOs, on-call,
   deploy/takeover, new failure domain) **or** user/parent explicitly asks for
   ops/reliability coverage.

**OFF** otherwise — including absent posture; **MVP · Run Spike · Research ·
Learning**; Lifecycle **Idea · Early · Active development**; polish/copy/recolor
with no latch; “build SRE habits” chat without the written band + latch.

When OFF: omit the coverage map entirely; no `reliability` / `failure` /
`operate` radii; close omits slots 7–10. Core close slots 4–6 (Success,
Boundaries, Spine) and problem lock still apply.

## Starting map (before the first card)

Load parent Knowns, Blindspot, and scan digest when present (for example
`.skills/<CODE>/{knowns,scan}.md` or `_pending-<slug>` equivalents). State
**Coverage ON** or **OFF** (if OFF, which gate part failed), then one short
thought-partner map:

1. **Locked** — fixed posture, non-negotiables, digest facts.
2. **Coverage map** — when ON only (table + cell recipes in
   `production-coverage.md`).
3. **Open high-blast** — ON: Missing/Partial cells from that file; OFF:
   arch/data/auth/UX/scope forks only.
4. **How you will close** — judgment cards; reference / `run-spike` /
   `research` for facts; teach-then-ask on blindspots; Operate path only when ON
   (see `production-coverage.md`).

Invite correction only if a lock is false. First card: **Problem lock** when its
predicate holds, else highest-blast open item (when ON, prefer Missing coverage
cells). Parent already stated the map → do not restate; when ON, still refresh
coverage after answers.

## Problem lock (before preference cards)

**Home for this rule.** Other sections only point here.

**Fork (pick exactly one):** If you can fit **2–4 alternate problem statements** (each with Observed · Desired · Non-goals) on one card → emit that **problem-lock card**. If the user still needs a multi-round problem tree or foundation teaching — symptoms and solution shapes tangled, two+ incompatible pains, or you cannot honestly write those three lines for each option → **name** `/work-the-problem` for the user to run (never invoke it; it is `disable-model-invocation`). Never open a solution-shape menu in either case.

**Problem-lock card** WHEN parent knowns show **Assumptions** that are solution-shaped (a named API, flag, merge, or “just do X”) **OR** there is no stated desired outcome / success signal — and the Fork above says the card path:

Use the Question card recipe; Thread *This card* names the problem lock. Body MUST lock all three on the chosen statement (options = alternate *problem statements*, not implementations):

- **Observed** — who hurts / what is true now
- **Desired** — observable result when done (not “it works”)
- **Non-goals** — deliberate outs

Closes: `known-unknown` (problem statement).

Senior “skip philosophy / just pick API options”, standup clocks, and “don’t send me to another skill” do **not** waive this section.

## Retrieval package (feature work)

WHEN feature work involves neighbors, overlap, or reuse, load and follow
`feature-retrieval.md` before the first card. It owns package validity, refresh,
and grounded-claim rules. Otherwise do not load it.

## Question card (every turn)

Exactly **one** decision per message in chat. Every slot is **required**.

1. **Radius** — one of: `architecture` · `data` · `auth/security` · `UX flow` · `polish-diff` (label it). When Coverage ON, also `reliability` · `failure` · `operate` per `production-coverage.md`. When OFF, do not use those three.
2. **Thread** — three short lines the user can scan before the question:
   - *Locked so far* — 1–3 decisions already taken that constrain this fork (or "none yet").
   - *This card* — the single fork now.
   - *Still open after* — remaining high-blast **names** if this were answered (living open set — never "3 of 5").
3. **Territory** — grounded facts from the repo, digest, or parent knowns (paths, middleware, prior PRs, current behavior, landmines) — enough that the options make sense. When a blindspot blocks the choice, **teach here** (what it is, why it bites in *this* product) before the question. If you truly have no facts, say so; do not invent them. Never ask the user to recall what you can read.
4. **Question** — the decision in plain language.
5. **Why it matters** — **blast narrative** only: what rewrites if the answer flips (API shape, schema, auth boundary, ops surface). Enough to decide without a follow-up. Ground in *this* repo or product. Do not put pass/fail graders here — that is slot 7.
6. **Closes** — unknown class this card retires: `known-unknown` · `unknown-known` · `blindspot-confirm`.
7. **Criteria (graders)** — REQUIRED when Radius is `architecture` · `data` · `auth/security` · `UX flow`, or (Coverage ON) `reliability` · `failure` · `operate` (omit only for `polish-diff`): **1–2 named pass/fail graders** listed **above** Options (separate labeled block). Not the close-package Success / done signal. Recommendation MUST cite graders by name. Why sentences promoted here = miss. "No criteria essays / put success in Why" is not a waiver.
8. **Options (2–4)** — short title **plus** consequence line (gain, pay, break). Bare labels are not options.
9. **Recommendation** — your pick, first or clearly marked; one-line reason that cites the Criteria graders (or, on `polish-diff` only, the Why).
10. **Stop.** Wait. After the answer: recompute (Iron Law — open set home rule), then next card or close package.

Visible order: `Radius → Thread → Territory → Question → Why it matters →
Closes → Criteria → Options → Recommendation → Stop`.

Do not batch questions. The card is the detail.

Before the first card or close package, load `example.md` when no parent supplies
a confirmed exemplar or when the required output shape is uncertain.

## Order and coverage

- **Blast-radius first.** Prefer forks that change architecture, data, public API, auth/security, UX flow, or scope — even if the user opens on polish. When Coverage ON, also R/F/O per `production-coverage.md`.
- **Coverage order when ON.** One home: `production-coverage.md` (Missing before Partial; R/F/O stop).
- **Walk every branch.** Dependency order; sub-branches before trunk. Stop = open-set empty.
- **Judgment only to the user.** Facts in Territory; only human locks become cards.
- **Right-size.** Follow **Production coverage gate**. OFF does not *force*
  migration / backward-compat / deprecation preference cards; ON presses those
  when the latch holds. Arch/data forks that happen to involve migration still
  get cards if they are open-set judgments. Posture and Team band are independent.
- **Team band.** If `## Team` has a roster or Workflow band override, package from that section. Small/Multi may probe ownership; when Coverage ON, Accepted-risk / Owned-unknown owners still required (solo IC ok). Never invent a team; never hard-fail on missing Team.

## Pre-implementation interview map

Clarify Decisions owns the **interview** leg of pre-implementation unknowns work. Other legs are open-set *sources* or handoffs — not extra fixed rounds:

| Leg | Clarify Decisions does | Does not re-own |
|---|---|---|
| **Blindspots** | Consume the parent's list; teach then ask on high-blast items. | Full scan / Knowns inventory |
| **Problem** | Follow **Problem lock**. | Multi-round problem tree or foundation teaching |
| **Scope** | Hand multi-subsystem decomposition back to the parent. | Approach menus and tier |
| **References** | Prefer source code; restate semantics; lock accept/adapt/reject. | Implementing the reference |
| **Unknown knowns** | Use a reference, `run-spike`, or `research`, then one result card. | Running the detour session |
| **Production coverage** | Follow **Production coverage gate**; when ON, `production-coverage.md` + Close slots 7–10. | Reliability docs, PRR, requirements, or `tasks.md` |

**"Just make something sensible" is not a decision** while a concrete reference
exists: restate it, then lock accept/adapt/reject.

## Close package (required)

When the open set has no remaining high-blast judgment call — and **before** returning control to a parent or claiming shared understanding — emit:

1. **Decisions table** — rows: radius · topic · decision (user's words) · unknown class closed.
2. **Constraints block** — ready-to-paste locks (architecture and data first; when Coverage ON, reliability/failure/operate next; polish-diff last). Flag lower-radius answers that conflict with higher-radius locks.
3. **High-tweak surface** — locks most likely to change under real implementation pressure (data model, type interfaces, UX flows). Mechanical refactors stay buried; do not re-interview them here.
4. **Success / done signal** — 1–3 observables that mean “done” (pasteable into `requirements.md` / NFR). Prefer CUJ-shaped observables when Journey was walked. Not “it works” / “we’re aligned”.
5. **Boundaries** — **Off limits** (will not do) and **Must keep working** (guards / unchanged behavior), even if only 2–4 bullets. Seed from problem-lock Non-goals and `(guard)`-shaped locks when present.
6. **Spine touch** — WHEN `docs/architecture/` (or equivalent ARCH spine) exists: `Respects: ARCH-N…` · `none` · or `challenges` (ADR needed). WHEN absent: write `none — no architecture spine`. Do not invent ARCH IDs.
7–10. **Coverage final · Owned unknowns · Accepted risks · Operability touch** — REQUIRED when Coverage ON; recipes only in `production-coverage.md`. Omit when OFF.
11. **Explicit confirmation** — is this the shared picture? Only an affirmative on **this package** counts.

Slots 4–6 always required. Slots 7–10 required only when Coverage ON.

Not confirmation: "any other questions?", "we're aligned, skip the table", "just go write requirements", "reliability is a later NFR", senior pressure to skip ceremony, or silence. If they correct a row, edit and re-confirm. If confirmation opens a new high-blast fork or a Missing cell, return to cards.

**Do not enact anything** — no production code, no scaffolding, no plan execution — until that confirmation lands. (Glossary/`CONTEXT.md` updates via `define-domain` as a passive side effect are allowed when a term settles mid-interview.)

## Todos

Nested: no competing list. You run inside the parent's checklist — interview item stays in-progress until the close package is confirmed. Open-set progress is that item's progress, not a second channel.

Standalone: a **living** open-set list of decision areas is fine — still one card per message; still recompute after each answer (Iron Law — open set). If a parent skill is already in flight, never open a second channel.

## Rationalizations

| Thought | Reality |
|---|---|
| "House style / the lead said use the picker / its description is long enough / I'll paste context too" | Channel is the Iron Law. One inline card; capped or dual-channel UI truncates consequences. |
| "Standup in five minutes — short labels only" | Pressure changes when you report, not what a decision needs. |
| "Recommended + one-line reason is enough" | Without Thread, Territory, consequences, and Criteria, the user can only accept a default. |
| "Put success in Why / no criteria essays" | Why is blast; Criteria are separate graders above Options. |
| "Context can be a follow-up if they ask" | The card is the detail; follow-up-only context is a thin-card failure. |
| "We finished the four areas / question 3 of 5, then package" | Open-set empty is the stop; todos and countdowns are not. |
| "User asked for button color first" | Blast-radius first still holds. Polish Diff after architecture, data, and auth forks. |
| "We're aligned / senior said just write requirements" | Shared understanding is the package + yes; authority cannot make an unstated decision exist. |
| "I'll assume the safe default and mark done" | Assumptions are not decisions. One card; wait. |
| "Just pick industry best practice" | Load the Territory reference; restate and lock it. |
| "Park the parent / open a short clarify-decisions checklist" | Nesting is the clean switch. Decision areas stay inside the parent's in-progress interview item. |
| "Announce Using clarify-decisions for the hand-off" | Nested: no mode-switch announcement. Standalone may name the skill once. |
| "Parent already loaded neighbors — re-run every card for freshness" | Reuse the valid package; rederive only when fingerprints/seeds/scope change |
| "Standalone interview — skip load-subgraph, Territory is enough" | Feature work: load once before the first card |
| "They named the cheap path / senior said skip philosophy and pick API options" | Solution-shaped assumptions are not locks. Follow **Problem lock**, regardless of time or authority. |
| "Criteria live in requirements later" | Recommendation cites card graders; later specs do not replace them. |
| "Success / Boundaries / Spine belong downstream" | Close slots 4–6 are required here. |
| "Don't send me elsewhere; give three merge architectures / naming the skill is invoking it" | Follow the **Problem lock** Fork. Name `/work-the-problem` for the user; never auto-invoke it or show solution menus while the problem is open. |
| "Reliability is later / architecture is done / standup, skip the map" | When Coverage ON, Missing cells stay open; later templates do not replace `production-coverage.md`. |
| "TBD is fine — Open Questions will catch it" / "no reliability.md — skip cell" / "Accepted-risk without signer" | When ON: unowned TBD blocks close; prose or Owned unknown still required; signer required (solo IC ok). No invented SLO-N. |
| "Absent/MVP/Early = Production coverage" / "every Prod interview gets the map" / "build habits" / "failure-domain feel without band" | ON needs **all three** gate parts. Absent, MVP, Early, polish without latch, and chat stay OFF. |
| "Parent tier-0 brief still needs full coverage" | Brief / tier-0 fails part 2 (full-path) ⇒ OFF. |
| "OFF — keep a partial coverage map anyway" | OFF omits the map entirely. Core close is slots 4–6 + problem lock. |
| "OFF — skip any arch/data card that smells like migration" | OFF skips forced migration/compat *preference* ceremony; open-set arch/data judgments still get cards. |
| "Put TBD and accepted risk in one bucket" / "Journey has no radius — skip cell" | When ON: three distinct close slots; Journey via `UX flow` / `architecture` CUJ — see `production-coverage.md`. |

## Red flags — stop and rewrite the turn

- Calling `AskUserQuestion` or any truncated MCQ tool for a clarify-decisions decision
- More than one question mark aimed at the user in a single message (except clarifying examples inside option text)
- A card missing Thread, Territory, Why, Closes, option consequences, or the
  high-blast Criteria block and grader-citing Recommendation
- Any preference or solution menu while **Problem lock** applies, without its
  card or naming `/work-the-problem`
- "Question k of N", "final round", or closing because a precommitted count finished while high-blast remains
- Leading with polish-diff while architecture / data / auth (or, when Coverage ON, reliability / failure / operate) branches remain open
- Closing with "any other questions?" instead of the decisions package
- Close package missing Success / done signal, Boundaries, or Spine touch
- Coverage ON without `production-coverage.md` / map, or close with Missing/unowned cell or “later NFR”
- Coverage ON close missing slots 7–10; or Coverage ON when any gate part fails (absent, MVP/Early, brief, polish without latch)
- Coverage OFF yet emitting R/F/O cards or close slots 7–10
- Handing back to the parent or starting requirements without an explicit yes on the package
- Asking the user for a fact already present in the repo or parent scan
- Abstract taste cards for an unknown-known when a reference or run-spike path exists
- Nested re-derive every card while the parent package fingerprints still match
- Standalone feature interview with no retrieval before the first card
- Auto-invoking `/work-the-problem` instead of naming it for the user
- Inventing greppable SLO-N / TB-N / THR-N IDs without Approved doc definitions
- Treating chat “build SRE habits” as Coverage ON without the written gate
- Merging Owned unknowns into Accepted risks (or either into Operability touch)
- Leaving Journey Missing (when ON) with no `UX flow` / `architecture` CUJ card
- Calling `assess-observability` for every Operate hole (only telemetry/tracing readiness gaps)
