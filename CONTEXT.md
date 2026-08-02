# Skills

An A-to-Z agentic development skill set: one system that carries a project from
ideation to release, with requirements traceability as the spine.

## Language

**Requirement ID**:
A first-class object of the form `CODE-N.M` that lives in the spec triad
(requirements, design `Satisfies:`, task `_Requirements:` footers) and optional
issue bodies. Immutable once approved. Not required in application source, tests,
or commit messages (docs-only spine).
_Avoid_: informal labels that only appear in one artifact; embedding IDs in
production code for "traceability"

**Spec triad**:
The three files that define a feature before implementation: `requirements.md`,
`design.md`, and `tasks.md` under `docs/specs/<feature>/`.

**Ceremony tier**:
How much process a change needs — 0 (trivial), 1 (bugfix/small), or 2 (feature).
Decided by `frame-change` or `amend-feature`, never silently by the agent.

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
The sampling units admitted for human attention by `select-review-sample` — binding
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
`plan-milestones` and recorded verbatim in that milestone's `Closed:` slot.
_Avoid_: HEAD, "latest", a branch name

**PR package**:
The three-file write-handoff `package-change` writes and `land-branch` submits:
`manifest.md` (title, base/head refs and SHAs, ticket linkage, commits, findings,
digest), `title.txt` (the title alone), and `body.md` (reviewer-facing prose only).
_Avoid_: PR draft, PR template, description file

**Advisory commit map**:
The written regrouping `package-change` proposes for commits that already exist —
groups, order, subjects, bodies, rationale, trailers to preserve — carrying no
runnable rewrite command, because existing commits are never rewritten.
_Avoid_: rebase plan, squash plan, cleanup script

**Run file**:
The single JSON artifact holding one review-product-flow run — every case's authored slots
plus its **case verdict** and **human tick** — at `.skills/<slug>-review-product-flow.json`.
_Avoid_: cases file, run ledger, catalog (all named separate artifacts before v2)

**Case verdict**:
A review-product-flow case's `pending` / `pass` / `fail` / `blocked` state, where `pass`
requires quoted screen evidence **and** a server probe. Written only by the agent.
_Avoid_: bare "verdict" in prose — that name also carries the two-axis
`inspect-change` verdict and the agent verdict inside a **milestone assessment**

**Human tick**:
A person's mark on a review-product-flow case, stored beside the **case verdict** and readable
by the agent, but never proof and never promotable to `pass`.
_Avoid_: manual pass, human verdict, checkbox state

**Vet report**:
The markdown artifact at `.skills/<slug>-vet-product-flow.md` produced by
`vet-product-flow`: open missing-situation findings, severity, code evidence,
authored-cases fingerprint, and re-check stamp. Freshness for dogfood is
fingerprint match, not whole-file `rev`.
_Avoid_: audit report, completeness certificate, “ready to ship” stamp

**Missing-situation finding**:
A code-grounded claim that the shipped product already exposes a user-observable
path or state the run file never exercises, identified as `VPF-N` (integer; not
a requirement id `VPF-N.M`).
_Avoid_: test failure, product defect, speculative “users will want”

**Cases fingerprint**:
SHA-256 of the run file’s authored case slots only (sections + eight slots per
case), excluding `run`, `human`, and top-level `rev`. Used to decide whether a
**vet report** is still fresh after ticks or verdict marks.
_Avoid_: file mtime, whole-file hash, `rev` alone

**Feature subgraph (derivation)**:
A bounded multi-hop view of existing feature IDs (CODE, ROAD, MILE, ARCH, paths)
computed at ask time by deterministic passes over SSOT (`**Files:**`, INDEX,
roadmap, `Respects:`) — not a written graph file.
_Avoid_: feature graph artifact, GRAPH.md, materialized edge store

**OWNS / OVERLAPS edge**:
Derived relations — feature CODE owns path tokens from task `**Files:**`; two
features OVERLAP when their normalized OWNS sets intersect after denoising.
Advisory for neighbor search; never a hard gate.
_Avoid_: hand-maintained ownership matrix as SSOT; boolean “shares src/” without denoising

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
- A **run file** holds many cases, each carrying exactly one **case verdict** and at most one **human tick**
- A **human tick** never becomes a **case verdict**, in either direction, by any code path
- A **vet report** is fresh for a **run file** only when its **cases fingerprint** matches the authored slots on disk
- A **missing-situation finding** lives in a **vet report** and blocks dogfood until cleared or named-overridden
- A **feature subgraph (derivation)** is computed from SSOT; it never defines requirement IDs
- **OWNS / OVERLAPS** edges feed advisory neighbor queries; they do not replace the vertical audit-trace spine

## Flagged ambiguities

- *(none yet)*
