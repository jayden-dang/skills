---
name: inspect-change
version: 1.2.0
description: Use when a branch, PR, diff, or set of changes needs review before merging —
  produces a two-axis verdict (repo-standards conformance plus
  spec/requirements conformance, reported separately) — when build-in-waves
  reaches its final whole-branch review, or when the user asks to review work
  since some ref.
---

# Inspect Change

Review a diff on two independent axes, each run by its own subagent:

- **Standards** — does the code follow this repo's documented conventions and avoid the baseline smells?
- **Spec** — does the code implement what the requirements asked for, ID by ID?

The axes are deliberately separate because a change can pass one and fail the other: flawless code that builds the wrong thing, or a faithful implementation that tramples the repo's conventions. Merged reports let one axis mask the other.

## 1. Pin the range — fail fast

Take the base ref the caller supplied (a sha, branch, tag, or merge-base). Confirm it resolves — `git rev-parse <base>` — and that `git diff <base>...HEAD` is non-empty. A bad ref or empty diff must fail HERE, not inside two parallel subagents. Also capture `git log <base>..HEAD --oneline`. If no base was given, ask. *Done when: the ref resolves and the diff is non-empty.*

## 2. Locate the spec

Find the governing requirements, in order:

1. A `docs/specs/<date>-<feature>/requirements.md` matching the branch, feature
   name, or INDEX feature code for paths in the diff.
2. A path the caller handed you.
3. Otherwise ask the user. If they confirm no spec exists, skip the Spec axis and say so in the final report.

(Commit trailers are not required carriers of requirement IDs — docs-only spine.)

*Done when: you hold a requirements.md path, or an explicit "no spec".*

## 3. Gather the standards sources

Collect whatever documents how code here should be written: CLAUDE.md, lint and formatter configs, CONTRIBUTING-style docs, plus CONTEXT.md for the repo's canonical vocabulary. Prefer **`docs/standards/`** (INDEX + applicable domain files) when present; IF only unmigrated `docs/product/guidelines.md` remains, use it as legacy fallback; IF guidelines is pointer-only, follow its links to `docs/standards/`. If `docs/agents/project.md` is missing, note it and suggest running `configure-repo`, then proceed with what exists. When `## Team` is present with a non-empty **roster** or band override, read **band** and **packaging** from that section: dual-axis review always; Solo report addresses the solo author; Small/Multi emphasize path ownership using ownership notes when present. Missing Team → pre-feature default.

**System-docs suggest:** IF standards are missing and the Standards axis lacks house rules, follow `skills/project/define-system-doc/consult-recipe.md` — suggest once `/define-system-doc standards/INDEX` (or testing/errors-logging); never auto-invoke.

On top of the repo's own documents, the Standards axis always carries `standards-baseline.md` (beside this file) — twelve code-quality smells that apply even when the repo documents nothing, plus a Security section and a Production-readiness section, each scoped by its own predicate — the file states them, and the Standards brief in step 4 is where they bind. Two rules bind it: a documented repo standard always overrides the baseline, and every baseline hit is a labeled judgment call, never a hard violation. Skip anything tooling already enforces — a reviewer repeating the linter is noise. *Done when: the source list and the baseline path are in hand.*

## 3a. Check for duplication against existing features

For the diff's changed source files (from the range pinned in step 1), REQUIRED
SUB-SKILL: use `load-subgraph` with those paths and optional key terms from the
diff/PR summary so P0 and P1 both contribute. Hold neighbor **cards** from schema
1.1 fields (`path_evidence`, `term_evidence`, `via_traces`); surface
**`owns_coverage`**. **Grounded claims** (one home): follow
`skills/execution/load-subgraph/references/grounded-claims.md` for every conclusion
from the package (including reuse-miss for Spec).
*Done when: you hold the overlapping features' cards, or an explicit "no overlap"
with emptiness/coverage stated per grounded-claims.md.*

## 3b. Invariant conformance (advisory)

When `docs/architecture/` exists, REQUIRED SUB-SKILL: use `review-invariants` on the diff — it returns a per-`Respects: ARCH-N` verdict (respects / violates / unclear). Hold the violates/unclear verdicts for step 5. This lane is advisory by construction and stays OUT of the two hard axes — it never becomes a merge blocker. If `docs/architecture/` does not exist, skip this step and inject nothing. *Done when: you hold the invariant verdicts, or an explicit "no spine".*

## 3c. Codebase navigation docs (optional context)

**Applicability:** diff paths intersect modules, ownership, or dependency surfaces in
standing nav docs. **Load:** `skills/project/define-system-doc/consult-recipe.md`.

**Paths:** `docs/codebase/modules.md`, `ownership.md`, `dependencies.md`.

**When Approved:** advisory Spec/Standards context only — flag conflicts with documented
boundaries/ownership/deps as advisory findings (not a hard merge gate by themselves).
Ownership docs are **not** access-control enforcement.

