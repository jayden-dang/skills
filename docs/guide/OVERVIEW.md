# Navigation

Three ways in: by role, by problem, or by phase.

---

## By role

### I'm adopting this on my team's repo

1. [When to use it](methodology/when-to-use.md) — and when not to
2. [Overview](methodology/overview.md) — what the system is, in one page
3. [Ceremony tiers](methodology/ceremony-tiers.md) — how it scales down for small work
4. [Adopting the skill set](resources/adopting.md) — install, `/setup-repo`, and the incremental path
5. [Tier 2: a feature, end to end](examples/tier-2-feature.md) — see it run

### I'm a teammate being handed this

1. [Overview](methodology/overview.md)
2. [Ceremony tiers](methodology/ceremony-tiers.md) — this answers "do I really have to write a spec for *this*?"
3. [The process](process/README.md) — the chain, and which flow your work belongs in
4. [Examples](examples/tier-0-tweak.md) — start with tier 0; it is the shortest
5. When lost: run `/ask`, or read [`ask`](skills/ask.md)

### I maintain this skill set

1. [Philosophy](methodology/philosophy.md) — the six principles and what enforces each
2. [The skill model](concepts/skill-model.md) — invocation kinds, the description rule, the authoring vocabulary
3. [`writing-skills`](skills/writing-skills.md) — the Iron Law, and the deployment checklist
4. [Enforcement and tooling](resources/scripts.md) — the `trace` skill and the session hook
5. [`DESIGN.md`](../../DESIGN.md) — the architecture spec of record

### I'm evaluating this from the outside

1. [Overview](methodology/overview.md) — the problem, and the shape of the answer
2. [Traceability](concepts/traceability.md) — the idea everything else hangs off
3. [Tier 2: a feature, end to end](examples/tier-2-feature.md) — the whole system in one story
4. [When to use it](methodology/when-to-use.md) — the honest boundaries

---

## By problem

| I want to… | Go here |
|---|---|
| …add a new feature | [`brainstorm`](skills/brainstorm.md) → [Discovery](process/discovery.md) |
| …tweak something that already shipped | [`amend`](skills/amend.md) → [Tier 0 example](examples/tier-0-tweak.md) |
| …fix a bug | [`debug`](skills/debug.md) → [Tier 1 example](examples/tier-1-bugfix.md) |
| …start a brand-new project | [`/scaffold-project`](skills/scaffold-project.md) |
| …adopt this on an existing repo | [`/setup-repo`](skills/setup-repo.md) → [Adopting](resources/adopting.md) |
| …understand why my tests aren't enough | [`acceptance-check`](skills/acceptance-check.md) → [Review and acceptance](process/review-and-acceptance.md) |
| …know why the trace check is failing | [Troubleshooting](resources/troubleshooting.md#the-trace-check-fails) |
| …review a branch before merging | [`code-review`](skills/code-review.md) |
| …respond to review feedback | [`receive-review`](skills/receive-review.md) |
| …cut a release | [`/release`](skills/release.md) |
| …handle an incoming issue | [`/triage`](skills/triage.md) |
| …find where to refactor next | [`/improve-architecture`](skills/improve-architecture.md) |
| …hand off before my context fills | [`/handoff`](skills/handoff.md) |
| …fix a spec that drifted from the code | [`sync-spec`](skills/sync-spec.md) |
| …write a new skill | [`writing-skills`](skills/writing-skills.md) → [The skill model](concepts/skill-model.md) |
| …understand the requirement-ID syntax | [Requirement IDs](concepts/requirement-ids.md) + [EARS](resources/ears.md) |
| …know which flow I'm even in | Run `/ask` |

---

## By phase

| Phase | Skills | Guide page |
|---|---|---|
| **0. Setup** | `/setup-repo`, `/scaffold-project` | [Adopting](resources/adopting.md) |
| **1. Discovery** | `brainstorm`, `grilling`, `research`, `prototype`, `domain-modeling` | [Discovery](process/discovery.md) |
| **2. Specification** | `write-requirements`, `write-design`, `write-plan` | [Specification](process/specification.md) |
| **3. Execution** | `worktrees`, `execute-plan`, `tdd`, `debug`, `verify`, `trace` | [Execution](process/execution.md) |
| **4. Review & acceptance** | `code-review`, `receive-review`, `acceptance-*`, `dogfood` | [Review and acceptance](process/review-and-acceptance.md) |
| **5. Ship & maintain** | `finish-branch`, `/release`, `sync-spec`, `amend`, `/triage`, `/improve-architecture`, `/handoff` | [Ship and maintain](process/ship-and-maintain.md) |

---

## Every page

### Methodology — the ideas
- [Overview](methodology/overview.md) — what this is and what it defends against
- [Philosophy](methodology/philosophy.md) — six principles, and what enforces each
- [When to use it](methodology/when-to-use.md) — boundaries, entry points, context hygiene
- [Ceremony tiers](methodology/ceremony-tiers.md) — tier 0, 1, 2, and what never scales down

### Concepts — the mechanics
- [Traceability](concepts/traceability.md) — the spine
- [Requirement IDs](concepts/requirement-ids.md) — grammar, immutability, status lifecycle
- [The artifact model](concepts/artifacts.md) — every file the system produces
- [The gates](concepts/gates.md) — the four Iron Laws
- [The skill model](concepts/skill-model.md) — how skills are built and how they compose
- [Feature overlap](concepts/feature-graph.md) — the horizontal layer: searching `docs/specs/` for neighbors

### Process — the chain
- [The process](process/README.md) — all three flows, with diagrams
- [Phase 1 — Discovery](process/discovery.md)
- [Phase 2 — Specification](process/specification.md)
- [Phase 3 — Execution](process/execution.md)
- [Phase 4 — Review and acceptance](process/review-and-acceptance.md)
- [Phase 5 — Ship and maintain](process/ship-and-maintain.md)

### Skills — one page each
- [Skill reference](skills/README.md) — all 32, indexed

### Examples
- [Tier 0: a tweak](examples/tier-0-tweak.md)
- [Tier 1: a bugfix](examples/tier-1-bugfix.md)
- [Tier 2: a feature, end to end](examples/tier-2-feature.md)

### Resources
- [Adopting the skill set](resources/adopting.md)
- [Enforcement and tooling](resources/scripts.md) — the `trace` skill and the session hook
- [Templates](resources/templates.md)
- [EARS reference](resources/ears.md)
- [Troubleshooting](resources/troubleshooting.md)
