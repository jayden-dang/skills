# Design: Walk Product sync

Feature code: DFSYNC
Status: Approved
Date: 2026-07-30
Requirements: ./requirements.md

## Context

A walk-product run today is three files that do not know about each other.
`scripts/walk-product` authors `.skills/<slug>-walk-product.cases.yaml`, renders a snapshot
of it into `.skills/<slug>-walk-product.html` by substituting a JSON blob between two
markers (`render_html`, `scripts/walk-product:484`), and records verdicts in a wholly
separate markdown ledger parsed by regex (`parse_ledger`, `:378`). The guide has
no channel to the ledger, so a person reading it cannot see what the agent
proved; and the guide's only writable state is a `localStorage` tick
(`shell/guide.html:264`) that nothing off that browser can read. The person and
the agent are looking at the same run through two windows that do not connect.

The binding constraint is **ARCH-3**: consumer-repo adoption must never mandate
Python, a daemon, or any running process for the methodology to work. That rules
out the obvious fix — making the guide fetch its state from a companion file or a
service — because a guide that only tells the truth while something is running is
a guide that lies whenever it is not. So the design keeps the rendered HTML
*self-sufficient*: `render` bakes current verdicts into the page, and the page is
correct on a `file://` double-click with nothing installed and nothing running.
The live layer sits strictly on top of that, and its absence costs freshness,
never correctness.

The second shaping constraint came out of the interview: a human tick must never
become a `pass`. `drive-walk`'s Iron Law is not "do not use localStorage" — it
is *the screen is necessary and not sufficient*, mechanically enforced by
`validate_mark` (`:447`), which refuses a `pass` with empty `--saw` or `--server`
and polices the `presentational` sentinel in both directions. Letting a checkbox
write a verdict would route around that gate through a door the gate cannot see.
So the run file carries two disjoint field spaces — `run` for the agent's
evidence-backed verdict, `human` for the person's tick — and no code path
promotes one into the other. This preserves decision **D1** in
`docs/specs/2026-07-26-drive-walk/research.md:231`; it does not reverse it.
What changes is only where a tick is stored and who can read it.

The third constraint is a trade the user made with the cost stated. `serve` is a
background process the agent starts, which is the largest ARCH-3 friction this
skill set has taken on: every other enforcement mechanism here is a `grep`, a
`git` call, or a file read. It is recorded as an ADR rather than smoothed over,
and it is bounded — bound to loopback, optional by construction, and stoppable
only through a check that proves the process is ours.

## Decisions

1. **One artifact, `version: 2`.** `.skills/<slug>-walk-product.json` holds cases and
   run state. The version bumps to 2 because embedded `window.__WALK PRODUCT__` blobs
   in already-rendered guides declare `"version": 1` (`catalog_from_dict`,
   `scripts/walk-product:119`); reusing 1 would make old and new indistinguishable.
2. **Hard cut, no migration.** No `migrate` command and no v1 reader.
   `load_cases_yaml`, `load_cases_html`'s regex scraper and its helpers are
   deleted; `extract_walk_product_json` survives. A `.yaml`/`-run.md` path is a named
   error, not a parse attempt (DFSYNC-1.7).
3. **PyYAML dropped.** The CLI becomes standard-library-only, removing the one
   hard third-party dependency (`scripts/walk-product:18-21`) — a direct ARCH-3 gain.
4. **Two disjoint field spaces per case.** `run` = `{verdict, saw, server,
   notes}`; `human` = `{checked, at, comment}`. The human key is `comment`, not
   `note`, so no reader can confuse it with `run.notes`.
5. **Exclusive lock for process mutual exclusion; `rev` for view staleness.**
   These solve different problems and both are needed — see *Store* below.
6. **Polling, not SSE.** The guide polls `/state` once a second. A 1 s interval
   meets the 3 s target of DFSYNC-7.1 with margin and keeps the server compatible
   with single-threaded `HTTPServer`, where a long-lived SSE connection would
   block every other request.
7. **`serve` does not daemonize itself.** It is an ordinary foreground process;
   the *caller* backgrounds it. DFSYNC-5.7 is satisfied by the skill body
   launching it backgrounded, not by a double-fork inside the CLI — which would
   add platform-specific process code for no behavioral gain. This reading is
   pinned here deliberately rather than left to the implementer.
8. **A stopped server is proven, never assumed.** `--stop` terminates only a
   process that answers `/whoami` with the pidfile's token. This is what makes a
   recycled PID structurally unkillable. → **ADR**
