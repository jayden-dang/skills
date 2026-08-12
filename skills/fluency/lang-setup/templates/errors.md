---
type: error-log
updated: {{date}}
open: 0
---

# Error log

One row per **pattern**, never per instance. An unnamed error cannot be scheduled, counted,
or retired.

## Status

A row's status is decided by evidence, not by how long it has been quiet.

| status | means |
| ------ | ----- |
| `open` | Recurring. In the correction set and in the due queue |
| `watch` | No occurrence for one cycle **and the structure was actually used**. Still checked |
| `resolved` | No occurrence for two cycles, and the linked capability sits at R2 or better |
| `regressed` | Was `watch` or `resolved`, then reappeared. Reopened with the date |

**Quiet is not the same as fixed.** A row with no occurrences where the structure never
appeared at all is avoidance, not progress: it stays `open` and goes to the next cycle's
avoidance set. `lang-review-practice-week` makes that call every week.

`open` rows stay within `config.limits.errors_live`. `resolved` rows leave the due queue and
move to Resolved — searchable, not scheduled.

## Live

| id | pattern | capability | count | first_seen | last_seen | next_due | status |
| ---- | ------- | ---------- | ----- | ---------- | --------- | -------- | ------ |
| E-01 | | | 0 | | | | open |

## Resolved

| id | pattern | capability | resolved | evidence |
| -- | ------- | ---------- | -------- | -------- |