**When absent / non-authoritative:** CONTINUE (no-op). Suggest once
`/define-system-doc codebase/modules|ownership|dependencies` only when a missing
nav doc would clarify the review; never auto-invoke.

*Done when: nav context is held or an explicit no-op for absence.*

## 4. Dispatch both subagents in parallel

Send ONE message containing both dispatches so they run concurrently and neither pollutes the other's context. Both are **read-only**: no mutation of the working tree, index, HEAD, or branch state; to inspect another revision, use a temporary worktree (`git worktree add <tmpdir> <sha>`), never move HEAD. Keep each brief under 400 words. Never pre-judge findings in a dispatch — no "do not flag", no pre-rated severities.

**Standards subagent** gets: the diff command and commit list; the standards-source paths; the path to `standards-baseline.md`, which it MUST read first.

Its report is a fixed shape — four parts, in order, each part complete before the next:

- **(a) Documented standards** — every place the diff breaks a repo-documented rule, citing the document and rule. Include CONTEXT.md vocabulary drift (a diff that renames or re-terms a glossary concept is a finding).
- **(b) The twelve smells** — one verdict line per smell, numbered 1–12, **including the ones that did not hit**. Write the smell's name then `HIT` (naming it and quoting the hunk) or `no hit`. A part-(b) section with fewer than twelve verdict lines is incomplete and gets re-run.
- **(c) Security** — items 13–18, only for hunks crossing a trust boundary (untrusted input, secret handling, a privileged action). No boundary crossed → say so once and move on; do not manufacture findings.
- **(d) Production readiness** — items 19–24, only when the diff changes runtime behavior, storage, a contract, or configuration. Name the item and what an operator would see when it bites. Item 24 MUST be answered from a search of the repo **beyond the diff** — the readers it asks about live in files the diff does not touch, so a diff-only reading always returns a false clean.

Parts (c) and (d) are each scoped by their own predicate; a part that does not apply is reported as not applying, never silently dropped. Adding a later part never licenses shortening an earlier one — (b) is walked in full whether or not (c) and (d) fire. Documented breaches may be hard findings; baseline smells, security and production-readiness items are always judgment calls; the repo's documents override the baseline; skip anything tooling enforces.

**Spec subagent** gets: the diff command and commit list; the requirements.md path; the brief — walk the requirements and report (a) IDs that are missing or only partially implemented, (b) behavior in the diff no requirement asked for (scope creep), (c) IDs that look implemented but wrong; quote the requirement ID on every finding; also check that each covered ID has **behavior** covered by tests or acceptance evidence (domain-language tests — do **not** require ID tags in test source). When step 3a found overlapping features, the Spec subagent ALSO receives those neighbor cards (owned paths + Out-of-Scope) as context, and its brief directs it to flag — as a **reuse-miss** finding citing the neighbor's feature code — any place the diff reimplements behavior a shares-surface neighbor already owns.

*Done when: both reports are back.*

## 5. Aggregate

Present the reports under `## Standards` and `## Spec` headings — lightly cleaned at most. Do NOT merge, dedupe across axes, or rerank one axis's findings against the other's; that reranking is exactly what the separation prevents. When step 3b produced invariant verdicts, present them under a separate `## Invariants (advisory)` heading — a third lane, never merged into or reranked against Standards/Spec.

Every finding carries: severity (Critical / Important / Minor), file:line, why it matters, and a suggested fix unless obvious.

End with the verdict:

```
Ready to merge? Yes | No | With fixes
[1–2 sentences of technical reasoning]
```

Then the **banked** slot. Where the verdict ships with **Minor** findings nobody will action on this branch, those findings exist nowhere but this report. For **each** such Minor emit this block — same slot names as `record-debt`'s **The entry**, except the heading has **no** `DEBT-N` (`/record-debt` stamps the ID). Name `/record-debt` for the user to run. Critical and Important are never banked.

```
### `<path>` — <one-line finding>

- **Found:** `<YYYY-MM-DD>` · inspect-change on `<branch or range>`
- **Cost:** <what this makes harder or riskier, concretely>
- **Deferred because:** unactioned Minor on this branch
- **Fix shape:** <one line | Unknown>
- **Ticket:** none
- **Status:** open
```

A slot with no answer gets `Unknown` — never omit the line. "Just list the leftovers" / "don't invent a ledger format" is not a skip of these slots. Minting `**DEBT-N**` here is a collision; do not.

*Done when: both axis sections, the verdict, and the banked slot are delivered — banked as "none to bank" when no Minor survives unactioned.*

## Inline fallback (no subagent capability)

No subagent capability in this harness? Run the two axes yourself, sequentially, in one context: **Standards first** — read `standards-baseline.md`, walk the diff against each of its twelve smells, the Security section, and the Production-readiness section — then **Spec** — walk the requirements ID by ID. Finish and record one axis completely before starting the next, and still present them under separate `## Standards` and `## Spec` headings without reranking one against the other. This loses the context isolation two subagents provide, so the discipline of closing out one axis before opening the next is what keeps them from bleeding together.
