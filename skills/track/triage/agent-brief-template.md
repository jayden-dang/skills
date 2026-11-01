# Agent briefs

An agent brief is the comment posted on an issue when it moves to `ready-for-agent`. It is the specification a future agent will implement from, possibly weeks later, with no access to today's conversation. The brief is the contract; the issue body and thread are background.

For a PR, the brief describes what remains to be done **to the existing diff** — finish it, close its gaps, address review points — rather than building from nothing. Same fields, same rules.

## Rules

**The issue's own sections.** The brief uses the sections of the issue's kind from `docs/agents/issue-tracker.md` **Issue format**, so a reader sees one shape everywhere.

**Behavior a person or client can observe.** The codebase changes while the issue waits, so the brief carries no type, function, file path or line number. The implementing agent explores the code fresh and makes its own structural choices.

**Every acceptance item checkable on its own**, with a concrete command, test, or observation. "Works correctly" is not an item. Where specs are shared and a spec covers the behavior, cite the requirement IDs in the item it covers, and add an item for each guard the change must not break.

**Out of scope is explicit.** That list is what stops an agent from gold-plating or wandering into adjacent features.

## Calibration example

A report says CSV export writes `NaN` for missing numeric cells.

Weak brief: "Export is broken for empty cells — see the export handler around line 200 in src/export/csv.ts and fix it." Everything wrong at once: no category, a file path and line number that will rot, no definition of correct output, nothing checkable.

Strong brief (abridged): What happens "numeric columns write the text `NaN` for missing values"; Expected "a missing value writes an empty field, regardless of column type"; How to reproduce "export a row with a missing numeric cell"; Acceptance "that row writes `a,,c`" and "populated cells write the same bytes as before"; Out of scope "changing the delimiter or quoting rules".
