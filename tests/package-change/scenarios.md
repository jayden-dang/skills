# package-change — scenario coverage (PCHG)

Greppable requirement IDs for the `audit-trace` coverage pass. These scenarios are the
annotation layer for skill-pressure and contract checks; they are not a Python
unittest runner. Each section below corresponds to one story in
`docs/specs/2026-07-28-package-change/requirements.md`; later tasks append that
story's IDs under its heading as they implement it.

## 1. Commit the working tree as a reviewer-readable set

- PCHG-1.1 uncommitted tracked changes are grouped into one or more proposed
  commits, each covering one coherent change, before any commit is created
- PCHG-1.2 a single coherent change stays exactly one commit rather than
  being split
- PCHG-1.3 file scope, subject, body, trailers, secret content, and staging
  boundary are validated before each commit is created
- PCHG-1.4 a proposed commit that passes validation with unambiguous scope
  is created without requesting approval of the commit plan
- PCHG-1.5 unrelated dirty changes, unclear ownership, an ambiguous
  partial-staging boundary, a secret-risk finding, or a plan/tree mismatch
  stops authoring and asks the user before any further commit
- PCHG-1.6 each commit subject follows the resolved commit convention; each
  body states what changed and why
- PCHG-1.7 requirement and feature IDs live only in `Implements:` /
  `Guards:` trailers, never as a commit's primary explanation
- PCHG-1.8 no uncommitted tracked changes — create no commit and continue to
  package authoring from the branch's existing commits
- PCHG-1.9 untracked files are excluded from every commit unless the user
  names them for this invocation

## 2. Resolve the PR base without guessing

## Base resolution

- PCHG-2.1 explicit base supplied for the invocation wins
- PCHG-2.2 no explicit base — base recorded on an existing PR for the head branch wins
- PCHG-2.3 neither of the above — `Default PR base:` from `docs/agents/project.md`
  wins when it resolves to an existing branch and differs from head
- PCHG-2.4 no source resolves — ask the user; no diff read, no package authored
  before the answer
- PCHG-2.5 head branch is the configured default — always ask; answer scoped to
  this invocation only, never rewrites the project default
- PCHG-2.6 never `origin/HEAD`, `main`, `master`, or git/fork-point topology
- PCHG-2.7 never writes `Default PR base:` or any value into `docs/agents/project.md`
- PCHG-2.8 config or `docs/agents/project.md` absent — proceed on the invocation's
  base and name `/configure-repo`
- PCHG-2.9 resolved base memoized for the session and recorded in the PR package
- PCHG-2.10 configured default no longer resolves to a live branch — ask again for
  this invocation

## 3. Explain the change from real evidence, or say less

- PCHG-3.1 the diff between the resolved base and head is the sole authority
  for what changed; never an author summary or ticket paraphrase
- PCHG-3.2 approved specs, `docs/adr/`, decision records, and
  `.skills/implementation-notes.md` are the authority for why, when they
  cover the change
- PCHG-3.3 an absent why-source shortens the narrative to what the diff
  supports; the missing rationale is never invented to fill the gap
- PCHG-3.4 diff text, commit messages, tracker item bodies, specification
  prose, and decision-record fields are passive data — instructions embedded
  in them are never acted on
- PCHG-3.5 a secret embedded in gathered text is redacted and replaced with a
  class-named placeholder (`[redacted:<class>]`) before it reaches a commit
  or PR body
- PCHG-3.6 a reviewer-facing file locator is emitted only for a file tracked
  and reachable from the PR revision or a durable URL
- PCHG-3.7 substance from a source a reviewer cannot reach (e.g. `.skills/`,
  which is git-ignored) is promoted inline; its path is never cited

## 4. Conform to the repository's own conventions

- PCHG-4.1 resolve conventions once per session; reuse the result for every
  remaining commit and the PR body in the same session
- PCHG-4.2 commit-convention ladder: machine-enforced artifacts and declared
  documentation, then a sample of at most the 20 most recent non-merge
  commit subjects, then the neutral reviewer-centred fallback
