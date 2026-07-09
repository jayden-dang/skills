---
name: release
description: Use when the user wants to cut a release — publish a version, bump semver,
  tag the repo, and draft the changelog and release notes — for work already
  merged to the release branch. Distinct from finish-branch, which only
  integrates a branch.
disable-model-invocation: true
---

# Release

Prepare and cut a release as a strict sequence of gates. Create one todo per step below and work them in order.

**The stop rule:** any step that fails means STOP — report exactly what failed and what remains, and leave the repo un-released. There are no partial releases: no tag without a passing build, no notes for artifacts that do not exist, no "we'll fix it after tagging."

Read the repo's commands from `docs/agents/project.md` (verify commands, release steps, smoke command). If it is missing, say so, suggest `setup-repo`, and ask the user for the commands before proceeding.

## a. Verify gate

Run every verify command in order — typecheck, lint, unit, e2e — plus the trace check (`check-trace.mjs`). All must pass fresh, now; prior green runs do not count. The trace check must be **clean**: an implemented requirement with no covering test is an untraced requirement, and untraced requirements block a release.

**Done when:** every command has a fresh passing run you have read the output of.

## b. Assemble the changelog

Find the last release tag (`git describe --tags --abbrev=0`) and collect `git log <last-tag>..HEAD`. Group commits by their requirement-ID trailers (`Implements: CODE-N.M`, `Guards: CODE-N.M`): for each cited ID, look up its requirement text in `docs/specs/` so the entry reads as shipped behavior ("Module selection persists across launches — SHELL-1.2"), not as commit prose. Guards become a "Protected behavior" grouping. Commits with no trailer go under a **Misc** section as-is.

If there is no prior tag, the range is the whole history; say so.

**Done when:** a draft changelog exists, organized by requirement, shown to the user.

## c. Propose the version bump

Reason from the changelog in semver terms: removed/changed public behavior → major; new requirements shipped → minor; only fixes and guards → patch. State the reasoning and the proposed version. **The user approves the number** — do not proceed on silence.

**Done when:** the user has approved an exact version string.

## d. Update version files and changelog

Write the approved version into the project's version files (manifest, lockfile if the ecosystem requires it, any hardcoded version constants) and prepend the changelog entry to the changelog file (create `CHANGELOG.md` if the repo has none). Commit these together.

**Done when:** the release commit exists and `git status` is clean.

## e. Build

Execute the ordered release steps from `docs/agents/project.md` exactly. Do not improvise flags or substitute commands; if a step is unclear or fails, stop and report.

**Done when:** every release step has run successfully and the artifact(s) exist.

## f. Smoke-check the artifact

Exercise the built artifact, not the source tree: run the project's smoke command if one is configured; otherwise walk a short manual checklist with the user (install/launch the artifact, touch the core flow) and get their explicit confirmation.

**Done when:** the smoke command passed, or the user has confirmed the checklist.

## g. Tag and push

Only after explicit user approval: create the tag (`git tag <version>`) and push the release commit and tag. Never push a tag on your own initiative.

**Done when:** the tag exists on the remote.

## h. Draft release notes

Turn the changelog entry into release notes in the tracker's format (for example `gh release create --draft`, or a notes file for manual publishing). Keep the requirement-grouped structure. Leave the release as a draft for the user unless they ask you to publish.

**Done when:** the draft notes exist and the user knows where.

## i. Flip spec status

REQUIRED SUB-SKILL: use `sync-spec` to move the shipped features' requirements to `Status: Shipped` and update `docs/specs/INDEX.md`.

**Done when:** sync-spec's closing trace report is clean.
