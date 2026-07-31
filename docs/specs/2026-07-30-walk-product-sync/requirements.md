# Requirements: Walk Product sync

Feature code: DFSYNC
Status: Implemented
Date: 2026-07-30

<!--
Rules:
- Feature code: 2-12 chars, A-Z0-9, starts with a letter, unique repo-wide.
  Register it in docs/specs/INDEX.md before use.
- Every acceptance criterion gets a hierarchical ID: <CODE>-<story>.<criterion>.
- Criteria use EARS phrasing:
    WHEN <event/condition> THE SYSTEM SHALL <behavior>          (event-driven)
    WHILE <state> THE SYSTEM SHALL <behavior>                   (state-driven)
    IF <unwanted condition> THEN THE SYSTEM SHALL <behavior>    (unwanted behavior)
    WHERE <feature is included> THE SYSTEM SHALL <behavior>     (optional feature)
    THE SYSTEM SHALL <behavior>                                 (ubiquitous)
- Guard requirements protect existing behavior this feature touches:
    WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing behavior>
- IDs are immutable once Status is Approved. Retire a requirement by striking it
  through (~~**CODE-N.M**~~ reason) — never renumber.
-->

Today a walk-product run is spread across three files: the cases YAML the agent
authors, the HTML guide rendered from a snapshot of it, and the markdown ledger
where verdicts actually live. Nothing reads anything else, so a person holding
the guide cannot see what the agent has proven, and a person testing by hand has
nowhere to put what they found. This feature collapses the three into one JSON
artifact and adds an optional local server so the guide can show live state and
accept a human's ticks — without weakening the evidence bar that makes a `pass`
mean something.

## 1. One artifact carries cases and verdicts

**Story:** As an agent driving a walk-product run, I want to mark a case and have the
guide's own data file change, so that what I proved and what the person reads
are the same record.

- **DFSYNC-1.1** THE SYSTEM SHALL keep each walk-product run in exactly one file, `.skills/<slug>-walk-product.json`, holding both case content and run state.
- **DFSYNC-1.2** WHEN any `walk-product` subcommand needs case content and run state THE SYSTEM SHALL read both from a single path argument, with no separate catalog path or ledger path.
- **DFSYNC-1.3** WHEN `walk-product init` runs against a file whose cases carry no run state THE SYSTEM SHALL add `verdict: pending` to every case and leave any case that already has run state untouched.
- **DFSYNC-1.4** IF `walk-product init` runs against a file that already holds a non-`pending` verdict and `--force` is absent THEN THE SYSTEM SHALL exit non-zero and write nothing.
- **DFSYNC-1.5** IF a run file is not valid JSON, declares a version other than 2, repeats a case `id`, carries a `kind` outside the seven-kind taxonomy, or omits a required case slot THEN THE SYSTEM SHALL exit non-zero and name both the offending case and the offending field.
- **DFSYNC-1.6** THE SYSTEM SHALL execute every `walk-product` subcommand using only the Python standard library.
- **DFSYNC-1.7** IF a subcommand is given a path ending `.yaml`, `.yml`, or `-run.md` THEN THE SYSTEM SHALL exit non-zero stating that only the v2 JSON run file is supported, rather than attempting to parse it.
- **DFSYNC-1.8** (guard) WHEN `walk-product list` runs THE SYSTEM SHALL CONTINUE TO print one tab-separated `id`, `req`, `kind`, `title` line per case, in file order.
- **DFSYNC-1.9** (guard) WHEN `walk-product show` runs against a case THE SYSTEM SHALL CONTINUE TO print its `id`, `req`, `kind`, `title`, `setup`, `try`, `expect`, and `backend`.
- **DFSYNC-1.10** (guard) WHEN `walk-product next` finds no case whose verdict is other than `pass` THE SYSTEM SHALL CONTINUE TO print nothing and exit 1.
- **DFSYNC-1.11** (guard) WHEN `walk-product mark` is called with verdict `pass` THE SYSTEM SHALL CONTINUE TO reject an empty `--saw` and reject an empty `--server`.
- **DFSYNC-1.12** (guard) WHEN a case declares `backend` as the literal `presentational` THE SYSTEM SHALL CONTINUE TO require `--server` to be `none — presentational` for a `pass`, and CONTINUE TO reject that same string for a case whose `backend` is anything else.
- **DFSYNC-1.13** (guard) WHEN `walk-product report` writes a report THE SYSTEM SHALL CONTINUE TO emit a markdown table with one row per case and to escape `|` in cell text.

