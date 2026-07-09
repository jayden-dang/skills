# Glossary

Domain terms for this repo. Keep definitions tight; challenge fuzzy usage.

- **Surface** — the set of source files a feature owns or touches, derived from its
  `design.md` and `tasks.md`.
- **Surface manifest** — one feature's Surface, split into `owns` and `touches`.
- **Reverse index** — the inverse mapping: a source path → the features that reference it.
- **Shared surface** — a path referenced by two or more features; the duplication signal.
- **Summary card** — a bounded per-feature digest (code, name, owned paths, interfaces,
  out-of-scope) used to load a neighbor's essence without its full spec.