9. **The ARCH-3 friction of an agent-managed background process is accepted and
   recorded, not hidden.** → **ADR**

Decisions 4, 8 and 9 are hard to reverse, surprising without the reasoning, and
carry real trade-offs, so they are recorded as two ADRs under `docs/adr/`:

- **Tick semantics** — decision 4, amending D1 in
  `docs/specs/2026-07-26-drive-walk/research.md:231`. D1's conclusion survives
  intact; only the storage location and the reader change.
- **The background server** — decisions 8 and 9 together: accepting the ARCH-3
  friction of an agent-managed process, and requiring its shutdown to be proven
  rather than assumed.

### Architecture invariants relied on

- **ARCH-3** — zero mandatory tooling for adopters. Shapes the whole
  render-bakes-verdicts approach and bounds `serve` to optional.
- **ARCH-2** — optional layers no-op when absent. `serve` absent leaves every
  other subcommand fully usable (DFSYNC-5.8).
- **ARCH-1** — vertical checks are exact file/grep passes, never LLM judgment.
  Verdict provenance is a stored field, never inferred from context.

## Architecture

### Run file schema (v2)

Satisfies: DFSYNC-1.1, DFSYNC-1.2, DFSYNC-1.5, DFSYNC-2.1, DFSYNC-3.1
Reuse: existing — extends the eight-slot case shape already validated by `normalize_case` (`scripts/walk-product:97`) (rung 2)
Respects: ARCH-1

```json
{
  "version": 2,
  "rev": 7,
  "feature": "notes",
  "slug": "notes",
  "title": "Notes App — Walk Product",
  "origin": "http://localhost:5173",
  "intro": "…",
  "sections": [
    { "name": "Create & persist",
      "cases": [
        { "id": "CASE-1", "req": "NOTE-1.1", "kind": "happy",
          "title": "Create a note",
          "setup": "…", "try": "…", "expect": "…",
          "backend": "GET /api/notes includes title Alpha",
          "run":   { "verdict": "pass", "saw": "…", "server": "…", "notes": "" },
          "human": { "checked": true, "at": "2026-07-30T14:02:11Z", "comment": "" } }
      ] }
  ]
}
```

The eight authored slots keep their current names and meanings, so a v1 cases
file converts by hand with no rewording. `run` and `human` are the only additions
per case; `rev` is the only addition at the top. Validation reuses the existing
rules — required slots, seven-kind `KINDS` set (`:23`), duplicate-id rejection
(`:79`) — reporting the offending case and field (DFSYNC-1.5).

`run` and `human` share no key name. That disjointness is not a convention the
code hopes readers respect: it is what makes the merge in *Store* provably
conflict-free, and it is enforced at the HTTP boundary in *Serve*.

### Store — exclusive lock, atomic replace, `rev` for stale views

Satisfies: DFSYNC-2.2, DFSYNC-3.2, DFSYNC-3.3, DFSYNC-3.4, DFSYNC-7.3, DFSYNC-7.4
Reuse: stdlib — `json`, `os.replace`, `os.open(O_CREAT|O_EXCL)` (rung 3)

This is the one genuinely hard seam in the feature, so the alternatives are
recorded rather than assumed.

| Model | Verdict |
|---|---|
| `rev` compare-and-set alone, no lock | **Rejected.** The compare and the replace are not one operation; a writer can land between them. At ~1 ms per write the window is small but not negligible, and DFSYNC-7.3 (100 interleaved writes across two processes) would flake rather than fail cleanly — the worst kind of test. |
| `fcntl.flock` | **Rejected.** POSIX-only. This repo is macOS, but the skill set ships to whatever a consumer runs, and a Windows-only failure in a supposedly stdlib-portable CLI is the kind of breakage ARCH-3 exists to prevent. |
| `O_EXCL` lockfile + `rev` | **Chosen.** Portable across platforms and filesystems, pure stdlib, ~15 lines. |

The two mechanisms have distinct jobs and neither replaces the other:

- **The lockfile** gives mutual exclusion between OS processes. Every writer —
  each `walk-product mark`, and the serve process — acquires `<runfile>.lock` via
  `os.open(..., O_CREAT | O_EXCL)`, performs the whole read-modify-write, then
  releases. Acquisition retries on a short backoff; a lockfile older than 10 s
  is treated as stale and broken, which is three orders of magnitude above a
  real write.
