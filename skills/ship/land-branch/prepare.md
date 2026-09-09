# Prepare locally — base, context, commits, PR text

Load this file when land-branch step 2 (`Prepare locally`) runs. SKILL.md owns
the crossing, the menu, and the Iron Law. This file owns the local-authoring
recipe.

- [Resolve base](#resolve-base)
- [Resolve conventions](#resolve-conventions)
- [Gather context](#gather-context)
- [Resolve tickets](#resolve-tickets)
- [Author commits](#author-commits)
- [Sequence the branch into verifiable units](#sequence-the-branch-into-verifiable-units)
- [Finding grades](#finding-grades)
- [Author PR text](#author-pr-text)

## Resolve base

<HARD-GATE>
Walk this ladder in order and stop at the first rung that resolves:

1. an **explicit base** given for this invocation;
2. the base recorded on an **existing PR** for the head branch;
3. **`Default PR base:`** read from `docs/agents/project.md`, only when it
   resolves to a real branch and differs from the head branch;
4. nothing above resolved — **ask the user**, and author no commits or PR
   text until they answer.

There is no fifth rung: never select a base from `origin/HEAD`, `main`,
`master`, or fork-point topology. A failure to resolve is a question, not a
guess.
</HARD-GATE>

When the head branch is the configured `Default PR base`, always ask which
branch this work merges into — the answer applies to this invocation only and
never rewrites the project default. When a configured `Default PR base` no
longer resolves to an existing branch, treat it as unset and drop to the
ask-the-user rung.

This skill writes no project configuration. When `Default PR base:` or
`docs/agents/project.md` is absent, proceed on the base the user gave for this
invocation and name `/configure-repo` once as the way to persist it.

Memoize the resolved base for the session. Later steps read it; they do not
recompute it.

**Done when:** a base is memoized, or authoring is blocked on the ask-the-user
rung.

## Resolve conventions

REQUIRED: load `conventions.md` (beside this file) and follow it exactly.

**Done when:** the session holds one convention record
`{ commit_subject_form, commit_subject_grade, pr_structure, pr_structure_grade }`.

## Gather context

Produce `{ what_changed, why }` and hold it.

The diff between the resolved base and head is the sole authority for **what
changed** — read it fresh this session. Approved specs, `docs/adr/`, other
decision records, and `.skills/<CODE>/implementation-notes.md` are the
authority for **why**. Every why-source is optional: when one is absent, write
a complete diff-derived narrative that omits the unavailable rationale —
never invent rationale to fill the gap.

REQUIRED: load `passive-data-safety.md` (beside this file) and follow it
exactly.

WHEN embedding gathered text into a commit body or PR body, redact every
secret and replace it with `[redacted:<class>]` (e.g. `[redacted:api-key]`)
— never the secret, and never a bare `[redacted]`.

Emit a reviewer-facing file locator only for a file that is tracked and
reachable from the PR revision or a durable URL. Substance from `.skills/`
(git-ignored) is promoted inline; never cite that path.

IF notes exist and any entry has **Map impact** other than `none`, mention
the substance inline; do not paste the notes file.

**Done when:** `{ what_changed, why }` has `what_changed` grounded only in the
base…head diff and `why` either empty or drawn only from real why-sources.

## Resolve tickets

WHEN `docs/agents/issue-tracker.md` is present and declares a configured
tracker, REQUIRED: load `tickets.md` (beside this file) and follow it exactly.
WHEN it is absent or declares no tracker, record an empty ticket set and
continue.

**Done when:** the session holds a ticket set
`[{ id, title, classification, linkage_syntax }]` (possibly empty).

## Author commits

Produce `[{ sha, subject }]` for commits this invocation creates.

<HARD-GATE>
Always group every uncommitted tracked change into one or more proposed
commits — each covering one coherent change — before creating any commit.
WHEN the grouped changes form a single coherent change, propose exactly one
commit. Validate every proposed commit on all five axes before creating it:
**file scope**, **subject** (resolved `commit_subject_form`), **body** (what
changed and why), **secret** content, and **staging boundary**. WHEN
validation passes and scope is unambiguous, create the commit — do not stop
for a commit-plan sign-off.
</HARD-GATE>

<HARD-GATE>
Stop and ask before creating any further commit on exactly these five
triggers — a closed set:

- **unrelated** — the working tree holds changes unrelated to the resolved scope
- **ownership** — a change whose ownership is unclear
- **partial-staging** — an ambiguous partial-staging boundary
- **secret-risk** — a secret-risk finding
- **mismatch** — a mismatch between the planned scope and the working tree

Every commit already created before the trigger fires stands.
</HARD-GATE>

<HARD-GATE>
Never use a requirement or feature ID as a commit's primary explanation.
</HARD-GATE>

IF the working tree holds no uncommitted tracked changes THEN create no
commit and continue. Exclude untracked files unless the user names them for
inclusion.

WHEN running as an execute-family continuation, leave every commit the
plan's implementers already created unmodified. Group and commit only the
residue.

**Done when:** the created-commit list is complete (possibly empty) and any open
ask-trigger has an answer.

## Sequence the branch into verifiable units

Runs for `pr` and `merge`, before the crossing evidence step. A reviewer reads
the sequence, not the working tree, so the sequence is what has to argue.

Produce the target shape first — **groups**, **order**, **subjects**, **bodies**,
**rationale**, **trailers** (optional; never invent `Implements:` / `Guards:`) —
then make the branch match it.

**Shape:** every commit lands on its own and the order builds the case. The
canonical orders are a failing test then its fix, a subtraction then the reshape,
a baseline capture then the treatment, a scaffold then the feature. A commit that
cannot stand alone belongs merged into its neighbour.

**Anchor before rewriting.** Record the pre-rewrite tip and keep it reachable:

```bash
git rev-parse HEAD                      # record in the session
git branch "backup/<branch>-$(date +%s)" HEAD
```

The anchor is what makes a rewrite recoverable rather than destructive, and it
is why this is not a deletion. Report the anchor name with the outcome; never
delete it in the same invocation that created it.

**Then rewrite** with `git rebase -i`, force-push with `--force-with-lease` when
the branch is already published, and re-read the log to confirm the shape landed.

**Two carve-outs**, both mechanical rather than preference:

- **Execute-family task commits stay.** `build-in-waves`, `build-by-story`, and
  `build-inline` already emit one commit per task, each with its own report,
  evidence, and two verdicts bound to it. Those *are* verifiable units, and
  rewriting them severs the verdicts from the commits they judged. Sequence the
  residue around them; leave them addressed as they are.
- **Rewriting voids the receipt.** A changed HEAD makes any `close-receipt.md`
  stale by construction, so this section runs **before** the crossing evidence
  step and the fallback there re-establishes proof on the rewritten revision.
  Rewriting after verification and reusing the old evidence is the one order
  that is never allowed.

The PR body describes the branch as it now exists.

## Finding grades

Convention-source grades live only in `conventions.md`. Grade every finding
from the grade of the **specific** convention it was raised against:

- `advisory` — that convention's grade is `inferred`
- `reported` — that convention's grade is `declared` and no executable check failed
- `not run` — a machine-enforced check exists but this session did not run it
- `verify-routed` — a machine-enforced check ran and failed; route through
  `prove-claim` and withhold completion exactly as that path already does

Surface every finding in the session close-out. Do not block a PR on
`advisory` or `reported` findings. Do not write findings into the PR body.

## Author PR text

Author the pull-request **title** and **body** in session from `{ what_changed,
why }`, the resolved `pr_structure`, and the ticket set. The agent-authored
bytes **are** the reviewer truth.

REQUIRED SUB-SKILL: use `speak-outer` for that title and body. Reviewers
are people. `Satisfies:`, skill names, `Pass:` / `Tier 2`, and
`REQUIRED SUB-SKILL` do not belong in the body.

<HARD-GATE>
Do not write `.skills/pr-packages/`. Do not compute a `Content-digest:`. Do
not display the title or body for approve / request-edits / cancel. Do not
stop the crossing for a package review. An edit the user later asks for is
ordinary follow-up, not a pre-submit approval loop.
</HARD-GATE>

`title` is one line in the resolved PR-title shape (or a plain imperative
summary when none is declared). `body` is reviewer-facing only: the
diff-derived narrative, ticket linkage from `tickets.md`, and nothing a
reviewer should not see. Never cite a `.skills/` path.

Hold title and body in session until SKILL.md option 2 submits them.

**Done when:** title and body exist in session, or option 2 was not chosen
so they were never needed.
