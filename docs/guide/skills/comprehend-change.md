# `comprehend-change`

> Build one self-contained HTML packet (Background → Intuition → Code → Quiz) so you can understand a git change before you ship — aid first, never a ship gate.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | user-invoked (`/comprehend-change`) |
| **Reads** | Local git (resolved range), optional `docs/decisions/` (read-only), optional `## Comprehend-change` / env for output dir |
| **Writes** | One HTML file **outside** the target repo worktree |
| **Calls** | Optional [`design-page`](design-page.md) (craft only — not required) |
| **Called by** | none in v1 (no soft-prompts from finish-branch / code-review) |

## When to reach for it

- You (or your agent) just changed a branch or working tree and you want a real comprehension pass before PR/merge.
- You want Background / Intuition / Code plus a five-question self-check quiz (personal only — the skill never records pass/fail).

## When not to

- You need a **Standards + Spec** merge verdict → [`code-review`](code-review.md)
- You need a production-boundary decision record → [`finish-branch`](finish-branch.md) / [`record-decision`](record-decision.md) / [`release`](release.md)
- You want a multi-lesson tutoring session → [`teach`](teach.md)

## Range defaults (D!)

When you omit a range, evaluation order is:

1. **Pure untracked only** → hard-stop (stage, pass paths, or `--include-untracked`) — never branch vs default base
2. **Tracked dirty** → working tree vs HEAD; **scope notice** if the branch also has commits vs default base
3. **Truly clean** → current branch vs default base (`origin/HEAD` → `main`/`master` → hard-fail for explicit base)
4. Empty diff → hard-fail

Untracked files are excluded by default (A+). Explicit ranges always win.

## Output

Outside the repo: env `COMPREHEND_CHANGE_OUTPUT_DIR` → project.md `## Comprehend-change` / `Output-dir:` → `~/.local/share/comprehend-change/packets` → OS temp. Filename `YYYY-MM-DD-comprehension-<slug>.html`. In-worktree paths hard-fail.

## Decision records

Optional read-only enrichment when `docs/decisions/` exists: forward-cite `DEC-*` tokens in the resolved range, plus any ids you name. Never emits or edits records.

## Related

- Philosophy: human understanding as the bottleneck; answerability remains DREC’s job
- [`code-review`](code-review.md) · [`finish-branch`](finish-branch.md) · [`design-page`](design-page.md)
