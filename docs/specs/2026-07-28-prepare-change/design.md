# Design: Prepare change

Feature code: PCHG
Status: Approved
Date: 2026-07-28
Requirements: ./requirements.md

## Context

Nothing in this skill set authors a commit message or a pull-request body. Commits
happen inside `execute-plan`'s implementer subagents, whose entire instruction is
*"Commit, with the requirement-ID trailer the brief's commit step names"*
(`implementer-prompt.md:44`) — subject and body are unspecified. `finish-branch`
owns the crossing end to end: it gates on `verify` + `trace` + `acceptance-check`,
prints a five-option menu verbatim, publishes a `record-decision` before any side
effect, then runs `git push -u origin` and *"create the PR"* with no template, no
body rules, and no reviewer-facing prose anywhere in the file. Downstream, `release`
groups commits by their `Implements:` / `Guards:` trailers to build the changelog and
drops untrailered commits into a `Misc` section, and `code-review` uses the same
trailers to map a commit back to its spec folder. So identifiers are load-bearing
machine input while the human-readable half of every commit and PR is unowned.

Three constraints chain together and decide the shape. **ARCH-5** forbids a
model-invoked skill from invoking a user-invoked one, and `/file-issues` is
user-invoked — so a skill that wants a missing ticket filed can only *name* it.
`finish-branch`'s record-before-crossing rule means the publication gate cannot be
duplicated without creating a second, weaker copy that will drift. And **ARCH-3**
forbids mandating vendored executables in adopting repos, so no bundled packager,
validator, or digest script may ship with this feature. Together these rule out the
obvious design — a self-contained ship skill that validates, commits, pushes, and
opens the PR through its own helper — and leave exactly one shape: an authoring
skill that mutates only local git, hands a **file-based package** across a seam to
`finish-branch`, and computes every hash with git's own plumbing.

**ARCH-2** (optional layers no-op when absent) is what makes the skill portable. Every
context source — the spec triad, ADRs, decision records, implementation notes, the
tracker, and `Default PR base:` itself — is optional, and each absence degrades to a
narrower but complete diff-derived narrative rather than to a failure or an invention.
**ARCH-6** shapes the findings model: a branch's pre-existing commits may come from
work this skill set never mediated, so a missing trailer or an off-convention subject
is reported as a finding, never enforced as a violation.

The remaining tension is between "structure the commits well" and "never rewrite
history". Rewriting is where the value would be on a messy branch, but a rewrite
discards the per-task trailers `release` groups on, orphans the `commits
<base7>..<head7>` correspondence the `.skills/progress.md` ledger records, and on a
pushed branch requires the force-push `finish-branch` forbids an agent from
initiating. The design therefore splits the capability: full authority over commits
that do not exist yet, zero authority over commits that do, and a written **advisory
commit map** for the gap.

Architecture invariants this feature relies on: **ARCH-2** (optionality), **ARCH-3**
(zero mandatory tooling), **ARCH-5** (invocation direction), **ARCH-6** (participant
boundary).

## Decisions

1. **`prepare-change` authors; `finish-branch` crosses.** The new skill produces
   content and mutates only local git. Push, PR creation, merge, discard, and block
   stay in `finish-branch` behind its existing gates. → ADR 0003.
2. **Commits that already exist are never touched.** The skill has full authority
   over commits it creates and none over commits it finds; the gap is covered by an
   advisory commit map that emits no runnable rewrite command. → ADR 0004.
3. **The PR base is declared, never inferred.** `setup-repo` persists `Default PR
   base:`; `prepare-change` reads it, and asks when it is absent or ambiguous. Git
   topology is a setup-time suggestion, never a selector. → ADR 0005.
