# `improve-architecture`

> A codebase-wide periodic scan for design friction — not a single diff or PR. The goal is testability and navigability: modules deep enough that their interface is the test surface.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | **user-invoked only** — run `/improve-architecture`. `disable-model-invocation: true`: no skill may auto-invoke it; other skills only name it for the user to run |
| **Reads** | `CONTEXT.md` (the domain names good seams), `docs/adr/` (decisions not to re-litigate), the codebase (via an explore subagent) |
| **Writes** | a self-contained HTML report in the OS temp directory (never the repo); no code changes of its own |
| **Calls** | an explore subagent, [`design-page`](design-page.md) (required, before the report's markup), [`grilling`](grilling.md), [`domain-modeling`](domain-modeling.md), then [`tdd`](tdd.md)/[`verify`](verify.md) (tier 0) or [`brainstorm`](brainstorm.md) (tier 1+) |
| **Called by** | nobody — the user runs it directly |

## When it fires

When the user asks for an architecture review, a codebase-health or technical-debt scan, wants to know where to refactor next, or asks for a periodic look at accumulated design friction across the whole codebase. It is a **codebase-wide scan, not a single diff or PR**, and because it is `disable-model-invocation: true`, no other skill triggers it — a skill may name `/improve-architecture`, but the user starts it.

## Vocabulary is strict throughout

The skill uses exactly five nouns, plus three qualities:

| Term | Meaning |
|---|---|
| **module** | a unit of code with an interface and an implementation |
| **interface** | the surface callers go through |
| **implementation** | what the module hides behind that surface |
| **seam** | a public boundary where behavior is both observable and substitutable — the same seam [`tdd`](tdd.md) and [`write-design`](write-design.md) name |
| **adapter** | a concrete substitution plugged in behind a seam |
| *depth / locality / leverage* | the qualities a good module has — deep, changes localized, small interface controlling much |

The skill never drifts into "component", "service", "layer", or "boundary": precision in the nouns is what keeps findings comparable run over run.

## 1. Explore for friction

Read `CONTEXT.md` and `docs/adr/` first. Then dispatch an explore subagent to walk the codebase **organically — no rigid checklist**, just noting where work hurts. Four friction kinds:

- **Shallow modules** — an interface nearly as complex as the implementation behind it.
- **Poor locality** — one conceptual change fans out across many files.
- **Missing or weak seams** — places substitution is needed but impossible, or a seam that exists with only **one hypothetical adapter**.
- **Untested-through-interface** — code only testable by reaching past its interface into internals.

The four kinds share a root — a module that fails to hold complexity behind its interface — so a single candidate often shows more than one. Apply the **deletion test** to anything suspect: *if this module vanished, how much would its callers need to know to rebuild the behavior?* "Almost everything" means the module was shallow — deleting it would **concentrate** complexity rather than lose it, and that concentration point is your candidate. The opposite answer, "almost nothing", means the module was already doing real work and hiding it well.

**Done when** you hold 3–7 candidates, each tied to specific modules and a named kind of friction.

## 2. Present the report

The **required sub-skill** is [`design-page`](design-page.md), loaded before any markup. The treatment is utilitarian — a real type scale, a chosen palette, no hero — and the report is scanned rather than read top-to-bottom, so its UI-not-a-document guidance is the part that bites: the confidence badge and the before/after sketch have to read at a glance.

Write a **self-contained HTML file** — inline CSS/SVG only, no external scripts, stylesheets, or CDNs — to the OS temp directory (`$TMPDIR`, falling back to `/tmp`; `%TEMP%` on Windows) as `architecture-review-<timestamp>.html`, so **nothing lands in the repo**. Open it and tell the user the absolute path.

One card per candidate:

| Card field | What it holds |
|---|---|
| **Files** | the modules involved (monospaced list; the report is ephemeral, so paths are fine here) |
| **Problem** | one sentence: what hurts and which friction kind it is |
| **Proposed direction** | one sentence, in the strict vocabulary: what would deepen |
| **Win** | bullets of at most 6 words each, named as qualities ("locality: change lands in one module") |
| **Confidence badge** | exactly one of `Strong` / `Worth exploring` / `Speculative` |
| **Before/after structure sketch** | side-by-side hand-built divs/SVG — shallow-vs-deep mass, fan-out collapses, seam lines |

The sketch carries the argument; if it needs a paragraph to explain, redraw it. The confidence badge is doing real work — it tells the user how much to trust the direction before investing grilling time in it. End with a top-recommendation section: which candidate first, one sentence why.

**Do not propose concrete interfaces yet** — the report names *directions*, not designs. Interface shape belongs to the grilling step, with the user in the loop. **ADR conflicts** are included only when the friction is severe enough to justify reopening the decision, marked with the ADR reference and why it deserves revisiting — not every refactor an ADR forbids.

**Done when** the report is open in the user's browser and you have asked which candidate to pursue.

## 3. Shape the chosen candidate

Once the user picks:

- Use [`grilling`](grilling.md) — walk the shape of the deepened module one question at a time: constraints, what sits behind the new seam, which adapters are real, which tests survive.
- Use [`domain-modeling`](domain-modeling.md) for side effects as decisions land:
  - A new module named after a concept missing from `CONTEXT.md` gets the term added.
  - A term sharpened mid-conversation gets updated now, not later.
  - A candidate the user rejects for a load-bearing reason earns a 1–3 sentence ADR, so future scans do not re-suggest it (skip ephemeral or self-evident reasons).

**Done when** the improvement has a confirmed shape and its ceremony tier is decided.

## 4. Feed the spec cycle

The chosen improvement now enters the same cycle as any other change, split by ceremony tier:

- **Tier 0** (mechanical, no behavior change) proceeds directly under [`tdd`](tdd.md) / [`verify`](verify.md) discipline.
- **Tier 1 or above** goes to [`brainstorm`](brainstorm.md), handed the shaped improvement to run the normal cycle to requirements.

**Architecture work earns no exemption from the spec gate** — a deepening that changes behavior is a spec'd change like any other.

**Done when** the work has an owner flow — in progress under tier 0 discipline, or handed to [`brainstorm`](brainstorm.md).

## Worked example

The user runs `/improve-architecture` on a mid-size app.

**Explore.** After reading `CONTEXT.md` and `docs/adr/`, the explore subagent reports that `NotificationDispatcher` is a thin pass-through: its interface exposes `send(channel, payload)` but callers must already know each channel's payload shape, retry policy, and formatting — the module hides almost nothing. Applying the **deletion test**: if it vanished, callers would need to know *almost everything* to rebuild sending, which means the module is shallow and merely concentrates knowledge without owning it. That is a candidate. The scan surfaces four others, landing at five total.

**Report.** A `architecture-review-1720579200.html` is written to `$TMPDIR` and opened. The dispatcher's card: Problem — "shallow module: interface as complex as the send logic it fronts"; Proposed direction — "deepen `NotificationDispatcher` so channels become adapters behind one seam"; Win — "interface shrinks", "tests hit one seam", "new channel = one adapter"; Confidence — `Strong`; and a before/after sketch showing five callers each wiring channel details collapse into one deep module with three adapters behind a seam line. No concrete interface is proposed. The top-recommendation section names the dispatcher first.

**Shape.** The user picks it. [`grilling`](grilling.md) draws out which channels are real adapters (email, SMS, in-app) versus hypothetical, and which existing tests survive the reshape. Because "channel adapter" is a concept not yet in `CONTEXT.md`, [`domain-modeling`](domain-modeling.md) adds the term.

**Feed.** The reshape changes behavior at the seam, so it is tier 1 — it goes to [`brainstorm`](brainstorm.md) for the full cycle rather than proceeding under bare `tdd`.

## Why it is written the way it is

The strict vocabulary is the load-bearing constraint: a review's findings are only worth anything if this run's "shallow module" means the same thing as last quarter's, and the moment the language softens into "components" and "layers" the findings stop being comparable and the periodic scan loses its point. The deletion test exists because shallowness is counterintuitive — a module can look like it is doing work while actually just relaying it — and the test makes that visible by asking what callers would have to relearn. The report is HTML in temp, not markdown in the repo, because a scan is a proposal, not a decision, and nothing should be committed until the user has chosen and the spec cycle has run. That is also why interfaces are deliberately withheld until grilling and why tier 1+ work is pushed to `brainstorm`: naming a direction is cheap and reversible, but designing the interface is a real decision that belongs with the user behind the spec gate.

## See also

- [`grilling`](grilling.md) — shapes the chosen candidate's interface one question at a time
- [`domain-modeling`](domain-modeling.md) — records new terms and rejection ADRs as the shape lands
- [`brainstorm`](brainstorm.md) — where any tier 1+ improvement enters the spec cycle
- [`tdd`](tdd.md) — the seam-based test surface this skill is trying to make possible
- [`write-design`](write-design.md) — names the same seams, from the greenfield side