- **`rev`** gives optimistic concurrency for *views that are already stale
  before the lock is taken*. The browser renders from a snapshot at `rev` 5 and
  the person ticks a case; by the time the POST arrives disk may be at `rev` 9.
  The request carries the `rev` it was based on, and the server applies the tick
  as a **field-scoped patch** onto the current document rather than writing back
  a whole stale object (DFSYNC-3.3). Because `human` and `run` share no keys,
  re-applying onto newer state can never clobber a verdict (DFSYNC-2.2) and
  always converges (DFSYNC-3.4).

Commit sequence, held under the lock:

```
acquire(lock) → read+parse → apply field-scoped patch → rev += 1
              → write <runfile>.tmp.<pid> in the same directory
              → os.replace(tmp, runfile) → release(lock)
```

`os.replace` within one directory is atomic, so a reader — or a run interrupted
mid-write — sees either the whole previous file or the whole next one, never a
partial (DFSYNC-7.4). The temp file lives beside the target so the rename never
crosses a filesystem boundary.

### CLI command surface

Satisfies: DFSYNC-1.3, DFSYNC-1.4, DFSYNC-1.6, DFSYNC-1.7, DFSYNC-1.8, DFSYNC-1.9, DFSYNC-1.10, DFSYNC-1.11, DFSYNC-1.12, DFSYNC-1.13, DFSYNC-2.3, DFSYNC-2.4, DFSYNC-2.5, DFSYNC-3.5, DFSYNC-3.6, DFSYNC-5.8
Reuse: existing — keeps the argparse subcommand layout (`scripts/walk-product:671`) and `validate_mark` unchanged (`:447`) (rung 2)
Respects: ARCH-2, ARCH-3

Every subcommand takes **one** path — the run file — replacing today's split
between a catalog argument and a ledger argument. `mark --catalog` disappears
because `backend` now lives in the same file the verdict is written to, which
also removes the failure mode where `validate_mark` silently skipped its
`presentational` checks when no catalog was reachable (`cmd_mark:591-606`).

| Command | Change |
|---|---|
| `list`, `show` | Output byte-identical to today (DFSYNC-1.8, 1.9) |
| `next` | Reads `run.verdict`; ignores `human` entirely (DFSYNC-2.3); still silent-with-exit-1 when none remain (DFSYNC-1.10) |
| `init` | Seeds `run.verdict = pending` where absent, leaves existing run state alone (DFSYNC-1.3), refuses a file holding a non-`pending` verdict without `--force` (DFSYNC-1.4) |
| `status` | Adds a `human:` count line beside the verdict counts (DFSYNC-2.4) |
| `mark` | Writes through the Store; opens no socket (DFSYNC-3.5) and behaves identically whether or not a server runs (DFSYNC-3.6) |
| `report` | Gains a human column; keeps one row per case and `\|` escaping (DFSYNC-1.13, 2.5) |
| `render` | See *Render and guide* |
| `serve` | New; see *Serve* |

`validate_mark`'s three rules are load-bearing and are carried over untouched
(DFSYNC-1.11, 1.12). Dropping `import yaml` makes the module standard-library-only
(DFSYNC-1.6); a `.yaml`, `.yml`, or `-run.md` path exits non-zero naming the v2
format instead of guessing (DFSYNC-1.7). With no server running, every one of
these still works (DFSYNC-5.8) — that is ARCH-2 in practice, not an aspiration.

### Render and guide — one shell, two modes

Satisfies: DFSYNC-4.1, DFSYNC-4.2, DFSYNC-4.3, DFSYNC-4.4, DFSYNC-4.5, DFSYNC-4.6, DFSYNC-4.7, DFSYNC-4.8, DFSYNC-4.9, DFSYNC-7.5
Reuse: existing — extends the `__CASES_JSON__` marker protocol (`scripts/walk-product:484`) and the guide's render IIFE (`shell/guide.html:172`) (rung 2)
Respects: ARCH-3

`render` keeps its exact mechanism — locate the marker pair, substitute a JSON
assignment via a **callable** replacement so `re.sub` never expands `\n` inside
JSON strings (`:510`, DFSYNC-4.8), and fail loudly when the markers are missing
(`:506`, DFSYNC-4.7). What changes is the payload: it now carries each case's
`run` and `human` alongside the authored slots (DFSYNC-4.1), plus the render
timestamp.

