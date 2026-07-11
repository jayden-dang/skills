# `release`

> Prepare and cut a release as a strict sequence of gates: any step that fails means STOP, and the repo is left un-released.

|  |  |
|---|---|
| **Bucket** | ship |
| **Invocation** | user-invoked only (`disable-model-invocation: true`) — run it as `/release` |
| **Reads** | `docs/agents/project.md` (verify commands, release steps, smoke command), `docs/specs/` (requirement text), git tags and log |
| **Writes** | version files, `CHANGELOG.md`, the release commit, the git tag, draft release notes |
| **Calls** | [`sync-spec`](sync-spec.md) (final step, to flip spec status) |
| **Called by** | no skill — it is user-invoked and may never be auto-invoked |

## When it fires

Only when the user runs `/release` to cut a release for work already merged to the release branch: publish a version, bump semver, tag the repo, and draft the changelog and release notes. Because it carries `disable-model-invocation: true`, no skill body may invoke it — a hand-off reaches it only by naming `/release` for the user to run. It is distinct from [`finish-branch`](finish-branch.md), which only integrates a branch.

The whole skill is one strict sequence of gates. It is not a menu of independent actions the agent picks from; it is a pipeline where each gate proves something before the next may run, and any failure stops the pipeline dead.

## Why it is user-invoked

Alone among the ship-bucket skills, `release` carries `disable-model-invocation: true`. That flag is load-bearing, not decorative: it means no skill body may auto-invoke it, and the agent may not reach for it on its own. A hand-off arrives here only by naming `/release` for the user to run — the same way [`handoff`](handoff.md) is reached — never through a `REQUIRED SUB-SKILL` directive, which is reserved for model-invocable targets. If another skill's body tried to invoke `release`, that would be a dead-end hand-off and a real bug. The practical effect is that a release only ever happens because a human asked for one.

## The stop rule

Any step that fails means STOP — report exactly what failed and what remains, and leave the repo un-released. There are no partial releases:

- No tag without a passing build.
- No release notes for artifacts that do not exist.
- No "we'll fix it after tagging."

Two of the gates additionally require the user's explicit word before the skill may move: the version number at gate c, and the tag push at gate g. The skill never proceeds on silence at either. Before any of this, it reads the repo's commands from `docs/agents/project.md` (verify commands, release steps, smoke command); if that file is missing it says so, suggests [`setup-repo`](setup-repo.md), and asks the user for the commands before proceeding.

## The nine gates

The skill creates one todo per step and works them in order. No gate begins until the one before it is done.

### a. Verify gate

Run every verify command in order — typecheck, lint, unit, e2e — plus the trace check (`check_trace.py`). All must pass **clean**, not merely green: an implemented requirement with no covering test is an untraced requirement, and untraced requirements block a release. Prior green runs do not count; everything runs fresh, now, and the skill reads the output of each command. This is the same gate [`finish-branch`](finish-branch.md) enforces before a branch may merge, applied here to the release branch as a whole. **Done when:** every command has a fresh passing run whose output you have read.

### b. Assemble the changelog

Find the last tag with `git describe --tags --abbrev=0`, collect `git log <last-tag>..HEAD`, and group the commits by their `Implements: CODE-N.M` and `Guards: CODE-N.M` trailers. For each cited ID, look up its requirement text in `docs/specs/` so the entry reads as shipped behavior — "Module selection persists across launches — SHELL-1.2" — rather than as commit prose. Guards become a "Protected behavior" grouping, and commits carrying no trailer go under a **Misc** section as-is. If there is no prior tag, the range is the whole history, and the skill says so. **Done when:** a draft changelog, organized by requirement, is shown to the user.

### c. Propose the version bump

Reason from the changelog in semver terms: removed or changed public behavior is a major bump, new requirements shipped is a minor, only fixes and guards is a patch. The skill states the reasoning and the proposed version, and the user approves the number — it does not proceed on silence. **Done when:** the user has approved an exact version string.

### d. Update version files and changelog

Write the approved version into the project's version files — manifest, lockfile where the ecosystem requires it, any hardcoded version constants — and prepend the changelog entry to the changelog file, creating `CHANGELOG.md` if the repo has none. Commit these together. **Done when:** the release commit exists and `git status` is clean.

### e. Build

Execute the ordered release steps from `docs/agents/project.md` exactly, improvising no flags and substituting no commands. If a step is unclear or fails, the skill stops and reports; it does not guess its way past a broken build. **Done when:** every release step has run and the artifact(s) exist.

### f. Smoke-check the artifact

Exercise the built artifact, not the source tree — the source can be green while the packaged artifact is broken. Run the project's smoke command if one is configured, or otherwise walk a short manual checklist with the user (install or launch the artifact, touch the core flow) and get their explicit confirmation. **Done when:** the smoke command passed, or the user confirmed the checklist.

### g. Tag and push

Create the tag (`git tag <version>`) and push the release commit and tag only after explicit user approval. The skill never pushes a tag on its own initiative — a tag on the remote is a public fact that cannot be quietly withdrawn. **Done when:** the tag exists on the remote.

### h. Draft release notes

Turn the changelog entry into release notes in the tracker's format — for example `gh release create --draft`, or a notes file for manual publishing — keeping the requirement-grouped structure. Leave the release a DRAFT unless the user asks to publish. **Done when:** the draft notes exist and the user knows where.

