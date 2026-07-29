# prepare-change — scenario coverage (PCHG)

Greppable requirement IDs for the `trace` coverage pass. These scenarios are the
annotation layer for skill-pressure and contract checks; they are not a Python
unittest runner. Each section below corresponds to one story in
`docs/specs/2026-07-28-prepare-change/requirements.md`; later tasks append that
story's IDs under its heading as they implement it.

## 1. Commit the working tree as a reviewer-readable set

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
  base and name `/setup-repo`
- PCHG-2.9 resolved base memoized for the session and recorded in the PR package
- PCHG-2.10 configured default no longer resolves to a live branch — ask again for
  this invocation

## 3. Explain the change from real evidence, or say less

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

## 6. Hand over one exact, self-describing package

## 7. Report what it could not repair

## 8. Approve the exact content at the crossing

## 9. Continue automatically from an executed plan

## 10. Configure the default PR base once

## 11. Preserved behavior of the skills this feature edits

- PCHG-11.13 skill exists, is model-invoked, and is registered in both plugin
  manifests, `AGENTS.md`, and `README.md`

## 12. Quality attributes

- PCHG-12.1 convention resolution runs at most once per session and reads no
  historical commit body or historical diff during it
