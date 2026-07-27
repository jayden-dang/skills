# Section contract (REQUIRED slots)

Load this file when authoring packet body content. Every successful packet
fills **all** slots below **in this order**. Omit none.

## Derived-from header

| Field | Rule |
|---|---|
| `range` | Exact resolved range string (e.g. `main..abc1234` or `working-tree`) |
| `generated` | ISO-8601 or clear local timestamp |
| `req_ids` | Only IDs actually resolved from real specs or the range; else omit or leave empty — **never invent** |

## Body sections (fixed order)

1. **`users`** — What changed for users / operators in plain language (not a file list).
2. **`decisions`** — Locks and choices (from grilling package, notes, or *evident in the diff* with a path cite — never invent a user decision).
3. **`breaks`** — What can break; top failure modes a reviewer should watch.
4. **`verify`** — How to verify in about five minutes (commands, clicks, or acceptance paths that exist).
5. **`intuition`** — System intuition; optional `figure_html` (HTML/CSS or inline SVG). ASCII MUST NOT be the primary figure form.
6. **`seams`** — Seams and files touched, grouped by role — not a full unified diff dump.

## Forbidden in any slot

- Quiz prompts, answer keys, pass scores, “reader must pass”
- Invented requirement IDs or invented locks
- Unredacted secrets (API keys, tokens, passwords)
- Full copy of `requirements.md` / `design.md` / `tasks.md`
