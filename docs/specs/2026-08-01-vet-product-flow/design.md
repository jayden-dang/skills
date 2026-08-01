# Design: Vet product flow

Feature code: VPF
Status: Approved
Date: 2026-08-01
Requirements: ./requirements.md

## Context

Today the acceptance chain is **author → (optional) dogfood**: `review-product-flow`
writes `.skills/<slug>-review-product-flow.json` and renders HTML; `run-product-walkthrough`
drives cases with FE+BE evidence. Authoring already has a §1 coverage gate and a
§4 “count kinds” self-check — both run in the **same session that wrote the cases**.
Under pressure that check rubber-stamps; dogfood then invents missing real-user
situations mid-run. DFSYNC fixed *where verdicts live*, not *whether the guide
mapped the shipped surface before drive*.

The binding constraint is the product claim: this is an **implementation-surface
judgment** with **code-grounded** missing-situation findings, not an ARCH-1
vertical check. Selling schema/kind counts as “complete for real users” would
create false confidence (Production posture + ARCH-1). The alternative rejected
by discovery is therefore CLI-first completeness or a longer same-agent §4. The
second shaping constraint is **isolation**: judgment must not share authoring
context; `inspect-change` is the peer pattern (fresh subagent / sequential
axis-close fallback), not `audit-trace`.

A third constraint is operational: dogfood must not re-vet every time `rev`
moves for human ticks or agent marks. Freshness therefore keys off an
**authored-cases fingerprint**, not the whole-file `rev` (which bumps on any
store write). Override remains explicit named consent, same shape as non-local
origin in `run-product-walkthrough`.

### Architecture invariants relied on

- **ARCH-1** — this skill is *not* a vertical check; design must never claim
  mechanical completeness as the product outcome. Fingerprint freshness and
  report presence *are* exact file/read recipes; the map itself is judgment.
- **ARCH-3** — no new mandatory consumer tooling; pure SKILL.md + markdown
  report under `.skills/`; optional later CLI hygiene stays out of v1 claim.
- **ARCH-5** — model-invoked skill; may name other model-invoked skills
  (`root-cause`, `test-first`); must not auto-invoke user-invoked skills.
- **ARCH-4** — criterion ids `VPF-N.M` immutable; finding ids `VPF-N` (integer
  only) are a separate namespace.

## Decisions

1. **New model-invoked skill `vet-product-flow`** at
   `skills/acceptance/vet-product-flow/` — judgment peer of
   `run-product-walkthrough`, not a CLI product surface.
2. **Product claim = implementation-surface map** with hard code-grounding;
   non-claims (novelty, feel, chaos, speculative design, global stamps) are
   first-class skill body sections, not footnotes.
3. **Hard dogfood gate** — fresh report + zero open findings, or explicit
   in-thread yes that **names** each remaining open finding. Severity orders
   fixes only.
4. **Freshness = authored-cases fingerprint**, not `rev`. Report stores
   `run_file`, `cases_fingerprint`, `stamped_at`, `pass_kind`, prior report
   path on re-check. Walkthrough recomputes fingerprint from the run file
   before drive; mismatch ⇒ not fresh.
5. **Isolation protocol** mirrors `inspect-change`: preferred read-only
   subagent with a brief; inline fallback = closed authoring boundary +
   separate judgment pass (not §4 extension). Skill never writes the run file.
6. **Guide-gap loop** lives in controller / author re-entry; large rewrites
   escalate to fixer subagent (≥5 findings or ≥2 ability areas); max 2 re-vet
   cycles then human. Product-defect dogfood loop is a **separate** patch to
   `run-product-walkthrough` failure routing (master re-test, subagent
   `root-cause`).
7. **Author hand-off (VPF-4.1)** names/invokes vet at §5 hand-over; it does
   **not** replace the VPF-5.x drive gate (isolation gate is walkthrough-side).
8. **Finding id stability** uses a `surface_key` string per miss; re-check
   reuses `VPF-N` when the same `surface_key` is still open. → ADR for judgment
   gate vs ARCH-1 confusion.

Decisions 1–4 are hard to reverse and surprising without context → **ADR-0009**.

## Architecture

### 1. Skill package — `vet-product-flow`

Satisfies: VPF-1.1, VPF-1.2, VPF-1.5, VPF-2.1, VPF-2.2, VPF-2.3, VPF-2.4, VPF-2.5, VPF-2.6, VPF-3.1, VPF-3.2, VPF-3.3, VPF-3.4, VPF-3.5, VPF-6.7
Reuse: none — new code (rung 7); patterns borrowed from `inspect-change` isolation and `vet-feedback` prove-against-code, but the skill package itself is new
Respects: ARCH-1, ARCH-3, ARCH-5
Interface: invoke with run-file path (+ optional triad paths); output = report path; never mutates product code or run file
Depth: if this package vanished, callers must still know: “map shipped user-observable surfaces to cases; write findings report; stay read-only”
Locality: new under `skills/acceptance/vet-product-flow/`; leave review-product-flow CLI; extend inventory docs only

