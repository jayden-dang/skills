# `study-change`

> Build one self-contained HTML packet (Background → Intuition → Code → Quiz) so you can understand a git change before you ship — aid first, never a ship gate.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | user-invoked (`/study-change`) |
| **Reads** | Local git (resolved range), optional `.skills/decisions/` (read-only), optional `## Comprehend-change` / env for output dir |
| **Writes** | One HTML file **outside** the target repo worktree |
| **Calls** | Optional [`craft-page`](craft-page.md) (craft only — not required) |
| **Called by** | none in v1 (no soft-prompts from land-branch / inspect-change) |

## When to reach for it

- You (or your agent) just changed a branch or working tree and you want a real comprehension pass before PR/merge.
- You want Background / Intuition / Code plus a five-question self-check quiz (personal only — the skill never records pass/fail).

## When not to

- You need a **Standards + Spec** merge verdict → [`inspect-change`](inspect-change.md)
- You need a production-boundary decision record → [`land-branch`](land-branch.md) / [`record-verdict`](record-verdict.md) / [`cut-release`](cut-release.md)
- You want a multi-lesson tutoring session → [`teach-pack`](teach-pack.md)

## Range defaults (D!)

When you omit a range, evaluation order is:

1. **Pure untracked only** → hard-stop (stage, pass paths, or `--include-untracked`) — never branch vs default base
2. **Tracked dirty** → working tree vs HEAD; **scope notice** if the branch also has commits vs default base
3. **Truly clean** → current branch vs default base (`origin/HEAD` → `main`/`master` → hard-fail for explicit base)
4. Empty diff → hard-fail

Untracked files are excluded by default (A+). Explicit ranges always win.

## Output

Outside the repo: env `COMPREHEND_CHANGE_OUTPUT_DIR` → project.md `## Comprehend-change` / `Output-dir:` → `~/.local/share/study-change/packets` → OS temp. Filename `YYYY-MM-DD-comprehension-<slug>.html`. In-worktree paths hard-fail.

## Decision records

Optional read-only enrichment when `.skills/decisions/` exists: forward-cite `DEC-*` tokens in the resolved range, plus any ids you name. Never emits or edits records.

## Related

- Philosophy: human understanding as the bottleneck; answerability remains DREC’s job
- [`inspect-change`](inspect-change.md) · [`land-branch`](land-branch.md) · [`craft-page`](craft-page.md)
