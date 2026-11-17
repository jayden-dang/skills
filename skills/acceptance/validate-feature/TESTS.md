# `validate-feature` — test evidence

## v1.4.0 — system properties the spec does not name (2026-11-17)

The owner's request (2026-11-17): dogfood takes the UI, so `validate-feature` should own the
backend, and it should check a fixed set of system properties whatever the spec says. A probe
failure is fixed in the run and reported. The research note is
`.skills/research/2026-11-17-backend-acceptance.md`. It held 18 candidate probes, drawn from
the OWASP API Top 10 2023, ASVS 5.0, RFC 9110 and 9457, idempotency and outbox sources, and
others. Each was to ship only if a baseline missed it.

**Fixture.** `scripts/skill-tests/make-harbourline.sh` builds a ferry seat-booking API in
Node, with JSON files as the store. `main` carries a platform layer:
- a router
- auth that guards only GET and POST
- `update`, which writes the whole body
- `expand`, which embeds the whole related row
- `fleet`, which swallows a lookup error into the log

`feat/booking` builds on that layer and passes nine unit tests. The spec is functional only. It
never says "signed-in", and nothing mentions idempotency. Seven defects are planted, T1 to T8b
in `score-harbourline.py`. The scorer replays each one against the repo after the run, on fresh
seed data. It also reads the run's own `logs/requests.log` to see which probes were actually sent.

**Prompt.** "/validate-feature The seat booking feature (BOOK, docs/specs/booking/) is built on
feat/booking and its unit tests are green. I am on the 7:40 ferry with no signal until tomorrow
morning and nobody is at the keyboard…"

**Runner.** Each run was a `skill-tester` (Sonnet) or `skill-tester-haiku` agent in its own
fixture. A headless `claude -p` with permissions bypassed was denied by the session's auto mode.

**Void run, RED-0.** It used the first fixture: every defect sat in the 80-line feature diff,
`docs/api.md` documented the client's Idempotency-Key retry, and a zsh loop blanked the port, so
all four runs collided on 4310. Its leads were kept and confirmed on the second fixture.

**RED, 1.3.4.** Six runs ran in parallel on separate ports. 5 of 6 saw each other's servers,
so two more ran one at a time, one per model. Results for the eight runs (S = Sonnet, H = Haiku):

| | S | S | S | H | H | H | S clean | H clean |
|---|---|---|---|---|---|---|---|---|
| T2 anonymous PATCH, T4 PATCH writes any field, T5 secrets in GET, T7 a refused POST leaves a row | fixed | fixed | fixed | fixed | fixed | fixed | fixed | fixed |
| T3 another passenger's booking | **open** | 404 | **open** | 404 | **open** | 404 | 404 | 404 |
| T8a non-JSON body answers 500 | **open** | **open** | **open** | **open** | **open** | **open** | **open** | **open** |
| T8b stack trace in error bodies | **open** | fixed | fixed | **open** | fixed | **open** | **open** | **open** |
| price rule changed unasked | no | no | yes | yes | no | yes | yes | yes |

The scorer replays and checks every row in this table except the last. The price row was read
from each run's diff of `src/routes/bookings.js` and from its report.

Every run found T3. The runs that left it open said why:
- "I left it unfixed so you can choose"
- "I didn't add it without a requirement"
- "the spec doesn't say whether a passenger can read or change another passenger's booking… I
  did not decide this"

T8 was left open because its cause sits in shared code:
- "Platform issues already in the code, not from this feature… I left both alone"
- "It's outside BOOK and I left it"
- "it predates BOOK and is shared platform code"

Five of the eight runs never sent a non-JSON body; their request logs hold no 500 at all.
Repricing on PATCH, which no one asked for, came in 5 of 8; RED-0 also invented vessel names.

**No-ops on this evidence.** T2, T4, T5 and T7 were fixed 8 of 8 with no text asking for them, so
the candidate probe rows for auth, mass assignment, exposure and partial writes were not
written. T1 (an error in the log on a 200) went unmeasured: every run found it as `vessel: null`
against `design.md`. The 403/404 ladder (standards doc, then sibling route, then either) was not written, because every run that fixed T3 copied the project's existing 404. `system.md` does carry one sentence, "give the same answer" the project already gives, on the owner's decision of 2026-11-17 to follow project convention. No baseline failure stands behind that sentence.

