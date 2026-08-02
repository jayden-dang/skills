# Design: Docs-only spine

Feature code: DOSP
Status: Approved
Date: 2026-08-02
Approved: 2026-08-02 (user)
Requirements: ./requirements.md

## Context

Today the pack treats a requirement ID as a greppable string that must appear
not only in the spec triad but also in **tests and commit trailers**. The
`audit-trace` skill encodes that contract as finding **E2** (Implemented/Shipped
ID has no test-file hit) and as pass 4 grepping application/test trees. Teach
paths (`AGENTS.md`, `configure-repo`, implementer prompts, guide examples,
package-change / cut-release) all reinforce ID-in-code. That works for a
skill-native solo repo; it fails for multi-skill teams (mailgate-class) where
only some agents adopted the pack and shared code must read as domain code.

The binding constraint is **consumer-code purity**: process artifacts stay in
`docs/specs/**` and `.skills/<CODE>/`; application source and test source are
not carriers of skill-set IDs. The alternative ruled out is keeping E2 under a
per-repo flag (`TraceMode: full|docs-only`) — user locked a single docs-only
reshape for the pack, not dual modes.

Horizontal ownership already does not need code-side IDs: **FSUB /
`load-subgraph`** derives OWNS/OVERLAPS from `**Files:**` and INDEX. Execute-family
**Spec** review already walks `_Requirements:` against the diff. This feature
**narrows** the vertical check and **rewrites doctrine**, and adds **comment
discipline** so agents stop littering production with narrating / process
comments.

### Architecture invariants relied on

- **ARCH-1** — audit-trace remains fixed `grep`/set ops (now over docs only).
- **ARCH-2** — missing `docs/specs/` still no-ops.
- **ARCH-3** — no new consumer tooling; markdown skill edits only.
- **ARCH-4** — **revised by this feature** (DOSP-5.2): immutability + greppable
  citation for docs-side carriers only (not tests/trailers).
- **ARCH-5 / ARCH-6** — unchanged; no new user-invoked skill.

## Decisions

1. **Single pack posture: docs-only vertical** — no `TraceMode` dual path; E2
   and test greps deleted everywhere (skill body, tests that assert E2 exists,
   guide).
2. **Keep skill name `audit-trace`** — update description + finding table; avoid
   rename churn across prove-claim / cut-release / realign-spec callers.
3. **E1 scope = task citations only** (plus existing ARCH/decision passes) —
   strings in `*.rs` / `*.test.ts` never feed E1 or coverage.
4. **Implemented evidence (DOSP-3.2)** = tasks checked + docs-only audit-trace
   zero errors + prove-claim verify green — not ID-in-test. Spec dual-verdict
   remains judgment, not a new E-code.
5. **Remove `Implements:` / `Guards:` entirely** from plan-tasks, implementer
   prompts, package-change, cut-release. Changelog derives from specs in the
   release range (requirement text for features at Implemented/Shipped and/or
   task footers + conventional subjects) — procedure text in cut-release, not
   a new tool.
6. **Comment discipline is prompt + polish-diff + guidelines** — no new skill;
   positive default “zero comments unless hazard/invariant/why”.
7. **Skill-set product tests may still embed `CODE-N.M`** as fixtures testing
   pack parsers (DOSP-2.5) — documented exception; not taught as consumer
   convention.
8. **No consumer migration tool** for existing `/// REQ:` (Out of Scope) —
   stop teaching; cleanup is human/consumer schedule.
9. **ADR:** none new — ARCH-4 supersede-by-edit (strikethrough old wording + new
   bold ARCH-4) is the immutability-compatible way to change an invariant the
   pack owns; recorded as design Decision 9 / DOSP-5.2 work item, not a
   product ADR under `docs/adr/` unless authoring convention prefers one.
   Prefer **edit ARCH-4 in place with strikethrough of the obsolete clause**
   per architecture INDEX rules.

## Architecture

### 1. audit-trace reshape (docs-only)