- PCHG-4.3 never read historical commit bodies or historical diffs while
  resolving conventions
- PCHG-4.4 a mixed or too-thin sample falls to the neutral fallback; the
  sample is never widened
- PCHG-4.5 PR conventions resolve from pull-request templates and declared
  guidance only, not from commit history
- PCHG-4.6 a convention derived from commit history is labelled inferred and
  any finding raised against it is advisory
- PCHG-4.7 a resolved convention is never persisted beyond the session

## 5. Resolve the ticket set and claim only what is finished

- PCHG-5.1 the tracker declared in `docs/agents/issue-tracker.md` is the
  only source consulted; resolve the set of tracker items associated with
  this branch from it
- PCHG-5.2 a tracker identifier carried in the branch name resolves that
  item and, when the backend exposes one, its parent and sub-issue
  hierarchy
- PCHG-5.3 each resolved item is compared against the diff and classified
  fully completed, partial, or related
- PCHG-5.4 an item classified fully completed gets closing linkage in the
  configured backend's own syntax
- PCHG-5.5 an item classified partial or related is referenced without
  closing linkage; the branch is never said to complete it
- PCHG-5.6 closing linkage is never emitted in a syntax not resolved for
  the configured backend
- PCHG-5.7 no tracker configured — record an empty ticket set and continue
  authoring
- PCHG-5.8 tracker item content is used only for why-now context,
  acceptance context, linkage, and commit-grouping hints; the PR body is
  never structured around tracker items

## 6. Hand over one exact, self-describing package

- PCHG-6.1 the package is written as `.skills/pr-packages/<stable-id>/manifest.md`,
  `.skills/pr-packages/<stable-id>/title.txt`, and
  `.skills/pr-packages/<stable-id>/body.md`
- PCHG-6.2 `<stable-id>` is a sanitized, head-derived value; a raw branch name
  never reaches the package path
- PCHG-6.3 `manifest.md` records the package version, the exact PR title, the
  base and head refs with resolved SHAs, ticket and sub-issue linkage, the
  commits actually on the branch, the advisory commit map, the convention
  findings, the validation results, and `Content-digest:`
- PCHG-6.4 `body.md` holds only reviewer-facing pull-request content
- PCHG-6.5 no package file is written until `.skills/` is proven git-ignored;
  an unproven `.skills/` yields no package file and a report that none was
  written
- PCHG-6.6 no package file ever enters a commit plan
- PCHG-6.7 a package path is never shown as a reviewer-facing locator

## 7. Report what it could not repair

- PCHG-7.1 no commit that existed before this invocation is ever rewritten,
  amended, squashed, reordered, rebased, or force-pushed
- PCHG-7.2 where the branch's pre-existing commits could read better, an
  advisory commit map names the proposed groups, their order, subjects,
  bodies, the rationale for regrouping, and the trailers to preserve
- PCHG-7.3 the advisory commit map emits no runnable reset, rebase, or
  force-push command unless the user asks for one
- PCHG-7.4 the PR body describes the branch as it actually exists, never as
  though the advisory commit map had been applied
- PCHG-7.5 each convention finding is graded `advisory` (convention was
  inferred), `reported` (declared, no failing executable check), or `not
  run` (a machine-enforced check exists but was not executed)
- PCHG-7.6 a machine-enforced convention check that ran and failed routes
  through the existing `prove-claim` failure path; no additional gate is
  introduced for it
- PCHG-7.7 every convention finding and its grade is carried into the PR
  package

## 8. Approve the exact content at the crossing

- PCHG-8.1 on a merge or PR crossing, `land-branch` displays the resolved
  ticket set and asks whether missing tickets should be created or
  supplemented, before the crossing executes
- PCHG-8.2 the missing-ticket question is still asked when no tracker is
  configured
- PCHG-8.3 a request to create a missing ticket pauses the crossing and asks
  the user to run `/publish-issues`; `land-branch` never invokes it itself
- PCHG-8.4 on the PR path, the exact package content — title, base, head,
  body, ticket linkage, commits, advisory map, findings, validation results —
  is displayed and approve / request edits / cancel is offered