4. **The package is three files plus a digest computed with `git hash-object`.**
   `manifest.md` holds every machine-checkable field, `title.txt` holds the approved
   title alone so it is read from disk rather than interpolated into a shell command,
   `body.md` holds only reviewer-facing prose, and the digest covers the exact title
   bytes and `body.md` bytes. `git hash-object` is chosen over `shasum`/`sha256sum`
   because git is already a hard dependency and its object hashing is uniform across
   platforms, which `shasum` is not — and because ARCH-3 forbids shipping a hashing
   script. → §F.
5. **The passive-data contract is reused by path, not copied.** `prepare-change`
   loads `skills/review/explain-change/references/passive-data-safety.md`. Precedent:
   `finish-branch/SKILL.md:116` already cites
   `skills/review/allocate-attention/references/signals.md` across skill boundaries.
   A third copy of that contract would be worse than the coupling.
6. **Convention resolution is memoized in session memory only.** No cache file, no
   config key; a new session re-resolves.
7. **Findings are graded, never gated.** A machine-enforced check that ran and failed
   rides the existing `verify` failure path inside `finish-branch`; nothing else
   withholds a crossing.
8. **Model-invoked with autonomous commits.** Validation precedes every commit;
   the only questions are the five exception triggers. The single content-approval
   point sits at the `finish-branch` checkpoint, over the real branch state.
9. **`/file-issues` is named, never invoked** (ARCH-5), and the crossing pauses while
   the user runs it.
10. **The package directory is keyed by a sanitized, head-derived stable id**, so a
    branch name containing `/`, `..`, or a shell metacharacter can never shape a path.

## Architecture

### A. Base resolution

Satisfies: PCHG-2.1, PCHG-2.2, PCHG-2.3, PCHG-2.4, PCHG-2.5, PCHG-2.6, PCHG-2.7, PCHG-2.8, PCHG-2.9, PCHG-2.10
Respects: ARCH-2
Reuse: existing — reads `docs/agents/project.md` through the same "skills read this file for repo-specific machine config" convention every other skill uses (rung 2)

A fixed four-rung ladder, evaluated in order and short-circuiting on the first hit:
explicit invocation base → base recorded on an existing PR for the head branch →
`Default PR base:` from `docs/agents/project.md` (only when it resolves to a real
branch **and** differs from head) → ask the user. There is no fifth rung: the skill
never consults `origin/HEAD`, `main`, `master`, or fork-point topology, and a failure
to resolve is a question, not a guess.

Two guards sit on the config rung. When head *is* the configured default (working
directly on `dev`), the skill always asks, and the answer is scoped to the invocation
— it never rewrites the project default. When the configured value no longer names a
live branch, it degrades to the ask rung rather than erroring. The skill writes no
project configuration at all; the absent-config path continues on a session-only value
and names `/setup-repo` once as the way to persist it.

The resolved base is memoized for the session and copied into `manifest.md`, which is
what makes `finish-branch` able to use it without recomputation.

### B. Working-tree commit authoring

Satisfies: PCHG-1.1, PCHG-1.2, PCHG-1.3, PCHG-1.4, PCHG-1.5, PCHG-1.6, PCHG-1.7, PCHG-1.8, PCHG-1.9, PCHG-9.2, PCHG-9.3, PCHG-9.4
Respects: ARCH-4, ARCH-6
Reuse: existing — git plumbing plus the trailer grammar already defined in `AGENTS.md` §4 and consumed by `release` (rung 2)

Group → validate → commit, one commit at a time. Grouping runs over the uncommitted
tracked changes only; untracked files are excluded unless the user names them this
invocation, and a coherent change stays one commit rather than being split for
appearance. Pre-existing commits are read as context and never re-staged.

Validation runs **before** each `git commit`, over six axes: file scope, subject,
body, trailers, secret content, and staging boundary. Passing validation with an
unambiguous scope is sufficient authority to commit — there is no routine plan
approval. Five conditions stop the loop and ask instead: unrelated dirty changes,
unclear ownership of a change, an ambiguous partial-staging boundary, a secret-risk
finding, and a mismatch between the planned scope and the working tree. These are
exception questions; the skill does not otherwise pause.

