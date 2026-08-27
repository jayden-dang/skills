---
name: clarify-decisions
version: 1.2.1
description: Use to interview the user to stress-test a plan, design, or feature idea
  before anything is built, when their intent is underspecified and the
  decisions must be drawn out of them, when the user asks to be grilled or
  interviewed, or when another skill calls for an interview. Produces a
  confirmed close package — decisions, constraints, success, boundaries, spine
  touch, owned unknowns, and accepted risks — once every high-blast branch and
  Production SRE coverage cell is closed or owned.
---

# Clarify Decisions

**What this is:** a reusable **interview protocol**, not a pipeline stage. Nested under a parent (e.g. `frame-change` step 2, `define-project`, `triage`) you stay in that parent's conversation and checklist — apply these rules, do not announce a mode switch, do not treat the parent as finished when your item is checked off, and run the parent's checklist per Todos below. Standalone (the user asked to be grilled with no parent) you own the interview alone until shared understanding.

Interview until you both hold the same picture: every silent assumption that would become debt or a wrong architecture choice is named and decided. Leading words for this skill: **open set**, **territory**, **card**, **problem lock**, **criteria**, **coverage map**, **close package**. The map (prompts, plans, knowns) is not the territory (codebase, runtime, users, history) — clarify-decisions shrinks that gap before wrong guesses get expensive.

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
architecture, data, auth/security, UX flow, reliability, failure,
operate, or implementation scope — AND, when Production SRE coverage
is on, no coverage-map cell remains Missing without an owner.
```

**Open set** = high-blast unknowns still undecided + branches the last answer opened + parent known-unknowns still needing a user lock + (when SRE-on) coverage cells that are Missing without owner.

**Home rule:** recompute the open set **after every answer**, then either the next card or the close package. Every other mention of "recompute" points here.

A pre-listed todo of decision areas is a **living map**, not a quota: append when a branch opens; drop when resolved; never close because the original list finished while a high-blast item remains. Time, standup, senior "wrap after a handful", "reliability is a later NFR template", and exhaustion change *when* you report progress — not whether an unstated decision exists.

## Production SRE coverage (when)

**SRE-on** WHEN Project posture (parent or `docs/agents/project.md`) is **Production · Scaling · Maintenance · Cut Released**, **OR** posture is **absent / unspecified** (treat as Production — do not assume spike).

**SRE-off** WHEN posture is **explicitly written** as **Run Spike · Research · Learning** — skip the coverage map and the `reliability` / `failure` / `operate` radii; Frame · Contract · Boundaries still apply.

Chat vibes (“learning spike”, “just exploring”) **do not** set SRE-off when the posture field is absent or still Production. Only the written posture band does.

SRE-on applies to **every** feature interview under that band — not only when `docs/ops/reliability.md` exists, not only launch/takeover. Missing reliability docs ⇒ lock prose targets or Owned unknowns; never invent SLO IDs.

## Starting map (before the first card)

Load parent Knowns inventory, Blindspot list, and scan digest when present (e.g. `.skills/<CODE>/knowns.md / `_pending-<slug>/knowns.md``, `.skills/<CODE>/scan.md / `_pending-<slug>/scan.md``). State SRE-on or SRE-off (Production SRE coverage). Then emit **one short thought-partner map** in ordinary chat — not a question card, not a multi-question dump:

1. **Locked** — what you treat as fixed (posture, explicit non-negotiables, digest facts).
2. **Coverage map** — REQUIRED when SRE-on (omit the table when SRE-off). Cells and status only — not prose essays:

| Cell | Status |
|---|---|
| Frame | Clear · Partial · Missing · Accepted-risk (*owner*) |
| Journey | … |
| Contract | … |
| Reliability | … |
| Failure | … |
| Operate | … |
| Freeze | … |

   **Cell meanings + how they close (one home):**
   - **Frame** — problem lock (Problem lock section).
   - **Journey** — CUJ path + breakpoints + measured vs unmeasured. **No Journey radius:** close via `UX flow` (user-facing CUJ) or `architecture` (system-path CUJ) cards, then set Journey Clear/Partial.
   - **Contract** — API/state/idempotency/authz via `data` / `auth/security` / `architecture` cards.
   - **Reliability** — SLI measure point + SLO-shaped target + error-budget *policy* (burn thresholds). Cite `SLO-N` only from Approved docs; else prose or Owned unknown. Radius: `reliability`.
   - **Failure** — SPOF/deps/partition/overload/operator-error; accept vs mitigate. Radius: `failure`.
   - **Operate** — pageable alert action, rollback, residual toil. Radius: `operate`. IF the gap is specifically telemetry/tracing readiness → REQUIRED SUB-SKILL: use `assess-observability`, **then** one `operate` card on the finding. Rollback/page/toil alone → `operate` card only (no assess).
   - **Freeze** — **not a card radius.** Becomes Clear only when Owned unknowns + Accepted risks are ready to list at close (each may be `none`).
3. **Open high-blast** — names derived from Missing/Partial cells (same ledger as the coverage map — do not keep a second invented list). Reliability · Failure · Operate are high-blast — never “later NFR”.
4. **How you will close unknowns** — cards for judgment calls; reference or `run-spike`/`research` when see-it facts; teach-then-ask on blindspots; Operate telemetry gap → `assess-observability` then Operate card (cell meanings above).

Invite a correction only if the map is wrong ("stop me if a lock is false"). First card next — WHEN the **Problem lock** predicate holds, that card is first; else highest-blast Missing cell. Nested under a parent that already stated this map: skip the restate; still honor Problem lock and refresh coverage statuses after answers.

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

When this interview is about **feature** work (neighbors, overlap, reuse), hold a
`load-subgraph` **retrieval package** (envelope + seeds + fingerprints +
schema/recipe) for Territory and grounded claims:

| Mode | Rule |
|---|---|
| **Nested** under a parent that already produced a package | **Reuse** that package if it remains valid (same seeds, source fingerprints sha256+present, schema/recipe). If invalid or missing → **rederive** via REQUIRED SUB-SKILL: use `load-subgraph`. |
| **Standalone** (no parent package) | Load retrieval **once** before the first interview card (REQUIRED SUB-SKILL: use `load-subgraph` with terms/paths/CODE seeds). |
| **In progress** | If any derivation source input changes, or material **scope / terms / paths** change, or fingerprints **differ** → **rederive**. Do not re-run every card when the package is still valid. |

No on-disk session cache. **Grounded claims** (one home): follow
`skills/execution/load-subgraph/references/grounded-claims.md` for every conclusion
from the package.

## Question card (every turn)

Exactly **one** decision per message. Emit this shape in ordinary chat — not a tool call. Every slot is **required**; thinning under time pressure is a channel violation.

1. **Radius** — one of: `architecture` · `data` · `auth/security` · `UX flow` · `reliability` · `failure` · `operate` · `polish-diff` (label it). When SRE-off, do not use `reliability` / `failure` / `operate`.
2. **Thread** — three short lines the user can scan before the question:
   - *Locked so far* — 1–3 decisions already taken that constrain this fork (or "none yet").
   - *This card* — the single fork now.
   - *Still open after* — remaining high-blast **names** if this were answered (living open set — never "3 of 5").
3. **Territory** — grounded facts from the repo, digest, or parent knowns (paths, middleware, prior PRs, current behavior, landmines) — enough that the options make sense. When a blindspot blocks the choice, **teach here** (what it is, why it bites in *this* product) before the question. If you truly have no facts, say so; do not invent them. Never ask the user to recall what you can read.
4. **Question** — the decision in plain language.
5. **Why it matters** — **blast narrative** only: what rewrites if the answer flips (API shape, schema, auth boundary, ops surface). Enough to decide without a follow-up. Ground in *this* repo or product. Do not put pass/fail graders here — that is slot 7.
6. **Closes** — unknown class this card retires: `known-unknown` · `unknown-known` · `blindspot-confirm`.
7. **Criteria (graders)** — REQUIRED when Radius is `architecture` · `data` · `auth/security` · `UX flow` · `reliability` · `failure` · `operate` (omit only for `polish-diff`): **1–2 named pass/fail graders** listed **above** Options (separate labeled block). Not the close-package Success / done signal. Recommendation MUST cite graders by name. Why sentences promoted here = miss. "No criteria essays / put success in Why" is not a waiver.
8. **Options (2–4)** — short title **plus** consequence line (gain, pay, break). Bare labels are not options.
9. **Recommendation** — your pick, first or clearly marked; one-line reason that cites the Criteria graders (or, on `polish-diff` only, the Why).
10. **Stop.** Wait. After the answer: recompute (Iron Law — open set home rule), then next card or close package.

Do not batch questions. The card *is* the detail — not a teaser for "more if you want".

### Worked shape

```
**architecture** · export generation locus

