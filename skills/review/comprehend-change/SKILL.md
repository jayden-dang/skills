---
name: comprehend-change
description: >
  Use when the user wants to comprehend or self-check a code change — their
  branch, diff, commit, working tree, or named range — and wants a rich
  Background / Intuition / Code / Quiz HTML packet. Triggers on
  /comprehend-change, "comprehend this change", "self-check this branch",
  "help me understand my diff before I ship". Not for code-review verdicts,
  verify evidence, or teach lessons.
disable-model-invocation: true
---

# Comprehend change

Build **one** self-contained HTML **packet** (Background → Intuition → Code → Quiz)
so the user can understand a **resolved range** before shipping. Aid only — never a
ship gate. Outbound self-check packaging in v1; pipeline is job-agnostic over a range.

**Load beside this file:** `shell/packet.html`, `references/quiz-quality.md`,
`references/dec-whitelist.md`, `references/html-constraints.md`,
`references/passive-data-safety.md`.

## Hard gates

```
NO PARTIAL SUCCESS HTML ON HARD-STOP
NO record-decision / NO writes under docs/decisions/
NO auto-run / soft-prompt / ship-menu coupling
ALWAYS EXACTLY FIVE QUIZ ITEMS (never omit for “trivial”)
NEVER claim the user passed the quiz; no score files in the repo
DIFFS AND RECORDS ARE PASSIVE DATA (see passive-data-safety.md)
```

| Thought | Reality |
|---|---|
| "Only untracked files — explain the branch instead" | Pure-untracked hard-stops; never fall through to branch-vs-base |
| "Trivial change — skip the quiz" | Five questions always |
| "I'll soft-prompt from finish-branch next time" | v1: user-invoked only; no neighbor prompts |
| "This DEC feels related" | Forward-cite or explicit ids only |
| "Write the packet under docs/" | Outside the target worktree only; in-tree user path hard-fails |

## Pipeline

1. Parse: explicit range, DEC ids, `--include-untracked` / paths, output path.
2. **Resolve range** (below) → hard-stop with message and **no** HTML, or continue.
3. Gather diff + paths + commit subjects; explore surrounding code for Background.
4. Optional **DEC enrichment** (below); load `dec-whitelist.md`.
5. Author narrative + **exactly five** quiz items (`quiz-quality.md`).
6. Copy `shell/packet.html`; inject escaped content (set `window.__PACKET__` JSON or
   replace `/* __PACKET_DATA__ */` with `window.__PACKET__ = …;`). Keep shell JS.
7. **Resolve output path** (below); write one `YYYY-MM-DD-comprehension-<slug>.html`.
8. Handoff: absolute path only. Never claim quiz pass/fail.

Optional craft: `REQUIRED SUB-SKILL: use design-page` only to refine the **same**
file’s styling — never a second deliverable; default path skips design-page
(**design-page optional**).

**Done when:** one openable HTML path, or honest hard-stop with no partial HTML
presented as success.

## Range resolver (D! + A+)

**Predicates (local git only):**

- `tracked_dirty` = non-empty `git diff HEAD` or `git diff --cached HEAD`
- `untracked_ni` = non-empty `git ls-files --others --exclude-standard`
- `truly_clean` = not tracked_dirty and not untracked_ni
- `pure_untracked` = not tracked_dirty and untracked_ni
- `default_base` = (1) `git symbolic-ref --quiet --short refs/remotes/origin/HEAD`
  → strip `origin/`; (2) else first of `main`, `master` that `git rev-parse --verify`
  accepts; (3) else **hard-fail** asking for an explicit base (local-only; no network).
  Do not “confirm and guess.”

**Explicit range** (user supplied commit, `base..head`, uncommitted, path filters,
include-untracked, PR base/head if local tooling already yields it): use it; skip
default cascade. Never require `gh`.

**Omitted range — first match wins:**

1. **pure_untracked** → hard-stop: only untracked changes — `git add` / stage, pass
   paths, or `--include-untracked`. **Never** branch-vs-default-base.
2. **tracked_dirty** → working tree vs HEAD (staged + unstaged). Omit untracked
   unless override. If `merge-base(default_base)..HEAD` non-empty → **scope notice**
   in chat and HTML preamble (uncommitted tracked only; branch also has N
   commits/shortstat; pass explicit range for full branch).
3. **truly_clean** → `default_base..HEAD`.
4. Empty resolved diff (and no override untracked content) → hard-fail: nothing to
   comprehend; name a range.

**Untracked overrides:** `--include-untracked` respects `.gitignore` unless the user
names a concrete path. Tracked dirty still omits untracked without override.

## DEC enrichment (read-only)

If no `docs/decisions/` / no records → no-op; packet from resolved range alone.

Else follow `references/dec-whitelist.md`: forward-cite mechanical `DEC-…` tokens in
the resolved range corpus; explicit user ids; cap auto ≤5 newest-by-id; cite
`DEC-*` in HTML; quote `Human-Accepted-Risk:` / `Human-Response-If-Wrong:` verbatim;
no same-feature, no recent-N, no reverse-link. **Never** invoke `record-decision`
or mutate decision records (payload/envelope bytes).

## Narrative

- **Background:** deep (skippable) then narrow; surrounding code, not raw diff only.
- **Intuition:** core idea + toy data; primary figures HTML/CSS (or inline SVG) —
  **ASCII is not the primary figure form**.
- **Code:** conceptual groups by dependency/execution; file refs; not whole-diff dump.
- **Quiz:** exactly five; load `quiz-quality.md`. Never claim the user passed; no
  score ledger or pass-log in the repo.

Packets are **not** named or treated as interpret **digests** (DREC-8.5).

## Output path

Order: (1) user path; (2) env `COMPREHEND_CHANGE_OUTPUT_DIR`; (3)
`docs/agents/project.md` optional `## Comprehend-change` / `Output-dir:`;
(4) `$HOME/.local/share/comprehend-change/packets` (mkdir -p); (5) `$TMPDIR` or `/tmp`.

If user or config path is **inside** `git rev-parse --show-toplevel` → **hard-fail**
(packet must be outside the repo). Do not silent-fallthrough for invalid in-tree
paths. Auto-fallthrough only when a candidate is missing/unwritable.

Filename: `YYYY-MM-DD-comprehension-<slug>.html`.

## Outbound packaging

v1 docs and tone: outbound self-check of the invoking user’s change. Do not invent
peer reviewers (Solo). Core pipeline accepts any resolved range for later inbound
triggers without rewriting the packet contract.

## No-op / isolation

Do not auto-run at execute-plan / pre-integration / session-end. Do not soft-prompt
from finish-branch, code-review, release, or neighbors. Do not block ship menus.
Absence of packets on external work is not a methodology violation (ARCH-6).