**Layout**

```
skills/acceptance/vet-product-flow/
  SKILL.md
  references/
    report-schema.md      # report fields + fingerprint recipe
    judgment-brief.md     # subagent brief template
```

**SKILL.md body (imperative checklist)**

1. **Inputs** — require run-file path; load JSON; refuse if missing/invalid (point
   author back to `review-product-flow`, do not invent cases). Optional:
   `docs/specs/<feature>/requirements.md` (and design/tasks when present) for
   OOS/persist triad evidence only.
2. **Isolation** — dispatch read-only subagent with `references/judgment-brief.md`
   filled (run path, fingerprint, triad paths, and concrete product paths from
   the feature `design.md` / tasks / known app layout — not a fictional
   “source roots” field in `project.md`). Subagent returns by writing the
   report file (or returning full report text for controller to write verbatim —
   either way controller does not re-judge content). Writing the **vet report**
   is allowed; product code and the run file stay unmodified.
3. **Inline fallback** (no subagents): controller states out loud
   `AUTHORING CLOSED — starting isolated vet-product-flow pass`, loads only the
   brief inputs, and runs the map steps below. Forbidden: continuing from open
   case-authoring todos, “just also count kinds,” or declaring clean without a
   report file.
4. **Surface map procedure** (judgment):
   - Enumerate **user-observable** paths/states from **opened** product code
     (routes, primary actions, empty/error/role UI actually rendered).
   - For each surface, search the run file for a corresponding case
     (setup/try/expect/kind — judgment match, not string equality only).
   - Missing → finding with `surface_key`, severity, situation prose, evidence
     `path` / symbol / route citations the reviewer opened.
   - Skip candidates never inspected (VPF-2.4).
   - Do not emit non-claim categories (story 3).
5. **Hygiene note (optional, non-blocking for product claim):** may list
   “author §1 hygiene observations” under a separate report section that
   **does not** create open missing-situation findings and **does not** affect
   the gate. Never title that section “complete for real users.”
6. **Write report** per report module; exit by handing path + open_count to
   caller (author fix loop or walkthrough gate).

**Rationalization table** (skill body must include): same-agent self-check;
CLI completeness; inventing chaos; “users will want”; global stamps; writing
run file from vet.

### 2. Report artifact and fingerprint

Satisfies: VPF-1.3, VPF-1.4, VPF-8.1
Reuse: none — new code (rung 7); markdown report + exact hash recipe (stdlib `hashlib` when tested); no new consumer runtime dependency
Respects: ARCH-1 (fingerprint recipe is exact), ARCH-4 (finding id namespace)
Interface: path `.skills/<slug>-vet-product-flow.md`; fields listed below; gate and re-check **read** this shape
Depth: if the report format vanished, callers need only “path, fingerprint of authored cases, open VPF-N findings with evidence, surface_key→id map”
Locality: `.skills/` only (gitignored ephemera); schema doc in skill package

**Fresh stamp fields (pinned)**

| Field | Meaning |
|---|---|
| `slug` | Run slug |
| `run_file` | Path to the JSON run file (repo-relative) |
| `cases_fingerprint` | SHA-256 hex of canonical authored content (below) |
| `stamped_at` | ISO-8601 UTC when this pass finished |
| `pass_kind` | `initial` \| `re-check` |
| `prior_report` | Path of previous report on re-check, or `—` |
| `open_count` | Integer count of open missing-situation findings |
| `gate_hint` | `clean` if open_count=0 else `blocked` (informational; walkthrough re-reads findings) |

**Authored-cases fingerprint recipe** (exact — agents and tests use the same):

1. Parse run JSON.
2. Build a JSON array of sections, each `{ "name": <section.name>, "cases": [ … ] }`
   where each case includes **only** the eight authored slots as a JSON object
   with **sorted keys** (ASCII sort): `backend`, `expect`, `id`, `kind`, `req`,
   `setup`, `title`, `try`.
3. Omit `run`, `human`, top-level `rev`, and any other keys.
4. Serialize the array with compact separators (`,`, `:`) and no trailing
   whitespace; section objects use sorted keys (`cases`, `name`).
5. `cases_fingerprint = sha256(utf-8 bytes).hexdigest()`.

Any authoring edit (add/reshape case) changes the fingerprint → prior report is
not fresh. Verdict marks and human ticks do **not**.

**Finding block shape**