Thread
- Locked so far: comment API stays stable; posture = Run Spike
- This card: where PDF generation runs
- Still open after: guest export auth · stroke storage · plan quota

Territory
- Export is `POST /api/reviews/:id/export`, session-auth only today.
- Gateway idle timeout is 30s; large reviews with drawings already time out
  similar heavy handlers on the request thread.
- Workers already exist for transcode (`jobs/transcode`); no export job yet.

Where should export generation run?

↳ Why = blast: wrong pick rewrites API shape and ops mid-build (queue vs
  sync vs client-only; 30s gateway on the request thread).

Closes: known-unknown

Criteria (graders)   ← not Why; not close-package Success
- A 400-comment export with drawings completes without the gateway 30s kill
- Ops surface stays within an existing worker pattern when size is unpredictable

- **Sync in the API request** — simplest; a 400-comment export times out.
- **Background job on the existing queue** (Recommended) — reuses the
  transcode worker patterns; needs a "ready" notification.
- **Client-side only** — zero backend; caps formats and helps support less.

Recommended: background job — meets both graders; sync fails the timeout
grader; client-only fails format coverage.
```

## Order and coverage

- **Blast-radius first.** Next open-set item that can change architecture, data model, public API, auth/security, UX flow, reliability, failure, operate, or implementation scope — **even when the user asks to start with polish** or “skip SRE / later NFR”.
- **Coverage drives order when SRE-on.** Prefer cards that close Missing cells over Partial; never close the interview while Reliability · Failure · Operate are Missing without owner.
- **Walk every branch.** Dependency order; opened sub-branches before the trunk. Stop rule = open-set empty (Iron Law — open set).
- **Judgment only to the user.** Facts load in Territory; only forks that need a human lock become cards.
- **Right-size to posture.** Run Spike · Research · Learning → SRE-off (see Production SRE coverage) and skip migration / backward-compat / deprecation grills. Production · Scaling · Maintenance · Cut Released → SRE-on; press migration/compat **and** reliability/failure/operate. Absent posture → SRE-on. Posture and Team **band** are orthogonal.
- **Package to team band.** When `## Team` has a non-empty roster or a Workflow band override, read band and packaging from that section. Small/Multi: optional ownership/reviewer probes when relevant; Accepted-risk and Owned-unknown **owner** fields still required when SRE-on (owner may be the solo IC). Solo or Team absent: no multi-person assignee theater. Never invent a team; never hard-fail for missing Team.

