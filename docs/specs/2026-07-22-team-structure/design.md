# Design: Team structure in setup-repo

Feature code: TEAM
Status: Approved
Date: 2026-07-22
Requirements: ./requirements.md

## Context

Today `setup-repo` configures machine answers under `docs/agents/` — tracker, labels, verify commands, test annotations, release steps, docs layout, **Project posture**, and an optional project-docs layer. Skills that need standing facts read `docs/agents/project.md` instead of re-asking. Nothing captures *who* works on the repo or how collaboration should be packaged. Downstream skills therefore default to a tacit single-developer (or generic multi-person) tone regardless of real roster.

The constraint that shapes this design is the established **posture pattern**: durable standing facts live as structured sections in `docs/agents/project.md`; setup walks one decision at a time, drafts, confirms, then writes additively; consumers right-size when the section is present and proceed without inventing data when it is absent. Team composition is the same kind of fact as posture — orthogonal to delivery intent / lifecycle stage — so it extends that pattern rather than introducing a new skill, a second config file, or a runtime team-context sub-skill.

Inference stays inside the same **local-only** boundary as `setup-repo` Step 1: git history, `CODEOWNERS`, AUTHORS/CONTRIBUTORS, and package manifests. No code-host collaborator APIs. Incomplete drafts are normal; the user confirms before any write. Workflow band (Solo / Small / Multi) is **derived** from the roster with an optional override line, and only changes **packaging** of high-impact skills — never Iron Law gates.

Scan digest: `.skills/team-structure-design-scan.md`. Independent design review: `.skills/team-structure-design-review.md` (findings C1, I1–I6 incorporated below). No `docs/architecture/` spine in this repo; no ADR required (decisions mirror existing posture and probe-ban patterns rather than creating a surprising new boundary).

## Decisions

1. **Location:** `## Team` section inside `docs/agents/project.md` (not `team.md`, not `CONTEXT.md`).
2. **Approach:** Posture pattern — setup Decision **H** (Team), template seed, consumer right-size conditionals; no new skill. Former project-docs decision renumbers to **I**.
3. **Fidelity:** Prefer `Role — Name`; allow `N × Role` counts; user edits the draft.
4. **Sources:** Local git (12 months default, top 10 humans), CODEOWNERS → **Ownership notes** (all owner tokens) and human-like names only into **Roster**, AUTHORS/CONTRIBUTORS, package.json author/contributors. No external membership APIs.
5. **Band:** Deterministic derive with precedence (see §1); optional `Workflow band override` line.
6. **Adaptation:** Packaging only for the seven high-impact skills; gates unchanged; no new mandatory task/PR schema fields.
7. **Decision lettering:** **H = Team** (after G posture); **I = project-docs layer (optional)** — renumber every former “decision H” reference. Walk order remains alphabetical A–I.
8. **Role vocabulary:** Suggested set + freeform strings.
9. **Refresh:** Manual only — re-run `/setup-repo` fill-the-gaps or edit `project.md`; no session-start resync.
10. **AGENTS.md (this skill-set repo):** Update the per-repo config blurb so agents building the set know Team is part of project.md.

## Architecture

### 1. `## Team` schema in `templates/agents/project.md`

Satisfies: TEAM-2.1, TEAM-2.3, TEAM-2.4, TEAM-2.6  
Reuse: existing — mirrors `## Project posture` block in `templates/agents/project.md` (rung 2)

Insert **`## Team` immediately after `## Project posture`** and before `## Verify commands`. Shape:

```markdown
## Team

Who works on this repo and how skills should package collaboration.
Skills that plan, review, or hand off read this section when present and
right-size **packaging** only (Solo / Small / Multi) — Iron Law gates never
change. Edit freely; re-run `/setup-repo` to re-draft from git/CODEOWNERS.
If this section is absent, skills do not invent a team.

### Roster

- <Role — Name | N × Role>
- …

Suggested roles (freeform allowed): Tech Lead, Backend Engineer, Frontend
Engineer, Full-stack Engineer, Designer, Product Manager, QA, DevOps/SRE, Docs.

### Ownership notes (optional)

- `<path-or-pattern>` → <owner-token>   <!-- all CODEOWNERS owners, including @org/team -->

### Workflow band

- **Override (optional):** `<blank | Solo | Small | Multi>` — when non-blank, skills use this.
- **Derive (when override blank):** see band rules below — **SSOT in this section**;
  consumers **read** these rules and do **not** re-copy them into skill bodies.
- **Packaging matrix:** embed Solo / Small / Multi / (no band) packaging rows here
  (same content as Architecture §4 table).
```

**Band derivation — normative precedence (lives only in `## Team` / this template):**

