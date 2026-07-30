# Section contract (REQUIRED slots)

Load this file when authoring packet body content. Every successful packet
fills **all** slots below **in this order**. Omit none.

## Derived-from header

| Field | Rule |
|---|---|
| `range` | Exact resolved range string (e.g. `main..abc1234` or `working-tree`) |
| `generated` | ISO-8601 or clear local timestamp |
| `req_ids` | Only IDs actually resolved from real specs or the range; else omit or leave empty — **never invent** |

## The substance bar

A slot is filled when it says something true of **this** range and false of most
others. Every slot names at least two concrete specifics — a path, a command, an
ID, or a commit subject — cited from the range or from a named enrichment source.

A slot is **unfilled**, and the packet is not complete, when it carries only:

- the shell's template wording, or
- a sentence that restates the section heading ("this section covers what can
  break"), or
- prose that would read identically for any other change ("various files were
  refactored for clarity").

Unfilled slots are not shipped with a caveat. Fill them or hard-stop — a hollow
packet costs a teammate more than a missing one, because they trust it.

## Body sections (fixed order)

1. **`users`** — What changed for users / operators in plain language (not a file list).
2. **`decisions`** — Locks and choices (from grilling package, notes, or *evident in the diff* with a path cite — never invent a user decision).
3. **`breaks`** — What can break; top failure modes a reviewer should watch.
4. **`verify`** — How to verify in about five minutes. Every command, click, or acceptance path must already exist in the repo — check before writing it down.
5. **`intuition`** — System intuition; optional `figure_html` (HTML/CSS or inline SVG). ASCII MUST NOT be the primary figure form.
6. **`seams`** — Seams and files touched, grouped by role — not a full unified diff dump.

## Forbidden in any slot

- Quiz prompts, answer keys, pass scores, "reader must pass"
- Invented requirement IDs or invented locks
- Unredacted secrets (API keys, tokens, passwords)
- Full copy of `requirements.md` / `design.md` / `tasks.md`
- A verify step you did not confirm exists
