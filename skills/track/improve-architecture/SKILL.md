---
name: improve-architecture
description: Use when the user asks for an architecture review, a codebase-health scan, "where should we refactor next", or a periodic look at accumulated design friction.
disable-model-invocation: true
---

# Improve the Architecture

Scan the codebase for accumulated friction, present deepening candidates as a visual report, and carry the one the user picks into the normal spec cycle. The goal is testability and navigability — modules deep enough that their interface is the test surface.

Vocabulary is strict throughout: **module, interface, implementation, seam, adapter** (plus depth/locality/leverage as qualities). Never drift into "component", "service", "layer", or "boundary" — precision in the nouns is what keeps the findings comparable run over run.

## 1. Explore for friction

Read `CONTEXT.md` (the domain names good seams) and `docs/adr/` (decisions not to re-litigate) first. Then dispatch an explore subagent to walk the codebase organically — no rigid checklist, just note where work hurts:

- **Shallow modules** — an interface nearly as complex as the implementation behind it
- **Poor locality** — one conceptual change fans out across many files
- **Missing or weak seams** — places substitution is needed but impossible, or a seam exists with only one hypothetical adapter
- **Untested-through-interface** — code only testable by reaching past its interface into internals

Apply the **deletion test** to anything suspect: if this module vanished, how much would its callers need to know to rebuild the behavior? "Almost everything" means the module was shallow — deleting it would concentrate complexity rather than lose it. That concentration point is your candidate.

**Done when:** you hold 3–7 candidates, each tied to specific modules and a named kind of friction.

## 2. Present the report

Write a **self-contained HTML file** (inline CSS/SVG only — no external scripts, stylesheets, or CDNs) to the OS temp directory (`$TMPDIR`, falling back to `/tmp`; `%TEMP%` on Windows) as `architecture-review-<timestamp>.html`, so nothing lands in the repo. Open it (`open` / `xdg-open` / `start`) and tell the user the absolute path.

One card per candidate:

- **Files** — the modules involved (monospaced list; this report is ephemeral, so paths are fine here)
- **Problem** — one sentence: what hurts and which friction kind it is
- **Proposed direction** — one sentence, in the strict vocabulary: what would deepen
- **Win** — bullets of at most 6 words each, named as qualities ("locality: change lands in one module", "interface shrinks, tests hit one seam")
- **Confidence badge** — exactly one of `Strong` / `Worth exploring` / `Speculative`
- **Before/after structure sketch** — side-by-side drawings (hand-built divs/SVG): shallow-vs-deep mass diagrams, fan-out collapses, seam lines. The sketch carries the argument; if it needs a paragraph to explain, redraw it.

End with a top-recommendation section: which candidate first, one sentence why.

**Do not propose concrete interfaces yet** — the report names directions, not designs. Interface shape belongs to the grilling step, with the user in the loop.

**ADR conflicts:** if a candidate contradicts an existing ADR, include it only when the friction is severe enough to justify reopening the decision, and mark the card with the ADR reference and why it deserves revisiting. Do not list every refactor an ADR forbids.

**Done when:** the report is open in the user's browser and you have asked which candidate to pursue.

## 3. Shape the chosen candidate

Once the user picks:

- REQUIRED SUB-SKILL: use `grilling` — walk the shape of the deepened module one question at a time: constraints, what sits behind the new seam, which adapters are real, which tests survive.
- REQUIRED SUB-SKILL: use `domain-modeling` for side effects as decisions land — new module named after a concept missing from `CONTEXT.md`? Add the term. Fuzzy term sharpened mid-conversation? Update it now, not later. User rejects a candidate for a load-bearing reason? Offer a 1–3 sentence ADR so future scans do not re-suggest it (skip ephemeral or self-evident reasons).

**Done when:** the improvement has a confirmed shape and its ceremony tier is decided.

## 4. Feed the spec cycle

Tier 0 (mechanical, no behavior change) can proceed directly under `tdd`/`verify` discipline. Anything tier 1 or above: hand the shaped improvement to `brainstorm` and let it run the normal cycle to requirements — architecture work earns no exemption from the spec gate.

**Done when:** the work has an owner flow — either in progress under tier 0 discipline, or handed to `brainstorm`.
