# Glossary

Domain terms for this repo. Keep definitions tight; challenge fuzzy usage.

- **Feature overlap** — a new idea or a diff touching source paths, or key concepts,
  that an existing feature already owns; the duplication signal `brainstorm` and
  `code-review` look for by searching `docs/specs/`. _Avoid:_ "conflict" (overlap is
  a signal to investigate, not a failure).
- **Summary card** — a bounded per-feature digest (code, name, owned paths,
  interfaces, out-of-scope) used to load a neighbor's essence without its full spec.
- **Covered** — a requirement is *covered* when its ID string appears in a test
  file (per the configured test globs). Coverage is textual presence, by design: the
  `trace` check greps for the ID and does not judge whether the test meaningfully
  asserts it — that judgment would make the result depend on the reader. A file
  whose IDs are fixtures, not coverage, is excluded via the trace ignore list, not
  case by case. _Avoid:_ "has a test" as if it meant more than the string being
  present; "ran and passed" — the trace check does not read test reports.
- **Citation** — an occurrence of an ID that the `trace` check counts: a requirement
  ID on a task's `_Requirements:_` footer, a requirement ID string in a test file, or
  an **invariant** ID on a `design.md`'s `Respects: ARCH-N` line. _Avoid:_
  "reference"/"mention" as vaguer synonyms — a citation is exactly what the grep passes
  collect.
- **Invariant** — a cross-cutting architecture rule that keeps independently-built
  features consistent, written as a bold `**ARCH-N**` ID plus one imperative sentence in
  the `docs/architecture/` spine. A feature's `design.md` cites the ones it relies on as
  `Respects: ARCH-N`; the `trace` check verifies that citation points at a *live* (not
  struck-through) invariant. Part of the optional project-documentation layer. _Avoid:_
  "constraint" as a synonym (a Global-Constraint is a per-plan rule, not a repo-wide
  invariant); conflating the deterministic `trace` citation check with the advisory
  semantic `check-invariants` verdict.
- **Fixture ID** — an ID-shaped string that is not real coverage (example data, a
  doc comment, a commented-out test). The `trace` check cannot tell a fixture from
  coverage by reading it, so a file full of fixture IDs is named in the trace ignore
  list and dropped from the test search wholesale.
- **Reuse ladder** — the seven-rung reuse-before-build check `write-design` climbs in Step 2
  (fed by the Step-1 scan digest) before committing to any component: (1) need it at all
  (YAGNI) (2) already in this codebase (3) stdlib/language builtin (4) platform/framework/
  runtime feature (5) already-installed dependency (6) one line (7) only then new code. Stop
  at the highest rung that holds; the chosen rung + concrete target is recorded on a `Reuse:`
  line that flows into the implementing task. _Avoid:_ conflating it with the deletion test
  (the ladder decides *whether* to build; the deletion test keeps rung-7 *new* code's
  interface deep) or with feature-level `[[feature-overlap]]` (the ladder is component/library
  granularity, overlap is whole-feature).
- **Reuse-miss** — a place where work reimplements something that already exists rather than
  reusing it. `code-review` emits it at the *feature* level (a diff rebuilds what a neighbour
  spec owns); `write-plan`'s Step-4 self-check emits it at the *component* level (a task
  Creates what the scan digest or an installed dependency already provides). Same term, two
  granularities. _Avoid:_ treating a deliberate rung-7 new-code decision (justified on its
  `Reuse:` line) as a reuse-miss — a miss is unjustified duplication, not a considered build.
- **Lowest invalidated artifact** — the classification law of `correct-course`: when a
  mid-execution discovery falsifies an approved plan, the divergence is routed to the
  *lowest* level in the chain that is genuinely invalidated (task / plan / design /
  requirements / vision), with cited evidence — never higher. It is the rule that keeps a
  rewind from over-correcting: a task-local discovery goes back to execution, not to
  re-design. "Blast radius" is the informal umbrella for the same idea (note: `file-issues`
  already uses "blast radius" in an unrelated refactor-sizing sense). _Avoid:_ rewinding to
  the highest plausibly-affected artifact "to be safe" — the law is lowest-with-evidence.
- **Definition** — a requirement ID written in bold (`**CODE-N.M**`) in a
  `requirements.md`/`fixes.md`, and not struck through. A struck-through ID
  (`~~**CODE-N.M**~~`) is *retired* — it stops counting as defined. A plain,
  non-bold ID in prose is not a definition.
