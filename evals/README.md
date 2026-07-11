# Skill evals

Automated checks on the skill set itself — the thing `writing-skills` needs to
close its TDD loop, and the thing CI needs to stop a broken skill from merging.
Two tiers, both free to run (no model calls, no network), Python 3.9+ stdlib
only — the same runtime the linters in `scripts/` already require.

```bash
./evals/run-evals.sh            # both tiers
./evals/run-evals.sh --tier 1   # structural only
./evals/run-evals.sh --tier 2   # routing only
./evals/run-evals.sh --json     # machine-readable summary
./evals/run-evals.sh --strict   # Tier-2 misses also fail the exit code
```

Exit code is non-zero when any **Tier-1** check fails (always) or any **Tier-2**
check fails (only under `--strict`) — so the default run is safe to gate merges
on, and `--strict` is available once the routing cases are trusted.

## Tier 1 — structural (hard)

Validates every `skills/<category>/<name>/SKILL.md` against the invariants the
whole system leans on. A violation is a bug and fails the run:

- frontmatter present and parseable, keys limited to `name`, `description`,
  `disable-model-invocation`
- `name` matches its directory and is kebab-case
- `description` states a triggering condition (starts with `Use`) — never a
  workflow summary, which would tempt an agent to follow the summary and skip
  the skill body
- `disable-model-invocation`, when present, is exactly `true` (the user-invoked
  marker)
- category is one of the nine buckets, and every bucket has at least one skill
- body stays under the 500-line budget (progressive disclosure)

## Tier 2 — routing (advisory by default)

A **lexical approximation** of skill selection. It is not a model; it ranks each
seeded prompt against every skill's description by idf-weighted keyword overlap
and checks:

- **positive** prompts — the intended skill ranks in the top 3
- **negative** prompts — the intended skill does *not* rank first

This deliberately catches the two failure modes that dominate real trigger bugs:
a description missing the vocabulary users actually say (false negative), and an
over-broad description that outranks the right skill (false positive). It will
not catch subtle semantic routing errors — that is Tier 3's job (a behavioral
eval that drives a real agent and judges compliance; not yet implemented here).

Cases live in [`triggers.json`](./triggers.json). Add a skill's real user
phrasings under `positive`, and prompts that belong to a *different* skill under
`negative`. Metadata keys start with `_` and are ignored.

## Adding cases when you write or change a skill

`writing-skills` should treat a red Tier-1 check as a failing test to fix before
the skill ships. When a skill's triggering conditions change, update its
`triggers.json` cases in the same commit and re-run `--strict`: if the intended
skill stops ranking, the description lost vocabulary users depend on.

## CI

Wire the default run into the pipeline beside the linters:

```yaml
- run: python3 evals/evals.py            # Tier 1 gates the merge
- run: python3 evals/evals.py --tier 2   # Tier 2 reports (drop --strict to keep advisory)
```
