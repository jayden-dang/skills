---
name: cut-release
version: 1.1.0
description: Cuts a release for work already merged to the release branch — version bump, tag,
  changelog, release notes, and Implemented specs in range marked Shipped.
  Run it with /cut-release.
disable-model-invocation: true
---

# Cut Release

Prepare and cut a release as a strict sequence of gates. Create one todo per step below and work them in order.

**The stop rule:** any step that fails means STOP — report exactly what failed and what remains, and leave the repo un-released. There are no partial releases: no tag without a passing build, no notes for artifacts that do not exist, no "we'll fix it after tagging."

**Terminal reject vs stop rule:** after a stop-rule failure, ask once whether the
user issues an **explicit terminal reject**. Yes → REQUIRED SUB-SKILL: use
`record-verdict` with verdict `release-reject`, `Boundary-Type: release`, durable
evidence inline; leave the repo un-released. No / silence / "fix later" → **no**
decision record (mechanical stop alone is not a terminal verdict). The same
`release-reject` write-handoff applies if the user rejects at version or tag approval.
Stop-rule discipline is unchanged: no partial releases.

Read the repo's commands from `docs/agents/project.md` (verify commands, release steps, smoke command). If it is missing, say so, suggest `configure-repo`, and ask the user for the commands before proceeding.

## a. Prove-claim gate

Run every verify command in order — typecheck, lint, unit, e2e — plus the docs-only
audit-trace check (REQUIRED SUB-SKILL: use `audit-trace`). All must pass fresh,
now; prior green runs do not count. The audit-trace check must be **clean** on
docs integrity (unknown task cites, duplicate definitions, etc.) — it does **not**
grep tests for requirement IDs.

**Done when:** every command has a fresh passing run you have read the output of.

## b. Release set, then changelog

Classify **before** drafting notes or proposing a version. A tag of HEAD
ships the code of every merged feature in range — `Status:` that still
says `Approved` is fiction. This step is the stop, not step i.

**Recipe — run and read:**

1. `last=$(git describe --tags --abbrev=0 2>/dev/null)` — no tag → range is
   the whole history; say so.
2. `git diff --name-only ${last:+$last..}HEAD` and `git log ${last:+$last..}HEAD
   --oneline`.
3. Map changed paths to `docs/specs/INDEX.md` features (spec-dir prefix or
   `**Files:**` ownership). That list is the **range set**.
4. For each feature, read `Status:` from its `requirements.md` (INDEX row if
   the file has no line). Partition:
   - `Implemented` → **cohort** (this cut will claim and later flip)
   - `Shipped` → **already** (changelog as an amend if the range touched it;
     do not flip)
   - `Approved`, `Draft`, or missing → **blocker**

**IF any blocker:** this step **fails**. STOP. List each blocker and its
`Status:`. Do not propose a version. Do not tag. Do not invoke
`realign-spec`. State that each blocker must reach `Implemented` first
(`realign-spec` on that one feature — land-branch's forget-net if they
are still landing) and then re-run `/cut-release`. `SHELL`/`BILLING`
wait with the rest of the cohort.

**IF no blockers:** draft the changelog from the **cohort** (and
**already** amends). Quote live requirement prose from `requirements.md`,
optionally parenthetical CODE. Group leftover commit subjects under
**Misc**. Do **not** require or parse `Implements:` / `Guards:` trailers.

**Done when:** either the stop list is in front of the user, or a draft
changelog of the cohort exists and has been shown.

## c. Propose the version bump

Reason from the changelog in semver terms: removed/changed public behavior → major; new requirements shipped → minor; only fixes and guards → patch. State the reasoning and the proposed version. **The user approves the number** — do not proceed on silence.

**Done when:** the user has approved an exact version string.

## d. Update version files and changelog

Write the approved version into the project's version files (manifest, lockfile if the ecosystem requires it, any hardcoded version constants) and prepend the changelog entry to the changelog file (create `CHANGELOG.md` if the repo has none). Commit these together.