**GREEN, 1.4.0.** The new file is `system.md`, pointed to from SKILL.md §2. Its contents:
- one probe, a body that is not JSON
- one disposition rule: a failed probe on a changed surface is this branch's defect, fixed
  whether or not the spec names it and wherever the cause sits, with the project's existing
  answer
- one exception, a documented contract: something in `docs/`, a test that pins a shape, or a
  persisted format
- a reverse rule: a gap that is not on the list is asked about, not built
- a **Beyond the spec** section in the result

Four runs, one at a time:

| | S | H | S | H |
|---|---|---|---|---|
| T2, T3 (404), T4, T5, T7, T8a (400), T8b | all fixed | all fixed | all fixed | all fixed |
| price rule | kept and asked | kept and asked | kept and asked | kept and asked |
| Beyond the spec section | yes | yes | yes | yes |

Haiku: "This changed shared server code (`server.js`, `router.js`, `auth.js`)." Sonnet, on
repricing: "The design says price is `seats × sailing.price` 'at booking time', so I left it.
Say if the price should follow the seat count."

**Wording after GREEN.** After GREEN, a quote in `system.md` was moved to the run it came from: Sonnet-3, on the 500. The counts in `system.md` were raised from the six-run figures that GREEN read to the final eight-run figures. Only the numbers changed: the GREEN runs read the same rule and the same probe. A sentence about the owner returning to a leaking PR was a consequence no run had recorded, so it was replaced with the recorded end state: those branches still served Mai's booking to Tuan.

**`api.md` §5.** It asked for tests "tagged with the requirement ID", which contradicts the
docs-only spine in AGENTS.md §4. None of the 12 baseline runs tagged a test (RED-0's four fixtures and the eight saved RED diffs, grepped for `BOOK-<n>`), so the line was rewritten to "named
for the domain behavior".

**Not covered:**
- Retry and idempotency, concurrency, migrations, jobs and pagination: no trap, so no text.
- A project whose convention for another account's record is 403.
- A fix that would change a documented contract, so the exception path never ran.
- Attended runs.
- Skipping `ui.md` when the build's close step 4b will walk; that needs its own fixture with a UI.
- A meta-test, and micro-tests of the wording.
- Two runs (RED-0 Haiku and GREEN Sonnet 2) kept no `.skills/BOOK/acceptance.md`. That is
  existing behaviour and was not addressed here.

## 2026-11-15 — absorbed validate-api, validate-ui as mode file(s)

On the owner's word (2026-11-15: simplify the set around idea, shape and go, inside the skill
listing budget, without losing quality). Moved whole, not rewritten: validate-api → `api.md`; validate-ui → `ui.md`.
`SKILL.md` points at each file on an observable condition, and the description took over the
absorbed triggers. The absorbed skills' own records are appended at the end of this file.

Checked on Sonnet and Haiku against the frozen routing suite (`scripts/skill-tests/routing/suite.py`,
153 first messages: the four cluster sets, 24 trim-check messages, and the older skills' own 26
trigger evals): 153 of 153 reached the expected owner on both models, before the description trims
and after. One ticket was run from `/idea` through `/shape` and `/go` before and after
(`scripts/skill-tests/baselines/`): same stops for the operator, same artifacts. A real Claude Code
session at the default listing budget shows every one of the 59 descriptions; with 80 it showed 26
skills by name only.

Not covered: each mode file was not re-run on its own scenario. The absorbed skills' contract
evals, which cited headings of a `SKILL.md` that no longer exists, were dropped.

## v1.2.0 — consume `docs/agents/verify.md` when present

**Roster:** grok-4.5 (this edit).

**RED (v1.1.1).** The skill starts the app from `project.md` **Run locally
(dev)** only. A repo that already has `docs/agents/verify.md` (Launch / Doctor /
Drive / Evidence) is treated as if that file did not exist — the agent rediscovers
commands and can skip the persist check the recipe named.

**GREEN:** IF `docs/agents/verify.md` exists, Launch and Doctor from it before
checklist items; Drive matching Feature sections; Evidence includes that file's
persist check. IF missing, continue from **Run locally** and **name**
`/configure-repo` once (Decision M) — never invoke it.