1. If **Workflow band override** is non-blank → use it; stop.
2. Compute **headcount** from **Roster only**: each `Role — Name` counts as 1; each `N × Role` / `N Role(s)` adds N. Ignore Ownership notes and placeholders (`<…>`).
3. Headcount buckets (hard cutoffs only):
   - headcount ≤ 0 (empty roster) → treat as **no band** (same as Team absent for packaging; do not invent Solo)
   - headcount = 1 → **Solo**
   - headcount 2–4 → **Small**
   - headcount ≥ 5 → **Multi**
4. **Specialty upgrade only:** if result is **Small** and the roster has **≥ 3 distinct role titles** (case-insensitive; freeform strings count as distinct when they differ after trim), upgrade to **Multi**. Never downgrade Multi→Small. Never use “one lead + few engineers” as a separate numeric rule — that phrase in requirements is covered by Small (2–4) + optional specialty upgrade.

### 2. `setup-repo` Decision H — Team (infer → draft → confirm)

Satisfies: TEAM-1.1, TEAM-1.2, TEAM-1.3, TEAM-1.4, TEAM-1.5, TEAM-1.6, TEAM-1.7, TEAM-1.8, TEAM-5.1  
Reuse: existing — Step 2 decision pattern (A–G) in `skills/setup/setup-repo/SKILL.md` (rung 2)

**Where:** New subsection **### H. Team** in Step 2, immediately after **### G. Project posture**. Renumber today’s **### H. Project-docs layer** to **### I. Project-docs layer**. Update Step 2 intro from “eight decisions” to “nine decisions (A–I; I optional project-docs)”.

**Renumber sites (complete list for implementers):**

| Site | Change |
|---|---|
| Step 2 intro count | eight → nine; list A–I |
| `### H. Project-docs…` heading | becomes `### I. Project-docs…` |
| New `### H. Team` | inserted after G |
| Step 4 item “decision H” / project-docs | “decision I” |
| Agent-skills block “if decision H was Yes” | “if decision I was Yes” |
| Guide setup-repo decision list | A–I; Team as H |
| adopting.md decision list | mention Team; fix stale “six decisions” |
| `docs/guide/skills/establish-project.md` | project-docs decision letter → **I** |

**Bodies of A–G:** unchanged except any internal “next is H project-docs” wording. **TEAM-6.1** means: A–G flow, additive write, Step 6 gate, and Step-1 probe ban continue; new H is additive; former H renumbered to I.

**Explainer:** Team composition is standing context for brainstorm/grilling/write-plan/execute-plan/code-review/finish-branch/handoff — same class of fact as Project posture. Wrong band → wrong packaging.

**Inference recipe (local only):**

1. **Repo age:** if first commit age span &lt; 12 months → all history; else commits since `now − 365d`.
2. **Active authors:** `git shortlog -sn --all` with matching since. Top **10**. Drop bots (`dependabot[bot]`, `github-actions`, `renovate`, names matching `*\[bot\]`). Prefer display name; email only as draft disambiguation note.
3. **CODEOWNERS** (first of `CODEOWNERS`, `.github/CODEOWNERS`, `docs/CODEOWNERS`):
   - Parse non-comment lines `pattern owner1 owner2…`.
   - **Ownership notes:** every owner token (including `@org/team`) → pattern → token lines. Do **not** resolve org teams via API.
   - **Roster:** add only **human-like** owner tokens (no leading `@org/` team slugs; no pure email unless the user later confirms that person). Humans not in top-10 still appear on Roster when they look like people/handles.
4. **Manifests:** `AUTHORS`, `CONTRIBUTORS`, `package.json` author/contributors name fields → human names into Roster if missing.
5. **Roles:** Do not invent titles from commit volume. Defaults: single human → `Contributor — <Name>` (user re-roles); else `Contributor — <Name>` placeholders. FE/BE suggestions only as recommendations in the presentation, never silent final titles.
6. **Present draft:** Roster, Ownership notes, derived band, suggested role list; invite add/remove/rename/re-role and named vs count form. Empty metadata → empty Roster + explicit ask (TEAM-1.5).
7. **Confirm gate:** no Team write until user confirms (TEAM-1.7).

**Forbidden:** `gh`/`glab` collaborator APIs, env key probing, inventing names/titles not in metadata or user answer.

**Fill-the-gaps (TEAM-1.8):** missing `## Team` is a Step 1 gap; walk only Decision H when filling that gap; leave other sections untouched.

### 3. `setup-repo` write path and discovery surface

Satisfies: TEAM-2.2, TEAM-2.5  
Reuse: existing — Step 3 draft/confirm + Step 4 additive write in `setup-repo/SKILL.md` (rung 2)

**Step 3:** Full `project.md` draft includes `## Team` once confirmed.

