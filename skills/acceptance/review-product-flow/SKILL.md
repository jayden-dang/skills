---
name: review-product-flow
description: Use when manually exercising a finished feature in the real running app from
  the user's seat — a hands-on product walk, case by case, over every
  user-facing ability, including the visuals, feel, and edge cases a human
  must eyeball rather than an automated test or a quick launch. Reach for it
  to try a feature for real, walk the whole user-facing surface, or produce a
  checkable, resumable review-product-flow guide (run file + rendered HTML) and
  its `vet-product-flow` report, kept open beside the app — not a one-off run.
  Not for executing an already-written guide (`run-product-walkthrough`).
---

# Review Product Flow

A product walk is a human driving the real app through every user-facing
ability and judging what they see. The deliverable is a **run file**, a
**rendered human guide**, and a **`vet-product-flow` report** — grounded in the
app's own rendering, one row per ability case, each tagged with the requirement
ID and a **case kind**. Cases and verdicts live in the same file, so what the
agent proves is what the person reads. Build the artifacts; a chat message is
not the deliverable. A guide of only happy paths is not done. Authoring is not
complete until the vet report exists.

## Case taxonomy (every guide uses these kinds)

| `kind` | Meaning | Typical source |
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
(`edge` or `error` + `setup` for the role).

## Todos — GATE

Before §1, create one todo per section (1–4) via TodoWrite, **and** one terminal
todo **Vet product flow** (`vet-product-flow` on the run file — created now, not
later). Check the vet todo off **only** when
`.skills/<CODE>/vet-product-flow.md` exists for this run file.
*Done when: the list exists before scoping and includes the vet todo.*

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
   `happy`/`edge` whose Expect + `backend` prove reload/store — prefer a
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
(discover and record it if missing — see `validate-ui`). Surface any degraded
area up front: a feature needing a key, a sub-feature not built yet. A behavior
with no UI surface still gets a case — with a real way to observe it (a devtools
`invoke(...)`, a read-only DB peek), never a pretend screen. *Done when: the app
is running and every not-yet-visible behavior has an observation method.*

## 4. Write cases + render the shell (do not invent CSS)

**Authoring SSOT is the run file**, not hand-rolled HTML.

1. Write `.skills/<CODE>/review-product-flow.json` (schema: load sibling
   `references/cases-schema.md` when unsure). Every case carries all required
   slots: `id`, `req`, `kind`, `title`, `setup`, `try`, `expect`, `backend`
   (`backend` is the server-side assertion, or the literal `presentational`).
   Run state (`run`, `human`) is filled in for you — author the eight slots.
2. Render the human guide from the checked-in shell — **do not** load
   `craft-page` or invent a palette/layout unless the user explicitly asks for
   custom craft:

   ```bash
   python3 <skill-root>/scripts/review-product-flow render .skills/<CODE>/review-product-flow.json \
     -o .skills/<CODE>/review-product-flow.html
   ```

   Resolve `<skill-root>` to this skill's install path (in this monorepo:
   `skills/acceptance/review-product-flow`). The shell is `shell/guide.html` — theme-aware
   CSS/JS, kind chips, verdict badges, and `data-*` attributes. The rendered page
   carries the verdicts as of render time and says so, so it is correct on a
   double-click with nothing running.
3. **Coverage self-check:** count cases by `kind` per section. If any ability
   area lacks a non-happy kind and has no *Coverage exception* line, add the
   missing cases before hand-off.

Optional: at most two `journey` rows; they do not replace atomic coverage.

**Never** ship a chat-only checklist. **Never** regenerate a full custom HTML
page as the default path — cases + `render` is the path.

*Done when: the run file and rendered HTML are on disk at known paths, coverage
holds, every case has all required slots.*

## 5. Hand over

Order: artifacts → **run** vet → optional serve → dogfood only after clean vet.

1. **Artifacts** — give both paths (run file + HTML), the fastest way in — a
   ~30-second first pass that lights the feature up (usually the first `happy`
   row) — then degraded-feature notes and coverage exceptions.

2. **Vet IMMEDIATELY.** After the run file and rendered HTML are on disk and §4
   coverage holds, **IMMEDIATELY** REQUIRED SUB-SKILL: use `vet-product-flow` on
   the run file — before serve, dogfood, or any “authoring done” claim. Mark the
   **Vet product flow** todo done only when `.skills/<CODE>/vet-product-flow.md`
   exists. §1 / §4 coverage self-check is authoring hygiene, not a substitute
   for this report.

3. **Optional serve** — offer the live guide when they will be testing by hand
   alongside the agent:

   ```bash
   python3 <skill-root>/scripts/review-product-flow serve .skills/<CODE>/review-product-flow.json
   ```

   It binds `127.0.0.1:8787`, follows verdicts as the agent records them, and
   writes their ticks back where the agent can see them. Tell them plainly what
   a tick means: it records that they looked, and never becomes a `pass`.
   Stopping it is `serve --stop`. Opened as a plain file instead, the guide still
   shows the verdicts it was rendered with — the server only buys freshness.

4. **Agent dogfood** — name `run-product-walkthrough` and the run-file path
   **only after** a clean `vet-product-flow` report (or a named override on open
   findings). Walkthrough still enforces its own gate; hand-off order does not
   replace that check.

*Done when: artifacts are on disk, grounded, the §1 coverage gate holds, every
case is fully slotted, and `.skills/<CODE>/vet-product-flow.md` exists for this
run file.*

## Rationalizations

| Thought | Reality |
|---|---|
| "A markdown checklist in chat is enough" | It saves no tick, cannot show the real badge being checked against, and scrolls away. The deliverable is the run file + rendered guide. |
| "I'll craft-page a unique layout for this feature" | Default is the checked-in shell. Custom craft only when the user asks. |
| "They're in a native desktop app, not a browser, so an artifact doesn't fit" | The artifact is a companion reference kept open beside the app; the app being native is no reason to inline the guide into chat. |
| "I'll describe the badge in words" | The user checks against what they SEE. Mirror the real rendering, or the Expect is unverifiable. |
| "One happy case per requirement is enough" | The coverage gate requires non-happy kinds (or a written exception). Happy-only is a demo, not review-product-flow. |
| "Edges belong in unit tests, not the guide" | Review Product Flow is the user-facing surface. If the user can hit the edge, it gets a row. |
| "Worse cases mean load/chaos/fuzz" | Those are other harnesses. Review Product Flow worse cases are edge, error, nonbehavior, persist. |
| "§4 coverage self-check already ran — skip vet" | Self-check is same-session authoring hygiene, not an isolated implementation-surface judgment. It is **not a substitute for vet**. |
| "I'll name vet as next and stop — the controller will run it" | Step 2 **runs** `vet-product-flow`; naming is not completion |
| "Artifacts are on disk — authoring is done" | Done when the vet report exists, not when the JSON/HTML land |

## Red Flags

- Hand-writing a full HTML/CSS page instead of the run file + `review-product-flow render`
- Missing `backend` / `setup` / `kind` on any case
- Happy-only section without a greppable coverage exception
- Telling the agent to mark progress via guide ticks instead of `review-product-flow mark`
- Treating §4 coverage self-check as a substitute for `vet-product-flow`
- Declaring this skill done without `.skills/<CODE>/vet-product-flow.md` for this run file
- Naming `run-product-walkthrough` (or offering dogfood) before a vet report exists
- Checking off the **Vet product flow** todo when the report path does not exist
