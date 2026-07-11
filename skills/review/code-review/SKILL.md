---
name: code-review
description: Use when a branch, PR, diff, or set of changes needs review before merging —
  produces a two-axis verdict (repo-standards conformance plus
  spec/requirements conformance, reported separately) — when execute-plan
  reaches its final whole-branch review, or when the user asks to review work
  since some ref.
---

# Code Review

Review a diff on two independent axes, each run by its own subagent:

- **Standards** — does the code follow this repo's documented conventions and avoid the baseline smells?
- **Spec** — does the code implement what the requirements asked for, ID by ID?

The axes are deliberately separate because a change can pass one and fail the other: flawless code that builds the wrong thing (Standards pass, Spec fail), or a faithful implementation that tramples the repo's conventions (Spec pass, Standards fail). Merged reports let one axis mask the other.

## 1. Pin the range — fail fast

Take the base ref the caller supplied (a sha, branch, tag, or merge-base). Confirm it resolves — `git rev-parse <base>` — and that `git diff <base>...HEAD` is non-empty. A bad ref or empty diff must fail HERE, not inside two parallel subagents. Also capture `git log <base>..HEAD --oneline`. If no base was given, ask. *Done when: the ref resolves and the diff is non-empty.*

## 2. Locate the spec

Find the governing requirements, in order:

1. Requirement-ID trailers in the commits (`Implements:`, `Guards:`) — the feature code maps to a spec folder via `docs/specs/INDEX.md`.
2. A `docs/specs/<date>-<feature>/requirements.md` matching the branch or feature name.
3. A path the caller handed you.
4. Otherwise ask the user. If they confirm no spec exists, skip the Spec axis and say so in the final report.

*Done when: you hold a requirements.md path, or an explicit "no spec".*

## 3. Gather the standards sources

Collect whatever documents how code here should be written: CLAUDE.md, lint and formatter configs, CONTRIBUTING-style docs, plus CONTEXT.md for the repo's canonical vocabulary. If `docs/agents/project.md` is missing, note it and suggest running `setup-repo`, then proceed with what exists.

On top of the repo's own documents, the Standards axis always carries `standards-baseline.md` (beside this file) — twelve code-quality smells that apply even when the repo documents nothing, plus a Security section that applies whenever the diff crosses a trust boundary. Two rules bind it: a documented repo standard always overrides the baseline, and every baseline hit is a labeled judgment call, never a hard violation. Skip anything tooling already enforces — a reviewer repeating the linter is noise. *Done when: the source list and the baseline path are in hand.*

## 3a. Check for duplication against existing features

Run the duplication check against the diff's changed source files (from the range pinned in step 1): `python3 scripts/check_graph.py --query --json --path <changed-file> [--path <changed-file> ...]`. It returns the overlapping features and their summary cards. If `check_graph.py` is **absent**, the feature graph is not installed in this repo — note that, name `setup-repo` as the remedy, and state it at most once per session rather than on every review. If it errors, note that the automated overlap check was unavailable. Either way, continue — this never blocks the review. If no changed file overlaps any feature, state that no existing feature shares the diff's surface and inject nothing into step 4. *Done when: you hold the overlapping features' cards, or an explicit "no overlap" / "overlap check unavailable".*

## 4. Dispatch both subagents in parallel

Send ONE message containing both dispatches so they run concurrently and neither pollutes the other's context. Both are **read-only**: no mutation of the working tree, index, HEAD, or branch state; to inspect another revision, use a temporary worktree (`git worktree add <tmpdir> <sha>`), never move HEAD. Keep each brief under 400 words. Never pre-judge findings in a dispatch — no "do not flag", no pre-rated severities.

**Standards subagent** gets: the diff command and commit list; the standards-source paths; the path to `standards-baseline.md`, which it MUST read first and check the diff against each of its twelve smells in turn, plus the Security section for any hunk that crosses a trust boundary (untrusted input, secret handling, a privileged action); the brief — report (a) every place the diff breaks a documented standard, citing the document and rule, (b) for each of the twelve baseline smells, every hit spotted, naming the smell and quoting the hunk, and (c) every security concern from the Security section the diff triggers, naming the item and the trust boundary it crosses; documented breaches may be hard findings, baseline smells and security items are always judgment calls; the repo's documents override the baseline; skip anything tooling enforces; include CONTEXT.md vocabulary drift (a diff that renames or re-terms a glossary concept is a finding).

**Spec subagent** gets: the diff command and commit list; the requirements.md path; the brief — walk the requirements and report (a) IDs that are missing or only partially implemented, (b) behavior in the diff no requirement asked for (scope creep), (c) IDs that look implemented but wrong; quote the requirement ID on every finding; also verify each covered ID has a test tagged with it per the conventions in `docs/agents/project.md`, and flag untagged coverage. When step 3a found overlapping features, the Spec subagent ALSO receives those neighbor cards (owned paths + Out-of-Scope) as context, and its brief directs it to flag — as a **reuse-miss** finding citing the neighbor's feature code — any place the diff reimplements behavior a shares-surface neighbor already owns.

*Done when: both reports are back.*

## 5. Aggregate

Present the reports under `## Standards` and `## Spec` headings — lightly cleaned at most. Do NOT merge, dedupe across axes, or rerank one axis's findings against the other's; that reranking is exactly what the separation prevents.

Every finding carries: severity (Critical / Important / Minor), file:line, why it matters, and a suggested fix unless obvious.

End with the verdict:

```
Ready to merge? Yes | No | With fixes
[1–2 sentences of technical reasoning]
```

*Done when: both axis sections and the verdict are delivered.*
