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
| **Draft surface** | `repo` — milestone drafts live in `docs/roadmap/INDEX.md` only. `notion` — each milestone draft is also a page in the Notion database below, where the sign-off role signs it off before any of its tickets reach the tracker | `repo` |

Slot vs CODE: one home in `plan-milestones` (**ROAD-N is a slot, not a feature**).

### Notion draft surface

Only when **Draft surface** is `notion`; delete this block otherwise.

- **Drafts data source:** `collection://<id>` — `<Workspace> / <page> / <database>`. The ID
  is the binding. It is the same on every machine, and a server name is not.
- **Workspace:** `<name>` (`<workspace_id>`, from `notion-get-self`)
- **Server at setup:** `<MCP server name>`. On any machine, use the connected Notion server
  whose `notion-fetch` returns the data source. If none returns it, write nothing to
  Notion.
- **Sign-off:** `Status` = `Signed off` with `Signed off by` = `<name of the sign-off role's
  Notion user>`. Only that person sets either property; agents write `Draft` or
  `In review`.

## Wayfinding operations

<Concrete command recipes for this tracker. Examples below — keep only the
configured tracker's section.>

### github

- List open issues: `gh issue list --state open`
- Read issue: `gh issue view <n> --comments`
- Create issue: `gh issue create --title <t> --body-file <f> --label <l>`
- Blocking: `gh issue create --blocked-by <n>,<n>`, `gh issue edit <n> --add-blocked-by <n>`
- Sub-issues: `gh issue create --parent <n>`
- Comment: `gh issue comment <n> --body-file <f>`

### linear

Two access paths: a connected **Linear MCP server** (preferred — lower friction,
handles auth) or the **GraphQL API**. Whichever you use, you must be able to
perform every operation below. Find the MCP tool for each; **fall back to the API
for any operation the MCP server does not expose.** Blocking relations are the
common MCP gap for multi-issue graphs (`publish-issues`). Default
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

## Issue format

Every writer follows this when creating an issue, with or without a skill loaded.

**Title:** what the reader gets, or for a bug what goes wrong, in plain words. No `Task N`, no `feat:`.

**Body of a bug:**

```markdown
## What happens
## Expected
## How to reproduce
Exact steps and a minimal reproduction, or "read from code, not reproduced".
## Evidence
Error text, versions, trace IDs.
```

**Body of anything else:**

```markdown
## Problem
Who hits what today, and why it matters now. The requester's own words stay verbatim.
## Outcome
What a person can do once this ships.
## Acceptance
- [ ] Observable, and checkable on its own
## Out of scope
- Adjacent work this must not touch, or "None"
```

In `shaping`, a section with nothing in it yet reads `Not decided yet`.

**Source paths, line numbers, function names, `Task N` items and implementation steps go in the spec.**
They stay out of the issue even when the request names them. Three of four baseline runs filed the
requester's "add a route, add a service method" as a "suggested approach". The first line of the
body is its first section: no line says who or what wrote it.

**Internal IDs follow reach.** `git check-ignore -q docs/specs/_probe/requirements.md` exiting 0
means specs are private, so no feature code, requirement ID or spec path appears anywhere on the
tracker. The same check on `docs/roadmap/INDEX.md` governs `ROAD-N` and `MILE-N`. Where specs are
shared, a plan's issue is titled `[CODE] <outcome>` and its last lines are `Requirements covered:`,
`Plan:` and `Roadmap:`. Where the roadmap is shared, `ROAD-N` leads the title of its claim. What
stays off the tracker goes in `.skills/<CODE>/tickets.md`, where `/board` and `/go` read it, one line
per ticket with the ID first: `<ticket id> covers: <requirement IDs> road: <ROAD-N>`.

**Fill all four fields, using the `Issue fields` table:**

- **Assignee:** whom the requester named, else the requester. Filing on someone's behalf still
  assigns them. Blank only when the requester said so, and say so in the reply.
- **Status:** one category role and one state role from `triage-labels.md`. The state is what the
  requester named, else `needs-triage`.
- **Priority:** the requester's word, else `## Focus` in the roadmap, else this table.
- **Estimate:** the requester's word, else this table.

| Priority | When |
|---|---|
| urgent | Production is down, data is being lost, or a security hole is open |
| high | It blocks users or other work, has a deadline this week, or is in `## Focus` |
| medium | The default, when nothing else applies |
| low | No time pressure; an improvement |

| Estimate | Complexity |
|---|---|
| 1 | One small change, approach known |
| 2 | A few places in one part of the system |
| 3 | Many places, with points to weigh |
| 5 | Several parts of the system, or open questions remain |
| 8 | Large with many unknowns; consider splitting |

**Blocking:** the tracker's relation when `Issue fields` names one, else one line in the body:
`Blocked by: #N, #M`.

**After creating:** read the issue back from the tracker. Reply with its ID, assignee, priority,
estimate and status, as the read shows them. A field that would not save: keep the issue, name the
field in the reply, and put nothing in the body in its place.

## Issue fields

Filled by `configure-repo`.

| Field | Write | Read |
|---|---|---|
| Assignee | <op> | <op> |
| Status | <op> | <op> |
| Priority | <op> | <op> |
| Estimate | <op> | <op> |
| Blocking | <op, or none> | <op> |
