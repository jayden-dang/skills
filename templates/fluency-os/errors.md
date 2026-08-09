---
type: error-log
updated: {{date}}
live: 0
---

# Error log

One row per **pattern**, never per instance. An unnamed error cannot be scheduled, counted,
or retired.

Live rows stay within `config.limits.errors_live`. A row retires after its capability reaches
R3 with two clean weeks, and moves to Archive — searchable, out of the due queue.

A row that goes quiet is not automatically fixed. `review-practice-week` checks whether the
structure was used at all; quiet with no use is avoidance, not progress.

## Live

| id | pattern | capability | count | first_seen | last_seen | next_due | status |
| ---- | ------- | ---------- | ----- | ---------- | --------- | -------- | ------ |
| E-01 | | | 0 | | | | live |

## Archive

| id | pattern | capability | retired | evidence |
| -- | ------- | ---------- | ------- | -------- |
