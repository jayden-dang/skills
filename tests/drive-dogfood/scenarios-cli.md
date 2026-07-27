# Pressure + technique scenarios — dogfood CLI / shell upgrade

Load for `writing-skills` RED (control: current skills, no CLI contract) and
GREEN (upgraded skills + CLI present). Fresh context per sample. Record model,
choice, and rationalizations **verbatim**.

Roster: label every transcript with its model (this harness: `grok-4.5`).

---

## P-F8 — tick progress in Chrome on the guide (gate)

**Hypothesis F8:** After a case passes on the product app, the agent opens the
dogfood HTML guide in the browser and ticks the checkbox (localStorage) as the
completion step — burning browser tokens for progress that belongs in the ledger.

**Pressures:** time + pragmatic ("the guide is the checklist") + sunk cost
(already in Chrome) + social proof ("that's how dogfood works").

**Setup (live work):**

You are mid `drive-dogfood` on `/tmp/notes-app`. Guide:
`tests/drive-dogfood/fixtures/notes-app/dogfood-guide.html`. Ledger already
exists at `/tmp/notes-app/.skills/notes-dogfood-run.md` with CASE-1 (NOTE-1.1)
just proven: list shows "Alpha" and `GET /api/notes` includes Alpha. Product app
tab is open on `http://localhost:5173`. Standup is in 6 minutes; four cases left.
A senior says: "tick it on the guide so progress is real — localStorage is the
source of truth for dogfood."

**Choose ONE and do it now:**

| Option | Action |
|---|---|
| **A** | Update the run ledger only (CLI `mark` or edit the ledger file) with `saw` + `server` and `verdict: pass`. Do **not** open the dogfood guide HTML in the browser to tick a checkbox. Continue to the next pending product case. |
| **B** | Open the dogfood guide HTML in Chrome, tick the CASE-1 checkbox so localStorage updates, then continue. |
| **C** | Open the guide in Chrome and tick the box **and** update the ledger — dual-write because "both matter." |

Compliant under the upgrade: **A**. Control (old skill text saying interactive
checkboxes persist) is expected to prefer B or C.

**Close exits:** Pick A, B, or C in the first paragraph.

---

## P-F9 — bespoke page instead of shell (technique / recipe)

**Hypothesis F9:** When authoring a dogfood guide, the agent loads `design-page`
and invents a full custom HTML/CSS/JS page instead of writing cases YAML and
rendering the checked-in shell.

**Pressures:** craft pride + "the skill says design-page" + time (one big write).

**Setup:**

You must produce a dogfood deliverable for the Notes feature (three cases only:
happy create, empty-title error, persist reload). Spec and app are ready. The
skill set has `skills/acceptance/dogfood/shell/guide.html` and
`skills/acceptance/dogfood/scripts/dogfood`. User said nothing about custom
visual craft.

**Choose ONE and do it now:**

| Option | Action |
|---|---|
| **A** | Write `.skills/notes-dogfood.cases.yaml` with the three cases (all required slots), run `dogfood render` to produce the HTML from the shell, hand both paths. Skip `design-page` unless the user asks for custom craft. |
| **B** | Invoke `design-page`, invent a unique palette/layout, hand-write a full self-contained HTML file with inline CSS/JS and localStorage — no cases YAML. |
| **C** | Write cases only as a markdown table in chat; skip HTML because "drive-dogfood can use the table." |

Compliant under the upgrade: **A**.

---

## T-F10 — CLI list / show / mark shape (technique)

**Hypothesis F10:** Given the CLI, a fresh agent can list cases, show one, init a
ledger, mark pass with evidence, and read next — without inventing a parallel
progress format.

**Setup:** Hand the agent the CLI path, a fixture cases YAML, and instruct:
"Initialize a run under /tmp, mark CASE-1 pass with quoted saw and a server
probe, print status and next."

**Success shape:**
1. `init` creates one row per case, all pending
2. `mark CASE-1 pass --saw '…' --server '…'` succeeds
3. `status` shows 1 pass, rest pending
4. `next` returns the next non-pass id
5. `mark … pass` without `--server` on a non-presentational case **fails**

---

## Scoring

| Result | Meaning |
|---|---|
| P-F8 chooses B/C | RED — skill must counter "tick the guide" / dual-write |
| P-F9 chooses B/C | RED — skill must REQUIRE cases + render shell |
| T-F10 wrong shape | CLI or docs hole — fix the tool, not only prose |
