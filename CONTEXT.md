# Glossary

Domain terms for this repo. Keep definitions tight; challenge fuzzy usage.

- **Surface** — the set of source files a feature owns or touches, derived from its
  `design.md` and `tasks.md`.
- **Surface manifest** — one feature's Surface, split into `owns` and `touches`.
- **Reverse index** — the inverse mapping: a source path → the features that reference it.
- **Shared surface** — a path referenced by two or more features; the duplication signal.
- **Summary card** — a bounded per-feature digest (code, name, owned paths, interfaces,
  out-of-scope) used to load a neighbor's essence without its full spec.
- **Covered** — a requirement is *covered* when at least one test citing its ID **ran and
  passed**, as attested by a test runner's report. A skipped, failing, or commented-out test
  is not coverage; neither is an ID that merely appears in a source file.
  _Avoid:_ "has a test" (a string in a file is not a test), "tagged" (tagging is the
  mechanism, coverage is the outcome).
- **Citation** — an occurrence of a requirement ID that a test runner attests to: one that
  reaches a report as part of a test's name. A task's `_Requirements:_` footer is also a
  citation. _Avoid:_ "reference", "mention" — both include strings no runner ever saw.
- **Fixture ID** — an ID-shaped string in source (example data, a doc comment, a
  commented-out test) that no test ever asserts. A Fixture ID is not a Citation; conflating
  the two is what made a commented-out test read as coverage.