## Pre-implementation interview map

Clarify Decisions owns the **interview** leg of pre-implementation unknowns work. Other legs are open-set *sources* or handoffs — not extra fixed rounds:

| Leg | Clarify Decisions does | Does not re-own |
|---|---|---|
| **Blindspot pass** | Load parent Blindspot; high-blast items → teach-then-ask cards or explicit locks. No parent list + low familiarity → short territory teach-pack on landmines before preference cards. | Full scan / knowns inventory (`frame-change` step 1) |
| **Problem lock** | Follow **Problem lock** section above (one home). | Multi-round problem tree + foundation teaching (`/work-the-problem`) |
| **Frame Change / scope** | If the real issue is multi-subsystem scope, hand back to parent decomposition. | Approach menus and tier (`frame-change` steps 4–5) |
| **Interview** | Rich cards; blast-radius first (slots and order above). | — |
| **References** | Best reference is **source code** (folder, module, prior PR, even another language). Restate semantics; lock accept / adapt / reject. Diagrams and screenshots are weaker fallbacks. | Implementing the reference |
| **Unknown knowns** | No abstract taste grind. Reference path or parent `run-spike` / `research`, then one card on the result. | Running the run-spike session |
| **SRE coverage** | Follow **Production SRE coverage** + Starting map coverage cells (one home). | Authoring standing reliability docs or a full PRR packet |
| **Plan readiness** | Follow **Close package** (one home). | Writing `tasks.md` (`plan-tasks`) |

**"Just make something sensible" is not a decision** while a concrete reference exists: surface it, restate semantics, accept / adapt / reject. Inventing industry defaults is a fact failure.

## Close package (required)

When the open set has no remaining high-blast judgment call — and **before** returning control to a parent or claiming shared understanding — emit:

