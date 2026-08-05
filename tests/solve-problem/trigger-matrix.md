# solve-problem — description trigger matrix

**Protocol:** `author-skills` / `pressure-testing.md` § Testing the description
**Hold-out:** TF-H1, TF-H2, TN-H1, TN-H2 are not used while editing the description;
score them only on the final pass.

Neighbor descriptions used for collision tests (abridged):

| Skill | Description (abridged) |
|---|---|
| `solve-problem` | Use when a symptom, opportunity, requested solution, or “problem” has no trustworthy gap or clear workflow yet — produces an evidence-grounded Problem Brief and routes it to the right discovery, diagnosis, decision, or improvement skill. |
| `root-cause` | Use when anything behaves unexpectedly — failing test, error, exception, crash, reported bug, wrong output, performance regression, flaky CI — before any fix. |
| `frame-change` | Use at the very start of the idea-to-ship chain — add/build/change a feature or new project when no requirements/design/code exist yet. |
| `amend-feature` | Use when an already-shipped, spec'd feature needs a small in-scope change (recolor, copy, tweak). |
| `reroute-plan` | Use when a mid-execution discovery invalidates an already-approved plan. |
| `clarify-decisions` | Use to interview the user to stress-test a plan/design when intent is underspecified. |
| `research` | Use when a design/planning question turns on external facts (library, API, RFC). |
| `run-spike` | Use when a design question needs a runnable answer / mock-up. |
| `inspect-change` | Use when a branch/PR/diff needs review before merging. |
| `specify-behavior` | Use when discovery is complete and requirements need writing. |
| `prove-claim` | Use before saying done/fixed/passing/works. |
| `pathfind` | Chart or advance a multi-session decision map until the route is clear. |

## Should-fire (TF) — expect `solve-problem`

| ID | Query | Why it should fire |
|---|---|---|
| TF1 | something feels off with checkout but tests are green — not sure if it's a bug or a product problem | ambiguous gap + unclear workflow |
| TF2 | the CEO wants us to add Redis because the API is slow | requested solution without demonstrated gap |
| TF3 | we have a problem but I don't know if we should debug or build something new | workflow unclear |
| TF4 | help me frame this problem properly before we start coding | problem intake before delivery |
| TF5 | conversion dropped 12% and nobody has a clear gap analysis | symptom without trustworthy gap model |
| TF6 | is this even a problem? platform lead wants caching | possible no-problem / gap check |
| TF7 | need a problem brief for an opportunity that might not be worth building | opportunity + outcome noun |
| TF8 | ambiguous symptom — root-cause or frame-change? can't tell yet | router competition; solve-problem should win |
| TF9 | ship the AI personalizer? no evidence the copy is the cause | requested solution + missing evidence |
| TF10 | stuck between shipping a fix and investigating — need intake | intake / Problem Brief shape |
| TF-H1 | prod looks weird after three releases; metrics incomplete; what process first? | hold-out; messy phrasing, no skill nouns |
| TF-H2 | “fix the conversion problem” — no stacktrace, no feature request yet | hold-out; casual “fix” without clear path |

## Should-not-fire (TN) — expect neighbor

| ID | Query | Expected |
|---|---|---|
| TN1 | test suite fails with NullPointerException in CheckoutService | `root-cause` |
| TN2 | let's add a dark mode toggle to the settings page | `frame-change` |
| TN3 | recolor the primary button on the already-shipped paywall | `amend-feature` |
| TN4 | the plan is wrong mid build-in-waves, scope changed and this task can't absorb it | `reroute-plan` |
| TN5 | grill me on these design decisions before we build | `clarify-decisions` |
| TN6 | what does the Stripe webhook signature verification API require? | `research` |
| TN7 | spike a state machine for the checkout wizard so we can feel if it holds up | `run-spike` |
| TN8 | review this PR before merge | `inspect-change` |
| TN9 | discovery is done — write requirements.md with EARS criteria | `specify-behavior` |
| TN10 | failing CI after my last commit, error in the logs | `root-cause` |
| TN-H1 | package the branch and open a PR description | hold-out → `package-change` (or ship lane) |
| TN-H2 | prove this is actually fixed before we say done | hold-out → `prove-claim` |

## Scoring

- **Hit:** selected skill matches Expected (or `solve-problem` for TF).
- **Miss:** TF → not `solve-problem` (undertrigger).
- **False fire:** TN → `solve-problem` (overtrigger).
- **Neighbor miss:** TN → wrong non-solve-problem skill (catalog issue; note but not a solve-problem failure unless it also false-fires).
