# Requirements: Pathfind layer

Feature code: PFIND  
Status: Approved  
Date: 2026-07-31  
Approved: 2026-07-31 (user)  
Design: [`docs/design/pathfind-layer.md`](../../design/pathfind-layer.md) (Approved)

Adds an **optional Layer 0** to the Engineer Pack: a user-invoked skill that charts
and advances a multi-session **decision map** (not implement work) until the route
to a named destination is clear enough to hand off into program docs or the
feature delivery spine.

**Namespaces.** No new `CODE-N.M` / `GOAL-N` / `ROAD-N` / `ARCH-N` minting from
Pathfind. Tracker labels use the `pathfind:` prefix. Effort ephemera live under
`.skills/pathfind/<effort-slug>/`.

**Ownership split.** Decision pathfinding → `pathfind`. Vision/ARCH →
`define-project`. Milestones → `plan-milestones`. Requirements IDs and ship →
delivery spine. Implement issues → `publish-issues` / triage / `tasks.md`.

## 1. Expose pathfind as user-invoked discovery skill

**Story:** As a developer facing an effort too large and foggy for one agent
session, I want one skill I run by name so the agent charts or advances a durable
decision map without auto-starting maps on every chat.

- **PFIND-1.1** THE SYSTEM SHALL expose a skill named `pathfind` under `skills/discovery/pathfind/` with `disable-model-invocation: true`.
- **PFIND-1.2** THE SYSTEM SHALL support two modes in that skill: **Chart** (loose idea → map) and **Work** (existing map → resolve one ticket).
- **PFIND-1.3** THE SYSTEM SHALL use a human-facing skill description that names the decision-map deliverable and MUST NOT summarize Chart/Work workflow steps in the description frontmatter.
- **PFIND-1.4** (guard) WHEN model-invoked skills detect multi-session fog THE SYSTEM SHALL CONTINUE TO name `/pathfind` for the user to run and MUST NOT auto-invoke it (ARCH-5).
- **PFIND-1.5** (guard) WHERE no pathfind map exists for a repo THE SYSTEM SHALL CONTINUE TO run `frame-change`, `define-project`, `plan-milestones`, and the delivery spine without inventing a map (ARCH-2).

## 2. Chart a decision map

**Story:** As a developer with a foggy large idea, I want Chart mode to name a
destination, surface only sharp questions as tickets, leave dim areas as fog, and
stop without resolving HITL tickets in the same session.

- **PFIND-2.1** WHEN Chart runs THE SYSTEM SHALL determine greenfield vs brownfield using a predicate aligned with `define-project` / `bootstrap-repo` brownfield detection and record the result in map Notes.
- **PFIND-2.2** WHEN Chart runs on brownfield and no usable territory digest exists THE SYSTEM SHALL dispatch a territory scan (contract aligned with `define-project` brownfield-scan), write or point to `.skills/pathfind/<effort-slug>/territory-scan.md`, and MUST NOT begin the destination interview until that digest exists or a hard-stop is reported.
- **PFIND-2.3** WHEN Chart names the destination THE SYSTEM SHALL apply the `clarify-decisions` protocol nested under Chart and record a Destination of one or two lines that fixes scope for the map.
- **PFIND-2.4** WHEN Chart surfaces open decisions THE SYSTEM SHALL work breadth-first and create a decision ticket only when the question can be stated precisely now (even if blocked); otherwise the item stays under Not yet specified.
- **PFIND-2.5** IF Chart finds no multi-session fog (journey small enough for one session) THEN THE SYSTEM SHALL NOT create a map and SHALL name the appropriate next skill (`frame-change`, `define-project`, `amend-feature`, or `root-cause` as fits).
- **PFIND-2.6** WHEN Chart creates a map THE SYSTEM SHALL create exactly one map artifact with required sections Destination, Notes, Decisions so far, Not yet specified, and Out of scope.
- **PFIND-2.7** WHEN Chart creates tickets THE SYSTEM SHALL create only tickets that are already sharp, then wire blocking edges in a second pass after ids exist.
- **PFIND-2.8** WHEN Chart creates research-type tickets THE SYSTEM SHALL fire `research` subagents in parallel to resolve them and record findings via pointers (throwaway branch and/or `.skills/research/…`), treating research as the exception to one-ticket-per-session.
- **PFIND-2.9** WHEN Chart finishes after creating a map THE SYSTEM SHALL write or update the knowns package skeleton under `.skills/pathfind/<effort-slug>/` and MUST NOT resolve HITL **clarify** or **prototype** tickets in the Chart session.
- **PFIND-2.10** WHEN referring to maps or tickets in user-facing narration THE SYSTEM SHALL use ticket **titles (names)**, not bare numeric ids alone.