Satisfies: DOSP-1.1, DOSP-1.2, DOSP-1.3, DOSP-1.4, DOSP-1.5, DOSP-1.6, DOSP-6.3, DOSP-7.1, DOSP-7.2
Reuse: rung 2 — extend existing `skills/execution/audit-trace/SKILL.md` (delete
  pass 4; rewrite E1/E2 rules; keep passes 1–3 and 5–6 + decision-record)
Respects: ARCH-1, ARCH-2, ARCH-3
Interface: same call sites (`prove-claim`, `cut-release`, `realign-spec`,
  `plan-tasks`); finding set without E2; inputs = specs (+ architecture +
  decisions); output = counts + findings. Callers learn nothing about test trees.
Depth: n/a — extends audit-trace
Locality: extend `skills/execution/audit-trace/**`; extend
  `tests/test_audit-trace_scope.py` and any scenario that asserts E2;
  leave load-subgraph; leave record-verdict validator invoke

**Concrete edits**

| Area | Change |
|---|---|
| Frontmatter `description` | “defined and task-cited in docs/specs” — drop “covering test” |
| Pass 4 (test coverage) | **Delete** entire section and default test roots |
| E1 | `taskCited \ defined` only (remove `testCovered` union) |
| E2 | **Delete** from table, rules, status obligations table |
| Status table | Approved → W1 only; Implemented/Shipped → no test column |
| Output example | No E2 line; counts drop “tested / test files” |
| Decision-record section | Unchanged (DOSP-6.3) |
| NON-NEGOTIABLE block | Rewrite “coverage is textual presence in tests” → “task citation integrity is textual; do not judge whether a task *really* implements the REQ” |

**Pack unit tests**

- Update `tests/test_audit-trace_scope.py`: `AUDIT TRACE_FINDINGS` no longer
  includes `E2`; assert skill body has no test-coverage pass / no E2 emission rule.
- Add fixture/scenario: fake ID only in a synthetic test-like path under fixtures
  → no E1; same ID on `_Requirements:` → E1.

### 2. Execute family + test-first + plan-tasks (no ID-in-tests)

Satisfies: DOSP-2.1, DOSP-2.2, DOSP-3.1, DOSP-3.3, DOSP-6.2
Reuse: rung 2 — extend implementer / reviewer prompts and plan-tasks coverage
  check
Respects: ARCH-4 (post-revise)
Interface: implementer still receives `_Requirements:` IDs and must satisfy
  them behaviorally; tests describe domain behavior without embedding IDs;
  Spec reviewer still cites IDs on findings (in **review prose**, not in product
  source).
Depth: n/a — extends execute / plan-tasks
Locality: extend
  `skills/execution/build-in-waves/implementer-prompt.md`,
  `task-reviewer-prompt.md`,
  build-by-story / build-inline equivalents,
  `skills/execution/test-first/SKILL.md` (or agents path),
  `skills/spec/plan-tasks/SKILL.md`,
  `templates/tasks.md` (remove Implements trailer step examples)

**plan-tasks**

- Coverage check: every Approved live ID in a `_Requirements:` footer; **remove**
  “ID must appear in a test annotation inside steps”.
- Task commit steps: no `Implements:` trailer instruction.
- Steps may still say “write failing test for &lt;behavior&gt;” without embedding
  `CODE-N.M` in the test source snippet.

**Implementer prompts**

- Remove “every test carries its requirement ID”.
- Add: tests assert observable behavior; map to brief REQs in the **report**,
  not in source.
- Add naming rule: do not name tables/modules/APIs after feature codes
  (DOSP-2.2).
- Add comment default zero (wired to module 4).

**Spec reviewer prompts**

- Keep Spec Compliance walk of brief IDs vs diff (DOSP-6.2).
- Quality axis: drop “does each test carry its requirement ID?”; keep edge-case
  coverage judgment.

### 3. Ship path — trailers out, changelog from specs

Satisfies: DOSP-2.3, DOSP-2.4
Reuse: rung 2 — extend package-change + cut-release
Locality: extend `skills/ship/package-change/**`, `skills/ship/cut-release/SKILL.md`;
  update `tests/package-change/**`, `tests/test_prepare_change_contract.py`
