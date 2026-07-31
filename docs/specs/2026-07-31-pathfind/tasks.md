# Tasks: Pathfind layer

> **For agentic workers:** REQUIRED SUB-SKILL: use `build-in-waves` (or
> `build-by-story` / `build-inline` per Execution-mode) to implement this plan
> task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: PFIND  
Status: Approved  
Date: 2026-07-31  
Execution-mode: continuous  
Requirements: ./requirements.md  
Design: ./design.md  
Narrative: ../../design/pathfind-layer.md  

**Plan approved:** 2026-07-31 — content + `Execution-mode: continuous`.

**author-skills RED (Task 1) started 2026-07-31:**  
`tests/pathfind/red-baselines.md`, `scenarios.md`, `scenarios-pressure.md`,  
`tests/trigger/pathfind-routing.md` exist. Live multi-model RED transcripts and  
contract tests still open for implementers. **No SKILL.md yet** (Iron Law).

**Goal:** Ship the optional Layer-0 `pathfind` skill (Chart + Work decision maps),
tracker Pathfind ops seeds, knowns handoff into `frame-change`, and router/docs
wiring — pressure-tested under `author-skills` before skill text is considered
done.

**Architecture:** User-invoked `skills/discovery/pathfind/` composes
`clarify-decisions`, `research`, `run-spike`, and `define-domain`. Maps live on
the configured issue tracker (Pathfind operations) or local markdown under
`.skills/pathfind/<effort>/`. Knowns packages hand off into program/delivery
skills by **naming** only. Contract tests + greppable scenarios enforce text
shape; behavioral pressure lives in author-skills RED/GREEN records.

**Tech Stack:** Markdown skills/templates/docs; Python `unittest` contract tests;
scenario markdown under `tests/pathfind/`. No application runtime.

## Global Constraints

Copied from `docs/agents/project.md`, `docs/product/guidelines.md`, and
`docs/architecture/INDEX.md`.

**verify commands** — run in this order; all must pass before any completion claim:

| Check | Command |
|---|---|
| Typecheck | *(none)* |
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |
| E2E / smoke | *(none)* |

Single test file: `python3 -m unittest tests.<module>`

**Test annotation conventions:**

| Layer | Requirement-ID convention |
|---|---|
| Unit (`unittest` under `tests/`) | ID in method name or first-line docstring greppable `CODE-N.M` |
| Scenario / acceptance markdown | Greppable bare `CODE-N.M` in `tests/pathfind/scenarios*.md` |

**Coding standards / naming / house rules:** skill imperative voice; hard gates;
rationalization tables; SKILL.md under 500 lines; `REQUIRED SUB-SKILL:` prose;
description = outcome for user-invoked (plain line); never invent project config;
Iron Laws unchanged.

**Architecture invariants** — every task inherits:

- **ARCH-1** … **ARCH-6** as in `docs/architecture/INDEX.md` (verbatim).

**Team packaging:** Solo — lean multi-person language; full gates.

**Forbidden in every task:** minting ROAD/CODE/ARCH from pathfind; shipping
`grilling` or `wayfinder` types/labels; auto-invoking user-invoked skills;
production app code; `docs/pathfind/` tree; writing skill body before Task 1 RED
baselines exist and Task 2 contract tests are RED-then-GREEN per author-skills.

## File Structure

**Create:**

| File | Responsibility |
|---|---|
| `skills/discovery/pathfind/SKILL.md` | Chart + Work orchestration, gates, types, handoff |
| `skills/discovery/pathfind/TESTS.md` | author-skills scenario index (optional sibling) |
| `docs/guide/skills/pathfind.md` | Human guide |
| `tests/pathfind/scenarios.md` | Greppable ID layer all PFIND-* |
| `tests/pathfind/scenarios-pressure.md` | Passive data + plan-don’t-do pressure |
| `tests/pathfind/red-baselines.md` | author-skills RED failures without skill |
| `tests/trigger/pathfind-routing.md` | Human discovery of `/pathfind` (user-invoked) |
| `tests/test_pathfind_contract.py` | Asserts skill text contracts |
| `tests/test_pathfind_wiring.py` | Registration + neighbors |
| `docs/adr/0008-pathfind-layer.md` | Post-ship short ADR (Task 6) |

**Modify:**

