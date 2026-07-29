# Write package — layout, fields, stable ID, digest

Load this file when phase 6 (`Write package`) runs. SKILL.md owns the phase
list and the Iron Law; this file owns the package layout, the `manifest.md`
field list, the stable-ID derivation, and the digest recipe.

## Contents

- [Layout](#layout)
- [Stable ID](#stable-id-sanitized-and-head-derived-never-the-raw-branch-name)
- [Precondition: `.skills/` git-ignored](#precondition-skills-must-already-be-proven-git-ignored)
- [manifest.md field list](#manifestmd-field-list)
- [title.txt](#titletxt-holds-the-exact-approved-title)
- [body.md](#bodymd-holds-reviewer-facing-content-only)
- [Content-digest](#content-digest--computed-with-git-hash-object-never-a-shipped-script)
- [Package files never enter a commit plan](#package-files-never-enter-a-commit-plan-or-a-reviewer-facing-locator)

## Layout

Write exactly three files, and only after the git-ignored precondition below
is proven:

```
.skills/pr-packages/<stable-id>/manifest.md
.skills/pr-packages/<stable-id>/title.txt
.skills/pr-packages/<stable-id>/body.md
```

`manifest.md` carries every field the field list below names, including a
`Title:` field holding the same text as `title.txt`. `title.txt` carries
the approved title alone, byte-exact, so the digest recipe and the
submission command can read it from disk instead of interpolating title
text into a shell command (see "`title.txt` holds the exact approved
title" below). `body.md` holds reviewer-facing pull-request content only —
no manifest field, no internal grading, no path or note a reviewer should
not see verbatim inside the PR description.

## Stable ID: sanitized and head-derived, never the raw branch name

Derive `<stable-id>` from the head branch with this exact rule, so
`finish-branch` (and any later re-read) can rederive the identical token from
the identical branch name:

1. Lowercase the branch name.
2. Replace every character that is not `a`-`z`, `0`-`9`, or `-` with `-`
   (this covers `/`, `:`, spaces, and every other separator or shell
   metacharacter — nothing outside `[a-z0-9-]` survives).
3. Collapse runs of two or more consecutive `-` into a single `-`.
4. Strip any leading or trailing `-`.
5. Truncate to 100 characters, the bound on `<stable-id>`.

Never place a raw branch name in the package path — the sanitized token is
the only value that reaches `.skills/pr-packages/<stable-id>/`; a branch
such as `feature/PROJ-34: fix a case` becomes `feature-proj-34-fix-a-case`,
a plain, reproducible token, not a literal copy of the branch string. Derive
`<stable-id>` once per session and reuse it for every write this invocation
makes — never re-derive mid-session and split one package across two
directories.

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
  apart from new ones. The current schema version, and the value to write
  here, is `1`.
- `Title:` — the exact PR title this session resolved, byte-for-byte the
  title that reaches the reviewer and the title fed into the digest below.
  Written identically to `title.txt` — the two never drift because both are
  written from the one approved title, once.
- `Base:` — the resolved base ref and its resolved commit SHA, carried
  forward unchanged from phase 1's `Base:` value — never recomputed here.
- `Head:` — the head ref and its resolved commit SHA at authoring time.
- `Ticket linkage:` — for every item in the resolved ticket set: its `id`,
  `title`, `classification`, and `linkage_syntax` (tickets.md's exact
  shape), copied through unchanged.
- `Commits:` — the created-commit list `[{ sha, subject, trailers }]`
  actually present on the branch, exactly as phase 5 produced it.
- `Advisory commit map:` — the advisory regrouping map, when one was
  proposed, in the shape SKILL.md's advisory-map rules define: for every
  proposed group, its **groups**, **order**, **subjects**, **bodies**,
  **rationale**, and the **trailers** to preserve. Never a runnable
  `reset`/`rebase`/`force-push` command. When no regrouping would improve the
  branch, record that nothing was proposed.
- `Convention findings:` — every finding raised this session, each with its
  **finding** grade from SKILL.md's findings-grading rules (`advisory` |
  `reported` | `not run` | `verify-routed`). Convention-source grades live in
  `conventions.md` only — do not restate or substitute them here.
- `Validation results:` — the outcome of the six-axis validation run
  against every commit this session created.
- `Content-digest:` — the digest computed below.

## `title.txt` holds the exact approved title

`title.txt` carries nothing but the approved title bytes followed by
exactly one trailing newline — no manifest field, no quoting, no other
line. It exists so the digest recipe and the `gh pr create` invocation
below can read the title from disk rather than interpolating title text
directly into a shell command: titles are authored from diff and commit
text, which this skill classifies as passive data, and a `"`, backtick, or
`$(…)` inside an interpolated title can break shell quoting or run as a
command. `body.md` already avoids this class of problem by being read from
disk instead of inlined; `title.txt` gives the title the same treatment.

## body.md holds reviewer-facing content only

`body.md` is the PR description exactly as a reviewer reads it: the
narrative phase 3 produced, ticket references placed per tickets.md, and
nothing else — no manifest field, no internal grading, no path under
`.skills/`. Never duplicate a manifest-only field into `body.md`, and never
let `body.md` prose substitute for a `manifest.md` field.

## `Content-digest:` — computed with `git hash-object`, never a shipped script

**This section is the single home of the digest recipe.** `finish-branch`
re-runs the fenced block below unparaphrased immediately before submission
(its skill text must stay byte-identical to that block — a contract test
enforces the match). Do not invent a second recipe elsewhere.

Compute `Content-digest:` with `git hash-object --stdin`, the plumbing
command already required elsewhere in this skill set, chosen because its
output is platform-uniform — unlike `shasum` or `sha256sum`, whose output
format varies across platforms — and because it introduces no new tooling
this repository, or an adopting repository, would have to install. Feed it
the exact bytes of `title.txt` (the title followed by exactly one trailing
newline) and then the full contents of `body.md`, in that order and with
no other bytes. Read both files from disk rather than interpolating the
title text into the command — the same shell-quoting hazard `title.txt`
exists to avoid (see above).

Always use the fully qualified paths
`.skills/pr-packages/<stable-id>/title.txt` and
`.skills/pr-packages/<stable-id>/body.md`, never a bare relative filename.
A bare `cat body.md` only resolves when the shell's working directory
happens to already be the package directory; run from the repository root —
the normal working directory for this skill — it fails with `cat: body.md:
No such file or directory` on stderr while the rest of the pipeline's bytes
still reach `git hash-object` through the pipe, which then hashes a partial
input and prints a valid-looking 40-character SHA. Nothing about that
output looks wrong, so the digest is silently corrupt.

<HARD-GATE>
Guard against exactly that: check `title.txt` and `body.md` are each
readable *before* piping into `git hash-object`, and abort with a visible
error instead of hashing partial input if either is not. Neither step needs
anything beyond a POSIX shell test and `git`:

```
test -r ".skills/pr-packages/<stable-id>/title.txt" || {
  echo "Error: title.txt missing or unreadable at .skills/pr-packages/<stable-id>/title.txt" >&2
  exit 1
}
test -r ".skills/pr-packages/<stable-id>/body.md" || {
  echo "Error: body.md missing or unreadable at .skills/pr-packages/<stable-id>/body.md" >&2
  exit 1
}
{ cat ".skills/pr-packages/<stable-id>/title.txt"; cat ".skills/pr-packages/<stable-id>/body.md"; } | git hash-object --stdin
```
</HARD-GATE>

## Package files never enter a commit plan or a reviewer-facing locator

<HARD-GATE>
A package file — `manifest.md`, `title.txt`, `body.md`, or the
`<stable-id>` directory itself — never enters a commit plan: phase 5's
grouping and validation never proposes, stages, or commits anything under
`.skills/pr-packages/`. A package path is never shown as a reviewer-facing
locator: never cite `.skills/pr-packages/<stable-id>/...` in a PR body, a
commit message, or any text a reviewer reads — `.skills/` is git-ignored
and unreachable from the PR revision, so a path into it tells a reviewer
nothing they can open.
</HARD-GATE>