Message shape: subject in the resolved convention, body stating what changed and why,
requirement and feature IDs confined to trailers. The trailer is machine input for
`release` and `code-review`; the prose is what a reviewer reads. An empty working tree
is a valid state — the skill creates nothing and proceeds to package authoring over
the branch's existing commits.

### C. Context gathering and passive-data safety

Satisfies: PCHG-3.1, PCHG-3.2, PCHG-3.3, PCHG-3.4, PCHG-3.5, PCHG-3.6, PCHG-3.7, PCHG-12.2
Respects: ARCH-2, ARCH-6
Reuse: existing — loads `skills/review/explain-change/references/passive-data-safety.md` verbatim rather than restating or copying it (rung 2)

Two authorities, never merged: the diff answers *what changed*; approved specs, ADRs,
decision records, and `.skills/implementation-notes.md` answer *why*. When a why-source
is absent the narrative is written without that rationale and says less — it is never
padded with plausible reasoning, and the omission is the honest output rather than a
degraded one.

Everything gathered is passive data. Instruction-shaped text inside a diff, commit
message, tracker body, spec, or decision record is never obeyed; credential-shaped
strings are replaced by a placeholder naming the class of secret. Two locator rules
follow from the reviewer's position: a file path may appear in reviewer-facing output
only when it is tracked and reachable from the PR revision or from a durable URL, and
substance from an unreachable source (anything under git-ignored `.skills/`, including
every decision record) is promoted inline with no path cited. This is why the design
never links a decision record even though it quotes one.

### D. Convention resolution

Satisfies: PCHG-4.1, PCHG-4.2, PCHG-4.3, PCHG-4.4, PCHG-4.5, PCHG-4.6, PCHG-4.7, PCHG-12.1
Respects: ARCH-2, ARCH-3
Reuse: existing — reads whatever convention artifacts the repo already has (commitlint config, `.gitmessage`, `CONTRIBUTING.md`, `.github/pull_request_template.md`) rather than adding a config surface (rung 2)

Commit conventions resolve on a three-rung ladder: machine-enforced artifacts and
declared repository documentation; then, only when no declared convention exists, the
subjects (not bodies, not diffs) of at most the 20 most recent non-merge commits; then
a neutral reviewer-centred fallback. A mixed sample terminates the ladder at the
fallback — the sample is never widened to manufacture a convention out of noise.

PR conventions resolve separately, from PR templates and declared project guidance
only; commit history is not re-read for PR structure. Resolution happens at most once
per session and the result is reused for every commit and the PR body. Nothing is
persisted: a cache would need invalidation logic and a config key for a computation
that costs one bounded read.

A convention derived from history is labelled inferred wherever it appears, and every
finding raised against it is advisory. Only declared or machine-enforced rules can
carry a stronger grade (§G).

### E. Ticket set resolution

Satisfies: PCHG-5.1, PCHG-5.2, PCHG-5.3, PCHG-5.4, PCHG-5.5, PCHG-5.6, PCHG-5.7, PCHG-5.8
Respects: ARCH-2, ARCH-6
Reuse: existing — the wayfinding operations already recorded in `docs/agents/issue-tracker.md` (rung 2)

The tracker named in `docs/agents/issue-tracker.md` supplies the read commands; the
skill adds no backend knowledge of its own. Where the branch name carries a tracker
identifier, that item is resolved along with its parent and sub-issue hierarchy when
the backend exposes one.

Each resolved item is then compared against the diff and classified **fully completed**
or **partial/related**. Only the first class earns closing linkage, and the linkage
syntax is whatever the configured backend uses — never assumed from another backend's
form. This classification is the whole point of the section: it is what stops a PR
from claiming to close a parent issue that the branch only partly advanced.

Tracker content is bounded to four uses — why-now context, acceptance context,
linkage, and commit-grouping hints. The PR body is never structured around tracker
items; that would rebuild the identifier-first document this feature exists to replace.
No tracker configured is a normal state: the ticket set is empty and authoring
continues.