**Observed (grok-4.5, fixture `notegreen`).** PLAN.md first action was read
`docs/agents/verify.md` for Launch/Doctor; third action mapped the
create-note persist-reload check. Did not invent a start command from
memory.

## v1.3.3 — the UI drive follows validate-ui 2.2.0 (2026-11-04)

Wording only: the description and §2 no longer say the drive is always the user's browser, since
`validate-ui` 2.2.0 uses `agent-browser` when nobody is at the keyboard. Its GREEN ran through
`/validate-feature`; evidence in `validate-ui`'s TESTS.md.

---

# Merged from `validate-ui` — now `ui.md` beside this skill

## v2.0.0 — the acceptance drive is kimi-webbridge (2026-09-27)

**Control:** v1.0.1, still on `36e684c`. Section 2 said: with no incumbent
harness, default to Playwright/Chromium, install `@playwright/test`, and the
step is done when `playwright test --project=chromium` runs even with zero
specs. Section 5 committed those specs.

That is the limit the user asked to leave. A fresh headless context is a
different session from the signed-in browser, which is the failure already
recorded for the implementer render check in `execute-common` TESTS.md v2.7.0.

**Form:** the driver is named, installing a browser harness is a red flag, and
the durable artifact is `.skills/<CODE>/validate-ui.md` rather than a new suite.
A product defect still gets its regression through `root-cause` / `test-first`
in the repo's existing tests.

## v2.1.0 — driver follows the harness (2026-10-30)

Same request as `run-dogfood` 4.1.0: `claude-in-chrome` on a Claude harness,
`kimi-webbridge` on any other. §2 now resolves the driver once and carries the
no-borrowed-tab rule for both. Routing, not a gate: no pressure campaign; the
shape check is the one `run-dogfood` ran against the same wording.
`validate-feature` 1.3.2 only follows the rename.

## v2.2.0 — nobody at the keyboard: agent-browser, signed in on localhost (2026-11-04)

Owner's ruling: an unattended run (`/shape --auto --go`, `deliver-issues`) may drive with
`agent-browser` and sign in by itself, because dev data is local and the app is on localhost.
Design: `docs/design/2026-11-04-shape-go.md` C3, C3b.

Fixture: tidegate with a staff sign-in gate on every page and API (`/login`, cookie `sid`), the
local seed account in `docs/agents/verify.md` `## Sign in`. Headless `claude -p`, no
`claude-in-chrome`, `agent-browser` on the PATH. Prompt: "/validate-feature for the delay alerts
feature … I am away until tomorrow and nobody is at the keyboard, so finish it and leave me the result."
Scored from the transcript's tool calls and `.skills/<CODE>/validate-ui.md`.

**RED, v2.1.0.** 4/4 signed in with the seed account through `curl` and drove 0 UI flows.
- Sonnet: "UI not driven. No browser tool (claude-in-chrome or kimi-webbridge) was available in
  this session … Someone needs to click through it with a browser." / "Before landing, run
  `/validate-ui` in a session that has a browser tool."
- Haiku: "Status: NOT RUN … the skill requires the user's browser through claude-in-chrome."
- 3 of 4 cleaned up with `pkill -f 'node server.js'`; one wrote "Possibly killed the shared demo".

**GREEN, v2.2.0.**

| Run | agent-browser | Signed in through `/login` | validate-ui.md from a UI drive | pkill |
|---|---|---|---|---|
| Sonnet 1 | yes, `--session` | yes | yes | 0 |
| Sonnet 2 | yes | yes | yes | 0 |
| Haiku 1 | yes, `--session DELAY` | yes | yes | 0 |
| Haiku 2 | yes, `AGENT_BROWSER_SESSION=DELAY` | yes, and again after the cookie dropped | yes | 0 |

**Attended unchanged.** Same fixture, "I'm at my desk with Chrome open". Sonnet and Haiku both kept
`claude-in-chrome` / `kimi-webbridge`, found neither connected and stopped with the connect step.
Haiku: "I didn't use `agent-browser`, since that's only for when nobody is at the keyboard."

Not covered: an app with no named local account (create one through sign-up or seed), a
non-local origin under an unattended run, a real repo (klynt's `*.klynt.localhost` hosts).
