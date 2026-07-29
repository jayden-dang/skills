# Resolve conventions — commit and PR

Load this file when phase 2 (`Resolve conventions`) runs. SKILL.md owns the
phase list and the Iron Law; this file owns the resolution recipe.

Produce one convention record and hold it in memory for the rest of the
session:

```
{ commit_subject_form, pr_structure, grade }
```

`commit_subject_form` — the resolved shape for every commit subject this
session writes (e.g. a declared format, an inferred pattern, or the
reviewer-centred fallback shape).
`pr_structure` — the resolved shape for the PR body (sections, required
fields) resolved separately from commit conventions.
`grade` — one of `declared` | `machine-enforced` | `inferred`, carried onto
every finding raised against the resolved convention.

<HARD-GATE>
Resolve conventions **at most once per session** and reuse the same
`{ commit_subject_form, pr_structure, grade }` record for every remaining
commit and for the PR body in this session. Never re-resolve mid-session, and
never persist the record beyond the session — no cache file, no write to
`docs/agents/` or anywhere else. The next session resolves fresh.
</HARD-GATE>

## Commit convention: the three-rung ladder

Walk this ladder in order and stop at the first rung that resolves:

1. **machine-enforced artifacts and declared repository documentation** —
   commitlint config, `.gitmessage`, `CONTRIBUTING.md`, or equivalent declared
   guidance. A resolution here is graded `declared` when it comes from
   documentation, or `machine-enforced` when it comes from an executable
   check (e.g. commitlint). Never inspect commit history when this rung
   resolves.
2. only when no declared or machine-enforced commit convention exists —
   sample **at most the 20 most recent non-merge commit subjects** on the
   current branch's history. Never read historical commit bodies or historical
   diffs while resolving conventions — this rung inspects the subject lines of
   the sample and nothing else. A convention resolved from this rung is
   graded `inferred`.
3. **neutral reviewer-centred fallback** — when neither preceding rung
   resolves, use a plain, imperative, reviewer-legible subject shape that
   invents no project-specific format. Grade this rung `declared`: it is the
   skill's own written default, stated here rather than sampled from the
   repository's commit history, so it takes the same non-advisory treatment
   as documentation-derived conventions.

### A mixed sample never widens

If the sampled subjects are mixed (no shared prefix/format/casing
convention) or too few to establish a pattern, fall straight to the neutral
fallback (rung 3). The sample size is fixed at 20 non-merge commit subjects;
a mixed or thin result is **never widened** to a larger sample, an older
window, or a different branch. Widening would trade a bounded, cheap read for
an unbounded one and still might not resolve — the fallback is strictly
cheaper and always resolves.

## PR convention: separate from commit history

Resolve `pr_structure` **only** from a repository **pull-request template**
(e.g. `.github/pull_request_template.md`) and declared project guidance (e.g.
`CONTRIBUTING.md` sections about PR structure).

This resolution is not derived from commit history — commit subjects say
nothing about how a PR body should be organized, and reading history for this
purpose would be reading data that cannot answer the question. When no
template or declared guidance exists, use the reviewer-centred fallback shape
(a short summary, what changed, why) and grade it `declared`: it is the
skill's own written default, not a claim derived from repository history.

## Grading and advisory treatment

| Grade | Source | Treatment of findings raised against it |
|---|---|---|
| `machine-enforced` | An executable check exists (e.g. commitlint) | Reported; route a failed run through the existing `verify` failure path |
| `declared` | Written documentation (`.gitmessage`, `CONTRIBUTING.md`, PR template) **or** the skill's own reviewer-centred fallback shape (commit-ladder rung 3, or the PR-structure fallback when no template or guidance exists) | Reported |
| `inferred` | Rung 2 — sampled from commit history | Labelled **inferred** and any finding raised against it is treated as **advisory** only — never a hard gate |

Where a convention was derived from commit history, label it `inferred` in
the convention record and in any finding raised against it, and treat that
finding as advisory: surface it, never block on it.

## No persistent cache

Nothing resolved here is written to disk. The record lives only in the
session's working memory for the phases and commits that follow. There is no
persistent cache across sessions — the next `prepare-change` invocation
resolves fresh from rung 1.
