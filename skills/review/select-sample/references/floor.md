# Floor — exactly one, when nothing bound

Loaded from `SKILL.md`'s **Floor** section, and only when SAMPLE would
otherwise be empty.

Runs only when SAMPLE would otherwise be empty. Total order, first key that discriminates wins:

| Rank key | Direction |
|---|---|
| 1. changed lines (added + deleted) | descending |
| 2. files changed | descending |
| 3. unit key | ascending, byte order |

Admit the top unit. Key 3 makes the order total, so a non-empty range always yields a pick — **never present an empty sample set** for a non-empty range.
