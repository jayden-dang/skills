# Export (change-impact only)

## Contents

- [Trigger](#trigger)
- [Formats](#formats)
- [Share view](#share-view)
- [Privacy denylist](#privacy-denylist)

## Trigger

Always write the local ledger. Portable export runs **only when requested**.

`--export` defaults to **Markdown**. Self-contained **HTML** only with
`--export html`. Export is an **output option**, not a fifth mode.

Ledger and export render from the **same evidence package** — no second SSOT.

## Formats

Markdown and HTML share the same semantic fields. HTML is an **immutable**
offline snapshot.

## Share view (allowed)

- Range + provenance
- Old → new behavior
- CODEs / OBS touched
- Ordered stops
- Verified claims + evidence
- Open impacts (non-private)

## Privacy denylist (never default-export)

Raw learner claims · `contradicted` detail · personal notes · handoff history ·
quiz · score · “passed”
