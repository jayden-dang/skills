---
name: architect-system
version: 2.1.0
description: "Use when deciding how the whole system should work, never for one feature (a single feature's architecture or design.md is design-solution): the front end of a web, desktop or mobile client (rendering, client state, data fetching, auth tokens, version skew, performance budget, accessibility), caching (Redis or none), messaging and queues (Kafka, outbox, background jobs), sync or async calls between modules and services, data stores and consistency, module boundaries, tenant isolation, retries and idempotency, failure and recovery, logging and secrets, or the principles every feature builds by, for a new project, a running codebase, a takeover or a migration. Produces a diagrammed system design decision note with proposed ARCH-N invariants, each with the check that keeps it true, ready for approval. Not for recording a decision already made (define-project), one feature's design.md (design-solution) or a refactor or tech-debt scan of existing code (scan-architecture)."
---

# Architect System

Choose how the system works, part by part, so every feature after it follows
the same rules. This skill decides. It writes one decision note and disposable
probes in scratch. Production code, `docs/architecture/`, `docs/adr/` and
`docs/standards/` stay untouched: `define-project` records them after the user
approves (step 8). In a baseline run an agent wrote `docs/adr/0001` before the
review it was preparing for, while its own note said nothing had been recorded.

The user owns the note's location. A filename alone means a file at the
checkout root. When the location is open, use the repo's review-note
convention. A project-wide UI design system (tokens, components) belongs to
`codify-design-system`: name it in the note. One screen's look belongs to `draft-ui`, one
feature's design to `design-solution`.

## 1. Establish the starting point

Read `docs/architecture/` first. Every live `ARCH-N` is a constraint: a
proposal that breaks one names it and the change it needs. Then choose every
applicable row and read only the code, records and runtime evidence the
decision needs.

| Situation | First move |
|---|---|
| Greenfield | Pick the first valuable flow and its hardest outcome. Note the fixed stack, team size and platform limits. |
| Running codebase | Trace the requested path through the code with file references. Name what the code already does consistently, and where two places disagree. |
| Takeover | Reproduce one local path. Reconcile the handover, checkout and deployed evidence. Name the release, data and recovery owners or mark them unconfirmed. A different local path leaves the reported live topology unconfirmed. |
| Migration | Find the seams, existing consumers and compatibility obligations. Identify how old and new run side by side, and what makes cutover or rollback safe. |

**Done when:** the note names a primary flow, a consequential failure and one
plausible next consumer or change.

## 2. Pin the forces and the user's calls

List what each choice turns on: load and peak, latency budget, how stale each
kind of data may be, consistency, the delivery guarantees of outside systems,
team size and operating capacity. Take each from the repo with its file, or
mark it unknown.

Some answers belong to the user, not to you: a product policy (who wins when a
late field update meets a reassignment, how old a price may be shown), a
budget, a compliance limit. Ask each one before the choice that turns on it.
REQUIRED SUB-SKILL: use `clarify-decisions`, one question at a time. When
nobody can answer in this session, pick a provisional default, list it as the
user's decision, and hold the parts that depend on it. Never write one as a
principle: a baseline run made "field writes are never rejected for being
late" principle 2 of a foundation, and the founder had not been asked.

**Done when:** every force has a source or is marked unknown, and every user
call is answered or listed as open with the parts it holds.

## 3. Cover every part

Read `parts.md` beside this file. The note carries a **Parts** table with one
row per part there, each with one status: **decided here**, **already
settled** (cite the `ARCH-N` or the code), **deferred** (with the trigger that
reopens it) or **not needed yet** (with why). Baseline foundations covered
exactly the parts the request named; backup, secrets and observability went
unmentioned. A request for one part still gets the table: decide that part and
the parts it depends on, in the order `parts.md` gives.

When the project has a client a person uses (a web, desktop or mobile app), also
read `frontend-parts.md` and add one row per part there. Baseline front-end
notes folded rendering, accessibility and i18n into "Code structure" and
"Principles" rows, and one web note never mentioned accessibility or a
Content Security Policy although an incident file reported rendered user HTML.

