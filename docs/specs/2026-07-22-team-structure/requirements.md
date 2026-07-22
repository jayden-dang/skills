# Requirements: Team structure in setup-repo

Feature code: TEAM
Status: Implemented
Date: 2026-07-22

## 1. Infer and confirm team during setup

**Story:** As a developer adopting the skill set, I want `setup-repo` to draft who works on the repo and in what roles from local repository metadata, so that I only fill gaps instead of typing the whole roster from scratch.

- **TEAM-1.1** WHEN `setup-repo` runs a full or fill-the-gaps configuration for the team profile THE SYSTEM SHALL walk a **Team** decision (one section at a time, same explainer → recommend → wait pattern as decisions A–H) before writing any team content.

- **TEAM-1.2** WHEN the Team decision runs THE SYSTEM SHALL build a draft roster using **only local repository files and local git** — specifically: `git` history for active authors, a root or conventional `CODEOWNERS` file when present, and contributor lists in common manifest/docs files (`AUTHORS`, `CONTRIBUTORS`, `package.json` `author`/`contributors` when present). THE SYSTEM SHALL NOT call code-host APIs, `gh`/`glab` collaborator endpoints, or other external membership services to infer the team.

- **TEAM-1.3** WHEN inferring active authors from git THE SYSTEM SHALL consider commits from the last **12 months** by default (or all history when the repository is younger than 12 months), rank authors by commit count descending, and include the top contributors in the draft (a documented small cap, e.g. top 10, plus anyone named in `CODEOWNERS`).

- **TEAM-1.4** WHEN `CODEOWNERS` maps paths or patterns to owners THE SYSTEM SHALL surface those owners in the draft with ownership notes (path patterns they own) and prefer them over silent omission even if they fall outside the top-N commit ranking.

- **TEAM-1.5** IF local metadata is missing, empty, or insufficient to assign roles (e.g. only bare git emails, no `CODEOWNERS`, single unknown author) THEN THE SYSTEM SHALL present the incomplete draft and ask the user to supply the missing people and/or roles before confirming — never invent personal names or job titles not grounded in metadata or the user's answer.

- **TEAM-1.6** WHEN presenting the draft THE SYSTEM SHALL let the user add, remove, rename, and re-role any entry, and accept either **named** form (`Role — Name`) or **count** form (`N Role(s)`) per entry, preferring named form when a real identity is known.

- **TEAM-1.7** WHEN the user confirms the Team decision THE SYSTEM SHALL treat that confirmation as the sole source of truth for what gets written — inference never writes without an explicit user confirm in the same setup run.

- **TEAM-1.8** WHERE the repo is already partly configured and the Team section is missing or the user asks to change team THE SYSTEM SHALL offer the Team decision on a fill-the-gaps run and leave other confirmed sections untouched (additive rule).

## 2. Persist a structured team profile

**Story:** As any later skill session, I want a durable Team section in `docs/agents/project.md`, so that every skill can read team composition without re-interviewing.

- **TEAM-2.1** THE SYSTEM SHALL seed a **`## Team`** section in `templates/agents/project.md` with placeholders for: roster entries (name+role and/or role counts), optional path/ownership notes from `CODEOWNERS`, optional **Workflow band override** (`Solo` | `Small` | `Multi` or blank for derive), and short prose telling skills how to use the section.

- **TEAM-2.2** WHEN `setup-repo` Step 4 writes configuration after a confirmed Team decision THE SYSTEM SHALL write or merge the `## Team` section into `docs/agents/project.md` without clobbering other sections the user already filled.

- **TEAM-2.3** THE SYSTEM SHALL record roster fidelity as available: each entry is either `Role — Name` or `N × Role` (or equivalent readable markdown), never a free-text-only blob that omits structure skills can parse.

- **TEAM-2.4** THE SYSTEM SHALL use a **suggested role vocabulary** (at least: Tech Lead, Backend Engineer, Frontend Engineer, Full-stack Engineer, Designer, Product Manager, QA, DevOps/SRE, Docs) while **allowing freeform role strings** the user or metadata imply.

- **TEAM-2.5** WHEN the `## Agent skills` block is written or updated THE SYSTEM SHALL include a bullet that team composition lives in `docs/agents/project.md` (`## Team`) so agents discover it alongside verify commands and posture.

- **TEAM-2.6** THE SYSTEM SHALL document in the Team section (or adjacent one-liner) that the **workflow band** is **Solo** when headcount is 1, **Small** when headcount is 2–4 (or one lead plus few engineers), **Multi** when headcount is 5+ or multiple distinct specialties — unless an explicit **Workflow band override** line is set.

## 3. High-impact skills right-size packaging by team band

