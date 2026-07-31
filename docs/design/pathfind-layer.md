# Pathfind Layer — Design Proposal

**Status:** **Approved** (2026-07-31) — design accepted for D1 requirements; not architecture SSOT until post-ship docs land (OD-9)  
**Date:** 2026-07-31  
**Approved by:** user (this conversation)  
**Authors:** design conversation (BMAD + wayfinder synthesis)  
**Audience:** maintainers of the Engineer Pack  
**Related:** `docs/architecture/{system,workflows,skills}.md`, `docs/adr/0002-*` (intent vs truth split), Matt Pocock `/wayfinder`, BMAD Analysis phase  

This document designs an **optional Pathfind layer** for the Engineer Pack: multi-session decision pathfinding that sits **above** program docs and feature delivery, without replacing either. Implementation (skill text, tracker seeds, tests) starts only after **D1 requirements** and `author-skills` RED baseline — not from this approval alone.

**Locked decisions** live in [§15](#15-locked-decisions-od). Normative body sections below match those locks.

---

## 1. Problem

### 1.1 What the pack already solves

The Engineer Pack is strong at **delivery under gates**:

- Discovery-to-ship spine (`frame-change` → triad → execute → inspect → land)
- Ceremony tiers 0–2
- Iron Laws (no-code / TDD / root-cause / evidence)
- Optional program layer (`define-project`, `plan-milestones`)
- Tracker config (`configure-repo` → `docs/agents/issue-tracker.md`)
- Brownfield-aware vision scan (`define-project` create)

### 1.2 The gap

When an effort is **larger than one agent session** and the route is still **foggy**, the pack has no first-class home:

| Pressure | Today | Failure mode |
|---|---|---|
| Multi-session discovery | Chat + `write-handoff` + `.skills/` ephemera | Decisions die on compact; concurrent agents collide |
| “Too big to frame” | Force into `frame-change` or jump to `plan-milestones` | Spec freezes untested assumptions; roadmap invents `ROAD-N` too early |
| Product-shaped fog (greenfield) | Partial: `clarify-decisions` + research + spike inside one session | No durable decision DAG; no BMAD-depth analysis modes as a system |
| Large brownfield change (migration, platform) | Scan + interview in one window | Window fills; territory facts and open decisions mix without a frontier |

External references that *partially* cover this gap:

- **Wayfinder (Matt Pocock):** decision tickets on a tracker map; fog of war; one ticket/session; plan-don’t-do.
- **BMAD Analysis phase:** brainstorm / forge / research / brief / PRFAQ — breadth of *lenses*, mostly single-session artifacts, not a multi-session frontier.

Neither should be forked wholesale. Both inform this design.

### 1.3 Why this matters more in the AI era

Code generation is cheap and fast. The expensive failures shift to:

1. **Wrong decisions shipped at high velocity**
2. **Lost decisions** across sessions and agents
3. **Over-ceremony** on trivial work (agent “process theater”)
4. **Under-ceremony** on high-blast fog (agent “just builds”)

Pathfind exists so agents stay **flexible on cheap work** and **deliberate on expensive fog**, without softening Iron Laws at delivery time.

---

## 2. Goals and non-goals

### 2.1 Goals

**G1.** Support **greenfield** (no or thin codebase) and **brownfield** (real, possibly large codebases) with **one layer model** and different **entry predicates**.

**G2.** Persist multi-session **decisions** (not implement work) on the repo’s **configured issue tracker** (reuse ARCH-3 / tracker-agnostic stance).

**G3.** Hand off a **knowns package** into existing skills so `frame-change` / `define-project` / `plan-milestones` do not re-interview settled questions.

**G4.** Compose existing primitives (`clarify-decisions`, `research`, `run-spike`, `define-domain`) rather than reimplement interview/research/spike.

**G5.** Remain **optional** (ARCH-2): repos that never pathfind behave exactly as today.

**G6.** Keep Pathfind **user-invoked only** (ARCH-5): agents may *suggest* it; they never auto-start a map.

### 2.2 Non-goals

- Not a second roadmap (`ROAD-N` / `MILE-N` stay in `plan-milestones`).
- Not a PRD factory (no BMAD `create-prd` clone; `specify-behavior` remains requirements owner).
- Not an implement queue (decision tickets ≠ build tickets; `publish-issues` / execute family remain separate).
- Not a persona cast (no Mary/John/Winston as required runtime).
- Not mandatory for tier 0/1 or clear single-session work.
- Not Personal OS scope (Engineer Pack only unless a later deliberate port).

---

## 3. Layer model

Three layers. Lower layers must not run while a higher layer still owns open **blocking** decisions for that effort — except explicit user override.

```text
Layer 0  PATHFIND     — “What must we decide before we can plan or build?”
Layer 1  PROGRAM      — “What outcomes, in what order?” (define-project, plan-milestones)
Layer 2  DELIVERY     — “What SHALL the system do, and ship with evidence?” (feature spine)
```

### 3.1 Ownership boundaries

| Concern | Owner | Pathfind may |
|---|---|---|
| Decision / investigation before build | **Pathfind** | Create/resolve decision tickets |
| Product vision, ARCH-N, guidelines | `define-project` | Recommend running it; never rewrite spine silently |
| Milestone / ROAD-N intent | `plan-milestones` | Recommend decomposition when ≥2 outcomes clear |
| Requirements IDs, tests, commits | Delivery spine | Never invent `CODE-N.M`; never ship |
| Implement issues for agents | `publish-issues` / triage / tasks.md | Only after fog clear (or user forces) |

### 3.2 Relationship diagram

```text
                    ┌─ no fog / small ──────────────────────────────┐
                    │                                              │
  loose idea ───────┤                                              ▼
                    │     frame-change → … → land                  │
                    │                                              │
                    └─ fog + multi-session ──► PATHFIND ──┐        │
                                                         │        │
              greenfield vision unclear ──► define-project ◄──────┤
                                                         │        │
              multi-outcome clear ──► plan-milestones ◄───┤        │
                                                         │        │
              single feature clear ──► frame-change ◄─────┘        │
                                                                   │
  brownfield tweak ──► amend-feature ─────────────────────────────┘
  brownfield bug   ──► root-cause
  brownfield foggy program change ──► PATHFIND (territory-first)
```

### 3.3 “Done” per layer

| Layer | Done when |
|---|---|
| Pathfind | Destination named; no open unblocked decision tickets remain *or* user accepts residual fog as deferred; knowns package written; handoff skill named |
| Program | Vision/ARCH (if used) and/or roadmap approved per existing gates |
| Delivery | Existing definition of done (tests, trace, inspect, land) |

---

## 4. Core concepts

### 4.1 Destination

One or two lines: what “end of this map” looks like. Examples:

- Greenfield: “Approved product vision + first milestone outcomes named”
- Greenfield small: “Enough decisions to write a tier-2 requirements.md for auth”
- Brownfield: “Migration approach locked (dual-write vs freeze) and rollback story agreed”

Destination **fixes scope**. Work past it is **out of scope**, not fog.

### 4.2 Decision ticket (not implement ticket)

A ticket whose resolution is a **decision or settled fact**, sized to roughly one HITL agent session (~context budget of a serious interview or research write-up).

Forbidden resolution: “implemented feature X in production code.”

### 4.3 Fog of war

Suspected future questions that **cannot yet be stated sharply**.

**Ticket vs fog test (normative):**

- **Ticket** when the question can be phrased precisely *now* (even if blocked).
- **Fog** when only a coarse area is known (“something about billing later”).

Do not pre-slice fog into fake tickets.

### 4.4 Frontier

Open + unblocked + unclaimed decision tickets. Native tracker dependencies preferred so humans see the frontier in UI.

### 4.5 Claim

First write on a work session for a ticket: assignee / `Status: claimed`. Prevents concurrent sessions from resolving the same decision.

### 4.6 Plan-don’t-do

Default: Pathfind produces decisions and pointers only.  
Override: only via explicit **Notes** on the map (“this effort includes Task-type unblocks”) — still no production feature delivery; production remains Delivery layer.

### 4.7 Knowns package

Durable handoff artifact produced when leaving Pathfind (or incrementally updated). Consumed by `frame-change` step 1 knowns inventory and by `define-project` / `plan-milestones` interviews.

**Canonical path (v1, locked — OD-3):**

```text
.skills/pathfind/<effort-slug>/knowns.md
.skills/pathfind/<effort-slug>/map-pointer.md   # optional: tracker URL / local map path
.skills/pathfind/<effort-slug>/territory-scan.md # brownfield digest path or copy-pointer
```

Stays under gitignored `.skills/` — no `docs/pathfind/` tree in v1 (ARCH-2/3: do not force a new committed docs surface). Teams that want permanent history keep it via the **issue tracker map** (Decisions so far), not a second docs tree.

---

## 5. Artifacts

### 5.1 The map (index, not store)

One tracker issue (or local markdown file) labelled/typed as the pathfind map.

**Body slots (required):**

```markdown
## Destination
…

## Notes
domain; skills every session consults; greenfield|brownfield; standing preferences

## Decisions so far
- [Ticket title](link) — one-line gist

## Not yet specified
… fog toward destination …

## Out of scope
… consciously ruled out …
```

Open tickets are **not** listed on the map; they are discovered by query.

Refer to tickets **by title (name)**, not bare `#42`.

### 5.2 Child decision tickets

Body minimum:

```markdown
## Question
…

## Type
clarify | research | prototype | task

## Context
optional: surfaces, ARCH-N, links to scan digests
```

On resolve: resolution comment / `## Answer` + close + map Decisions-so-far pointer.

### 5.3 Ticket types

| Type | Mode | Resolves via | Notes |
|---|---|---|---|
| **clarify** | HITL | `clarify-decisions` (+ `define-domain` passive) | Default. Pack-native name for Matt’s “grilling” ticket — **there is no `grilling` skill** in this set. Agent never answers for the human |
| **research** | AFK | `research` **subagent** | Exception to one-ticket-per-session: may burn in parallel at chart time; findings on throwaway branch or `.skills/research/…` with pointer |
| **prototype** | HITL | `run-spike` | Throwaway by contract; link artifact; never promote spike to prod inside Pathfind |
| **task** | HITL or AFK | checklist / agent automation | Only unblocks a decision (access, sample data, signup). Not destination delivery |

**Vocabulary note:** User speech may still say “grill me”; that phrase is a *trigger synonym* in `clarify-decisions`’s description only. Canonical skill name, REQUIRED SUB-SKILL target, ticket Type, and labels all use **clarify** / **`clarify-decisions`** — never a skill or type named `grilling`.

### 5.4 Labels / typing (tracker)

Reuse configured tracker. Seeds use the **`pathfind:`** namespace (locked — OD-4):

- `pathfind:map`
- `pathfind:clarify` | `pathfind:research` | `pathfind:prototype` | `pathfind:task`

Local markdown: `Type:` and `Status:` lines (mirror Matt local tracker ops).

**Why not `wayfinder:`:** pack-native, greps with skill name, no brand collision with Matt’s plugin.  
**Why not `decision:` alone:** one namespace for map + types is simpler ops; “decision” semantics live in skill prose and ticket body Type, not a second label family.

---

## 6. Skill surface (proposed)

### 6.1 New user-invoked skill: `pathfind`

- **Name:** `pathfind` (verb-first) — locked OD-1; see §15 for why not the runners-up
- **Invocation:** user-only (`disable-model-invocation: true`)
- **Category:** `skills/discovery/pathfind/` — locked OD-2 (`project/` stays vision + roadmap only)
- **Modes:**
  1. **Chart** — loose idea → destination + initial tickets + optional parallel research
  2. **Work** — map id/url → claim one frontier ticket → resolve → graduate fog

Description (human-facing, user-invoked): plain line naming the deliverable, e.g.  
*“Chart or advance a multi-session decision map until the route to a destination is clear.”*

### 6.2 No new model-invoked interview engine

`pathfind` **REQUIRED SUB-SKILL** targets:

- `clarify-decisions` for **clarify** tickets (HITL interview protocol)  
- `research` for research tickets  
- `run-spike` for prototype tickets  
- `define-domain` passive glossary/ADR when terms settle  

### 6.3 Optional analysis *lenses* (BMAD-inspired, not personas)

Documented **Notes** or explicit user flags on Chart — not separate mandatory skills in v1:

| Lens | When | Behavior |
|---|---|---|
| Explore | No options yet | Breadth-first **clarify** tickets; more fog tolerated |
| Forge | Idea exists, needs kill/harden | Adversarial recommended answers (`clarify-decisions` card pressure) |
| Recon | External facts missing | Prefer research tickets early |

v1 ships lenses as **guidance inside `pathfind` only** (locked OD-5) — not three new skills. Split later only if a distinct trigger fails without a separate skill (author-skills split rule).

### 6.4 Router updates (after skill exists)

`route-task` / `gate-session` / teach-pack gains an on-ramp:

- Multi-session fog, destination unclear, effort > one window → name `/pathfind` for the user  
- Clear single feature → `frame-change`  
- Program vision missing on large work → `/define-project`  
- Bug → `root-cause`  
- Shipped tweak → `amend-feature`

Agents **suggest**; user runs `/pathfind` (ARCH-5).

### 6.5 Explicit non-skills

Do not add: `pathfind-prd`, `pathfind-implement`, persona launchers.

---

## 7. Workflows

### 7.1 Chart the map (session A)

1. Detect greenfield vs brownfield (predicate aligned with `define-project` / `bootstrap-repo` where possible).
2. **Brownfield (locked OD-6):** if no usable territory digest exists, **dispatch** a scan (predicate/contract aligned with `define-project` brownfield-scan) and write `.skills/pathfind/<effort>/territory-scan.md` (or pointer to an existing digest) **before** the destination interview. Candidates are untrusted evidence (same ratification spirit as `define-project`).
3. **Name destination** via `clarify-decisions` (nested interview protocol).
4. Breadth-first surface decisions; if **no fog and single-session**, stop — recommend `frame-change` / `define-project` / `amend-feature` as fits; **do not create a map**.
5. Create map + specify-able tickets; second pass wire blocking.
6. Fire research subagents for research tickets (parallel).
7. Write/update knowns package skeleton; stop (chart does not resolve HITL **clarify** / **prototype** tickets).

### 7.2 Work the map (sessions B…N)

1. Load map (low-res only).
2. Pick named ticket or first frontier; **claim first**.
3. Resolve via type table; zoom related closed tickets on demand.
4. Record answer → close → Decisions so far gist.
5. Graduate fog → new tickets; out-of-scope close mis-scoped tickets.
6. **One HITL ticket per session** (research exception remains).
7. **Exit (locked OD-8):** finalize knowns package + name handoff skill when either:
   - frontier is empty **and** Not yet specified is empty, or
   - frontier is empty **and** user **explicitly accepts** residual fog deferred in Not yet specified (written into knowns as Known unknowns), or
   - user **stops early** with explicit accept of open state (knowns records open tickets + fog; not a clean Pathfind-complete).

   Do **not** force-ticket remaining fog. Do **not** hand off “complete” while open **unblocked** tickets remain unless the user explicitly abandons them (close as deferred/out-of-scope with reason).

### 7.3 Handoff matrix

| After Pathfind, if… | Name for user |
|---|---|
| No vision/ARCH and multi-feature product | `/define-project` |
| ≥2 independent outcomes / build order | `plan-milestones` (model-invoked from frame later, or user asks roadmap) |
| One feature-shaped destination | continue / start `frame-change` with knowns path |
| Change to shipped spec’d feature, small | `amend-feature` |
| Pivot collides shipped | `/assess-pivot-impact` |
| Residual fog only operational | may `publish-issues` for human ops — not decision map |

Pathfind never auto-invokes user-invoked skills; it **names** them (ARCH-5).

---

## 8. Greenfield vs brownfield predicates

### 8.1 Greenfield

**Signals:** empty/minimal tree, bootstrap path, no meaningful `docs/specs/`, no production surface.

**Pathfind bias:** destination often product/outcome shaped; Explore/Forge lenses common; research may include market/API; `define-project` often follows.

**Does not replace** `bootstrap-repo` — stack skeleton stays bootstrap’s job. Pathfind may run before or after bootstrap; Notes should record whether a runnable repo exists.

### 8.2 Brownfield

**Signals:** substantial source (reuse `define-project` brownfield-scan predicate).

**Pathfind requirements:**

1. Territory context before Chart destination (scan digest path in Notes).
2. Tickets prefer a **Surfaces:** line (paths/components) or explicit “surface unknown — research”.
3. Must not silently rewrite ARCH-N / shipped requirements; collisions → name `/assess-pivot-impact` or `amend-feature` / mini-spec routes.
4. Prefer decisions that **ratify** existing behavior vs invent greenfield architecture on top of production.

### 8.3 Mixed (monorepo / brownfield product, greenfield module)

Destination states the **effort boundary** (“new billing module inside monorepo X”). Brownfield rules apply to shared surfaces; greenfield rules apply inside the new boundary.

---

## 9. Flexibility dials (runtime policy)

Three dials guide **whether** to pathfind and **how deep** — stated in skill + teach-pack, not a separate configurator in v1.

| Dial | Low | High |
|---|---|---|
| **Fog density** | Skip map; frame/amend/root-cause | Chart map; fog section active |
| **Blast radius** | Tier 0/1 delivery; thin pathfind | Full pathfind; research/prototype before locks |
| **Session budget** | One-session `clarify-decisions` inside frame-change | Multi-session map + claim + frontier |

**Normative shortcuts:**

- Fog low + blast low → **no Pathfind**
- Fog high + blast high → **Pathfind**
- Fog high + blast low → short map or research/spike inside `frame-change` (user choice)
- Fog low + blast high → skip Pathfind; still full delivery ceremony (tier 2)

Iron Laws at Delivery **do not dial down** because Pathfind existed or because agents code fast.

---

## 10. Tracker operations

### 10.1 Principle

Pathfind **reads** `docs/agents/issue-tracker.md`. If missing: say once, suggest `/configure-repo`, default to **local markdown** under `.skills/pathfind/<effort>/` (or `.scratch/` if that convention exists) — mirror setup-matt local ops without requiring GitHub.

### 10.2 Seeds to add later (implementation phase)

Extend configure-repo / issue-tracker templates with a **Pathfind operations** section:

- Map create/label  
- Child create + parent link  
- Blocking / frontier query  
- Claim / resolve  

Parity targets: Matt’s GitHub + local markdown “Wayfinding operations” (renamed Pathfind).

### 10.3 Concurrency

Expect parallel sessions. Claim is mandatory. Map Decisions-so-far appends must be race-aware (re-read map before edit).

---

## 11. Integration contracts

### 11.1 Into `frame-change`

When user points at a knowns package or open map:

- Step 1 **Knowns inventory** seeds from Decisions so far + residual fog as known unknowns  
- Do not re-open closed decisions unless user reopens a ticket  
- Blindspot still required from territory scan (brownfield)

### 11.2 Into `define-project` / `plan-milestones`

- Pathfind may clear product questions that feed vision goals  
- Pathfind does not write `GOAL-N` / `ROAD-N` itself  
- When charting surfaces ≥2 build outcomes, Chart exit names roadmap planning

### 11.3 Versus `publish-issues` (locked OD-7)

| | Pathfind | publish-issues |
|---|---|---|
| Unit | Decision | Implementable tracer / agent-ready work |
| When | Fog | Path relatively clear or capture of agreed work |
| Plan-don’t-do | Yes | No — issues are to do |
| Tracker edges | Blocking **among pathfind tickets only** | Blocking among implement issues only |

**Strict separation in v1:**

- Pathfind **never** creates implement issues and **never** adds `Blocked by` edges from implement issues onto decision tickets (or the reverse).
- Cross-reference is **URL / title only** in body prose or knowns package (“see map …”, “after decisions … run `/publish-issues`”).
- Mis-typed build work on a pathfind ticket → close as type error, tell user to run `/publish-issues` (or wait for requirements + tasks) — do not “fix” by converting the ticket in place.
- When destination is clear enough for work capture but delivery triad is not started yet, Pathfind **names** `/publish-issues` as an optional fast lane; it does not run it (ARCH-5).

### 11.4 Versus `write-handoff`

`write-handoff` snapshots **conversation**. Pathfind map is **authoritative decision index**. After Pathfind, handoff may *point at* map + knowns; it does not replace them.

### 11.5 Versus Personal OS

No coupling. If later ported, destination becomes life-outcome; Engineer Iron Laws do not apply — separate design.

---

## 12. Architecture invariant fit

| Invariant | How Pathfind complies |
|---|---|
| **ARCH-1** | No LLM-only “trace” of decisions as coverage; map/ticket state is structural. Optional later: deterministic grep that open `pathfind:*` tickets exist — never “does this decision quality-cover the destination” as audit-trace |
| **ARCH-2** | Entire layer optional; no skill invents a map when user didn’t pathfind |
| **ARCH-3** | Tracker ops via existing config; local markdown fallback; no new runtime deps |
| **ARCH-4** | Pathfind does not mint `CODE-N.M` / renumber ARCH |
| **ARCH-5** | `pathfind` user-invoked; only model-invoked sub-skills invoked from it |
| **ARCH-6** | Only mediates pathfind-labelled artifacts and handoffs this skill creates; no policing external contributors’ missing maps |

Possible **future** invariant (not proposed for approval now):

> Optional Pathfind maps MUST treat tickets as decisions-not-delivery; production implementation CONTINUES TO require the delivery spine.

Capture as ARCH-N only if baseline agents violate plan-don’t-do after skill ships.

---

## 13. Failure modes and counters (design-time)

| Failure | Counter in skill design |
|---|---|
| Agent implements inside Pathfind | Hard gate + rationalization table; run-spike only for prototype type |
| Agent creates implement tickets as pathfind tickets | Type recipe + publish-issues boundary section |
| Map created for tier-0 work | Chart step “no fog → stop” |
| Brownfield pathfind ignores codebase | Chart hard requirement: territory digest before destination |
| Double interview after handoff | Knowns package REQUIRED slot; frame-change consumption rule |
| Concurrent double-resolve | Claim-first rule |
| Infinite fog / never hand off | Exit criteria: empty frontier or user accepts deferred fog in Not yet specified with explicit handoff |
| Roadmap pollution | Non-goal: no ROAD-N writes from pathfind |
| Context blow-up loading all tickets | Map is index; zoom on demand |

---

## 14. Phased delivery (implementation later)

Do **not** start until this design is accepted and `author-skills` RED baselines exist.

| Phase | Deliverable | Exit |
|---|---|---|
| **D0 — this doc** | Design proposal approved or revised | **Done** — Approved 2026-07-31 |
| **D1 — requirements** | `docs/specs/2026-07-31-pathfind/requirements.md` (PFIND) | **Done** — Approved 2026-07-31 |
| **P1** | Tracker Pathfind operations seeds + local map schema | configure-repo docs mention Pathfind |
| **P2** | `pathfind` SKILL.md Chart + Work modes | Pressure-tested per author-skills |
| **P3** | Knowns package template + frame-change consumption paragraph | Integration scenario green |
| **P4** | route-task / teach-pack / workflows.md / skills.md inventory | Docs consistent |
| **P5** | Lenses polish only if pressure tests demand; **no** `docs/pathfind/` tree | Only if P2–P4 hold |
| **P6** | Pack architecture docs (OD-9) | ADR + workflows + skills inventory; domain file only if narrative overflow |

No parallel implementers on the skill text (pack authoring rule).

---

## 15. Locked decisions (OD)

All rows locked 2026-07-31 unless noted.

| ID | Decision | Lock |
|---|---|---|
| **OD-1** | Skill name = **`pathfind`** | See rationale below |
| **OD-2** | Category = **`skills/discovery/pathfind/`** | Chốt |
| **OD-3** | Knowns + effort ephemera = **`.skills/pathfind/<effort>/` only** (no `docs/pathfind/` in v1) | Chốt |
| **OD-4** | Tracker label namespace = **`pathfind:`** | See rationale below |
| **OD-5** | Analysis lenses = **guidance inside skill only** (v1) | Best method — see below |
| **OD-6** | Brownfield Chart = **dispatch scan if digest missing** before destination | Chốt yes |
| **OD-7** | vs `publish-issues` = **strict separation**; URL/title only; no cross-type blocking edges | See below |
| **OD-8** | Residual fog = **handoff allowed** if user explicitly accepts deferred fog in Not yet specified + knowns | See below |
| **OD-9** | Post-ship docs = **ADR + `workflows.md` + `skills.md` first**; domain file only if needed; **no ARCH-N until pressure proves need** | See below |
| **OD-10** | HITL interview ticket type / label = **`clarify`** / **`pathfind:clarify`**; resolve via **`clarify-decisions`**. Never name a type or skill `grilling` | Vocabulary lock — see below |

### OD-1 — Name: why `pathfind` (and what lost)

| Candidate | Pros | Cons |
|---|---|---|
| **`pathfind`** | Verb-first; one token; teaches the metaphor; distinct from Matt without being cute | Slightly abstract for newcomers |
| `wayfind` / `wayfinder` | Familiar if you know Matt | Brand/collision; looks like a fork |
| `chart-decisions` | Outcome-clear (“decisions”) | Longer; “chart” collides with Chart *mode*; weaker metaphor for multi-session journey |
| `clear-fog` | Vivid | Implies finish state only; weak for Work mode mid-map |
| `map-route` | Concrete | Sounds like HTTP routing / geo |

**Lock `pathfind`:** best balance of pack naming style (`frame-change`, `root-cause`), metaphor (journey before build), and non-fork identity. Teach-pack one-liner carries the “decision map” outcome noun.

### OD-4 — Labels: why `pathfind:`

One namespace greppable with the skill (`pathfind:map`, `pathfind:clarify`, …). Avoids `wayfinder:` fork optics. Avoids splitting `decision:*` tickets + `pathfind:map` into two families agents will mis-apply. Semantic “this is a decision not a build” is enforced in skill gates + body Type, not a second label taxonomy. Ticket type **clarify** maps to skill **`clarify-decisions`** — not Matt’s `grilling` name.

### OD-5 — Lenses: why guidance-only is the best v1 method

- author-skills: split only on **distinct trigger** or real context boundary — Explore/Forge/Recon share one trigger (“multi-session fog”).
- Separate skills would multiply route-task surface and tempt auto-invocation theater.
- Guidance in Chart Notes is enough to bias ticket mix (more research vs more clarify) without new frontmatter.
- **Promote to skills later** only if pressure tests show agents cannot hold lens behavior without a separate fire.

### OD-7 — Strict separation from `publish-issues`

Crossing blocking graphs (decision ↔ implement) creates:

- frontier queries that mix “decide X” with “build Y”
- agents resolving a decision by opening a PR
- triage confusion (`ready-for-agent` on a question)

v1 rule: **two graphs, prose links only.** Handoff may *name* `/publish-issues` when work is capturable; Pathfind does not author those issues.

### OD-8 — Deferred fog handoff

Forcing every fog patch into a ticket either invents fake sharpness or blocks shipping forever. Allow complete-with-deferred when:

1. No open **unblocked** pathfind tickets (or user explicitly abandons them with recorded reason), and  
2. User **explicitly accepts** remaining Not yet specified as deferred, and  
3. Knowns package lists them under **Known unknowns** (not locks).

`frame-change` then treats those as known unknowns — not silent locks.

### OD-9 — Architecture docs after ship

| Step | When | What |
|---|---|---|
| 1 | Skill pressure-tested green | Short **ADR**: Pathfind layer optional; plan-don’t-do; knowns under `.skills/`; user-invoked |
| 2 | Same PR as ADR | **`workflows.md`**: pathfind on-ramp in diagram + boundaries vs publish-issues |
| 3 | Same | **`skills.md`** inventory row under discovery/ |
| 4 | Only if ADR+workflows overflow (~narrative for brownfield/lenses) | Domain **`docs/architecture/pathfind.md`** + INDEX Domains table |
| 5 | Only if agents still implement inside pathfind after skill text | Consider **ARCH-N** plan-don’t-do — not pre-emptive |

Do **not** mint ARCH-N in the design phase; invariants earn their ID from failures.

### OD-10 — Not “grilling”: pack vocabulary

Matt’s wayfinder ticket type **grilling** maps *functionally* to our interview primitive, but the **name in this pack is not grilling**.

| Surface | Canonical term |
|---|---|
| Skill | **`clarify-decisions`** (model-invoked) |
| Pathfind ticket Type | **`clarify`** |
| Tracker label | **`pathfind:clarify`** |
| REQUIRED SUB-SKILL | `use \`clarify-decisions\`` |
| Colloquial user speech | “grill me” may still appear in `clarify-decisions` description as a *should-fire synonym* only |

**Why rename for Pathfind:** agents copy ticket type strings into labels and handoffs. Shipping `pathfind:grilling` would reintroduce a retired skill name and fight `route-task` / inventory (`clarify-decisions` only). **Forge lens** remains a *style* of clarify-decisions cards, not a ticket type.

---

## 16. Acceptance of *this design* (not the skill)

**Accepted 2026-07-31** (user: approve).

- OD-1…OD-10 locked  
- Goals G1–G6 and non-goals stand  
- Layer boundaries stand (Pathfind ≠ roadmap ≠ delivery)  
- Vocabulary: **`clarify` / `clarify-decisions`**, not `grilling`

**Does not authorize:** shipping skill text, tracker seeds, or architecture SSOT edits without D1 + author-skills RED.

**D1 Approved:** [`docs/specs/2026-07-31-pathfind/requirements.md`](../specs/2026-07-31-pathfind/requirements.md) (feature code **PFIND**, Status: **Approved** 2026-07-31).

**Next:** feature `design.md` (or cite this file as design SSOT in tasks) → `tasks.md` → `author-skills` RED → implement per §14 / PFIND phases.

---

## 17. Summary

Pathfind is the missing **Layer 0**: a tracker-backed, multi-session **decision map** with fog, frontier, and plan-don’t-do — informed by wayfinder mechanics and BMAD analysis *lenses*, implemented as **one user-invoked skill** that composes pack primitives and hands off into **program + delivery** spines that already work for greenfield and brownfield.

It makes agents **more flexible** by giving them a legal place to stay undecided (and durable), and **safer** by refusing to let undecided fog become production code under Iron Laws.
