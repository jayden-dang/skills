# Issue tracker configuration (agent-facing)

Written by `configure-repo`. Skills that read or write issues consult this file.

**Tracker:** <github | gitlab | linear | local>

## Publish and program sync

Filled by `configure-repo`. Missing lines → defaults in italics. `plan-tasks` Step 5
and program writers read these fields.

| Field | Values | Default |
|---|---|---|
| **Publish unit** | `feature` — one issue per approved plan; tasks stay in `tasks.md`. `tasks` — legacy one issue per plan task | `feature` |
| **Close linkage** | Tracker-native close text for the feature PR | e.g. GitHub `Closes #N` |
| **Program sync** | `local` — MILE/ROAD only in `docs/roadmap/`. `labels` / `project_fields` — metadata on the feature issue only. `initiatives` — lead/admin remote program mirror | `local` |
| **Program write role** | `owner` \| `lead` \| `ic` — who may create remote program objects | `ic` (with Program sync `local`) |

Slot vs CODE: one home in `plan-milestones` (**ROAD-N is a slot, not a feature**).

## Wayfinding operations

<Concrete command recipes for this tracker. Examples below — keep only the
configured tracker's section.>

### github

- List open issues: `gh issue list --state open`
- Read issue: `gh issue view <n> --comments`
- Create issue: `gh issue create --title <t> --body-file <f> --label <l>`
- Sub-issues / blocking: `gh api` dependency endpoints (fill in per repo)
- Comment: `gh issue comment <n> --body-file <f>`

### linear

Two access paths: a connected **Linear MCP server** (preferred — lower friction,
handles auth) or the **GraphQL API**. Whichever you use, you must be able to
perform every operation below. Find the MCP tool for each; **fall back to the API
for any operation the MCP server does not expose.** Blocking relations are the
common MCP gap for multi-issue graphs (`publish-issues`, pathfind). Default
`plan-tasks` publish is one feature issue — no task-to-task blocking edges.

| Operation | GraphQL |
|---|---|
| List open issues | `query` on `issues(filter: {...})` → `identifier`, `title`, `state { name type }`, `labels { nodes { name } }` |
| Read an issue | `issue(id: "<UUID>")` → `title description comments { nodes { body } }` — resolve a human identifier like `ENG-123` via an `issues` filter, not the `id:` argument (which takes the UUID) |
| Create an issue | `issueCreate` mutation: `teamId`, `title`, `description`, `labelIds`, optional `parentId` for a sub-issue |
| Comment | `commentCreate` mutation: `issueId`, `body` |
| Blocking edge | `issueRelationCreate` mutation with `type: blocks` |

GraphQL endpoint: `https://api.linear.app/graphql` (POST, `Content-Type: application/json`).
Auth: header `Authorization: <key>` — a **personal API key is used raw** (no
prefix); an OAuth access token needs a `Bearer ` prefix. Read the key from the
environment (`LINEAR_API_KEY`); never commit it or paste it into a file. Consult
Linear's live GraphQL schema for exact field names rather than guessing.

Roles live in Linear's native fields: map them to workflow **states** and
**labels** per `triage-labels.md`, not to a `Status:` line in an issue body.

### local

- Issues live in `.scratch/<feature>/issues/NN-slug.md`
- Each file carries a `Status: <state>` line; PRDs in `.scratch/<feature>/PRD.md`
- "Claiming" = setting `Assignee:` in the file and committing

## Pathfind operations

Used by `/pathfind`. The **map** is one issue (or local file); **decision tickets** are its children. Labels use the `pathfind:` namespace. Keep decision tickets **out of** implement/`publish-issues` blocking graphs (URL/title cross-links only).

### github (Pathfind)

- **Map:** `gh issue create --title "…" --body-file … --label pathfind:map`
- **Child ticket:** GitHub sub-issue under the map when enabled; else task-list + `Part of #<map>` in the child body. Labels: `pathfind:clarify` | `pathfind:research` | `pathfind:prototype` | `pathfind:task`
- **Blocking:** native issue dependencies when available (`gh api` blocked_by); else `Blocked by: #<n>` at top of child body
- **Frontier:** open children of the map with no open blocker and no assignee — first in map order
- **Claim:** `gh issue edit <n> --add-assignee @me` before any resolve work
- **Resolve:** comment the answer → `gh issue close <n>` → append gist + link on the map's Decisions so far

### local (Pathfind)

- **Map:** `.skills/pathfind/<effort>/map.md` (or under `.scratch/<effort>/map.md` if preferred)
- **Child:** `.skills/pathfind/<effort>/issues/NN-<slug>.md` with `Type:` and `Status:` (`claimed` / `resolved`)
- **Blocking:** `Blocked by: NN, NN` near the top
- **Frontier / claim / resolve:** unblocked + unclaimed first; set `Status: claimed` before work; `## Answer` + `Status: resolved`; append to map Decisions so far

### linear (Pathfind)

- **Map:** issue labeled `pathfind:map` (or equivalent project label)
- **Child:** sub-issue / parentId under the map; labels `pathfind:*` types as above
- **Blocking:** `issueRelationCreate` with `type: blocks` among pathfind tickets only
- **Claim / resolve:** assignee + state transitions per team workflow; append Decisions so far on the map issue

## Conventions

- Issue bodies describe behavior and interfaces, never file paths (they go stale).
- Issues produced from a **plan** (`plan-tasks`) carry a `Requirements covered:` section
  listing the **union** of plan requirement IDs (one feature issue by default).
- AI-authored content is disclaimed on its first line, and the disclaimer is the
  marker downstream skills read to skip AI-born work:
  - `triage` comments start: `> *This was generated by AI during triage.*`
  - `publish-issues` issue bodies open with a marker line beginning `> *This issue was drafted by AI with` — `triage` skips these; they are already agent-ready.
  - `plan-tasks` feature issues open with `> *This issue was drafted by AI with \`plan-tasks\`.*`