The shell picks its mode from the URL it was loaded under:

```js
var LIVE = location.protocol === "http:" || location.protocol === "https:";
```

- **`file://`** — paint from the embedded blob and stop. No `fetch`, no polling,
  no network of any kind (DFSYNC-4.2). A banner states that verdicts are the
  render-time snapshot and gives that timestamp, so a stale page announces its
  own staleness instead of impersonating live state (DFSYNC-4.3). Ticks continue
  to persist to `localStorage` under the existing `walk-product-ticks:<slug>` key,
  with the reset control intact (DFSYNC-4.6).
- **`http://`** — same first paint, then poll `/state` every second and repaint
  the badges whose `rev` moved (DFSYNC-5.4). Ticks POST instead of writing
  `localStorage`.

Each case grows a verdict badge beside — not replacing — its existing kind chip,
reusing the established `.chip` pattern and CSS custom properties so both colour
schemes are inherited rather than re-specified (DFSYNC-4.9). All case-supplied
strings keep going through `escapeHtml`/`escapeAttr` (`shell/guide.html:278`,
DFSYNC-4.4), and the five `data-*` attributes stay on each case element
(`:233`, DFSYNC-4.5). Ticks remain `<label>`-wrapped checkboxes, which is what
keeps them keyboard-reachable; the verdict badge is text plus colour, never
colour alone, and the focus indicator becomes explicit rather than
browser-default (DFSYNC-7.5).

### Serve — the optional loopback layer

Satisfies: DFSYNC-2.6, DFSYNC-5.1, DFSYNC-5.2, DFSYNC-5.3, DFSYNC-5.4, DFSYNC-5.5, DFSYNC-7.1, DFSYNC-7.2
Reuse: stdlib — `http.server.HTTPServer` + `secrets.token_hex` (rung 3)
Respects: ARCH-3

A single-threaded `HTTPServer` bound to `("127.0.0.1", port)` — the host is a
literal, not a flag, so there is no configuration path that exposes a writable
endpoint to the network (DFSYNC-5.1, 7.2). It tries 8787 and walks upward on
`OSError` until a port binds, then prints the URL actually taken (DFSYNC-5.2).
One process serves both the page and the state (DFSYNC-5.3).

| Route | Behavior |
|---|---|
| `GET /` | The guide, rendered on demand from current state so a reload is never stale |
| `GET /state` | `{rev, cases: {<id>: {verdict, human}}}` — verdicts and ticks only, not the authored case bodies the page already holds |
| `POST /human/<case-id>` | Applies a tick as a field-scoped patch through the Store |
| `GET /whoami` | `{token, slug, pid}` — the shutdown proof |

`POST /human/<case-id>` accepts exactly `checked`, `comment`, and `base_rev`.
Any other key — and in particular `verdict`, `saw`, `server`, or `notes` — is a
400 that writes nothing (DFSYNC-2.6). There is no route that writes a verdict at
all; the allowlist is a second lock on a door that was never built. A tick lands
via the Store's patch path, so it inherits the lock and the retry (DFSYNC-5.5).

`/state` is deliberately small: the page already holds every authored slot from
its first paint, so the poll carries only what can change. A 1 s interval puts a
mark on screen well inside the 3 s budget (DFSYNC-7.1).

### Process identity and shutdown

Satisfies: DFSYNC-5.6, DFSYNC-5.7, DFSYNC-6.1, DFSYNC-6.2, DFSYNC-6.3, DFSYNC-6.5
Reuse: stdlib — `os.kill`, `signal`, `json` (rung 3)

On start the server writes `.skills/<slug>-walk-product-serve.pid`:

```json
{ "pid": 41234, "port": 8787, "token": "<secrets.token_hex(16)>", "slug": "notes" }
```

The token is what makes shutdown safe. A pidfile holds a PID that the operating
system may since have recycled onto an unrelated process; `kill -0` cannot tell
the difference, because it answers "does this PID exist", which is exactly what
stays true after a recycle. So `--stop` never trusts the PID alone:

```
read pidfile → GET http://127.0.0.1:<port>/whoami
  ├─ token matches   → SIGTERM <pid>, remove pidfile          (DFSYNC-6.1)
  └─ no answer / mismatch → remove pidfile, report gone, kill nothing (DFSYNC-6.2)
```

