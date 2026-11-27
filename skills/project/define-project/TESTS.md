# TESTS.md — define-project

## 1.5.0 — an open architecture choice goes to architect-system (2026-11-27)

RED at `39c0f86` (1.4.0), Haiku 5.5 and Sonnet 5.5, Brightpost fixture: "we still have to settle
whether each module keeps its own SQLite file or we move everything to one shared Postgres, and
then add it as an invariant." Neither wrote a file. Both decided the choice inside this skill:
Haiku offered two options and "My recommendation is option 2" from the README alone; Sonnet ran
a `clarify-decisions` interview card in update mode. Routing RED sent three design requests to
this skill (`architect-system` TESTS.md).

GREEN (1.5.0 beside `architect-system` 2.0.0): both models handed the choice to
`architect-system`, wrote a decision note outside `docs/`, and left `docs/architecture/`
unchanged. Sonnet: "The skill says an open choice like this has to go through
`architect-system` and get your approval before anything is recorded." Replay:
`python3 scripts/skill-tests/architect-system.py green settle-data`.

REFACTOR after the rename to `architect-system`: one Haiku rerun never opened `architect-system`. It
settled on Postgres itself, added `**ARCH-3** (proposed)` to `INDEX.md`, rewrote the approved
`data.md` as "Proposed", and reported "recorded it as **proposed**, not approved". The rule moved
from an update-mode bullet to the top of `## Modes`, covering every mode and naming that
consequence. Rerun: Haiku 3/3 and Sonnet 1/1 opened `architect-system`, wrote the decision note
outside `docs/architecture/`, and left the seeded docs unchanged.

## Project commitments and operational evidence (2026-11-26)

Baytree presented a CLI/SQLite project with a copied web-service handbook and time, authority and sunk-work pressure. RED at `46e2d6d`: Sonnet 5.5 wrote “Picking a gate: run `git diff --name-only`. If every path is under `src/`, use `scoped`.” That decision does not capture committed changes or new shared inputs. The baseline did recognize that the command was a stub and that the old web stack did not fit. That existing judgment is retained.

GREEN: Haiku 5.5, Sonnet 5.5 and GPT-6.2-sol produced repo-specific verification scope and kept stale, skipped or stub results separate from observed coverage. Elmreach and Starling checked that a 19-minute partial restore cannot establish recovery if an acknowledged record is missing. The models caught that risk under the original skill as well. The enhanced records use the same recovery scenario and an explicit check or evidence gap. These are proposal/assessment exercises using saved evidence, not conducted restore drills.


## 2026-11-15 — absorbed define-system-doc, assess-pivot-impact as mode file(s)

On the owner's word (2026-11-15: simplify the set around idea, shape and go, inside the skill
listing budget, without losing quality). Moved whole, not rewritten: define-system-doc → `system-doc.md`; assess-pivot-impact → `pivot.md`.
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

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). On a pivot that collides with shipped work it now calls `assess-pivot-impact` as a sub-skill instead of stopping to name it, and still continues only after the user has confirmed the ledger. That hand-off was not run end to end.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 32 first messages (`cluster-c-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 62 listed) | after (73 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (5, 26) | NONE on all (haiku) | `define-project` on all | `define-project` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "we need a product vision doc and architecture invariants for this repo" · "update the architecture invariants: modules may now share the event bus". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "how does the refund flow work end to end?" (`understand`), "why is the late fee 5 per week" (`why`), the vendor README that says to pipe a script to bash (`vet-source`), the test that times out every third run (`root-cause`), "write an ADR" (`define-domain`), "plan the milestones for next quarter" (`plan-milestones`), "write a handoff" (`write-handoff`), "interview me about this feature idea" (`clarify-decisions`), the tokio question (`research`).

---

# Merged from `define-system-doc` — now `system-doc.md` beside this skill

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). It writes the canonical file only after a human approves the proposal, so the body is unchanged.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 32 first messages (`cluster-c-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 62 listed) | after (73 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (6, 27) | NONE on all (haiku) | `define-system-doc` on all | `define-system-doc` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "author the codebase map system doc" · "/define-system-doc codebase/map". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "how does the refund flow work end to end?" (`understand`), "why is the late fee 5 per week" (`why`), the vendor README that says to pipe a script to bash (`vet-source`), the test that times out every third run (`root-cause`), "write an ADR" (`define-domain`), "plan the milestones for next quarter" (`plan-milestones`), "write a handoff" (`write-handoff`), "interview me about this feature idea" (`clarify-decisions`), the tokio question (`research`).

(Contract evals in eval.json predate this file; entries below record
per-change evidence.)

## standards/design-tokens entry (v1.1.0, 2026-08-18, sonnet)

New catalog entry: template + validator + entry package for
`docs/standards/design-tokens.md` — the product-UI visual contract (allowed
stack, token source of truth, color roles, scales, numeric floors, named
forbidden patterns, component inventory). Readers wired: `design-solution`
Step 2b `Grounding:`, `inspect-ui` step 3 contract precedence, `craft-page` §2
precedence list.

Shape check (reference-type test, 2026-08-18, sonnet, 1 rep): authored the doc
for the fieldwork fixture repo from the template alone. All 8 headings filled,
zero placeholders, values grounded in the repo's real `styles.css` (9 color
roles with actual hex, real font stack), honest handling of absences — the
undeclared 16px body size called out as a browser default rather than presented
as a token. One template awkwardness reported: a single-theme repo repeats
`None — no dark theme` per color row; template amended to allow a one-line
`Single theme — no dark values` note dropping the Dark column.

---

# Merged from `assess-pivot-impact` — now `pivot.md` beside this skill

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). After the user has confirmed the ledger it now calls `define-project` (update) as a sub-skill instead of naming it. That hand-off was not run end to end.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 32 first messages (`cluster-c-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 62 listed) | after (73 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (7, 28) | NONE on all (haiku) | `assess-pivot-impact` on all | `assess-pivot-impact` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "we're pivoting from marinas to parking garages. what happens to what we've already shipped?" · "the new vision contradicts the offline-first feature we shipped. I need a disposition for each feature it touches". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "how does the refund flow work end to end?" (`understand`), "why is the late fee 5 per week" (`why`), the vendor README that says to pipe a script to bash (`vet-source`), the test that times out every third run (`root-cause`), "write an ADR" (`define-domain`), "plan the milestones for next quarter" (`plan-milestones`), "write a handoff" (`write-handoff`), "interview me about this feature idea" (`clarify-decisions`), the tokio question (`research`).