```markdown
### VPF-3
- **status:** open
- **severity:** Important
- **surface_key:** `ui:settings/empty — no rows`
- **situation:** Settings list already renders empty-state copy when zero rows; guide has only happy create/list.
- **evidence:** `src/pages/Settings.tsx:88` (EmptyState), route `/settings`
```

On re-check: still-open same `surface_key` keeps the same `VPF-N`; new misses get
next free integer; resolved misses move to `## Cleared this pass` with prior id
(or simply omit from open list — skill documents that open list is authoritative
for the gate; cleared section is audit trail).

**Id allocation:** scan prior report (if any) for max `VPF-N` and
`surface_key`→id map; reuse; assign max+1 for new keys. Criterion ids remain
`VPF-N.M` — greppable distinction is the `.M` segment.

### 3. Author hand-off — `review-product-flow` §5

Satisfies: VPF-4.1, VPF-4.2, VPF-4.3
Reuse: rung 2 — extend existing hand-over section only
Interface: after artifacts on disk, next required step is `vet-product-flow` (path named); then human guide / serve / (later) walkthrough
Depth: n/a — extends `review-product-flow`
Locality: extend `skills/acceptance/review-product-flow/SKILL.md` §5; leave §1–4 substance; leave CLI

Replace “if the agent should run the guide, name `run-product-walkthrough`”
with ordered hand-off:

1. Paths (run file + HTML) + 30s first pass + degraded notes (unchanged).
2. **Required next:** `vet-product-flow` on the run file (invoke when model-invoked
   conditions match; otherwise instruct). Do not treat the guide as ready for
   agent dogfood until vet has produced a report.
3. Optional `serve` for human-beside-agent (unchanged).
4. Agent dogfood: name `run-product-walkthrough` **only after** clean vet report
   or named override (walkthrough still enforces the gate).

§1 coverage self-check remains; it is not a substitute for vet (rationalization
row). Description frontmatter may mention that dogfood is gated by vet — keep
triggers for authoring vs walkthrough distinct.

### 4. Hard gate — `run-product-walkthrough` preconditions

Satisfies: VPF-5.1, VPF-5.2, VPF-5.3, VPF-5.4, VPF-5.5, VPF-5.6, VPF-6.1
Reuse: rung 2 — extend §1 Preconditions (or new §0/§1a before seed)
Respects: ARCH-1 (freshness check is file recipe), ARCH-5
Interface: before **any product case is driven** (before §3 drive loop; after
  origin consent may run in parallel but gate fails closed before first product
  click): report path, fingerprint match, open_count=0 or named override on record
Depth: n/a — extends `run-product-walkthrough`
Locality: extend `skills/acceptance/run-product-walkthrough/SKILL.md`; leave Iron Law / mark rules

**Gate algorithm (skill prose, agent-executed)**

```
REPORT = .skills/<slug>-vet-product-flow.md
IF missing REPORT → STOP (run vet-product-flow)
Parse REPORT: run_file, cases_fingerprint, open findings
IF run_file path ≠ this RUN (normalized) → STOP
IF sha256(authored cases of RUN) ≠ cases_fingerprint → STOP (stale; re-vet)
IF open findings non-empty:
  IF chat has explicit user yes naming EACH open VPF-N id → proceed
     (append override line to .skills/progress.md or the walkthrough close notes:
      "VPF override: VPF-1, VPF-4 named by user <timestamp>")
  ELSE → STOP (list open findings; point to guide-gap loop)
ELSE → proceed (origin/app preconditions remain mandatory before product clicks)
```

`init` may seed pending verdicts before or after the gate, but **no product
click and no `mark` of a driven case** until the gate passes. Severity never
drops a finding from the open set for gate purposes.

### 5. Guide-gap fix loop (controller + optional fixer)

Satisfies: VPF-6.2, VPF-6.3, VPF-6.4, VPF-6.5, VPF-6.6
Reuse: none — new code (rung 7); borrows fixer-brief pattern from `build-in-waves` and run-file edit ownership from `review-product-flow`, but the loop protocol is new skill prose
Interface: inputs = open findings + run path; outputs = patched run file + new report; caps = 2 re-vet cycles
Depth: if vanished, callers need “patch cases by severity → re-vet isolated → max 2 → human”
Locality: primarily skill prose in `vet-product-flow` (fix loop section) + short cross-link from walkthrough when gate fails; leave product code

| Step | Owner |
|---|---|
| Order by severity | controller |
| Patch run file + `render` | controller, or fixer subagent when ≥5 findings **or** ≥2 ability-area rewrites |
| Fresh `vet-product-flow` | always isolated (new subagent / new closed pass) |
| Clear finding | only absent from new open list or named override |
| After 2 cycles still open | stop for human |

Fixer brief path: `.skills/<slug>-vpf-fix-brief.md` (finding set + run path +
evidence pointers). Fixer must not self-declare clean.