## 2. A human tick the agent can see but cannot mistake for proof

**Story:** As a person testing a case by hand, I want my tick recorded where the
agent will see it, so that my manual pass is visible without it ever being
counted as evidence I did not produce.

- **DFSYNC-2.1** WHEN a human tick is recorded THE SYSTEM SHALL store it inside that case's `human` object, whose key names never overlap with `verdict`, `saw`, `server`, or `notes`.
- **DFSYNC-2.2** WHEN a human tick is recorded THE SYSTEM SHALL leave that case's `verdict` unchanged.
- **DFSYNC-2.3** WHEN `walk-product next` selects a case THE SYSTEM SHALL return the first case whose `verdict` is not `pass`, disregarding every `human` field.
- **DFSYNC-2.4** WHEN `walk-product status` runs THE SYSTEM SHALL print the count of human-ticked cases on its own line, separate from the verdict counts.
- **DFSYNC-2.5** WHEN `walk-product report` writes a report THE SYSTEM SHALL give the human tick its own column, distinct from the verdict column.
- **DFSYNC-2.6** IF a request to the serve endpoint attempts to write `verdict`, `saw`, `server`, or `notes` THEN THE SYSTEM SHALL reject it with a 4xx status and change nothing on disk.

## 3. Two writers, no lost work

**Story:** As a person ticking cases in the guide while the agent marks others, I
want both of our writes to survive, so that neither of us silently loses what we
just recorded.

- **DFSYNC-3.1** THE SYSTEM SHALL carry an integer `rev` at the top level of the run file and increase it by one on every successful write.
- **DFSYNC-3.2** WHEN any writer commits a change THE SYSTEM SHALL write a temporary file in the target's own directory and move it onto the target atomically.
- **DFSYNC-3.3** IF the `rev` on disk differs from the `rev` a writer read before making its change THEN THE SYSTEM SHALL re-read the file, re-apply only that writer's own fields, and retry the write.
- **DFSYNC-3.4** WHEN a human tick and an agent verdict are committed against the same run file at the same time THE SYSTEM SHALL preserve both.
- **DFSYNC-3.5** THE SYSTEM SHALL complete `walk-product mark` without opening a network connection.
- **DFSYNC-3.6** WHILE a serve process is running THE SYSTEM SHALL leave the observable result of `walk-product mark` identical to its result when no serve process is running.

## 4. A guide that is correct on its own

**Story:** As a person handed a walk-product guide, I want to double-click the HTML
file and see which cases have passed, so that the guide is useful with nothing
else running.

- **DFSYNC-4.1** WHEN `walk-product render` runs THE SYSTEM SHALL embed both case content and each case's current verdict into the generated HTML.
- **DFSYNC-4.2** WHILE the guide is open from a `file://` URL THE SYSTEM SHALL display the embedded verdicts and issue no network request.
- **DFSYNC-4.3** WHILE the guide is open from a `file://` URL THE SYSTEM SHALL state on the page that the verdicts shown are the render-time snapshot rather than live state.
- **DFSYNC-4.4** (guard) WHEN the guide renders a case THE SYSTEM SHALL CONTINUE TO HTML-escape every string taken from the run file before inserting it into the document.
- **DFSYNC-4.5** (guard) WHEN the guide renders a case THE SYSTEM SHALL CONTINUE TO set `data-case`, `data-req`, `data-kind`, `data-backend`, and `data-setup` on that case's element.
- **DFSYNC-4.6** (guard) WHILE the guide is open from a `file://` URL THE SYSTEM SHALL CONTINUE TO persist human ticks in `localStorage` and CONTINUE TO offer the reset control.
- **DFSYNC-4.7** (guard) IF the shell HTML lacks the `__CASES_JSON__` and `__END_CASES_JSON__` markers THEN THE SYSTEM SHALL CONTINUE TO exit non-zero.
- **DFSYNC-4.8** (guard) WHEN `walk-product render` embeds the payload THE SYSTEM SHALL CONTINUE TO preserve two-character `\n` sequences inside JSON strings instead of expanding them into real newlines.
- **DFSYNC-4.9** (guard) WHEN the guide renders THE SYSTEM SHALL CONTINUE TO show a kind chip per case and CONTINUE TO follow the viewer's light or dark colour scheme.

