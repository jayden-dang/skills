# Design: <Feature Name>

Feature code: <CODE>
Status: Draft
Date: <YYYY-MM-DD>
Requirements: ./requirements.md

## Context

<Why this feature, what exists today, what constraint shapes the approach.
2-4 paragraphs maximum.>

## Decisions

<Numbered list of decisions locked during discovery, each 1-2 sentences.
Anything hard-to-reverse AND surprising AND a real trade-off also gets an ADR.>

## Architecture

Vocabulary for every section below: **module**, **interface**, **implementation**,
**seam** (public surface where behavior is observable and substitutable). Prefer
deep modules — an interface much simpler than what it hides.

### <Module / area 1>

Satisfies: <CODE>-1.1, <CODE>-1.2
Reuse: <rung> — <concrete target, or none — new code (rung 7) with reason>
Respects: <ARCH-N if the design relies on a spine invariant; else omit this line>
Interface: <what callers know — names, inputs, outputs; keep this smaller than the implementation>
Depth: <deletion test for new modules (Reuse rung 7): if this module vanished, what must callers still know to rebuild the behavior? Answer in one sentence. If that answer is "nearly everything it did", redesign before continuing.>
Locality: <where a change for these Satisfies IDs lands; neighbor impact on existing modules: leave | extend | extract — one line>

<What it is, where it lives, how data flows through it. Diagrams welcome.>

### <Module / area 2>

Satisfies: <CODE>-2.1
Reuse: …
Interface: …
Depth: <required when Reuse is rung 7; for reuse of an existing module, write `n/a — extends <target>`>
Locality: …

...

## Seams for testing

<The public boundaries tests will be written at, agreed here — the test-first skill
refuses tests at unconfirmed seams. Prefer existing seams; the ideal number of
new seams is zero or one.>

| Seam | Kind | Covers |
|---|---|---|
| <module/interface> | unit / integration / e2e | <CODE>-1.x |

## Coverage check

<Every requirement ID from requirements.md appears in exactly one Satisfies:
line above. List any deliberately unmapped IDs and why.>