Interface: package-change no longer collects/preserves Implements/Guards as
  required trailers; cut-release groups changelog by scanning
  `docs/specs/**/requirements.md` Status + requirement prose for features
  touched in range (prefer: commits’ paths → load-subgraph / Files / INDEX →
  feature codes → live criteria text). Fallback: conventional commit subjects
  under Misc when no spec bind.

**cut-release procedure (design)**

1. Collect `git log <last-tag>..HEAD` (subjects + paths).
2. Map changed paths → feature CODEs via INDEX + tasks `**Files:**` when
   available (reuse load-subgraph blast_radius / OWNS optional; if thin, use
   commit message / path heuristics).
3. For each CODE with Status Implemented or Shipped (or tasks completed in
   range), list **behavior bullets** from live bold criteria text (not IDs as
   primary headline — ID may appear parenthetically optional for skill-native
   readers, but subject lines stay domain language).
4. No trailer parse step.

**package-change**

- Delete rationalization that IDs belong in trailers.
- Advisory commit map: subjects explain change; no trailer field required.
- Update PCHG scenarios that lock Implements-only placement of IDs → IDs only
  in specs/process artifacts, never commits.

### 4. Comment discipline

Satisfies: DOSP-4.1, DOSP-4.2, DOSP-4.3, DOSP-4.4
Reuse: rung 2 — extend implementer prompts, polish-diff, guidelines
Locality: extend `skills/review/polish-diff/SKILL.md` (or agents path),
  execute implementer prompts (module 2), `docs/product/guidelines.md`
Interface: rule set below; polish-diff step “strip narrating/process comments”

**Rule set (positive first)**

- Default: write **no** new comments.
- Allowed: non-obvious invariant, hazard, protocol/wire constraint, or “why
  not the obvious alternative” that the code alone does not show.
- Forbidden: restate next line; narrate control flow; cite `CODE-N.M` / feature
  code; “as per plan/spec”; TODO that only restates the task.

**polish-diff**

- New checklist item: scan diff hunks for comments matching forbidden list;
  delete or rewrite to allowed class; never invent long essay comments.

**guidelines.md**

- New bullets under Coding standards mirroring the rule set so plan-tasks
  Global Constraints can cite them.

### 5. Doctrine surface (AGENTS, ARCH, CONTEXT, guide, configure-repo)

Satisfies: DOSP-2.5, DOSP-5.1, DOSP-5.2, DOSP-5.3, DOSP-5.4, DOSP-5.5, DOSP-5.6
Reuse: rung 2 — edit existing doctrine files
Respects: ARCH-4 (after revise), ARCH-1
Locality: extend AGENTS.md, CONTEXT.md, docs/architecture/{INDEX,artifacts}.md,
  docs/guide/concepts/{requirement-ids,traceability}.md, examples, process
  pages, resources/scripts.md, skills/setup/configure-repo, templates/agents/project.md,
  docs/agents/project.md (this pack’s config)
Interface: single narrative — “IDs live in docs/specs; tests prove behavior;
  paths prove ownership; Spec review proves match”

**ARCH-4 rewrite (substance)**

- Strike obsolete: “every task, test, commit trailer, and Respects: line MUST
  use the same greppable string…”
- Live: “Requirement IDs (`CODE-N.M`) and architecture IDs (`ARCH-N`) are
  immutable once defined: never renumber or reuse; retire only by
  strikethrough; every **docs-side** citation (`Satisfies:`, `_Requirements:`,
  `Respects:`, and bold definitions) MUST use the same greppable string as the
  definition. Application source and tests MUST NOT be required to embed these
  IDs.”

**configure-repo / project.md template**

- Remove mandatory “Test annotation conventions” interview that exists only
  for code-side audit-trace.
- Optional note: “Legacy annotations in consumer code are ignored by
  audit-trace; do not add new ones.”
- Drop audit-trace test-glob configuration as **coverage** input (may keep
  specsDir only).

**CONTEXT.md**

- Requirement ID definition: first-class object in the **spec triad** (and
  optional issues), not “tests, commits, and changelog” as required carriers.
  Changelog may still *look up* IDs from specs.

**Guide**

- Rewrite requirement-ids.md, traceability.md, tier examples, scripts.md
  audit-trace section; grep-clean `Implements:` and `/// REQ` teaching patterns
  under `docs/guide/`.

