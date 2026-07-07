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

### <Component / area 1>

Satisfies: <CODE>-1.1, <CODE>-1.2

<What it is, where it lives, how data flows through it. Diagrams welcome.>

### <Component / area 2>

Satisfies: <CODE>-2.1

...

## Seams for testing

<The public boundaries tests will be written at, agreed here — the tdd skill
refuses tests at unconfirmed seams. Prefer existing seams; the ideal number of
new seams is zero or one.>

| Seam | Kind | Covers |
|---|---|---|
| <module/interface> | unit / integration / e2e | <CODE>-1.x |

## Coverage check

<Every requirement ID from requirements.md appears in exactly one Satisfies:
line above. List any deliberately unmapped IDs and why.>