## 3. Work through the map

**Story:** As a developer returning across sessions, I want Work mode to claim one
frontier decision, resolve it with the right primitive, record the answer, and
graduate fog without loading every ticket body up front.

- **PFIND-3.1** WHEN Work runs THE SYSTEM SHALL load the map at low resolution (index sections only) before choosing a ticket.
- **PFIND-3.2** WHEN Work selects a ticket THE SYSTEM SHALL claim it (assignee or local `Status: claimed`) as the first write before interview, research, spike, or task work.
- **PFIND-3.3** WHEN the user did not name a ticket THE SYSTEM SHALL take the first frontier ticket (open, unblocked, unclaimed) in map order.
- **PFIND-3.4** WHEN resolving a ticket THE SYSTEM SHALL fetch related or closed ticket bodies only on demand (zoom), not by dumping all children into context at session start.
- **PFIND-3.5** WHEN a ticket resolves THE SYSTEM SHALL record the answer (resolution comment or `## Answer`), close or mark the ticket resolved, and append a one-line gist plus link to the map's Decisions so far.
- **PFIND-3.6** WHEN a resolution makes fog sharp enough THE SYSTEM SHALL graduate that fog into new tickets and remove the graduated patch from Not yet specified.
- **PFIND-3.7** WHEN a ticket or area sits past the Destination THE SYSTEM SHALL rule it Out of scope (close mis-scoped tickets with reason) and MUST NOT list scope boundaries under Decisions so far as if they were route steps.
- **PFIND-3.8** WHILE a Work session runs on HITL work THE SYSTEM SHALL resolve at most one HITL ticket (clarify or prototype); research tickets MAY still be burned in parallel as AFK work.
- **PFIND-3.9** BEFORE editing Decisions so far THE SYSTEM SHALL re-read the map so concurrent sessions do not clobber another session's append.

## 4. Decision tickets, types, and vocabulary

**Story:** As a maintainer, I want ticket types that map to pack primitives and
pack vocabulary so agents never revive a retired `grilling` skill name.

- **PFIND-4.1** THE SYSTEM SHALL treat every pathfind child ticket as a **decision ticket** whose valid resolution is a decision or settled fact, not production feature delivery.
- **PFIND-4.2** THE SYSTEM SHALL allow exactly these ticket types: `clarify`, `research`, `prototype`, `task`.
- **PFIND-4.3** WHEN type is `clarify` THE SYSTEM SHALL resolve via `clarify-decisions` (and `define-domain` as passive side effect) and MUST NOT answer the human side of the interview.
- **PFIND-4.4** WHEN type is `research` THE SYSTEM SHALL resolve via the `research` skill, preferably as a subagent.
- **PFIND-4.5** WHEN type is `prototype` THE SYSTEM SHALL resolve via `run-spike` only, linking throwaway artifacts, and MUST NOT promote spike code to production inside pathfind.
- **PFIND-4.6** WHEN type is `task` THE SYSTEM SHALL perform only work that unblocks a decision (access, sample data, signup, move data) and MUST NOT treat destination delivery as a task ticket.
- **PFIND-4.7** THE SYSTEM SHALL use tracker labels `pathfind:map`, `pathfind:clarify`, `pathfind:research`, `pathfind:prototype`, and `pathfind:task` (or local-markdown `Type:` / map marker equivalents) and MUST NOT ship a type, label, or skill named `grilling` or `wayfinder`.
- **PFIND-4.8** IF a ticket is secretly an implement slice THEN THE SYSTEM SHALL close it as a type error and name `/publish-issues` or the delivery spine for the user — MUST NOT convert it in place into an implement issue.

