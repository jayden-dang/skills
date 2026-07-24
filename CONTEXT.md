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

## Relationships

- A **spec triad** defines one feature and owns many **requirement IDs**
- A **requirement ID** is covered by ≥1 test that cites it and passed
- **Workflow band** is derived from the **Team** roster (or an explicit override)
- The **architecture spine** is the invariant subset of the **architecture SSOT**
- A **sample set** and its **residue** partition a range's **sampling units**
- The **binding pass** admits **sampling units** into the **sample set**

## Flagged ambiguities

- *(none yet)*