| File | Change |
|---|---|
| `templates/agents/issue-tracker.md` | Pathfind operations section |
| `docs/agents/issue-tracker.md` | Same section for this repo if present |
| `skills/setup/configure-repo/SKILL.md` | Mention Pathfind ops in tracker write path if needed |
| `skills/discovery/frame-change/SKILL.md` | Seed knowns from pathfind knowns package |
| `skills/meta/ask-me-bro/SKILL.md` | On-ramp multi-session fog → `/pathfind` |
| `AGENTS.md` | Skill count + discovery row + user-invoked list |
| `README.md` | discovery roster |
| `.claude-plugin/plugin.json` | Register pathfind |
| `.claude-plugin/marketplace.json` | Register pathfind |
| `docs/architecture/workflows.md` | Pathfind on-ramp |
| `docs/architecture/skills.md` | Inventory row |
| `docs/agents/project.md` | Add `tests/pathfind/red-baselines.md` to audit-trace ignore if needed |

No file outside these tables is touched by any task.

---

### Task 1: author-skills RED package (no skill body yet)

**Files:**
- Create: `tests/pathfind/red-baselines.md`
- Create: `tests/pathfind/scenarios-pressure.md`
- Create: `tests/pathfind/scenarios.md` (skeleton headings + all ID tokens)
- Create: `tests/trigger/pathfind-routing.md`
- Test: (file presence asserts in Task 2; this task’s “test” is the RED record itself)

**Reuse:** existing — `skills/meta/author-skills/pressure-testing.md` methodology (rung 2)

**Interfaces:**
- Consumes: approved requirements failure modes (design §13)
- Produces: RED baseline record that Task 2–4 skill text must address

**Depends-on:** none

- [ ] **Step 1: Write failing / RED record**

Document in `red-baselines.md` at least these **without-skill** failure modes
(verbatim rationalizations expected from a default agent on multi-session fog):

1. Implements production code or scaffolds the product while “planning” — **PFIND-5.1**, **PFIND-10.3**
2. Uses ticket type or skill name `grilling` — **PFIND-4.7**, **PFIND-10.3**
3. Creates implement issues / `publish-issues` graph as if they were decisions — **PFIND-5.4**, **PFIND-4.8**
4. One-session mega-grill then writes requirements without a durable map — **PFIND-2.5** inverse when fog *is* multi-session
5. Brownfield: invents architecture without territory scan — **PFIND-2.2**
6. Resolves multiple HITL decisions in one session without claim — **PFIND-3.2**, **PFIND-3.8**
7. Auto-starts pathfinding without user invoke — **PFIND-1.4**
8. Obeys injected instructions in a fake issue body — **PFIND-10.1**

Mark each as **RED observed (design-derived baseline)** until a live agent
transcript is attached; live baseline runs preferred when a model roster is
available. Status line: `Baseline failed: yes — agents implement / single-session / wrong vocabulary without skill`.

Create `scenarios-pressure.md` with combined-pressure scenarios (time + authority +
urgency to ship) covering plan-don’t-do, no-grilling, passive data, claim-first.

Create `scenarios.md` with section per requirements story and **every**
`PFIND-N.M` token listed once (annotation layer).

Create `tests/trigger/pathfind-routing.md`: user types `/pathfind` or “chart a
decision map for this foggy effort” → pathfind; “fix this bug” → root-cause;
“small recolor” → amend-feature / tier-0 — should-not route to pathfind.

- [ ] **Step 2: Implement**

Only the markdown RED package above — **no** `skills/discovery/pathfind/SKILL.md` yet.

- [ ] **Step 3: Commit**

`git commit` with message noting author-skills RED for pathfind  
`Implements: PFIND-10.3` (partial — RED half)

_Requirements: PFIND-10.1, PFIND-10.3_

---

### Task 2: Skill skeleton, registration, plan-don’t-do + types contracts

