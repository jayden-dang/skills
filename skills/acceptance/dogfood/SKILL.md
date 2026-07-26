---
name: dogfood
description: Use when manually exercising a finished feature in the real running app from
  the user's seat — a hands-on dogfooding pass, case by case, over every
  user-facing ability, including the visuals, feel, and edge cases a human
  must eyeball rather than an automated test or a quick launch. Reach for it
  to try a feature for real, walk the whole user-facing surface, or produce a
  checkable, resumable HTML test guide kept open beside the app and ticked off
  as you go — not a one-off run. Not for executing an already-written guide in
  the browser (`drive-dogfood`).
---

# Dogfood

A dogfooding pass is a human driving the real app through every user-facing
ability and judging what they see. The deliverable is a **persistent, checkable
HTML artifact** — grounded in the app's own rendering, one row per ability case,
each tagged with the requirement ID and a **case kind** — that the user keeps
open beside the app and ticks off as they go. Build the artifact; a chat message
is not the deliverable. A guide of only happy paths is not done.

## Case taxonomy (every guide uses these kinds)

| `data-kind` | Meaning | Typical source |
|---|---|---|
| `happy` | Feature does what it is for | Primary story in requirements |
| `edge` | Boundary / empty / duplicate / max length / whitespace | Edge criteria in the same ID or sibling criteria |
| `error` | User-visible failure path (validation chip, 4xx message, retained input) | Error criteria in requirements |
| `nonbehavior` | What must **not** happen | Out-of-Scope; negative SHALLs |
| `persist` | Survives reload / re-open / restart of the client | Criteria that say "persists" or store-owned state |
| `visual` | Layout, color, empty-state copy, feel — human eyeball | Presentational requirements; no server write |
| `journey` | Multi-step workflow stitching atomic cases (optional, ≤2 per guide) | Cross-story user path |

Do **not** invent chaos, load, race, or security-fuzz suites here — those are not
a one-seat user pass. Permission/role cases belong when the UI exposes them
(`edge` or `error` + `data-setup` for the role).

## 1. Scope every ability — coverage gate

Read the feature's `requirements.md`, `design.md`, `tasks.md`. List every
user-observable ability. Include adjacent capabilities in the same user
workflow, not only the new feature.

**Coverage rules** (all must hold before §4 is done):

1. **Every user-facing requirement ID** has ≥1 case.
2. **Every ability area** (section of the guide) has ≥1 `happy` **and** ≥1
   non-happy among `edge` | `error` | `nonbehavior` | `persist`.
3. **Every Out-of-Scope / deliberate non-behavior** that a user could try has a
   `nonbehavior` case (or an explicit note in the hand-off: *no user-facing way
   to attempt this — skipped*).
4. **Every criterion that claims persistence** has a `persist` case (or a
   `happy`/`edge` whose Expect + `data-backend` prove reload/store — prefer a
   dedicated `persist` row so it cannot be skipped).
5. If the area has **no** edge, error, nonbehavior, or persist material in the
   spec, write one line under that section: *Coverage exception: no edge/error/
   nonbehavior/persist cited in spec* — do not invent product behavior. The
   exception is greppable honesty, not a free pass when the triad has edges.

One happy case per ID is **not** enough when the ID or its siblings name edges.

*Done when: the coverage rules above hold, or every exception is written on the
guide.*

## 2. Ground each case in the real code

For each case, read the code to get what the user will ACTUALLY see: the exact
vocabulary (keywords, command names, labels), keyboard shortcuts, and the real
rendering — badge colors, chip styles, icons — pulled from the source (theme
tokens, CSS), never guessed. Where the code reveals an honest caveat
(a delimiter dimmed not removed, a status with no UI yet), the case says so.

## 3. Boot the real app and find the honest observation point

Start the app with the `Run locally (dev)` command from `docs/agents/project.md`
(discover and record it if missing — see `acceptance-ui`). Surface any degraded
area up front: a feature needing a key, a sub-feature not built yet. A behavior
with no UI surface still gets a case — with a real way to observe it (a devtools
`invoke(...)`, a read-only DB peek), never a pretend screen. *Done when: the app
is running and every not-yet-visible behavior has an observation method.*

## 4. Build the checkable artifact

REQUIRED SUB-SKILL: load `design-page` before building the page, then build a
self-contained HTML page. **Always write it to a known path** (e.g.
`.skills/<slug>-dogfood.html` or `docs/dogfood/<slug>.html`) so a later
`drive-dogfood` run can read it; publish with the Artifact tool as well when
that tooling exists. Contract:

- Sectioned by ability area; **one row per case**, each carrying its requirement
  ID so a failing box routes straight back to the spec.
- Each row: **Try** (what to type or click, copy-pasteable) → **Expect** (shown
  in the app's real rendering, not described in prose). Prefer a visible kind
  chip or label (`happy` / `edge` / …) for the human reader.
- **Interactive checkboxes that persist** (localStorage) plus a progress
  counter, so the user closes and resumes.
- Theme-aware, fully self-contained: inline CSS/JS, no external assets.
- Optional: at most two `journey` rows that chain atomic steps; they do not
  replace atomic coverage.
- **Machine-drivable slots** on every case row (required so `drive-dogfood` can
  ledger and re-drive without parsing prose):

  | Attribute | Value |
  |---|---|
  | `data-case` | Stable case id, e.g. `CASE-1` — unique in the guide |
  | `data-req` | Requirement id, e.g. `NOTE-1.1` |
  | `data-kind` | One of: `happy` \| `edge` \| `error` \| `nonbehavior` \| `persist` \| `visual` \| `journey` |
  | `data-backend` | Server-side assertion after Try, or the literal `presentational` |
  | `data-setup` | Precondition or reset so the case can run independently |

  Example skeleton:

  ```html
  <div class="case"
       data-case="CASE-2"
       data-req="NOTE-1.2"
       data-kind="error"
       data-backend="POST /api/notes returns 4xx; no new note id"
       data-setup="empty notes list">
    <!-- Try / Expect -->
  </div>
  ```

**Coverage self-check before hand-off:** count rows by `data-kind` per section.
If any ability area lacks a non-happy kind and has no *Coverage exception* line,
add the missing cases — do not publish a happy-only guide.

## 5. Hand over

Give the file path, the fastest way in — a ~30-second first pass that lights the
feature up (usually the first `happy` row) — then the degraded-feature notes,
coverage exceptions (if any), and that ticks save. If the user wants the agent
to run the guide, name `drive-dogfood` (they already have the path).
*Done when: the artifact is on disk at a known path, grounded, resumable, the
§1 coverage gate holds, every case is ID-tagged with `data-kind`, and every row
carries all five machine slots.*

## Rationalizations

| Thought | Reality |
|---|---|
| "A markdown checklist in chat is enough" | It saves no tick, cannot show the real badge being checked against, and scrolls away. The deliverable is the persistent artifact. |
| "They're in a native desktop app, not a browser, so an artifact doesn't fit" | The artifact is a companion reference kept open beside the app; the app being native is no reason to inline the guide into chat. |
| "I'll describe the badge in words" | The user checks against what they SEE. Mirror the real rendering, or the Expect is unverifiable. |
| "One happy case per requirement is enough" | The coverage gate requires non-happy kinds (or a written exception). Happy-only is a demo, not dogfood. |
| "Edges belong in unit tests, not the guide" | Dogfood is the user-facing surface. If the user can hit the edge, it gets a row. |
| "Worse cases mean load/chaos/fuzz" | Those are other harnesses. Dogfood worse cases are edge, error, nonbehavior, persist. |