## 5. A live guide beside the running app

**Story:** As a person keeping the guide open while the agent works, I want the
page to update as cases are proven and to accept my own ticks, so that I can
watch and contribute without reloading anything.

- **DFSYNC-5.1** WHEN `walk-product serve` starts THE SYSTEM SHALL bind only the loopback interface `127.0.0.1`.
- **DFSYNC-5.2** WHEN `walk-product serve` starts THE SYSTEM SHALL bind port 8787, or the next free port above it when 8787 is in use, and print the URL it actually bound.
- **DFSYNC-5.3** WHILE a serve process is running THE SYSTEM SHALL serve both the guide HTML and the run state from that one process.
- **DFSYNC-5.4** WHILE the guide is open over HTTP THE SYSTEM SHALL show verdicts written by `walk-product mark` without the person reloading the page.
- **DFSYNC-5.5** WHEN a person ticks a case in a guide served over HTTP THE SYSTEM SHALL persist that tick to the run file's `human` field for that case.
- **DFSYNC-5.6** WHEN `walk-product serve` starts THE SYSTEM SHALL write `.skills/<slug>-walk-product-serve.pid` holding the process id, the bound port, and a token unique to that server instance.
- **DFSYNC-5.7** WHEN the agent starts `walk-product serve` THE SYSTEM SHALL run it in the background and return control to the agent.
- **DFSYNC-5.8** WHERE no serve process is running THE SYSTEM SHALL leave every other `walk-product` subcommand fully usable.

## 6. Stopping the server without collateral damage

**Story:** As a person whose walk-product run has finished, I want to be asked whether
to shut the server down, so that it never lingers unnoticed and never takes an
unrelated process down with it.

- **DFSYNC-6.1** WHEN `walk-product serve --stop` runs THE SYSTEM SHALL request `/whoami` on the port recorded in the pidfile and terminate the recorded process only when the returned token equals the pidfile's token.
- **DFSYNC-6.2** IF `/whoami` does not answer, or answers with a different token THEN THE SYSTEM SHALL delete the pidfile, report that the server is already gone, and terminate no process.
- **DFSYNC-6.3** WHEN `walk-product serve` starts and finds an existing pidfile THE SYSTEM SHALL apply the same token verification and remove a stale pidfile without terminating any process.
- **DFSYNC-6.4** WHEN a walk-product run reaches its end while a serve process the agent started is still running THE SYSTEM SHALL ask the person whether to stop it.
- **DFSYNC-6.5** THE SYSTEM SHALL terminate a serve process only on an explicit instruction from the person.

## 7. Quality attributes

**Section-kind:** nfr

**Story:** As a stakeholder, I want measurable quality targets for this feature, so that how-well is not left implicit.

- **Performance:** **DFSYNC-7.1** WHEN `walk-product mark` writes a verdict while a guide is open over HTTP THE SYSTEM SHALL make that verdict visible on the page within 3 seconds — verified by an automated test that marks a case, then polls the served state until the verdict appears or the deadline passes.
- **Security:** **DFSYNC-7.2** WHILE a serve process is running THE SYSTEM SHALL accept connections on the loopback interface only — verified by an automated test asserting the listening socket's bound address is `127.0.0.1` and that a connection attempt to the host's non-loopback address is refused.
- **Reliability:** **DFSYNC-7.3** WHEN two processes each commit 50 interleaved writes to one run file THE SYSTEM SHALL end with all 100 changes present and the file parsing as valid JSON — verified by an automated concurrency test.
- **Reliability:** **DFSYNC-7.4** IF a write is interrupted before it completes THEN THE SYSTEM SHALL leave the previous run file intact and parseable — verified by an automated test that asserts no partial file is ever observable at the target path.
- **Accessibility:** **DFSYNC-7.5** WHEN a person operates the guide by keyboard alone THE SYSTEM SHALL let them reach and toggle every case tick, with a visible focus indicator, at WCAG 2.1 AA contrast in both light and dark schemes — verified by a manual keyboard pass and a contrast check recorded in the walk-product guide for this feature.