**Done when:** the cut-release commit exists and `git status` is clean.

## e. Build

Execute the ordered release steps from `docs/agents/project.md` exactly. Do not improvise flags or substitute commands; an unclear step is a failing step under the stop rule.

**Optional deployment narrative:** follow
`skills/project/define-system-doc/consult-recipe.md` for
`docs/ops/deployment.md` — **narrative only**. It MUST NOT replace or override
executable release commands in `docs/agents/project.md`. Suggest once if material;
never auto-invoke.

**Done when:** every release step has run successfully and the artifact(s) exist.

## f. Smoke-check the artifact

Exercise the built artifact, not the source tree: run the project's smoke command if one is configured; otherwise walk a short manual checklist with the user (install/launch the artifact, touch the core flow) and get their explicit confirmation.

**Done when:** the smoke command passed, or the user has confirmed the checklist.

## g. Tag and push

Only after explicit user approval (this approval **is** the successful terminal verdict for the cut-release):

1. REQUIRED SUB-SKILL: use `record-verdict` with verdict `release-approve`, `Boundary-Type: release`, Accountable depth inputs, and evidence lines folding version / build / smoke / tag approvals (one record for the whole cut-release — never separate records per intermediate approval). Publish **before** creating the tag.
2. On publication failure: do **not** create or push the tag; report the verdict was not enacted.
3. On success: create the tag (`git tag <version>`), push the cut-release commit and tag, then append to the record envelope:
   `Execution-Outcome: tag <ref-name>@<object-id> pushed <UTC>`.

**Done when:** the tag exists on the remote and the cut-release decision record cites it (or the cut-release was explicitly rejected/stopped without a tag).

## h. Draft release notes

Turn the changelog entry into release notes in the tracker's format (for example `gh cut-release create --draft`, or a notes file for manual publishing). Keep the requirement-grouped structure. Leave the cut-release as a draft for the user unless they ask you to publish.

**Done when:** the draft notes exist and their URL or path has been stated to the user.

## i. Flip spec status

The **cohort** is the Implemented list recorded at step b — same set, no
re-discovery. For each cohort feature, write `Status: Shipped` on that
`requirements.md` and the matching `docs/specs/INDEX.md` row. One commit.

Do **not** invoke `realign-spec`. This skill owns `Implemented → Shipped`
for the cohort. `realign-spec` realigns one drifted triad; it does not
stamp a release.

"Always run realign-spec so we cannot forget", "skip the spec paperwork",
"nobody reads INDEX", and "the tag is the real work" are **not** skips of
this step and are **not** a reason to hand the flip to `realign-spec`.

**Done when:** every cohort feature is `Shipped` in the file and INDEX
(or step b already stopped the cut).

## Red flags — never

- Tag while any range-set feature is `Approved`, `Draft`, or missing `Status:`
- Invoke `realign-spec` from this skill
- Flip a blocker (`Approved`/`Draft`) to `Shipped`
- Skip step i because the tag exists or a lead said status can wait
- Claim Approved work in the changelog as shipped behavior

| Thought | Reality |
|---|---|
| "AUTH is only Approved — I'll realign it as step i after the tag" | Too late. Code is in the tag. Step b stops *before* version/tag. |
| "Code is already on main, so they all shipped" | On-main is land. This skill tags a cohort of `Implemented` specs. |
| "REQUIRED SUB-SKILL realign-spec is how we flip Shipped" | Not anymore. Step i is a Status/INDEX edit. `realign-spec` is one-feature anti-rot. |
| "Always run realign-spec so we cannot forget" | Same shape as always-polish. Clean Implemented cohort → mechanical flip. |
| "Skip the spec paperwork / nobody reads INDEX / we're done" | Step i is a gate. The tag is not the end of the sequence. |
| "Standup in five — just cut, flip everything" | Time and a lead do not create a skip of step b's blocker list. |
| "Flip AUTH Approved → Shipped; the cut is the evidence" | `Shipped` requires `Implemented` first. Blocker stays a blocker. |