**Step 4:**

- Fill **Project posture** (G) as today.
- Fill **`## Team`** from confirmed Decision H (merge: replace Team subsection content only).
- Project-docs seeds remain gated on **decision I** (renamed).
- Extend **Repo config the skills read** in the `## Agent skills` block:

```markdown
- Team composition (roster, ownership notes, workflow band): `docs/agents/project.md` (`## Team`)
```

**Step 1:** missing `## Team` under an otherwise complete project.md → list as gap.

### 4. Shared band derivation (consumer contract)

Satisfies: TEAM-2.6, TEAM-3.1, TEAM-3.5, TEAM-3.6  
Reuse: existing — posture “read section or proceed without” pattern in brainstorm/grilling (rung 2)

No shared library skill (Approach A: posture pattern, not a new `team-context` skill). **Band derivation and the packaging matrix live only in `## Team`** (template → written `project.md`). High-impact skills load that section and apply it; they do not re-author the algorithm (avoids seven-way drift).

| Band | Packaging emphasis (also embedded in template `## Team`) |
|---|---|
| **Solo** | Lean multi-person ritual language; no invented peer reviewers/assignees; agent-as-pair; still full gates |
| **Small** | Design-review checkpoints; ownership boundaries in plans/tasks via **optional freeform notes**; name people when roster has names |
| **Multi** | CODEOWNERS-aware review language when ownership notes exist; explicit review responsibilities as prose; handoff/docs emphasis; clearer ownership boundaries |
| **(no band)** Team absent, empty roster + blank override | Pre-feature default; do not invent team; do not hard-fail |

```
IF project.md has ## Team AND (non-empty Roster OR non-blank override):
  band = apply Workflow band rules written in that section
  packaging = apply packaging matrix written in that section
ELSE:
  pre-feature default (same as Team absent)
NEVER: skip review / tdd / verify / root-cause because Solo
```

Posture remains independent (TEAM-6.2).

### 5. High-impact skill patches

Satisfies: TEAM-3.1, TEAM-3.2, TEAM-3.3, TEAM-3.4, TEAM-3.5, TEAM-3.6, TEAM-6.2, TEAM-6.4  
Reuse: existing — each skill’s existing project.md / posture read site (rung 2)

**Schema rule:** no new mandatory slots on `tasks.md` (no required Owner field). Small/Multi ownership is **optional freeform** in Steps notes or a single optional “Owner: …” line agents may add. finish-branch does not gain a new menu item — only packaging prose on existing Option 2 (PR).

| Skill | Exact insertions | Packaging effect |
|---|---|---|
| `brainstorm` | Step 1 after Project posture | State derived band once; Solo: fewer peer-coordination branches in interview/approaches; Small/Multi: surface ownership/review capacity in approach trade-offs. **Tier rules unchanged.** |
| `grilling` | Adjacent to posture right-size bullet | **Additive probes only** when Team present and band Small/Multi: optional ownership/reviewer questions when relevant to the plan. When Solo or Team absent: **do not introduce** multi-person assignee/scheduling questions (default grilling already has none — do not invent a “skip list”). |
| `write-plan` | Step 1 when reading project.md / writing Global Constraints + task bodies | Solo: no fake multi-assignee theater. Small/Multi: optional freeform owner/review notes when names/notes exist — **not** a new required task field. |
| `execute-plan` | **(a)** Setup after step 3 (read plan): load Team + band into controller context. **(b)** Per-Task brief build: Solo = pair-with-user brief tone; Small/Multi = mention owners when roster/notes apply. **(c) Non-goal:** do not alter dual-verdict / Standards+Spec subagent review steps or skip them for Solo. |
| `code-review` | After gather standards | Dual-axis review always. Solo: report to solo author. Small/Multi: path-aware emphasis using ownership notes when present. |
| `finish-branch` | Option 2 (PR) prose only | Solo: no invented reviewer list. Small/Multi: if creating a PR, suggest reviewers from roster/ownership notes in the PR body language — not a new menu option. |
| `handoff` | Contents checklist | When Team present: one-line team/band; Small/Multi: who owns next actions when relevant. |

Missing Team or `docs/agents/`: existing suggest-setup-repo where already present; never hard-fail solely for missing Team (TEAM-6.4).

### 6. Human docs and skill-set constitution touch

Satisfies: TEAM-4.1, TEAM-4.2  
Reuse: existing — guide mirrors under `docs/guide/` (rung 2)