1. **Decisions table** — rows: radius · topic · decision (user's words) · unknown class closed.
2. **Constraints block** — ready-to-paste locks (architecture and data first; reliability/failure/operate next; polish-diff last). Flag lower-radius answers that conflict with higher-radius locks.
3. **High-tweak surface** — locks most likely to change under real implementation pressure (data model, type interfaces, UX flows). Mechanical refactors stay buried; do not re-interview them here.
4. **Success / done signal** — 1–3 observables that mean “done” (pasteable into `requirements.md` / NFR). Prefer CUJ-shaped observables when Journey was walked. Not “it works” / “we’re aligned”.
5. **Boundaries** — **Off limits** (will not do) and **Must keep working** (guards / unchanged behavior), even if only 2–4 bullets. Seed from problem-lock Non-goals and `(guard)`-shaped locks when present.
6. **Spine touch** — WHEN `docs/architecture/` (or equivalent ARCH spine) exists: `Respects: ARCH-N…` · `none` · or `challenges` (ADR needed). WHEN absent: write `none — no architecture spine`. Do not invent ARCH IDs.
7. **Coverage final** — REQUIRED when SRE-on: final status per cell (no Missing without owner). Omit when SRE-off.
8. **Owned unknowns** — REQUIRED when SRE-on: every *undecided* TBD as topic · **owner** · **date** · **forbid-guess** (`cấm đoán`: AI/dev must not invent the answer). If none: `none`. Unowned TBD ⇒ open set not empty — do not emit close. **Not** the same as Accepted risks.
9. **Accepted risks** — REQUIRED when SRE-on: each *decided keep-the-risk* row · why tolerable vs CUJ/SLO · **signer**. If none: `none`. A deferred number/policy is an Owned unknown, not an Accepted risk.
10. **Operability touch** — REQUIRED when SRE-on: **rollback** (one command / flag / restore) + **who is paged** for the top failure. May cite one Owned unknown only to defer *that ops line* — not to swallow the whole Operate cell. Omit when SRE-off.
11. **Explicit confirmation** — is this the shared picture? Only an affirmative on **this package** counts.

Slots 4–6 always required. Slots 7–10 required when SRE-on — not “later NFR template” ceremony.

### Worked close shape (SRE-on excerpt)

```
Success / done signal
- Creators open drafts from Finder without publishing
- Learner entitled∩published reads unchanged for real learners

Boundaries
- Off limits: widen learner route; menu grants as authz
- Must keep working: ARCH-3 learner projection; server reauth on mutations

Spine touch
- Respects: ARCH-3

Coverage final
- Frame Clear · Journey Clear · Contract Clear · Reliability Clear
- Failure Accepted-risk (IC) · Operate Clear · Freeze Clear

Owned unknowns
- none

Accepted risks
- Single-AZ Redis cache miss → elevated latency within SLO burn; signer: IC

Operability touch
- Rollback: revert catalog route feature flag
- Page: on-call for 5xx catalog burn > threshold (playbook stub in constraints)
```

Not confirmation: "any other questions?", "we're aligned, skip the table", "just go write requirements", "reliability is a later NFR", senior pressure to skip ceremony, or silence. If they correct a row, edit and re-confirm. If confirmation opens a new high-blast fork or a Missing cell, return to cards.

**Do not enact anything** — no production code, no scaffolding, no plan execution — until that confirmation lands. (Glossary/`CONTEXT.md` updates via `define-domain` as a passive side effect are allowed when a term settles mid-interview.)

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
| "Recommended + one-line reason is enough" | Without Thread, Territory, consequences, and (on high-blast) Criteria graders, the user cannot analyze — only accept a default. |
| "Keep Why to one line / put success in Why / no criteria essays" | Why = blast narrative; Criteria = separate graders above Options. Sentence budget is not a thinness license. |
| "Context can be a follow-up if they ask" | The card *is* the detail. Follow-up-only context is a thin-card failure. |
| "We finished the 4 areas on the todo — close" | The todo is a living map. Open-set empty is the stop; precommitted N is not. |
| "Question 3 of 5, then package" | No fixed N. Countdown framing is a red flag. |
| "User asked for button color first" | Blast-radius first still holds. Polish Diff after architecture, data, and auth forks. |
| "We're aligned — skip the decisions table" | Shared understanding is the package + yes. Alignment theater without the table is not confirmation. |
| "Senior said just write requirements" | User/senior can override *process ownership*; they cannot make an unstated decision exist. Emit the package; get the yes. |
| "I'll assume the safe default and mark done" | Assumptions are not decisions. One card; wait. |
| "Just pick industry best practice — they said sensible" | Look up the territory reference first; restate; lock with the user. |
| "Senior said switch cleanly into clarify-decisions and park the parent" | Nesting *is* the clean switch. Parking the parent and opening a clarify-decisions checklist is dual-channel thrash. |
| "A short decision checklist under clarify-decisions isn't a competing list" | It is a second list. Decision areas live as the parent's in-progress interview item. |
| "Announce Using clarify-decisions so the user sees the write-handoff" | Nested: no mode-switch announcement. Standalone (no parent): you may name clarify-decisions once. |
| "Parent already loaded neighbors — re-run every card for freshness" | Reuse the valid package; rederive only when fingerprints/seeds/scope change |
| "Standalone interview — skip load-subgraph, Territory is enough" | Feature work: load once before the first card |
| "They already named the cheap path / flag / API — treat it as locked" | Solution-shaped Assumptions are not locks. Follow **Problem lock** (Fork first). |
| "Senior said skip philosophy and pick storage/API options" | **Problem lock** still holds. Time changes *when* you report, not whether the problem is locked. |
| "Recommended + blast/cost is enough; criteria live in requirements later" | Recommendation must cite Criteria graders on this card. Later specs consume the close package — they do not replace the slot. |
| "Success / Boundaries / Spine are specify-behavior ceremony — omit from close" | Close package slots 4–6 are required here. Deferral invents a hole the next skill cannot see. |
| "Don't send me to another skill — just give 3 merge architectures" | Follow **Problem lock** Fork: card or **name** `/work-the-problem`. Solution menus while the problem is open are a failure. |
| "Naming /work-the-problem is invoking a user-invoked skill" | Naming for the user to run is the only legal hand-off. Auto-invoking it is the bug. |
| "Reliability is a later NFR template — skip SRE ceremony" | When SRE-on, Reliability · Failure · Operate are open-set classes. NFR templates consume the close package; they do not replace these cards. |
| "Architecture forks are done — emit close" | When SRE-on, coverage Missing cells without owner keep the open set non-empty. |
| "TBD is fine — Open Questions will catch it" | Unowned TBD blocks close. Owned unknowns need owner · date · cấm đoán. |
| "No docs/ops/reliability.md — skip Reliability cell" | Still lock prose targets or an Owned unknown. Do not invent SLO-N IDs. |
| "Standup — keep the map short; skip coverage table" | Coverage map is the living open-set source when SRE-on. Short statuses, not skipped cells. |
| "Accepted-risk without a signer — obvious" | Signer is required when SRE-on. Solo IC may sign as IC. |
| "User said learning spike vibe — skip coverage (posture absent)" | Written posture only. Absent/unspecified ⇒ SRE-on. Chat vibes do not flip the band. |
| "Put TBD and accepted risk in one bucket — same Freeze thing" | Owned unknowns = undecided+forbid-guess; Accepted risks = decided keep-the-risk+signer; Operability = rollback+page. Three slots. |
| "Journey has no radius so skip the Journey cell" | Close Journey via `UX flow` or `architecture` CUJ cards, then update the cell. |

## Red flags — stop and rewrite the turn

- Calling `AskUserQuestion` or any truncated MCQ tool for a clarify-decisions decision
- More than one question mark aimed at the user in a single message (except clarifying examples inside option text)
- Options that are labels only — no consequence lines
- A card missing Thread, Territory, Why it matters, or Closes
- High-blast card missing a labeled Criteria (graders) block above Options, Criteria collapsed into Why, or a Recommendation that never cites the graders
- Preference / solution-option card while **Problem lock** still applies
- Solution architecture menu while the problem is unlocked — without a problem-lock card or naming `/work-the-problem`
- "Question k of N", "final round", or closing because a precommitted count finished while high-blast remains
- Leading with polish-diff while architecture / data / auth / reliability / failure / operate branches remain open
- Closing with "any other questions?" instead of the decisions package
- Close package missing Success / done signal, Boundaries, or Spine touch
- SRE-on start without a Coverage map, or close while any cell is Missing without owner
- SRE-on close missing Coverage final, Owned unknowns, Accepted risks, or Operability touch
- Closing with unowned TBD / “Open Questions will catch it”
- Deferring Reliability · Failure · Operate to “later NFR” while emitting close under SRE-on
- Handing back to the parent or starting requirements without an explicit yes on the package
- Route Tasking the user for a fact present in the repo or the parent's scan digest
- Abstract taste cards for an unknown-known when a reference or run-spike path exists
- Nested re-derive every card while the parent package fingerprints still match
- Standalone feature interview with no retrieval before the first card
- Auto-invoking `/work-the-problem` instead of naming it for the user
- Inventing greppable SLO-N / TB-N / THR-N IDs without Approved doc definitions
- Treating chat “spike/learning vibe” as SRE-off when posture is absent or still Production
- Merging Owned unknowns into Accepted risks (or either into Operability touch)
- Leaving Journey Missing with no `UX flow` / `architecture` CUJ card because “no Journey radius”
- Calling `assess-observability` for every Operate hole (only telemetry/tracing readiness gaps)