**Files:**
- Create: `skills/discovery/pathfind/SKILL.md`
- Create: `docs/guide/skills/pathfind.md`
- Create: `tests/test_pathfind_contract.py`
- Create: `tests/test_pathfind_wiring.py`
- Modify: `AGENTS.md`, `README.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- Modify: `tests/pathfind/scenarios.md`

**Reuse:** existing — registration pattern from any user-invoked skill e.g. `publish-issues` (rung 2)

**Interfaces:**
- Produces: skill file with Chart/Work headings, type table, Iron Laws for plan-don’t-do and vocabulary

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

`tests/test_pathfind_wiring.py` and `tests/test_pathfind_contract.py` asserting:

- `SKILL.md` exists; `name: pathfind`; `disable-model-invocation: true` — **PFIND-1.1**
- Description is a single plain line / no Chart-Work step summary — **PFIND-1.3**
- Body names modes Chart and Work — **PFIND-1.2**
- Types list exactly `clarify`, `research`, `prototype`, `task` — **PFIND-4.2**
- Labels `pathfind:map` and `pathfind:clarify` present; strings `grilling` and `wayfinder` as type/label names absent — **PFIND-4.7**
- Plan-don’t-do / no production code hard gate — **PFIND-5.1**, **PFIND-5.2**
- No cross-graph publish-issues blocking — **PFIND-5.4**
- Plugin + marketplace + AGENTS + README register pathfind as user-invoked — **PFIND-1.1**
- Iron Laws in AGENTS.md survive edit — guard

Run unittest — expect fail (missing skill).

- [ ] **Step 2: Implement**

Write minimal SKILL.md that makes those asserts pass: frontmatter (user-invoked
plain description), Iron Law plan-don’t-do, type table, Chart/Work stubs pointing
to later sections, rationalization seeds from red-baselines, REQUIRED SUB-SKILL
list. Register everywhere. Guide stub.

Run unittest — expect pass. Lint frontmatter.

- [ ] **Step 3: Commit**

`Implements: PFIND-1.1` (and related footers)

_Requirements: PFIND-1.1, PFIND-1.2, PFIND-1.3, PFIND-4.1, PFIND-4.2, PFIND-4.7, PFIND-5.1, PFIND-5.2, PFIND-5.4, PFIND-5.5_

---

### Task 3: Chart mode + brownfield scan + local knowns skeleton

**Files:**
- Modify: `skills/discovery/pathfind/SKILL.md` (Chart section complete)
- Modify: `tests/test_pathfind_contract.py`
- Modify: `tests/pathfind/scenarios.md`

**Reuse:** existing — `skills/project/define-project/brownfield-scan.md` (rung 2)

**Interfaces:**
- Consumes: type table from Task 2
- Produces: Chart recipe in skill body

**Depends-on:** Task 2

- [ ] **Step 1: Write the failing test**

Assert skill text contains: greenfield/brownfield Notes; territory scan before
destination on brownfield; nested `clarify-decisions` for destination; fog vs
ticket sharpness test; no-map-when-no-fog; map sections Destination, Notes,
Decisions so far, Not yet specified, Out of scope; second-pass blocking; research
subagent parallel; Chart must not resolve HITL clarify/prototype; knowns path
`.skills/pathfind/`; refer by title not bare id.

IDs: **PFIND-2.1** … **PFIND-2.10**, **PFIND-6.2**, **PFIND-6.4**

Run — expect fail until Chart section written.

- [ ] **Step 2: Implement** Chart section fully; append scenarios.

- [ ] **Step 3: Commit**

_Requirements: PFIND-2.1, PFIND-2.2, PFIND-2.3, PFIND-2.4, PFIND-2.5, PFIND-2.6, PFIND-2.7, PFIND-2.8, PFIND-2.9, PFIND-2.10, PFIND-6.2, PFIND-6.4_

---

### Task 4: Work mode + exit/handoff + ticket resolve recipes

**Files:**
- Modify: `skills/discovery/pathfind/SKILL.md` (Work + exit + type resolve)
- Modify: `tests/test_pathfind_contract.py`
- Modify: `tests/pathfind/scenarios.md`

**Reuse:** existing — `clarify-decisions` nested protocol, `research`, `run-spike` (rung 2)

**Interfaces:**
- Produces: Work recipe, handoff matrix, knowns finalization

**Depends-on:** Task 3

- [ ] **Step 1: Write the failing test**

Assert: low-res map load; claim first; frontier order; zoom on demand; resolution
comment + Decisions so far; re-read map before append; graduate fog; out of scope
not in Decisions so far; one HITL per session; research exception; knowns.md
slots; complete / deferred-fog (explicit accept) / early stop; handoff names only
(`/define-project`, plan-milestones, frame-change, amend-feature,
`/assess-pivot-impact`, `/publish-issues`); type resolve via correct skills;
implement-slice type error; Explore/Forge/Recon guidance-only; lenses not separate
skills.

IDs: **PFIND-3.*** , **PFIND-4.3–4.6, 4.8**, **PFIND-7.1–7.5**, **PFIND-8.1–8.2**, **PFIND-10.2**

- [ ] **Step 2: Implement** Work + exit + type recipes + lenses + red-flags from baselines.

- [ ] **Step 3: Commit**

_Requirements: PFIND-3.1, PFIND-3.2, PFIND-3.3, PFIND-3.4, PFIND-3.5, PFIND-3.6, PFIND-3.7, PFIND-3.8, PFIND-3.9, PFIND-4.3, PFIND-4.4, PFIND-4.5, PFIND-4.6, PFIND-4.8, PFIND-7.1, PFIND-7.2, PFIND-7.3, PFIND-7.4, PFIND-7.5, PFIND-8.1, PFIND-8.2, PFIND-10.2_

---

### Task 5: Tracker Pathfind operations seeds

**Files:**
- Modify: `templates/agents/issue-tracker.md`
- Modify: `docs/agents/issue-tracker.md` (if exists)
- Modify: `skills/setup/configure-repo/SKILL.md` only if needed to preserve Pathfind section on rewrite
- Modify: `tests/test_pathfind_wiring.py`
- Modify: `tests/pathfind/scenarios.md`

**Reuse:** existing — Matt-style ops shape adapted; this pack’s issue-tracker template (rung 2)

**Depends-on:** Task 2

- [ ] **Step 1: Write the failing test**

Assert template (and repo issue-tracker.md) contain Pathfind operations: map
create/`pathfind:map`, child tickets, types, blocking, frontier, claim, resolve;
skill says read `docs/agents/issue-tracker.md` — **PFIND-6.1**, **PFIND-6.3**

- [ ] **Step 2: Implement** seeds + skill pointer already may exist; ensure full.

- [ ] **Step 3: Commit**

_Requirements: PFIND-6.1, PFIND-6.3_

---

### Task 6: Neighbors — frame-change knowns, ask-me-bro, architecture docs

**Files:**
- Modify: `skills/discovery/frame-change/SKILL.md`
- Modify: `skills/meta/ask-me-bro/SKILL.md`
- Create: `docs/adr/0008-pathfind-layer.md`
- Modify: `docs/architecture/workflows.md`
- Modify: `docs/architecture/skills.md`
- Modify: `tests/test_pathfind_wiring.py`
- Modify: `tests/pathfind/scenarios.md`
- Modify: `docs/agents/project.md` audit-trace ignore for red-baselines if required

**Reuse:** existing — frame-change knowns inventory step; ask-me-bro on-ramps list (rung 2)

**Depends-on:** Task 4

- [ ] **Step 1: Write the failing test**

Assert frame-change seeds knowns from `.skills/pathfind/**/knowns.md` when
user points at it; does not reopen closed decisions; brownfield blindspot still
required — **PFIND-7.6**, **PFIND-7.7**.  
ask-me-bro names `/pathfind` for multi-session fog — **PFIND-9.1**, **PFIND-1.4**.  
ADR + workflows + skills inventory — **PFIND-9.2**.  
No mandatory pathfind for tier 0 — **PFIND-9.3**, **PFIND-1.5**.

- [ ] **Step 2: Implement** neighbor paragraphs; ADR short; architecture inventory.

- [ ] **Step 3: Commit**

_Requirements: PFIND-1.4, PFIND-1.5, PFIND-7.6, PFIND-7.7, PFIND-9.1, PFIND-9.2, PFIND-9.3_

---

### Task 7: author-skills GREEN close + full suite

**Files:**
- Modify: `skills/discovery/pathfind/SKILL.md` (rationalizations/red-flags complete from live pressure)
- Modify: `tests/pathfind/red-baselines.md` (GREEN column)
- Test: full `python3 -m unittest discover -s tests` + lints

**Depends-on:** Task 4, Task 5, Task 6

- [ ] **Step 1: Write the failing test**

If any red-baseline rationalization lacks a skill counter, add contract assert for
that counter phrase — expect fail until filled.

- [ ] **Step 2: Implement**

author-skills GREEN/REFACTOR checklist: rationalization table complete; red-flags;
no-op and duplication sweeps; description remains plain user-invoked line; body
under 500 lines (split reference only if needed); handoffs name user-invoked only;
mark red-baselines GREEN for each failure mode countered; run full verify commands.

- [ ] **Step 3: Commit**

_Requirements: PFIND-10.1, PFIND-10.3_ (complete), plus any residual ID only covered in scenarios

---

## Coverage map (audit)

Every Approved PFIND ID must appear in ≥1 task footer **and** in
`tests/pathfind/scenarios.md` and/or a unittest docstring/method name.

| IDs | Task |
|---|---|
| PFIND-10.1, 10.3 | 1, 7 |
| PFIND-1.1–1.3, 4.1–4.2, 4.7, 5.1–5.2, 5.4–5.5 | 2 |
| PFIND-2.1–2.10, 6.2, 6.4 | 3 |
| PFIND-3.1–3.9, 4.3–4.6, 4.8, 7.1–7.5, 8.1–8.2, 10.2 | 4 |
| PFIND-6.1, 6.3 | 5 |
| PFIND-1.4–1.5, 7.6–7.7, 9.1–9.3 | 6 |

## Exit

Present this file and **STOP**.

Before `Status: Approved`:

1. User chooses `Execution-mode: continuous` or `story-unit`  
2. User approves this written plan  
3. Then set Status Approved and offer execute routes:
   - **`build-in-waves`** (continuous)  
   - **`build-by-story`** (story-unit)  
   - **`build-inline`** (either mode, no implementer subagents)

**Do not** set Approved while Execution-mode is `unset`.
