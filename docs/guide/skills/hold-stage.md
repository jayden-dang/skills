# `hold-stage`

> The stage holds what this act uses. Everything else stays on the page.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable |
| **Reads** | the file under the act; `requirements.md` as a warehouse |
| **Writes** | the outgoing review or edit, citing only the IDs this act uses |
| **Calls** | none |
| **Called by** | description trigger when a working set is larger than the act |

## When it fires

When more is live than this act can use — a twelve-ID working set, a
review that walks every requirement, a change that "must stay
consistent" with the whole spec. It does **not** replace
[`inspect-change`](inspect-change.md) (two-axis verdict) or
[`load-subgraph`](load-subgraph.md) (neighbors). It caps what rides
along in the outgoing text.

## The Iron Law

```
ONLY THE IDEAS THIS ACT USES
```

Cite IDs this file implements or violates. Usually one or two. A third
that this file fails still belongs on the stage. Persist / PDF / void
do not.

## Why it is written the way it is

Baseline reviews of a 5-line `tax.js` tabled all twelve BILL IDs
because `WORKING_SET.md` said to keep them live. A first wording
("at most two ideas") stopped the recap and also dropped BILL-1.10,
the actual blocker. The iron law is therefore about recap, not about
discarding findings.

## See also

- [`inspect-change`](inspect-change.md) — the two-axis review this stage feeds
- [`speak-outer`](speak-outer.md) — register, not capacity
- [`load-subgraph`](load-subgraph.md) — neighbors stay on disk until admitted