| File | Change |
|---|---|
| `docs/guide/skills/setup-repo.md` | Document Decision **H** (Team): local sources, CODEOWNERS→notes vs human roster, named vs count, band derive/override, consumers; project-docs as **I**; decision count A–I. |
| `docs/guide/resources/adopting.md` | Brief team-composition bullet; fix outdated “six decisions” list to include G posture, H Team, I project-docs (brief). |
| `docs/guide/skills/establish-project.md` | Project-docs decision letter → **I** (was wrongly G; must not stay H after renumber). |
| `AGENTS.md` | Per-repo config paragraph: project.md holds verify commands, posture, and Team. |

### 7. Guards preserved in skill text

Satisfies: TEAM-6.1, TEAM-6.3  
Reuse: existing — Step 1 probe ban + A–G flow (rung 2)

Decision H text restates: does not relax Step 1 service probe ban; A–G decision bodies stay; Step 6 wiring gate still required; tracker still never auto-chosen from remote probe. Project-docs remains optional last decision (**I**). Implementation is additive: new H, renumber old H→I, no rewrite of A–G substance.

## Seams for testing

This feature ships as skill and template markdown. Testing follows `writing-skills`: baseline/pressure scenarios and structural checks.

| Seam | Kind | Covers |
|---|---|---|
| `templates/agents/project.md` `## Team` shape + band prose | structural | TEAM-2.1, TEAM-2.3, TEAM-2.4, TEAM-2.6 |
| `setup-repo` Decision H inference + confirm (rich metadata) | skill scenario | TEAM-1.1–1.4, TEAM-1.6–1.7, TEAM-5.1 |
| `setup-repo` Decision H incomplete metadata | skill scenario | TEAM-1.5, TEAM-1.7 |
| `setup-repo` fill-the-gaps when `## Team` missing | skill scenario | TEAM-1.8, TEAM-2.2 |
| CODEOWNERS → Ownership notes vs human Roster split | skill scenario | TEAM-1.4, TEAM-1.5 |
| Band precedence: override &gt; headcount &gt; specialty upgrade | skill scenario | TEAM-2.6, TEAM-3.1 |
| Agent skills block Team bullet | structural | TEAM-2.5 |
| High-impact: Team present Solo vs Multi packaging | skill scenario | TEAM-3.1–3.4, TEAM-3.6 |
| High-impact: Team absent / empty roster | skill scenario | TEAM-3.5, TEAM-6.4 |
| execute-plan: band loads + brief packaging; dual review steps untouched | skill scenario | TEAM-3.2–3.4, TEAM-3.6 |
| write-plan/finish-branch: optional prose only (no new required schema) | skill scenario | TEAM-3.3–3.4 |
| grilling: additive Small/Multi probes only | skill scenario | TEAM-3.2–3.4 |
| Posture independent of Team | skill scenario | TEAM-6.2 |
| Step 1 file-only; A–G + Step 6; I optional | skill scenario | TEAM-6.1, TEAM-6.3 |
| Guide + adopting docs mention Team as H | structural | TEAM-4.1, TEAM-4.2 |

**New runtime seams:** none.

## Coverage check

| ID | Satisfies section |
|---|---|
| TEAM-1.1 | §2 Decision H |
| TEAM-1.2 | §2 Decision H |
| TEAM-1.3 | §2 Decision H |
| TEAM-1.4 | §2 Decision H (CODEOWNERS split) |
| TEAM-1.5 | §2 Decision H |
| TEAM-1.6 | §2 Decision H |
| TEAM-1.7 | §2 Decision H |
| TEAM-1.8 | §2 Decision H |
| TEAM-2.1 | §1 Team schema |
| TEAM-2.2 | §3 write path |
| TEAM-2.3 | §1 Team schema |
| TEAM-2.4 | §1 Team schema |
| TEAM-2.5 | §3 write path |
| TEAM-2.6 | §1 band derivation |
| TEAM-3.1 | §4 + §5 |
| TEAM-3.2 | §4 matrix + §5 |
| TEAM-3.3 | §4 matrix + §5 |
| TEAM-3.4 | §4 matrix + §5 |
| TEAM-3.5 | §4 + §5 |
| TEAM-3.6 | §4 + §5 |
| TEAM-4.1 | §6 human docs |
| TEAM-4.2 | §6 human docs |
| TEAM-5.1 | §2 Decision H |
| TEAM-6.1 | §7 guards |
| TEAM-6.2 | §4 + §5 |
| TEAM-6.3 | §7 guards |
| TEAM-6.4 | §5 high-impact |

Deliberately unmapped: none.

**Reuse coverage:** all sections `Reuse: existing` (rung 2); no new dependencies.

**Review fixes applied:** C1 decision lettering (Team=H, project-docs=I); I1 band precedence; I2 CODEOWNERS roster vs notes; I3 renumber site list; I4 execute-plan split insertions; I5 grilling additive probes; I6 no new mandatory schema.