### F. Package writer

Satisfies: PCHG-6.1, PCHG-6.2, PCHG-6.3, PCHG-6.4, PCHG-6.5, PCHG-6.6, PCHG-6.7
Respects: ARCH-3
Reuse: existing — the `.skills/` scratch convention and `git hash-object` (rung 2 and rung 4); no new tooling

```
.skills/pr-packages/<stable-id>/
├── manifest.md   ← every machine-checkable field
├── title.txt     ← the approved title alone, byte-exact
└── body.md       ← reviewer-facing PR content, nothing else
```

`<stable-id>` is sanitized and head-derived; a raw branch name never reaches the path,
so `feature/foo..bar` cannot traverse or inject. `manifest.md` carries: package
version, exact PR title, base and head refs with resolved SHAs, ticket and sub-issue
linkage, the commits actually present on the branch, the advisory commit map, the
convention findings, the validation results, and the digest of the title together with
`body.md`. `title.txt` holds the same title text, alone, for the digest recipe and the
`gh pr create` invocation to read from disk — the same treatment `body.md` already gets
— rather than interpolating title text (authored from diff and commit text, which this
skill classifies as passive data) directly into a shell command, where a `"`, backtick,
or `$(…)` could break quoting or run as a command.

The digest is `git hash-object` over `title.txt`'s bytes and over `body.md` — git is
already required, its hashing is uniform across platforms in a way `shasum` is not,
and ARCH-3 forbids shipping a script to do it. Three prohibitions complete the
section: nothing is written until `.skills/` is proven git-ignored (a line-presence
check, matching `execute-plan`'s existing idempotent pattern); no package file ever
enters a commit plan; and no package path is ever shown as a reviewer-facing locator,
because `.skills/` is git-ignored and a reviewer could not open it.

### G. Advisory commit map and findings grading

Satisfies: PCHG-7.1, PCHG-7.2, PCHG-7.3, PCHG-7.4, PCHG-7.5, PCHG-7.6, PCHG-7.7
Respects: ARCH-6
Reuse: none — new content (rung 7); no existing artifact describes a commit regrouping, and the grading vocabulary is specific to this feature's severity lock

The prohibition is absolute: no rewrite, amend, squash, reorder, rebase, or force-push
of any commit that existed before the invocation. What replaces it is a written map —
proposed groups, their order, subjects, bodies, the rationale for the regrouping, and
the trailers that must survive it — carried in `manifest.md`. It emits no runnable
`reset`/`rebase`/`push --force` command unless the user asks for one, because an
emitted command is an invitation to run it, and the trailers `release` depends on are
exactly what a careless rewrite drops.

The PR body always describes the branch as it is. A body written as though the map had
been applied would describe commits that do not exist.

Findings carry one of four grades: **advisory** (convention was inferred),
**reported** (convention is declared and no executable check failed), **not run** (a
machine-enforced check exists but was not executed), and — for a machine-enforced check
that ran and failed — routing through the repository's existing `verify` failure path
inside `finish-branch`. That last case is the only one with teeth, and it borrows teeth
that already exist rather than adding a gate. All findings and grades travel in the
package.

### H. The `finish-branch` checkpoint

Satisfies: PCHG-8.1, PCHG-8.2, PCHG-8.3, PCHG-8.4, PCHG-8.5, PCHG-8.6, PCHG-8.7, PCHG-8.8, PCHG-8.9, PCHG-8.10, PCHG-11.1, PCHG-11.2, PCHG-11.3, PCHG-11.4, PCHG-11.5, PCHG-11.6, PCHG-12.3
Respects: ARCH-5
Reuse: existing — extends `finish-branch`'s Step 4 execution path; adds no menu item and no new gate (rung 2)

The checkpoint is inserted **after** the user's menu selection and **before** the
crossing executes — so the five options still print verbatim and the decision order is
unchanged. It runs two questions in sequence:

1. **Ticket question (merge and PR paths).** Display the resolved ticket set; ask
   whether missing tickets should be created or supplemented. Asked even with no
   tracker configured, because the answer may be "yes, and there is nowhere to put it".
   A yes pauses the crossing and asks the user to run `/file-issues` — named, never
   invoked, because ARCH-5 forbids a model-invoked skill from calling a user-invoked one.
2. **Content approval (PR path).** Display the exact package — title, base, head, body,
   ticket linkage, commits, advisory map, findings, validation results — and offer
   approve / request edits / cancel. Edits re-author, revalidate, redisplay, and demand
   a fresh approval; there is no partial-approval state.

Immediately before submission the base and head SHAs are re-resolved and the digest
recomputed. Any difference invalidates the approval outright and forces the whole
re-author → revalidate → redisplay → reapprove cycle, which is what stops an approved
body from describing a branch state that moved underneath it. Submission then supplies
the approved local title, base, head, and body to the hosting adapter without
re-authoring them (`--body-file` for GitHub); the design claims nothing about what the
remote subsequently stores or renders. The approved digest travels as inline decision
evidence, never as a citation of the git-ignored package path. Because
`record-decision` already published against the now-invalidated digest, the
reapproval requires a fresh `record-decision` publish carrying the reapproved
values before submission is retried.

**Limitation.** After an invalidated approval, `.skills/decisions/` holds
both the stale record and the fresh one with no mechanical link between
them — `record-decision` exposes no `Supersedes:`/`Superseded-by:` input,
and its validator would fail the fresh publish if the stale record's
bidirectional pairing were hand-authored ahead of it, so linking the two
is not attempted here. Giving them a mechanical link would require
`record-decision` to grow a supersede-write capability, which is
deliberately out of this feature's scope. The fresh record is the
authoritative one and carries the reapproved values; the stale record
simply remains in place, with nothing marking it superseded.

Everything already in `finish-branch` survives unchanged: merge and PR stay withheld
on a red gate, the five options print verbatim, `record-decision` still publishes
before every crossing, discard still requires the typed word, the risk-glob naming of
`/comprehend-change` and `/explain-change` is untouched, and force-push remains
user-request-only. Content approval is additive to the integration decision, not a
replacement for it.

### I. The `execute-plan` tail

Satisfies: PCHG-9.1, PCHG-11.7, PCHG-11.8, PCHG-11.9
Reuse: existing — inserts one step into the existing "After the Last Task" sequence (rung 2)

`execute-plan`'s closing sequence becomes: whole-branch review → one fixer if needed →
polish → acceptance → **`prepare-change`** → `finish-branch`. The insertion point is
after acceptance because acceptance can still change the code, and authoring must
describe the code that will actually ship. Every existing step keeps its order and its
`Done when`, the per-task ledger append is untouched, and continuous mode still never
pauses between tasks — the new step runs at the end of the plan, not inside the loop.

### J. `setup-repo` decision and template slot

Satisfies: PCHG-10.1, PCHG-10.2, PCHG-10.3, PCHG-10.4, PCHG-10.5, PCHG-11.10, PCHG-11.11, PCHG-11.12
Respects: ARCH-2
Reuse: existing — one more lettered decision in the existing A–I walk, and one more slot in `templates/agents/project.md` (rung 2)

A new decision joins the walk, taking the same shape as its neighbours: a
two-or-three-sentence explainer naming which skills consume the value, a
recommendation with a one-line reason, then a wait for the answer. Git topology and
common branch names (`dev`, `staging`, `main`) appear as **suggestions** in the
prompt; none is pre-selected. A confirmed value is written as `Default PR base:` into
`docs/agents/project.md` under the existing additive rule, and the slot is added to
`templates/agents/project.md` so new repos get it seeded. Declining writes nothing —
`prepare-change` then asks per invocation (§A), which is why the field is genuinely
optional rather than a new required setup step (ARCH-2).

The one-decision-at-a-time walk, the additive write rule, and the Step 6 verification
gate are unchanged.

### K. Registration and roster (infrastructure)

Satisfies: PCHG-11.13
Reuse: existing — the established registration points for any new skill (rung 2)

Infrastructure, not behavior: `AGENTS.md` (skill count, category table, model-invoked
list — with the four Iron Laws and the forbidden-pattern list unchanged), `README.md`'s
ship-category row, `docs/guide/skills/prepare-change.md`, and the skill path lists in
`.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. Without these the
skill exists but is neither installable nor discoverable.

## Seams for testing

No new seam *kinds*. This repo already tests skills at exactly two boundaries — a
greppable scenario-markdown annotation layer under `tests/<feature>/`, and Python
contract tests that assert what a `SKILL.md` does and does not say (e.g.
`tests/test_finish_branch_risk_signal.py`). Both are declared in
`docs/agents/project.md`'s test-annotation table. New files, established seams.

| Seam | Kind | Covers |
|---|---|---|
| `tests/prepare-change/scenarios.md` — greppable ID annotation layer | integration (declared annotation layer) | every behavioral ID: PCHG-1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| `tests/test_prepare_change_contract.py` — `prepare-change/SKILL.md` text contract | unit | PCHG-1.5, 1.7, 1.9, 2.6, 2.7, 3.4, 3.6, 3.7, 4.3, 4.4, 4.7, 5.6, 5.8, 6.2, 6.5, 6.6, 6.7, 7.1, 7.3, 7.4 |
| `tests/test_prepare_change_checkpoint.py` — `finish-branch/SKILL.md` contract and guards | unit | PCHG-8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 8.10, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 12.3 |
| `tests/test_prepare_change_wiring.py` — `execute-plan` tail, `setup-repo` decision, template slot, roster registration | unit | PCHG-9.1, 9.2, 9.3, 9.4, 10.1, 10.2, 10.3, 10.4, 10.5, 11.7, 11.8, 11.9, 11.10, 11.11, 11.12, 11.13 |
| `tests/prepare-change/scenarios-pressure.md` — injected instruction and planted credential | integration (declared annotation layer) | PCHG-3.5, 12.2 |
| `tests/test_prepare_change_convention.py` — bounded, once-per-session resolution | unit | PCHG-4.1, 4.2, 4.5, 4.6, 12.1 |
| `tests/trigger/prepare-change-routing.md` — description routing baseline | integration (declared annotation layer) | PCHG-1.1 |

Every seam row names a boundary that already exists in this repo's test layout; the
new-seam count is zero.

## Coverage check

Every requirement ID appears in exactly one `Satisfies:` line:

| Section | IDs |
|---|---|
| A. Base resolution | PCHG-2.1 … 2.10 |
| B. Working-tree commit authoring | PCHG-1.1 … 1.9, 9.2, 9.3, 9.4 |
| C. Context gathering and passive-data safety | PCHG-3.1 … 3.7, 12.2 |
| D. Convention resolution | PCHG-4.1 … 4.7, 12.1 |
| E. Ticket set resolution | PCHG-5.1 … 5.8 |
| F. Package writer | PCHG-6.1 … 6.7 |
| G. Advisory commit map and findings grading | PCHG-7.1 … 7.7 |
| H. The `finish-branch` checkpoint | PCHG-8.1 … 8.10, 11.1 … 11.6, 12.3 |
| I. The `execute-plan` tail | PCHG-9.1, 11.7, 11.8, 11.9 |
| J. `setup-repo` decision and template slot | PCHG-10.1 … 10.5, 11.10, 11.11, 11.12 |
| K. Registration and roster | PCHG-11.13 |

All 90 defined criteria are mapped; there are no deliberately unmapped IDs. The
Accessibility quality attribute is recorded as `None` with a reason and — per the
requirements template's rule that an all-`None` attribute omits its IDed line — carries
no requirement ID, so it is a recorded non-applicability rather than an uncovered
criterion.
