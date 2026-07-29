# Write package — layout, fields, stable ID, digest

Load this file when phase 6 (`Write package`) runs. SKILL.md owns the phase
list and the Iron Law; this file owns the package layout, the `manifest.md`
field list, the stable-ID derivation, and the digest recipe.

## Layout

Write exactly two files, and only after the git-ignored precondition below
is proven:

```
.skills/pr-packages/<stable-id>/manifest.md
.skills/pr-packages/<stable-id>/body.md
```

`manifest.md` carries every field the field list below names. `body.md`
holds reviewer-facing pull-request content only — no manifest field, no
internal grading, no path or note a reviewer should not see verbatim inside
the PR description.

## Stable ID: sanitized and head-derived, never the raw branch name

Derive `<stable-id>` from the head branch: sanitize it into a filesystem-
and-path-safe token — lowercase, `/` and other separators replaced, no
leading `-`, bounded length. Never place a raw branch name in the package
path — the sanitized token is the only value that reaches
`.skills/pr-packages/<stable-id>/`; a branch such as
`feature/PROJ-34: fix a case` becomes a plain, reproducible token, not a
literal copy of the branch string. Derive `<stable-id>` once per session and
reuse it for every write this invocation makes — never re-derive mid-session
and split one package across two directories.

## Precondition: `.skills/` must already be proven git-ignored

<HARD-GATE>
Prove `.skills/` is git-ignored before writing any package file: check that
`.gitignore` contains a line matching `.skills/` or `.skills` — a plain
line-presence check, never an inference and never a check run after a file
is already written. IF `.skills/` is not proven git-ignored THEN write no
package file at all and report that the package was not written — do not
fall back to writing it anywhere else and do not retry silently.
</HARD-GATE>

## manifest.md field list

Record every one of these fields in `manifest.md`; omit none:

- `Package version:` — the package-contract schema version this manifest
  was written against, so a later contract change can tell old packages
  apart from new ones.
- `Title:` — the exact PR title this session resolved, byte-for-byte the
  title that reaches the reviewer and the title fed into the digest below.
- `Base:` — the resolved base ref and its resolved commit SHA, carried
  forward unchanged from phase 1's `Base:` value — never recomputed here.
- `Head:` — the head ref and its resolved commit SHA at authoring time.
- `Ticket linkage:` — for every item in the resolved ticket set: its `id`,
  `title`, `classification`, and `linkage_syntax` (tickets.md's exact
  shape), copied through unchanged.
- `Commits:` — the created-commit list `[{ sha, subject, trailers }]`
  actually present on the branch, exactly as phase 5 produced it.
- `Advisory commit map:` — the advisory regrouping map, when one was
  proposed, in the shape the advisory-map rules define.
- `Convention findings:` — every finding raised against the resolved
  convention record, each carrying the `grade` phase 2 assigned it.
- `Validation results:` — the outcome of the six-axis validation run
  against every commit this session created.
- `Content-digest:` — the digest computed below.

## body.md holds reviewer-facing content only

`body.md` is the PR description exactly as a reviewer reads it: the
narrative phase 3 produced, ticket references placed per tickets.md, and
nothing else — no manifest field, no internal grading, no path under
`.skills/`. Never duplicate a manifest-only field into `body.md`, and never
let `body.md` prose substitute for a `manifest.md` field.

## `Content-digest:` — computed with `git hash-object`, never a shipped script

Compute `Content-digest:` with `git hash-object --stdin`, the plumbing
command already required elsewhere in this skill set, chosen because its
output is platform-uniform — unlike `shasum` or `sha256sum`, whose output
format varies across platforms — and because it introduces no new tooling
this repository, or an adopting repository, would have to install. Feed it
the exact bytes of the title, a single newline, and then the full contents
of `body.md`, in that order and with no other bytes — the same recipe
`finish-branch` re-runs immediately before submission to detect any edit
made since approval:

```
{ printf '%s\n' "<title>"; cat body.md; } | git hash-object --stdin
```

## Package files never enter a commit plan or a reviewer-facing locator

<HARD-GATE>
A package file — `manifest.md`, `body.md`, or the `<stable-id>` directory
itself — never enters a commit plan: phase 5's grouping and validation never
proposes, stages, or commits anything under `.skills/pr-packages/`. A
package path is never shown as a reviewer-facing locator: never cite
`.skills/pr-packages/<stable-id>/...` in a PR body, a commit message, or any
text a reviewer reads — `.skills/` is git-ignored and unreachable from the
PR revision, so a path into it tells a reviewer nothing they can open.
</HARD-GATE>