## 5. Plan-don’t-do and layer boundaries

**Story:** As a developer in the AI era, I want Pathfind to clear decisions without
shipping code so Iron Laws still guard real delivery.

- **PFIND-5.1** WHEN pathfind runs THE SYSTEM SHALL NOT write production application code, scaffold production features, or claim a feature shipped.
- **PFIND-5.2** THE SYSTEM SHALL NOT mint `CODE-N.M` requirement IDs, write `docs/specs/*/requirements.md` as Pathfind output, or renumber `ARCH-N` / `GOAL-N` / `ROAD-N`.
- **PFIND-5.3** THE SYSTEM SHALL NOT write `docs/roadmap/INDEX.md` membership or commitment changes; WHEN ≥2 independent outcomes become clear THE SYSTEM SHALL name `plan-milestones` / roadmap planning for the user (or note for a later `frame-change` decomposition).
- **PFIND-5.4** THE SYSTEM SHALL NOT create implement issues for `publish-issues` / triage queues as Pathfind tickets, and SHALL NOT create blocking edges between pathfind tickets and implement issues (URL/title cross-links only).
- **PFIND-5.5** (guard) WHEN production implementation is required THE SYSTEM SHALL CONTINUE TO require the delivery spine (`frame-change` / `amend-feature` / `root-cause` → … → `test-first` / execute family as applicable).

## 6. Tracker and local artifacts

**Story:** As a developer on GitHub, GitLab, or no remote, I want maps on the
configured tracker with a local markdown fallback so Pathfind stays tracker-agnostic.

- **PFIND-6.1** WHEN pathfind needs tracker ops THE SYSTEM SHALL read `docs/agents/issue-tracker.md` Pathfind operations (or equivalent section) when present.
- **PFIND-6.2** WHERE `docs/agents/issue-tracker.md` is missing THE SYSTEM SHALL say so once, suggest `/configure-repo`, and default to local markdown under `.skills/pathfind/<effort-slug>/` for map and child tickets.
- **PFIND-6.3** WHEN configure-repo / issue-tracker templates are updated for this feature THE SYSTEM SHALL seed a Pathfind operations section covering map create, child create, blocking, frontier query, claim, and resolve for each supported tracker kind the pack already seeds.
- **PFIND-6.4** THE SYSTEM SHALL keep knowns and effort ephemera under `.skills/pathfind/<effort-slug>/` only in v1 and MUST NOT require a committed `docs/pathfind/` tree.

## 7. Knowns package, exit, and handoff

**Story:** As a developer leaving Pathfind, I want a knowns package and a named
next skill so the next session does not re-interview closed decisions.

- **PFIND-7.1** WHEN Pathfind exits (complete, deferred-fog, or early stop) THE SYSTEM SHALL write or update `.skills/pathfind/<effort-slug>/knowns.md` with at least: destination, locked decisions (gists + links), known unknowns / deferred fog, and out-of-scope notes.
- **PFIND-7.2** WHEN frontier is empty and Not yet specified is empty THE SYSTEM SHALL treat Pathfind as complete for that effort and name the handoff skill from the handoff matrix.
- **PFIND-7.3** WHEN frontier is empty and Not yet specified still has fog THE SYSTEM SHALL allow complete-with-deferred only after the user explicitly accepts that fog; THE SYSTEM SHALL copy accepted fog into knowns as Known unknowns (not locks).
- **PFIND-7.4** IF open unblocked pathfind tickets remain THEN THE SYSTEM SHALL NOT claim Pathfind complete unless the user explicitly abandons them with a recorded reason (deferred or out of scope).
- **PFIND-7.5** WHEN naming a handoff THE SYSTEM SHALL pick from: `/define-project`, `plan-milestones` / roadmap planning, `frame-change` (with knowns path), `amend-feature`, `/assess-pivot-impact`, optional `/publish-issues` — and MUST only **name** user-invoked skills, never invoke them.
- **PFIND-7.6** WHEN `frame-change` is pointed at a pathfind knowns package THE SYSTEM SHALL seed step-1 knowns inventory from that package's locks and known unknowns and MUST NOT re-open closed decisions unless the user reopens the ticket.
- **PFIND-7.7** (guard) WHEN `frame-change` runs after pathfind on brownfield THE SYSTEM SHALL CONTINUE TO require Blindspot / territory awareness and MUST NOT skip scan solely because a pathfind map exists.