### 6. prove-claim + realign-spec (Implemented evidence)

Satisfies: DOSP-3.2, DOSP-3.4
Reuse: rung 2 — extend claim tables and status transition tables
Locality: `skills/execution/prove-claim/SKILL.md` (or agents path),
  `skills/track/realign-spec/SKILL.md`
Interface: “requirements met” = docs-only audit-trace clean + criteria vs
  observed behavior; Implemented flip per DOSP-3.2 without E2

**realign-spec**

- Status table: remove “audit-trace shows every live requirement covered by a
  test”; replace with DOSP-3.2 evidence list.

**prove-claim**

- Claim row “Requirements met” still REQUIRES SUB-SKILL audit-trace (docs-only)
  + per-criterion observation; green tests alone still insufficient (DOSP-3.4).

### 7. Guards — FSUB / Spec / decisions (leave)

Satisfies: DOSP-6.1
Reuse: rung 2 — leave load-subgraph and map-features bodies; only cross-link
  guide if doctrine pages mention “IDs in code”
Locality: leave `skills/execution/load-subgraph/**`, `skills/track/map-features/**`
  unless a single sentence in guide cross-ref needs update (covered in module 5)
Interface: unchanged
Depth: n/a
Locality: leave

## Seams for testing

This feature ships markdown skill/doctrine changes. Seams are **pack unit tests
and scenarios** that lock prose contracts (same pattern as FSUB/PCHG).

| Seam | Kind | Covers |
|---|---|---|
| `tests/test_audit-trace_scope.py` — findings set excludes E2; skill has no test-coverage pass | unit | DOSP-1.1–1.6, 7.1 |
| Fixture: ID only in fake test path → no E1; ID on `_Requirements:` unknown → E1 | unit / scenario | DOSP-1.2, 1.4 |
| Fixtures for E3/W1/W2/E4/E5/W3 still green | unit | DOSP-1.5, 6.3, 7.2 |
| Source contract: implementer prompts lack “test carries requirement ID”; contain comment default-zero | unit | DOSP-2.1, 3.3, 4.1, 4.2 |
| Source contract: plan-tasks coverage has no test-annotation requirement; no Implements trailer step | unit | DOSP-2.3, 3.1 |
| Source contract: package-change / cut-release no mandatory Implements | unit | DOSP-2.3, 2.4 |
| package-change scenarios updated (IDs not in commits) | scenario | DOSP-2.3 |
| Source contract: AGENTS.md / ARCH-4 / guidelines comment rules / configure-repo no annotation mandate | unit | DOSP-2.2, 2.5, 4.4, 5.1–5.5 |
| Source contract: prove-claim / realign-spec Implemented evidence without E2 | unit | DOSP-3.2, 3.4 |
| Source contract: polish-diff has comment-discipline step | unit | DOSP-4.3 |
| Grep guide for retired teaching (`Implements:`, “/// REQ” as required) empty or legacy callouts only | unit / scenario | DOSP-5.5 |
| FSUB load-subgraph skill body unchanged (hash or “no edit” scenario) | scenario | DOSP-6.1 |
| Spec reviewer prompts still walk requirement IDs | unit | DOSP-6.2 |

Ideal **new** seam count: one small unit module `tests/test_dosp_docs_only_spine.py`
(source contracts) + audit-trace fixture updates — not a new runtime library.

## Coverage check

| IDs | Module |
|---|---|
| DOSP-1.1–1.6, 6.3, 7.1, 7.2 | 1 audit-trace reshape |
| DOSP-2.1, 2.2, 3.1, 3.3, 6.2 | 2 execute + plan-tasks |
| DOSP-2.3, 2.4 | 3 ship path |
| DOSP-4.1–4.4 | 4 comment discipline |
| DOSP-2.5, 5.1–5.6 | 5 doctrine surface |
| DOSP-3.2, 3.4 | 6 prove-claim / realign-spec |
| DOSP-6.1 | 7 FSUB leave |
| Security None, Accessibility None | no module (explicit None) |

Deliberately unmapped: none.

**Count:** behavioral+NFR IDs all assigned (Security/A11y None excluded).
