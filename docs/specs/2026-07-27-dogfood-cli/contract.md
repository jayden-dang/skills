# Contract — dogfood cases + CLI + shell (2026-07-27)

**Status:** binding for skill bodies after RED confirms F8/F9.  
**Ceremony:** skill edit + new substrate (shell, CLI, schema).  
**Decisions:** YAML cases SSOT + generated HTML; ledger via CLI; browser only for the product under test.

---

## 1. Artifacts

| Artifact | Path (convention) | Role |
|---|---|---|
| Cases catalog | `.skills/<slug>-dogfood.cases.yaml` | **Authoring SSOT** — cases, taxonomy, backend slots |
| Human guide | `.skills/<slug>-dogfood.html` | Generated view from shell + cases (localStorage ticks optional for humans) |
| Run ledger | `.skills/<slug>-dogfood-run.md` | **Agent progress SSOT** — verdicts + evidence |
| End report | `.skills/<slug>-dogfood-report.md` | End-of-run handoff (optional CLI `report`) |

Legacy HTML guides with `data-*` remain readable by the CLI (`list` / `init` / `show`). New authoring always starts from cases YAML.

---

## 2. Cases YAML schema (v1)

```yaml
version: 1
feature: notes          # short label
slug: notes             # path stem
title: Notes App — Dogfood
origin: http://localhost:5173
intro: |
  Optional multi-line intro shown on the human guide.
sections:
  - name: Create & persist
    cases:
      - id: CASE-1                 # required, unique in file
        req: NOTE-1.1              # required
        kind: happy                # happy|edge|error|nonbehavior|persist|visual|journey
        title: Create a note       # human label
        setup: empty notes list    # data-setup
        try: |                     # what to do
          Open app → New note → title Alpha → Save
        expect: |                  # what to see
          List shows "Alpha"
        backend: GET /api/notes includes title Alpha
        # use literal "presentational" when no server write
```

**Kinds:** `happy` | `edge` | `error` | `nonbehavior` | `persist` | `visual` | `journey`.

**Required per case:** `id`, `req`, `kind`, `title`, `setup`, `try`, `expect`, `backend`.

---

## 3. Ledger format (parseable markdown)

```markdown
# Dogfood run ledger
- source: `.skills/notes-dogfood.cases.yaml`
- slug: notes
- origin: http://localhost:5173

## CASE-1
- req: NOTE-1.1
- kind: happy
- verdict: pending
- saw:
- server:
- notes:
```

**Verdicts:** `pending` | `pass` | `fail` | `blocked`.

**`mark` rules:**
- `pass` requires non-empty `saw`.
- `pass` requires non-empty `server`; if case `backend` is `presentational`, `server` must be exactly `none — presentational` (or agent-supplied equivalent accepted: starts with `none` and contains `presentational`).
- `fail` / `blocked` still require `saw` when evidence was collected; empty saw allowed only for `blocked` with notes explaining the block.

---

## 4. CLI surface

Executable: `skills/acceptance/dogfood/scripts/dogfood` (python3).

| Command | Purpose |
|---|---|
| `list <cases\|html>` | Print case ids + req + kind + title |
| `show <cases\|html> <CASE-ID>` | Full case detail (try/expect/setup/backend) |
| `init <cases\|html> [-o run.md]` | Create ledger, all `pending` |
| `status <run.md>` | Counts by verdict + next pending |
| `next <run.md>` | Print first non-`pass` case id (or empty + exit 1) |
| `mark <run.md> <CASE-ID> <verdict> --saw S --server S [--notes N]` | Update one row |
| `render <cases.yaml> [-o guide.html] [--shell path]` | Fill shell → HTML |
| `report <run.md> [-o report.md]` | End-of-run report from ledger |

**Agent progress rule:** only `init` / `mark` / ledger file edits via CLI. Never open the guide in a browser to tick checkboxes.

---

## 5. Shell

`skills/acceptance/dogfood/shell/guide.html` — theme-aware CSS/JS, progress + localStorage for humans, injects cases via `/* __CASES_JSON__ */` or a replaced `__CASES_JSON__` marker.

`design-page` is **optional** craft on the shell, not the default path.

---

## 6. Skill deltas (summary)

**dogfood:** coverage gate + ground + boot unchanged; §4 becomes write cases YAML → `dogfood render` → hand paths. No bespoke CSS unless user asks.

**drive-dogfood:** §2 `dogfood init` (or trust existing ledger); §3 `dogfood show` + drive **product** only; `dogfood mark` after evidence; §5 `dogfood report`. Guide HTML checkboxes never required.
