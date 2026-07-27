# Changelog

## 0.2.5 — 2026-07-27

### New: `repoint-project` — pivot disposition ledger

Closes the gap where `establish-project` (brownfield), `sync-spec`, and
`improve-architecture` all treat **code as truth**. When the user pivots intent
and shipped reality collides with the new vision, nothing previously owned that
flow.

- **New skill** `skills/project/repoint-project/` (user-invoked `/repoint-project`)
  — Iron Law: no vision/architecture rewrite until every contradicted shipped
  feature and live `ARCH-N` has a user-confirmed disposition in
  `docs/product/pivot-ledger.md`
- **Single-writer preserved:** skill never writes `vision.md` /
  `architecture/`; names `/establish-project` (update) after confirmation
- **RED/GREEN** under `tests/repoint-project/` (Ledgerly fixture; Sonnet + Haiku)
  - S1 deadline pivot: baseline **failed** (both models rewrote vision) → skill
    **green** after REFACTOR (ledger-on-disk + named-repo counters for Haiku)
  - S2 challenge-pivot and S3 bare-delete: baseline **passed** → cut from skill
    text (no-op rule)
- **Neighbors:** `establish-project` update routes pivots-with-collisions here;
  `correct-course` Vision re-entry names `/repoint-project` when shipped code
  collides

### Packaging

- Engineer Pack version **0.2.5**; plugin path list adds
  `./skills/project/repoint-project`

## 0.2.4 — 2026-07-27

### `dogfood` / `drive-dogfood` — cases YAML + CLI ledger (no guide ticks for agents)

Stops agent progress living in HTML `localStorage` (Chrome ticks burned tokens)
and stops re-authoring full CSS per dogfood pass.

- **Cases SSOT:** `.skills/<slug>-dogfood.cases.yaml` with required slots
  (`id`, `req`, `kind`, `title`, `setup`, `try`, `expect`, `backend`)
- **Shell:** `skills/acceptance/dogfood/shell/guide.html` — theme-aware, kind
  chips, human-only localStorage ticks
- **CLI:** `skills/acceptance/dogfood/scripts/dogfood` —
  `list` / `show` / `init` / `status` / `next` / `mark` / `render` / `report`
- **`dogfood` skill:** write cases → `render`; `design-page` opt-in only
- **`drive-dogfood` skill:** Iron Law adds *progress lives in the ledger*; browser
  only for the product under test; `mark` enforces `saw` + `server`
- **Contract:** `docs/specs/2026-07-27-dogfood-cli/contract.md`
- **Tests:** `tests/test_dogfood_cli.py`; scenarios in
  `tests/drive-dogfood/scenarios-cli.md`

### Packaging

- Engineer Pack version **0.2.4** (skill/docs + scripts; plugin path list
  unchanged — scripts ship inside the dogfood skill folder)

## 0.2.3 — 2026-07-26

### `dogfood` coverage gate + case taxonomy

Stops happy-only dogfood guides: each ability area needs non-happy cases (edge /
error / nonbehavior / persist) or a greppable coverage exception.

- **Taxonomy** on every row: `data-kind` = `happy` \| `edge` \| `error` \|
  `nonbehavior` \| `persist` \| `visual` \| `journey`
- **Coverage rules** replace "≥1 case per requirement ID" as the sole bar
- **Self-check** before hand-off: count kinds per section
- **`drive-dogfood`**: ledger carries `kind`; no demo-only happy-path subset
- Guide + review-and-acceptance docs updated

### Packaging

- Engineer Pack version **0.2.3** (skill/docs only; plugin path list unchanged)

## 0.2.2 — 2026-07-26

### New: `drive-dogfood` + machine-drivable dogfood guides

Agent-driven execution of an existing dogfood HTML guide in a real browser, with
paired front-end and backend evidence, a resumable run ledger, and a fix loop
through `debug`.

- **New skill** `skills/acceptance/drive-dogfood/` — model-invocable; outcome is
  an evidence-backed run ledger (pass / fail / blocked per case), not committed
  e2e specs (`acceptance-ui`) and not guide authoring (`dogfood`)
- **`dogfood` upgrade** — every case row carries `data-case`, `data-req`,
  `data-backend`, `data-setup`; guide always written to a known file path;
  descriptions disambiguate author vs drive
- **RED/GREEN** recorded under `tests/drive-dogfood/` (baselines on `grok-4.5`)
- **Inventory:** plugin + marketplace, guide page, AGENTS/README skill counts,
  See also links from acceptance neighbors

### Packaging

- Engineer Pack version **0.2.2**

## 0.2.1 — 2026-07-26

### Packaging: Engineer Pack + Personal Pack

`npx skills add jayden-dang/skills` now presents two clear packs instead of
"Jayden Skills" plus an ungrouped bucket:

| Pack | Plugin name | Contents |
|---|---|---|
| **Engineer Pack** | `engineer-pack` | All engineering skills (default plugin) |
| **Personal Pack** | `personal-pack` | All Personal OS skills (opt-in) |