**Story:** As a team (solo or multi-person), I want planning, review, and handoff skills to package work for how we actually collaborate, so that outputs match our review and ownership reality without changing the Iron Law gates.

- **TEAM-3.1** WHEN any of the high-impact skills (`brainstorm`, `grilling`, `write-plan`, `execute-plan`, `code-review`, `finish-branch`, `handoff`) starts and `docs/agents/project.md` contains a `## Team` section THE SYSTEM SHALL read that section, derive the workflow band (or use the override), and right-size **packaging** of its outputs — not skip gates.

- **TEAM-3.2** WHILE the workflow band is **Solo** THE SYSTEM SHALL package those skills for a single-developer flow: leaner multi-person ritual language, no invented reviewer/assignee roster, agent-as-pair framing where collaboration language would otherwise assume peers.

- **TEAM-3.3** WHILE the workflow band is **Small** THE SYSTEM SHALL encourage design-review checkpoints, ownership boundaries in plans/tasks, and clearer task delegation (using names when the roster has them).

- **TEAM-3.4** WHILE the workflow band is **Multi** THE SYSTEM SHALL generate outputs that support collaboration: code-ownership-aware review language when ownership notes exist, explicit review responsibilities, documentation/handoff sections, and clearer ownership boundaries.

- **TEAM-3.5** IF the `## Team` section is absent THEN THE SYSTEM SHALL CONTINUE TO the pre-feature default: do not invent a team, do not assume multi-person process beyond what each skill already does, and do not block the skill on missing team data.

- **TEAM-3.6** THE SYSTEM SHALL NOT weaken Iron Laws by band: Solo does not skip `code-review`, test-first, verify evidence, or root-cause gates; band only changes packaging and emphasis.

## 4. Human docs stay aligned

**Story:** As a human adopting or maintaining the skill set, I want the setup-repo guide and related adoption docs to describe Team capture, so that the documented behavior matches the skill.

- **TEAM-4.1** WHEN the feature ships THE SYSTEM SHALL update `docs/guide/skills/setup-repo.md` to document the Team decision, local inference sources, named-vs-count fidelity, band derivation/override, and that high-impact skills read `## Team`.

- **TEAM-4.2** WHERE `docs/guide/resources/adopting.md` describes setup decisions THE SYSTEM SHALL mention team composition as a setup concern (brief, not a full duplicate of the skill guide).

## Non-functional requirements

- **Performance:** None — setup is conversational and local `git`/`grep`/`read` only; no latency target beyond "agent-runnable on a normal repo history."
- **Security:** **TEAM-5.1** THE SYSTEM SHALL NOT require or perform external identity-service authentication to populate Team; personal names written to `docs/agents/project.md` are only those the user confirmed (metadata-derived or user-entered), so the user controls what is committed.
- **Reliability:** None beyond existing setup additive-write rules.
- **Accessibility:** None — agent- and markdown-facing config only.

## 5. Guards for existing setup and posture behavior

- **TEAM-6.1** (guard) WHEN `setup-repo` runs THE SYSTEM SHALL CONTINUE TO walk decisions A–H one at a time, apply the additive write rule, run the Step 6 wiring gate, and forbid Step-1 service probing for tracker/auth detection.

- **TEAM-6.2** (guard) WHEN `docs/agents/project.md` carries **Project posture** THE SYSTEM SHALL CONTINUE TO have `brainstorm`, `grilling`, and `interpret` right-size ceremony from delivery intent and lifecycle stage independently of Team band (posture and team are orthogonal).

- **TEAM-6.3** (guard) WHEN `setup-repo` Step 1 classifies the repo THE SYSTEM SHALL CONTINUE TO detect configuration from repo files only and never auto-choose the issue tracker from a remote probe.

- **TEAM-6.4** (guard) WHEN a high-impact skill runs without `docs/agents/` THE SYSTEM SHALL CONTINUE TO suggest `setup-repo` where it already does and proceed with available context rather than hard-failing solely because Team is missing.

## Out of Scope

- Probing GitHub/GitLab/Linear for org members, collaborators, or team APIs
- A separate `docs/agents/team.md` file or team data in `CONTEXT.md`
- A new model-invoked `team-context` skill
- Changing Iron Law gates or ceremony tier rules by band
- Updating every skill in the set (only the listed high-impact skills in v1)
- Automatic ongoing re-sync of Team from git on every session (re-run `/setup-repo` or edit `project.md` to refresh)
- Enforcing real-world HR titles or HRIS integration
- Privacy redaction automation beyond user confirmation of the draft

## Open Questions

None — resolved in brainstorm (location, fidelity, sources, consumer scope, role vocabulary, activity window, band model, override, packaging-only adaptation, approach A).
