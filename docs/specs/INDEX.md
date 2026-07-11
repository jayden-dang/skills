# Spec Index

Feature-code registry: every requirements.md registers its code here before use.
Codes are 2-12 chars, A-Z0-9, start with a letter, unique forever (never reuse a
retired code).

| Code | Feature | Spec | Status |
|---|---|---|---|
| FGRAPH | Horizontal feature-graph layer (surface manifest, reverse index, summary cards) | ./2026-07-09-feature-graph/ (requirements + design + tasks) | Implemented |
| TRACE | check-trace `ignore` capability — exclude fixture-bearing test files from the trace scan | ./2026-07-09-check-trace-ignore/ | Approved |
| PYPORT | Port the spec linters from Node `.mjs` to Python 3.9 stdlib, behavior-identical (see docs/adr/0001) | ./2026-07-10-python-linters/ (requirements + design + tasks) | Approved |