`serve` runs the identical check on startup when it finds an existing pidfile: a
live server with a matching token means report the running URL and start nothing
second; anything else is a stale file to delete without signalling any process
(DFSYNC-6.3). Termination happens only down this path, which is reachable only
from an explicit `--stop` (DFSYNC-6.5).

Per decision 7, the CLI does not daemonize; the skill body launches it in the
background and the pidfile is what makes that process addressable afterwards
(DFSYNC-5.7).

### Skill bodies

Satisfies: DFSYNC-6.4
Reuse: existing — extends `drive-walk` §5 *Close the run* and `walk-product` §5 *Hand over* (rung 2)
Respects: ARCH-5

`drive-walk` §5 gains one step: when the run ends and a server the agent
started is still up, ask the person whether to stop it (DFSYNC-6.4). Neither
silently stopping nor silently walking away is permitted, which is why this is a
requirement rather than a note.

Text that becomes false is corrected, not left to rot: the Iron Law's second
line (`drive-walk/SKILL.md:26`) and the two rationalization rows about
localStorage (`:170-171`) describe a ledger that will no longer exist. The Law's
*substance* — evidence before `pass` — is unchanged and stays mechanically
enforced by `validate_mark`. `walk-product` §5 gains the `serve` command in its
hand-over, and `references/cases-schema.md` is rewritten for v2.

## Seams for testing

Tests are written at these boundaries and no others.

| Seam | Kind | Covers |
|---|---|---|
| `walk-product` CLI subprocess (existing seam, `tests/test_walk_product_cli.py:24` `run_cli`) | integration | DFSYNC-1.3, 1.4, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11, 1.12, 1.13, 2.3, 2.4, 2.5, 3.5, 5.8 |
| Run-file schema validation via `list`/`show` on crafted files | integration | DFSYNC-1.1, 1.2, 1.5, 2.1, 3.1 |
| Store commit function, called directly in-process | unit | DFSYNC-2.2, 3.2, 3.3, 7.4 |
| Two concurrent CLI subprocesses against one run file | integration | DFSYNC-3.4, 3.6, 7.3 |
| `render` output HTML, asserted as text | integration | DFSYNC-4.1, 4.3, 4.5, 4.7, 4.8 |
| Guide shell JS, loaded in a headless page over `file://` and over `http://` | e2e | DFSYNC-4.2, 4.4, 4.6, 4.9, 5.4, 5.5 |
| Serve HTTP endpoints, driven by an in-process client | integration | DFSYNC-2.6, 5.1, 5.2, 5.3, 5.6, 7.1, 7.2 |
| `serve --stop` against a live server and against a stale pidfile | integration | DFSYNC-6.1, 6.2, 6.3, 6.5, 5.7 |
| `drive-walk` scenario markdown under `tests/drive-walk/` | e2e | DFSYNC-6.4 |
| Manual keyboard and contrast pass, recorded in this feature's own walk-product guide | manual | DFSYNC-7.5 |

One new seam only — the Store commit function. Everything else extends the
existing `run_cli` subprocess seam or the existing scenario-markdown layer.

The guide-shell e2e seam is the one place this feature needs a browser. The repo
has no Playwright harness today (`docs/agents/project.md` records
`Browser E2E: (none)`), so `plan-tasks` must either stand one up as its own task
or route those five IDs to `validate-ui`, which owns harness setup. Flagged
here rather than discovered mid-implementation.

## Coverage check

All 52 requirement IDs appear in exactly one `Satisfies:` line.

| Story | IDs | Mapped to |
|---|---|---|
| 1 — one artifact | 1.1–1.13 | Schema (1.1, 1.2, 1.5), CLI (1.3, 1.4, 1.6–1.13) |
| 2 — human channel | 2.1–2.6 | Schema (2.1), Store (2.2), CLI (2.3–2.5), Serve (2.6) |
| 3 — two writers | 3.1–3.6 | Schema (3.1), Store (3.2–3.4), CLI (3.5, 3.6) |
| 4 — guide alone | 4.1–4.9 | Render and guide (all) |
| 5 — live guide | 5.1–5.8 | Serve (5.1–5.5), Process identity (5.6, 5.7), CLI (5.8) |
| 6 — safe shutdown | 6.1–6.5 | Process identity (6.1–6.3, 6.5), Skill bodies (6.4) |
| 7 — quality | 7.1–7.5 | Serve (7.1, 7.2), Store (7.3, 7.4), Render and guide (7.5) |

No deliberately unmapped IDs.