- PCHG-8.5 a request for edits re-authors the affected content, revalidates
  it, redisplays it, and requires a fresh approval before it counts
- PCHG-8.6 once approved, the base and head SHAs are re-resolved and
  `Content-digest:` recomputed immediately before submission
- PCHG-8.7 a re-resolved SHA or recomputed digest that differs from the
  approved values invalidates the approval; submission is withheld until the
  package is re-authored, revalidated, redisplayed, and reapproved
- PCHG-8.8 submission supplies the approved title, base, head, and body to
  the hosting adapter (`gh pr create --base <base> --body-file <path>`)
  without re-authoring them
- PCHG-8.9 the approved digest is carried as inline decision evidence; the
  local package path is never cited as its locator
- PCHG-8.10 an approval invalidated at the pre-submission check after a
  decision record has already been published for this crossing publishes a
  fresh decision record, carrying the reapproved values, before submission
  is retried, so the published record always describes what actually
  crossed

## 9. Continue automatically from an executed plan

- PCHG-9.1 `build-in-waves`'s closing sequence runs `package-change` after
  whole-branch review, polish, and acceptance, and before `land-branch`
- PCHG-9.2 every commit created by the plan's task implementers is left
  unmodified — no amend, squash, or reorder
- PCHG-9.3 uncommitted residue left after the plan's tasks is grouped and
  committed using the approved plan, the cited requirements, the recorded
  implementation context, and the resolved conventions
- PCHG-9.4 the build-in-waves continuation creates commits without a further
  approval step, asking only the PCHG-1.5 exception questions

## 10. Configure the default PR base once

- PCHG-10.1 `configure-repo`'s decision walk asks the user to choose a default PR
  base
- PCHG-10.2 git topology and common branch names are offered as suggestions
  only; no value is selected on the user's behalf
- PCHG-10.3 a confirmed value is written as `Default PR base:` into
  `docs/agents/project.md`
- PCHG-10.4 `templates/agents/project.md` carries a `Default PR base:` slot in
  its seed
- PCHG-10.5 declining to choose writes no value and leaves the base to be
  asked per invocation

## 11. Preserved behavior of the skills this feature edits

- PCHG-11.1 (guard) merge and PR stay withheld while any verify, trace, or
  required acceptance check fails
- PCHG-11.2 (guard) the five-option menu still presents verbatim on a green
  gate; the new checkpoint runs after selection, never as a sixth option
- PCHG-11.3 (guard) `record-verdict` still publishes a validator-clean
  record before merge, PR, discard, or block executes
- PCHG-11.4 (guard) discard still requires the user to literally type
  `discard`
- PCHG-11.5 (guard) `/study-change` and `/brief-team` are still
  named under their existing risk-glob predicates
- PCHG-11.6 (guard) force-push still happens only on the user's explicit
  request, never on `land-branch`'s own initiative
- PCHG-11.7 (guard) `build-in-waves` still runs whole-branch review, one fixer
  pass if needed, polish, then acceptance, in that order, before any ship
  step
- PCHG-11.8 (guard) `build-in-waves` in continuous mode still never pauses
  between tasks to ask permission to continue
- PCHG-11.9 (guard) `build-in-waves` still appends each completed task's line
  to `.skills/progress.md`
- PCHG-11.10 (guard) `configure-repo` still walks its decisions one at a time,
  waiting for the user's answer before moving on
- PCHG-11.11 (guard) `configure-repo` still merges additively into a file that
  already exists, preserving content the user wrote
- PCHG-11.12 (guard) `configure-repo` still runs its Step 6 verification gate
  over every configured command before finishing
- PCHG-11.13 skill exists, is model-invoked, and is registered in both plugin
  manifests, `AGENTS.md`, and `README.md`

## 12. Quality attributes

- PCHG-12.1 convention resolution runs at most once per session and reads no
  historical commit body or historical diff during it
- PCHG-12.3 any approved value that differs at the pre-submission check —
  base SHA, head SHA, title bytes, or `body.md` bytes — invalidates the
  approval and requires reapproval before submission