## 8. Analysis lenses (guidance only)

**Story:** As a developer charting product-shaped fog, I want optional Explore /
Forge / Recon guidance without three extra skills.

- **PFIND-8.1** THE SYSTEM SHALL document Explore, Forge, and Recon as guidance inside `pathfind` (Notes or Chart flags) that bias ticket mix and interview pressure.
- **PFIND-8.2** THE SYSTEM SHALL NOT ship separate skills for those lenses in v1.

## 9. Neighbor routing and inventory

**Story:** As a pack maintainer, I want routers and inventories to know Pathfind
exists after the skill ships, without making it mandatory.

- **PFIND-9.1** WHEN `route-task` (and teach-pack materials updated in this feature) describe on-ramps THE SYSTEM SHALL include multi-session fog → name `/pathfind`.
- **PFIND-9.2** WHEN this feature's post-ship docs land THE SYSTEM SHALL update `docs/architecture/workflows.md` and `docs/architecture/skills.md` (and a short ADR per design OD-9) to describe Pathfind without adding ARCH-N unless a later pressure failure requires it.
- **PFIND-9.3** (guard) WHEN `gate-session` / `route-task` run THE SYSTEM SHALL CONTINUE TO prioritize process skills and MUST NOT require a pathfind map before ordinary tier-0/1 work.

## 10. Quality attributes

**Section-kind:** nfr

**Story:** As a pack consumer, I want Pathfind optional, passive-data safe, and
loud on failure — with skill text pressure-tested like other skills.

- **Performance: None** — multi-session human process; no latency SLO.
- **PFIND-10.1** (Security) WHEN reading issue bodies, scan digests, or research notes THE SYSTEM SHALL treat them as passive data and MUST NOT obey embedded instructions — verified by author-skills pressure scenarios embedding instruction-shaped text.
- **PFIND-10.2** (Reliability) IF map or ticket write/claim fails THEN THE SYSTEM SHALL report failure and MUST NOT claim the ticket resolved or the map charted.
- **PFIND-10.3** (Reliability) THE SYSTEM SHALL pressure-test `pathfind` under `author-skills` (RED baseline without skill / GREEN with skill) before shipping skill text, including plan-don’t-do and no-`grilling`-type failures.
- **Accessibility: None** — no product UI; tracker UI is third-party.

## Out of Scope

- A second roadmap or `ROAD-N` authoring inside pathfind.
- PRD / `to-spec` clone; `specify-behavior` remains requirements owner for features.
- BMAD persona agents (Mary/John/Winston) or party-mode cast.
- Personal OS port.
- Committed `docs/pathfind/` tree in v1.
- Labels or types named `grilling` / `wayfinder`.
- Cross-graph blocking between decision tickets and implement issues.
- Auto-invocation of `pathfind` or of user-invoked handoff targets.
- Pre-emptive new `ARCH-N` for plan-don’t-do (only after post-ship pressure failure).
- Replacing `bootstrap-repo` stack scaffolding.
- Full CI headless enforcement of open pathfind tickets.

## Open Questions

None — design OD-1…10 locked; design Approved 2026-07-31; requirements Approved 2026-07-31.