- Renamed default plugin `jayden-skills` → `engineer-pack`
- Renamed personal plugin `personal-os` → `personal-pack`
- Added `.claude-plugin/marketplace.json` so the skills CLI groups both packs
- Moved three program-layer skills into Engineer Pack inventory (they were on
  disk under engineering categories but missing from `plugin.json`, so the CLI
  put them in **Other** / **General**):
  - `write-roadmap` (`skills/project/write-roadmap`)
  - `check-roadmap` (`skills/track/check-roadmap`)
  - `assess-milestone` (`skills/track/assess-milestone`)
- Docs: `docs/packages.md`, root README inventory, package READMEs

## 0.2.0 — 2026-07-26

### New: Personal OS package (independent, opt-in)

A standalone life and multi-project **management** skill set. Agent role is
secretary / coach — not product implementer. Does not depend on the engineering
package; not included in the default Claude engineering plugin.

- **18 skills** under `skills/personal/`: `using-personal-os`, `setup-personal-os`,
  `capture`, `process-inbox`, `orient`, `plan-day`, `execute-session`,
  `open-project`, `plan-project`, `close-project`, `maintain-area`,
  `open-learning-track`, `log-learning`, `review-week`, `review-quarter`,
  `replan`, `life-charter`, `sync-workspaces`
- **Templates** under `templates/personal-os/` (project, area, daily, weekly,
  quarterly, learning track, session, inbox, config example)
- **Docs:** package README, `docs/personal-os/START-HERE.md`, `docs/packages.md`
  (multi-package install isolation)
- **Optional plugin** manifest: `.claude-plugin/personal-os.plugin.json`
- **Secretary default / permission rules:** management only unless the user grants
  a scoped act; registry-first workspaces; config-mapped layouts (no forced rename)
- Default `.claude-plugin/plugin.json` remains **engineering-only**

### Docs / packaging

- Root README and AGENTS.md describe dual independent packages
- Engineering install docs avoid a blind `skills/*/*` loop that would pull Personal OS
- `skills/engineering/README.md` package index (paths unchanged)

### Misc

- Version bump to **0.2.0** (minor: new optional package surface)

## 0.1.1 — 2026-07-24

### New requirements shipped

#### Outbound comprehend-change (XDIFF)

User-invoked `/comprehend-change` builds one self-contained HTML comprehension
packet (Background → Intuition → Code → Quiz) for a resolved git range —
outbound self-check aid, never a ship gate.

- On-demand user-invoked skill with explicit triggers; no auto-run, soft-prompt, or ship-menu coupling — **XDIFF-1.1–1.6**
- D! range cascade with pure-untracked hard-stop, tracked-dirty + scope notice, truly-clean branch vs default base, empty hard-fail — **XDIFF-2.1–2.7**
- A+ untracked policy (exclude by default; flag/paths; untracked-only honest stop) — **XDIFF-3.1–3.5**
- Single offline HTML packet via checked-in shell template; optional design-page craft only — **XDIFF-4.1–4.12**
- Fixed five-question interactive quiz; personal pass only; never omit for “trivial” — **XDIFF-5.1–5.9**
- Optional DREC read-only enrichment (forward-cite + explicit ids; no emit) — **XDIFF-6.1–6.10**
- Passive-data safety and HTML escape constraints — **XDIFF-7.1–7.3**
- Package, plugin inventory, guide, ARCH-3 pure skill path — **XDIFF-8.1–8.4**
- No partial success HTML; quiz a11y basics — **XDIFF-9.1–9.2**
- Neighbor isolation guards (DREC emitters, finish-branch/release, code-review, digest term, ARCH-6) — **XDIFF-10.1–10.9**

#### Boundary Decision Records (DREC)

Immutable decision records at production boundaries (`finish-branch` / `release`)
with validator, record-before-crossing, and ARCH-6 participant model.

- Record substrate, identity/reissue, depth classification — **DREC-1.x–3.x**
- Verbatim human provenance and storage classes — **DREC-4.x–5.x**
- Emission rules for finish-branch and release — **DREC-6.x–7.x**
- Durable evidence, record-decision skill, participant SSOT — **DREC-8.x–10.x**
- Trace extension, validator, adoption anchor — **DREC-11.x**
- interpret ledger/labels/digest upgrades — **DREC-12.x**
- Spec-folder discovery convention; NFR secret scan / determinism — **DREC-13.x–14.x**
- Record-before-crossing ordering and publication failure — **DREC-15.x**

### Protected behavior

- Record-before-crossing and caller gate pressure hardening — **Guards: DREC-15.1, DREC-9.5, DREC-6.3**
- Doctrine SSOT / description trigger polish — **Guards: DREC-9.1, DREC-9.4, DREC-15.1**

### Misc

- `sync-spec(DREC)`: mark triad Implemented; ARCH-6 design citation
- `fix(drec)`: move e-spine fixture IDs out of unittest source (trace E1)
- `refactor(xdiff)`: writing-skills checklist hardening (Iron Law, red flags, pointers)
- `docs(xdiff)`: pressure-test results; range decision-tree callout
