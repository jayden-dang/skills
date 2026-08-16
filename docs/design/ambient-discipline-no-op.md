# Ambient discipline (simplicity / surgical axes) — tested, not written

**Date:** 2026-08-15 · **Roster:** Sonnet, Haiku 4.5, Opus 5 · **Reps:** 14 ·
**Verdict:** no-op on all three proposals. No skill text was written.

## What was proposed

A comparison against the community "Karpathy `CLAUDE.md`" distillation — four
principles: think before coding, simplicity first, surgical changes, goal-driven
execution — produced three candidate edits. Each looked like a real hole when
read against the set; none survived a baseline run.

| # | Proposal | Home it would have landed in |
|---|---|---|
| 1 | A **write-time volume check** ("could this be half the code?") — the set bans *scope* creep but never *volume* creep, and catches overweight-but-in-scope code only later, in `polish-diff` | `test-first` § GREEN, implementer self-review |
| 2 | A **match-the-existing-style** rule for the inline lane — the rule exists only in `implementer-prompt.md` (subagent lane) and `run-spike` | `build-inline` per-task loop |
| 3 | A **thin always-on layer** — the four principles as ambient text, because they hold today only *while a skill is loaded*, and `gate-session` carries routing, not conduct | `gate-session`, or a repo `CLAUDE.md` |

## What was tested

Three scenarios, each forcing a concrete A/B/C choice with "ask the user"
explicitly closed, under sunk cost + informal authority + end-of-day exhaustion.
Proposals 1 and 2 are *edits*, so their baseline carried the **current** skill
text verbatim; proposal 3's baseline carried **no skill text at all**, because
its whole premise is what happens when nothing fires.

**1 — Volume creep** (5 reps). Requirement CART-3.2, RED test green-able three
ways: a 9-line function, a 74-line `Discount`/`DiscountResolver`/`DiscountResult`
hierarchy already drafted and committed that afternoon, or a 31-line
`PromoCalculator` with a one-entry strategy map. None of the three adds a feature
or parameter the requirement did not ask for — the axis is *structure per unit of
behavior*, which is exactly the axis the current text does not name. A sibling
module's `CarrierRateResolver` (six carriers, two years) plus a tech-lead "nice —
matches how we do rates" supplied the authority pressure.

**5/5 chose the 9-line version**, and named the mechanism unprompted:

> "One entry is not a pattern, it's a rehearsal for a pattern." — Haiku
> "a strategy map with exactly one entry is a fork in the road with only one road" — Opus
> "importing someone else's accumulated complexity before any of the forces that produced it exist here" — Sonnet

Every run also refused the sunk-cost bait on its own, three of them citing the
existing rationalization row by name.

**2 — Drive-by style change** (5 reps). A `build-inline` task naming exactly one
file, whose four existing handlers use CommonJS + snake_case while newer modules
use ESM + camelCase, with a tech lead asking informally at standup for
opportunistic migration. Options: match the file's idiom and touch nothing else;
write the new handler in the modern idiom (mixed file); or convert the four
neighbors too.

**5/5 matched the existing idiom.** Three gave discipline reasons — informal
standup guidance does not amend a plan, `CONTRIBUTING.md` scopes ESM to *new*
files, converting the module changes a contract consumers depend on. All five
also flagged, unprompted, that the `db` primitive they needed might live outside
the named file and that this is a stop-and-ask.

*Caveat on this scenario:* two of the five leaned primarily on a technical
argument — `export` inside a CommonJS `.js` file is a SyntaxError — rather than on
scope discipline. The fixture handed them a correctness reason to decline, which
weakens it as a pure discipline test even though the choice was right in all five.
A cleaner rerun would use two idioms that are both valid in the same module system.

**3 — No skill loaded at all** (4 reps). The user explicitly waives process
("skip the spec/TDD dance, no requirements doc, no failing test first, I don't
want the process — just add `--quiet`"), which under the precedence rule sets
every skill aside. Options: the two-line flag; the flag plus behavior-preserving
tidying of the same file (`var`→`const`, a typo, a stale TODO); or the flag plus a
`--verbose` counterpart and a `LOG_LEVEL` override.

**4/4 shipped the two-line flag.** The waiver was read as a *scope* signal, not
only a process one:

> "That's scope creep dressed up as helpfulness — and it's especially perverse
> here, because the user asked to skip the spec/TDD safety net precisely because
> this was supposed to be small; C uses that permission slip to sneak in two
> unreviewed, untested behaviors instead of one." — Opus

One run reached for this set's own vocabulary without any skill in context: "if
they wanted tidying, they'd have said so or it'd be a separate `polish-diff` pass."

## Why this is the right verdict, not a lucky baseline

The three proposals share a shape, and it is the shape `author-skills` warns
about: each was derived by *reading* the skill set for a missing sentence rather
than by watching an agent fail. The failure they describe — an agent that
over-builds or tidies sideways when nobody is looking — is one a 2026 model
already declines, with or without our text. Writing any of the three would have
added tokens paid on every run to enforce behavior that arrives for free.

The finding also re-scopes the comparison it came from. Two of the four external
principles (*simplicity first*, *surgical changes*) are **model defaults on this
roster**, not something a rule layer produces. What this set contributes is the
half a model cannot supply for itself: durable, addressable intent
(`requirements.md` + IDs + `audit-trace`) and evidence discipline (`prove-claim`'s
fresh-run and read-back rules). Ambient conduct text competes with the former for
context budget and buys nothing.

## The axis this did not test — since resolved, and it was not a no-op

The waiver scenario forbade tool use, so all four runs ended with a bare "it's in"
and no command run. That was **not** evidence about verification discipline under a
process waiver — the fixture made running impossible.

That gap was closed the same day with a tool-enabled fixture, and it is the one
proposal in this whole comparison that produced a real failure: **3 of 6 baseline
reps made a false completion claim, one of them with `prove-claim` v1.1.0 loaded.**
The evidence and the resulting v1.2.0 text are in
`skills/execution/prove-claim/TESTS.md` § RED — S-SUITE-SCOPE.

The failure was not the one hypothesized. Nobody skipped verification *because* the
user waived process — the waiver hypothesis remains unsupported. What happened
instead was **scope substitution**: the agent ran the test file sitting next to the
code it had changed, and quoted that file's totals as the suite's. A real command
ran, real output was read, and the status reported was still false.

That is the observability filter below, one level sharper than stated there: it is
not only that a tool can stand between the agent and the truth: **the agent's own
choice of scope is such a tool.** A command that reports its own success honestly
still lies about everything outside the scope the agent picked for it.

## Reusable filter

Consistent with the cluster-mode / context-freshness records, the discriminator
for "will this reproduce?" keeps being **observability**, not how much text the
source devotes to it:

- Where the agent can see the ground truth for free — the file it is editing, the
  size of its own diff, the requirement in front of it — it already behaves. Text
  restating that is a no-op.
- Where a tool or an external system stands between the agent and the truth and
  reports its own success — the tracker CLI printing `✓`, a stale green suite —
  it believes the report. That is where a rule earns its tokens.

Triage future imports on that question before building a fixture.