### i. Flip spec status

Hand off to [`sync-spec`](sync-spec.md) to move the shipped features' requirements to `Status: Shipped` and update `docs/specs/INDEX.md`. **Done when:** sync-spec's closing trace report is clean.

## Worked example

The user runs `/release` on a repo whose last tag was `v1.3.0`. Since that tag, four commits landed on the release branch: three carrying `Implements:` or `Guards:` trailers for the `SHELL` feature, and one untrailered chore.

Gate a passes clean — typecheck, lint, unit, e2e, and `check_trace.py` all fresh, no untraced `SHELL` requirements. Gate b collects `git log v1.3.0..HEAD`, reads the requirement-ID trailers, and resolves each ID to its text in `docs/specs/`, producing this draft:

```markdown
## Unreleased

### Features
- Module selection persists across launches — SHELL-1.2
- Modules can be reordered by drag — SHELL-2.1
- Keyboard shortcut cycles the active module — SHELL-2.4

### Protected behavior
- Persisted module survives a corrupt store file — SHELL-1.2 (Guards)

### Misc
- chore: bump CI runner image to node 20
```

The `Features` entries came from `Implements:` trailers, the `Protected behavior` line from a `Guards:` trailer, and the untrailered chore commit fell through to `Misc`. None of these came from reading commit subjects — the trailers pointed at requirement IDs, and the IDs pointed at the requirement text in `docs/specs/`.

At gate c the skill reasons in semver terms: new requirements shipped, no public behavior removed or changed, so this is a minor bump — proposed `v1.4.0`, with the reasoning stated. The user approves the exact string. Gate d writes `v1.4.0` into the manifest and prepends the entry to `CHANGELOG.md` in a single commit, leaving `git status` clean.

Gate e runs the project's ordered build steps from `docs/agents/project.md` verbatim, and gate f launches the built artifact to touch the module-switch flow rather than trusting the green source. After the user gives explicit approval, gate g tags `v1.4.0` and pushes the commit and tag. Gate h drafts `gh release create --draft` notes in the same requirement-grouped shape and leaves them as a draft, and gate i runs [`sync-spec`](sync-spec.md) to flip the `SHELL` requirements to `Status: Shipped` and update `docs/specs/INDEX.md`.

Had gate e's build failed instead, the stop rule would apply: report the failing step and what remains, leave `v1.4.0` untagged, and cut nothing — no tag without a passing build. The `CHANGELOG.md` commit from gate d would already exist, but no version would be published against it until a clean build is produced and the user re-approves the push.

## Why it is written the way it is

`release` is user-invoked by design. Cutting a version is irreversible in practice — a pushed tag and published notes are public facts — so the set forbids any skill from auto-invoking it and requires the user to type `/release`. The nine gates are ordered so that no artifact of the release exists until the thing it describes is proven: the changelog is assembled before the version is chosen, the build runs before the tag, the smoke check runs against the artifact rather than the source, and the tag is pushed only on explicit approval.

The requirement-grouped changelog is the direct dividend of the trace spine that [`tdd`](tdd.md) and [`check-trace`](../resources/scripts.md#check-trace) maintain across the whole methodology. Because every commit carries the ID of the requirement it implements or guards, and every ID resolves to requirement text in `docs/specs/`, the release notes can be assembled at the level of shipped behavior for free — no one has to hand-write them from commit prose. Gate a's insistence that the trace check be clean is what keeps that dividend honest: a release cannot ship an implemented requirement that has no covering test.

## Distinct from `finish-branch`

The two ship-bucket skills are easy to confuse and do different jobs. [`finish-branch`](finish-branch.md) integrates a single feature branch — it decides between merge, PR, keep, and discard — and it is model-invocable, running as the last step of [`execute-plan`](execute-plan.md). `release` operates on work already merged to the release branch and turns it into a published version. They share exactly one thing: the verify-plus-trace gate. Everything downstream — the changelog, the version bump, the build, the tag, the notes — belongs to `release` alone.

## What a finished release leaves behind

When the sequence completes cleanly, the repo carries a consistent set of artifacts, each produced by a specific gate:

- A release commit bumping the version files and prepending the changelog entry (gate d).
- A pushed git tag naming the version (gate g).
- Draft release notes in the tracker, requirement-grouped (gate h).
- The shipped requirements moved to `Status: Shipped` in `docs/specs/`, with `INDEX.md` updated (gate i).

If any gate stopped the sequence, only the artifacts of the gates that ran exist, and the version is not considered published. That is the whole point of the stop rule: the set of artifacts is always internally consistent, never a tag pointing at an unbuilt version or notes describing an artifact that was never produced.

Nothing here is invented by the skill on the fly — the build steps, verify commands, and smoke command all come from `docs/agents/project.md`, and the changelog and notes are assembled from trailers the commits already carry.

## See also

- [The gates](../concepts/gates.md) — how the verify gate here matches the one [`finish-branch`](finish-branch.md) enforces
- [Traceability](../concepts/traceability.md) — why the changelog reads in requirement text, and why untraced work blocks the cut
- [`finish-branch`](finish-branch.md) — integrates a branch; `release` cuts the version afterward
- [`sync-spec`](sync-spec.md) — the final gate that flips shipped requirements to `Status: Shipped`