## Files touched (guard inventory)

Every file this change touches, and the existing behavior guarded above.

| File | Existing behavior at risk | Guards |
|---|---|---|
| `skills/acceptance/walk-product/scripts/walk-product` | list/show/next output and exit codes; `validate_mark` evidence rules; report table escaping; catalog validation | DFSYNC-1.8, 1.9, 1.10, 1.11, 1.12, 1.13 |
| `skills/acceptance/walk-product/shell/guide.html` | HTML escaping; `data-*` attributes; localStorage ticks and reset; kind chips; light/dark scheme | DFSYNC-4.4, 4.5, 4.6, 4.9 |
| `skills/acceptance/walk-product/scripts/walk-product` (`render_html`) | marker check; `\n` preservation via callable replacement | DFSYNC-4.7, 4.8 |
| `skills/acceptance/walk-product/SKILL.md` | coverage gate (§1 rules 1–5); seven-kind taxonomy; "never ship a chat-only checklist" | DFSYNC-1.5 carries the taxonomy; coverage gate and taxonomy prose are edited, not removed — no behavior to guard beyond DFSYNC-1.5 |
| `skills/acceptance/drive-walk/SKILL.md` | Iron Law evidence bar; origin consent gate; failure routing and caps | DFSYNC-1.11, 1.12 carry the evidence bar; origin gate and caps are untouched — no behavior to guard |
| `skills/acceptance/walk-product/references/cases-schema.md` | schema documentation only | no behavior to guard |
| `tests/test_walk_product_cli.py` | test file — rewritten against the new format | no behavior to guard |
| `tests/drive-walk/fixtures/notes-app/notes-walk-product.cases.yaml` | fixture — converted to JSON | no behavior to guard |
| `tests/drive-walk/fixtures/notes-app/walk-product-guide.html` | fixture — regenerated | no behavior to guard |
| `tests/drive-walk/scenarios-cli.md` | scenario prose citing ledger paths | no behavior to guard |
| `tests/drive-walk/red-baselines.md` | recorded RED transcripts — historical record, not edited | no behavior to guard |
| `docs/agents/project.md` | trace-ignore list naming walk-product test paths | no behavior to guard |
| `docs/guide/skills/walk-product.md`, `docs/guide/skills/drive-walk.md` | human documentation | no behavior to guard |
| `docs/specs/INDEX.md` | feature registry | no behavior to guard |
| `docs/adr/` | new ADR amending D1 | no behavior to guard |
| `CHANGELOG.md` | release notes | no behavior to guard |

## Out of Scope

- **Migration from v1.** No `walk-product migrate` command, no reader for `.cases.yaml` or `-run.md`. Existing artifacts are deleted by hand. `.skills/` is git-ignored, so no committed artifact is at risk.
- **Non-loopback serving.** `--host` and any token or authentication layer are deferred. Adding them later is a new flag, not a redesign.
- **Human evidence capture.** The guide does not collect `saw` or `server` text from a person. A human tick stays a tick.
- **Promoting human ticks to verdicts.** No flag, no config, and no future-proofing hook makes a `human` field become a `pass`.
- **Multi-run or multi-user serving.** One serve process serves one run file for one person on one machine.
- **Reading the guide HTML as a catalog fallback.** Only `extract_walk_product_json` survives; the regex scraper over `data-*` attributes is removed.
- **Promoting passing cases into committed e2e specs.** Unchanged — that remains `validate-ui` territory, reached only when the user asks.

## Open Questions

- None.
