# Skills

An A-to-Z agentic development skill set: one system that carries a project from
ideation to release, with requirements traceability as the spine.

## Language

**Requirement ID**:
A first-class runtime object of the form `CODE-N.M` that flows from requirements
through design, tasks, tests, commits, and changelog. Immutable once approved.
_Avoid_: informal labels that only appear in one artifact

**Spec triad**:
The three files that define a feature before implementation: `requirements.md`,
`design.md`, and `tasks.md` under `docs/specs/<feature>/`.

**Ceremony tier**:
How much process a change needs — 0 (trivial), 1 (bugfix/small), or 2 (feature).
Decided by `brainstorm` or `amend`, never silently by the agent.

**Workflow band**:
Solo / Small / Multi packaging derived from the Team roster in
`docs/agents/project.md`. Affects collaboration packaging only, never Iron Law gates.

**Architecture spine**:
The greppable ARCH-N invariants in `docs/architecture/INDEX.md`. Feature designs
cite them as `Respects: ARCH-N`. Not a diagram doc.
_Avoid_: informal "architecture notes" outside `docs/architecture/`

**Architecture SSOT**:
`docs/architecture/` as a whole — INDEX (invariants) plus domain files (system,
artifacts, skills, workflows). Product intent stays in `docs/product/`.
_Avoid_: a second top-level design narrative (former repo-root DESIGN.md)

**Sampling unit**:
The atom of attention allocation: a depth-2 repo-relative path prefix
(`skills/execution`). Every file changed in a range belongs to exactly one.
_Avoid_: "chunk", "area", or per-file/per-commit grouping

**Sample set**:
The sampling units admitted for human attention by `allocate-attention` — binding
signal hits, agent adds, user adds, and the floor pick. Complement of the
**residue**.

**Residue**:
The sampling units of a range that no human looked at, carried as a first-class
output and labelled *agent verdicts only*.
_Avoid_: calling it reviewed, cleared, approved, or safe

**Binding pass**:
The fixed `git`/`grep` pass that decides sample membership with no model
judgment, so the same range and repo state always admit the same units.
_Avoid_: describing sample membership as a ranking or a score

**Milestone assessment**:
One append-only judgment event on a milestone, held in
`docs/roadmap/assessments/<MILE-N>.md`: an agent-authored verdict on the
outcome, plus the human disposition of it. A further assessment is appended only
when the requested closing revision or material evidence changes.
_Avoid_: retrospective (the team ceremony), milestone review

**Human disposition**:
The explicit human act on an agent assessment — `Accepted`, `Overridden`,
`Deferred`, or `Pending` until one arrives — recorded separately from the
agent's verdict and never inferred from silence. Only the first two are terminal;
acceptance proves adoption, not authorship.
_Avoid_: approval, sign-off, treating agent reasoning as human-authored

**Close eligibility**:
The two-part condition for closing a milestone: non-overridable mechanical
eligibility (same `MILE-N`, same candidate closing revision, resolved bindings),
**and** a **human disposition** whose effective verdict permits the close.
_Avoid_: "ready to close" as a single agent-computed boolean

**Candidate closing revision**:
The immutable commit a **milestone assessment** is resolved against, handed to
`write-roadmap` and recorded verbatim in that milestone's `Closed:` slot.
_Avoid_: HEAD, "latest", a branch name

**PR package**:
The two-file handoff `prepare-change` writes and `finish-branch` submits:
`manifest.md` (title, base/head refs and SHAs, ticket linkage, commits, findings,
content digest) plus `body.md` (reviewer-facing prose only).
_Avoid_: PR draft, PR template, description file

**Advisory commit map**:
The written regrouping `prepare-change` proposes for commits that already exist —
groups, order, subjects, bodies, rationale, trailers to preserve — carrying no
runnable rewrite command, because existing commits are never rewritten.
_Avoid_: rebase plan, squash plan, cleanup script

## Relationships

- A **spec triad** defines one feature and owns many **requirement IDs**
- A **requirement ID** is covered by ≥1 test that cites it and passed
- **Workflow band** is derived from the **Team** roster (or an explicit override)
- The **architecture spine** is the invariant subset of the **architecture SSOT**
- A **sample set** and its **residue** partition a range's **sampling units**
- The **binding pass** admits **sampling units** into the **sample set**
- A **milestone assessment** pairs one agent verdict with one **human disposition**
- **Close eligibility** needs mechanical eligibility *and* a permitting **human disposition**
- A **milestone assessment** resolves against exactly one **candidate closing revision**
- A **PR package** is authored against exactly one base/head pair and is invalidated when either moves
- An **advisory commit map** describes commits a **PR package** still reports as they actually are

## Flagged ambiguities

- *(none yet)*