### 6. Product-defect isolation during dogfood

Satisfies: VPF-7.1, VPF-7.2, VPF-7.3, VPF-7.4, VPF-7.5
Reuse: rung 2 — extend `run-product-walkthrough` §4 Failure routing; `root-cause` + `test-first` unchanged
Interface: master keeps drive/mark/re-test; subagent gets red-capable brief only
Depth: n/a — extends walkthrough failure routing
Locality: `run-product-walkthrough/SKILL.md` §4; leave vet skill out of product patches

Change the product-defect row:

| Observation | Action |
|---|---|
| Deterministic product defect | Master marks fail with evidence. Dispatch **subagent** with brief: case id, req, try/expect, saw/server, repro. Subagent runs **`root-cause`** (+ test-first). Master does **not** patch product in the long dogfood context. On DONE: master re-drives failed case + related already-pass per existing rules. |

Guide-wrong row stays master-side run-file edit (not root-cause). Explicit:
guide-gap findings from vet are **not** routed here — gate should have blocked
drive; if a miss is discovered mid-run, treat as guide wrong / re-enter vet, not
as product defect.

### 7. Inventory, glossary, trigger routing

Satisfies: (packaging for VPF-1.1 discoverability — no separate behavioral IDs)
Reuse: rung 2 — existing AGENTS / architecture / trigger test patterns
Interface: skill name appears in acceptance inventory; trigger scenarios distinguish author / vet / walkthrough / validate-ui
Depth: n/a
Locality: extend `AGENTS.md`, `docs/architecture/skills.md`, `docs/architecture/system.md`, `README.md` acceptance tables, `docs/guide/skills/` if present, `tests/trigger/*`; leave Personal OS package

Optional `CONTEXT.md` terms: **vet report**, **missing-situation finding**,
**cases fingerprint** — written when skill ships (define-domain side effect).

## Seams for testing

This feature is almost entirely skill/prose + markdown artifacts. Prefer
scenario and contract tests already used by walkthrough/routing — **no new
Python runtime seam** for the product claim.

| Seam | Kind | Covers |
|---|---|---|
| Skill frontmatter + path contract (`skills/acceptance/vet-product-flow/SKILL.md` exists; `name: vet-product-flow`) | unit / source contract | VPF-1.1 |
| Report schema + fingerprint recipe fixtures (`tests/vet-product-flow/` golden JSON → expected sha; report markdown required fields) | unit | VPF-1.3, VPF-1.4, VPF-5.1, VPF-8.1 |
| Scenario: isolation (subagent brief / inline fallback forbids same-session §4 clear) | scenario markdown | VPF-1.2, VPF-1.5 |
| Scenario: surface map + evidence required / refuse non-claims | scenario | VPF-2.1–2.6, VPF-3.1–3.5, VPF-6.7 |
| Scenario: author hand-off names vet before dogfood | scenario / trigger | VPF-4.1–4.3 |
| Scenario: walkthrough gate (missing/stale/open/named override) | scenario | VPF-5.1–5.6, VPF-6.1 |
| Scenario: guide-gap loop (patch → re-vet; escalate ≥5; 2-cycle stop) | scenario | VPF-6.2–6.6 |
| Scenario: dogfood defect subagent + master re-test; loops separate | scenario | VPF-7.1–7.5 |
| Trigger routing matrix (author vs vet vs walkthrough vs validate-ui) | scenario | VPF-1.1, VPF-4.1, VPF-5.1 |
| Grep inventory: AGENTS + architecture skills list include `vet-product-flow` | unit / source contract | packaging |

Fingerprint unit tests are pure Python over fixture run files (stdlib `hashlib`)
— optional small `tests/test_vet_product_flow_fingerprint.py` implementing the
recipe once so scenarios and docs do not drift. That is the only optional new
code seam; skill bodies remain the behavior SSOT.

## Coverage check

Every requirement ID appears in exactly one `Satisfies:` line:

| Story | IDs | Module |
|---|---|---|
| 1 | 1.1, 1.2, 1.5 | Skill package |
| 1 | 1.3, 1.4 | Report artifact |
| 2 | 2.1–2.6 | Skill package |
| 3 | 3.1–3.5 | Skill package |
| 4 | 4.1–4.3 | Author hand-off |
| 5 | 5.1–5.6 | Hard gate |
| 6 | 6.1 | Hard gate |
| 6 | 6.2–6.6 | Guide-gap fix loop |
| 6 | 6.7 | Skill package |
| 7 | 7.1–7.5 | Product-defect isolation |
| 8 | 8.1 | Report artifact (id stability via surface_key map) |

No deliberately unmapped IDs. No ID in two Satisfies lines. NFR None attributes need no Satisfies.