**Done when:** every row has a status, and every decided part's dependencies
are decided or already settled.

## 4. Compare and draw

For each part decided here, write: the forces it answers, two or three viable
options, the choice, each rejected option with its reason, and what would
change the choice. When only one option meets a confirmed constraint, state
the constraint and test the survivor. Name callers, modules, dependency
direction, where authoritative state lives, and where permission, mutation
and recovery are enforced.

Read `diagrams.md` and draw the views that carry the decision. Every note has
an architecture view. Put the comparison and figures in the note.

**Done when:** a reader can follow the primary flow from its entry point to
its authority and see what each rejected option would have changed.

## 5. Probe what the decision turns on

Run the smallest slice that crosses the seams under decision, in scratch,
through the primary flow and the consequential failure. Use the project's
real entry point or adapter wherever its behavior is the question, and
existing harnesses first. Use the smallest input that tells the options
apart. Give concurrent or external probes a deadline.

**Exercise the next change.** Run a second consumer through the proposed
interface, or apply the next change in scratch. Use an existing caller when
one exists. "No second caller exists yet" does not skip this check: write
that consumer in scratch and run it through the proposed interface with its
own input, such as an existing record and a missing ID for a detail reader.
Label interface evidence as such. If a check cannot run, name the
missing input, permission or environment and the work it holds.

Record each load-bearing claim with **scope, command or source, observed
result, and what it leaves open**, and keep the script or exact invocation. A
fake is evidence for the part it exercised. Show the observed boundary in the
figure as well as the note.

**Done when:** the primary, failure and next-change checks each have an
outcome or an explicit open entry.

## 6. Turn rules into invariants with checks

Every rule the team must follow becomes a proposed **ARCH-N**: the next ID
past the highest live one, marked proposed, one imperative rule. Give each its
**keeping check**: what fails when someone breaks the rule (an import or
dependency lint, a test, a schema constraint, a `grep` in CI) and where it
runs. A rule no automated check can hold names the review step that does.
Baseline notes proposed eight rules with no check, and one marked its own
module boundary "not enforced by tooling" and moved on.

**Done when:** every proposed rule has an ID, one imperative sentence and a
keeping check or a named review step.

## 7. Decide what can start

Ask four questions of the supported scope: does it fit the product, can a
second consumer use it, do the ownership boundaries hold, and can someone run,
change and operate it? Mark each material answer **observed**, **off-target**
or **open**. A well-presented design does not clear a missing result.

- **Ready:** start the named slice; its foundation risks are settled.
- **Ready within limits:** start the named independent work and enumerate
  what waits. A test at one seam supports a slice at that seam, not rollout.
- **Needs another check:** name the smallest check that can change the verdict
  and any settled work that can proceed meanwhile.

For each held item, name the evidence that releases it and an owner or role.

## 8. Stop for approval, then hand off

End the note with **Awaiting approval** and the exact list to be recorded:
each proposed `ARCH-N`, each part document, each ADR-worthy decision. Stop
there. Once the user approves, REQUIRED SUB-SKILL: use `define-project` in
update mode to record what they approved. Hand the first feature to the repo's
normal spec and build workflow.

## Red Flags

- A file under `docs/architecture/`, `docs/adr/` or `docs/standards/`, or a production file, changed before approval.
- A principle that settles a product policy nobody asked the user about.
- A rule with no ID, or an ID with no keeping check.
- A Parts table missing a row from `parts.md`.
- Caching a value before deciding who owns it and how stale it may be.
- Testing only the rejected option, then recommending the untried one.
- Treating a later reuse plan as a second consumer result.
- A next-change check marked "not run" because the second consumer is not built yet.
- Describing two local call sites as two active production writers.
- Counting a skipped restore or a passing local storage probe as release evidence.
- Ending with a project-wide yes when the checks covered independent local work.

**No-op:** a decision already made and only to be written down or checked goes
to `define-project`. One feature's design, one screen, or a refactor scan
stays with its existing owner.
