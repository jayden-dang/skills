# Notion as the draft surface (plan T3c)

Date: 2026-10-19 · Plan: `2026-10-18-survey-upgrade-plan.md` T3c · jdk `36573d1`

## Question

Survey ask, Flexible Mode: the agent proposes the next epic or milestone in Notion as a
draft, keeps managing the drafts, creates Linear tickets only after the TPM signs off,
and only then builds. The owner adds one condition: a person who works on several
projects must have each repo's drafts land in that project's own Notion area. That holds
whether the projects share one workspace or sit in different workspaces.

The owner decided the sign-off evidence on 2026-10-19: a `Status` property
(`Draft · In review · Signed off`) and a `Signed off by` person property on the draft's
page. The agent never sets either one.

## What the Notion MCP gives a skill

Source: Notion's MCP docs (`developers.notion.com/guides/mcp`, read through Context7 on
2026-10-19).

- **Connection.** Notion hosts the server at `https://mcp.notion.com/mcp`, reached over HTTP
  with OAuth. To add it to Claude Code, run `claude mcp add --transport http <name> https://mcp.notion.com/mcp`,
  then `/mcp` to sign in.
- **One connection reaches one workspace.** The token exchange returns that workspace's
  `workspace_id`. A person with two workspaces adds the server twice under two names. The
  tools then arrive as `mcp__<name>__notion-*`, so the server name is how a session tells the
  workspaces apart. Nothing in a tool's output says which repo it is for.
- **Tools a draft surface uses:**
  - `notion-search`: query, optional teamspace filter.
  - `notion-fetch`: a page, a database, or a `collection://` data source, given by URL or ID.
  - `notion-create-pages`: `parent` plus a list of pages, each with properties and markdown content.
  - `notion-update-page`.
  - `notion-get-comments` and `notion-create-comment`.
  - `notion-get-self`: the connection's workspace and user. `notion-get-users` with `user_id: "self"` returns the user only.
- **A create without a `parent` makes a private page.** The docs say: "If a parent is not
  specified, a private page will be created." Nobody but the connected user can see that page,
  so the TPM never sees the draft.
- **Search is by title, across the whole workspace.** Two projects that both keep a
  "Roadmap drafts" database return two hits with the same title. Only the path above each
  hit tells them apart.

## Fixture

`skill-fixtures/mcp/fake-mcp.py` is a stdio MCP server. It uses the hosted Notion tool names
and argument shapes (and the Linear MCP's for `linear`), keeps its state in a JSON file, and
logs every call. `scenarios/notion-world.py` seeds the world below. `run-headless.sh` loads it
through `FIXTURE_MCP`.

| Server | Workspace | Areas |
|---|---|---|
| `notion-saltgrass` | Saltgrass Marina | `Harbor Ledger / Roadmap drafts` (this repo's), `Harbor Portal / Roadmap drafts` (Thu's product, same name), a 2025 `Roadmap` page at the root |
| `notion-klynt` | Klynt Labs | `Ledger / Roadmap drafts` (another company's ledger product) |
| `linear` | Saltgrass | teams `LED` (this repo) and `POR` (harbor-portal) |

The repo is `harbor-ledger` with overlays `roadmap-draft` and `notion-linear`. MILE-1 is
Committed and MILE-2 is Planned. The working agreement in `project.md` has Quang approve
new tickets and sign off milestones. The tracker is `linear`, team `LED`.

## Result

There were 86 headless runs, costing 3.14 USD. Each count below is scored from the server
state files and the call log.

| Probe | Baseline | Shipped |
|---|---|---|
| Which database a draft lands in, with two projects in one workspace | 7/7 the right one | 4/4 + 4/4 trigger runs |
| Draft lands with a renamed server (`notion`) | 3/3 found it by ID | n/a (no-op) |
| Draft lands when the server reaches the wrong workspace | 5/5 wrote nothing there | n/a (no-op) |
| Setup with the right workspace: binding by ID | 3/3, in three ad-hoc shapes | 5/5 in the template fields |
| **Setup when only another company's workspace is reachable** | **3/3 bound Klynt's `Ledger / Roadmap drafts`** | 4/4 `repo`, told to re-authenticate |
| Draft names the tickets its sign-off releases | 0/7 | 4/4 + 4/4 |
| **Signed-off draft published** | **2/5** ("The sign-off is on the milestone") | 4/4, exactly the listed tickets |
| Unsigned or self-signed draft not published | 9/9 | (unchanged) |
| Publish follows the page Quang edited, not the stale repo copy | 7/7 | (unchanged) |
| **Status reports the TPM's blocking comment** | **1/7** | 4/4, quoted verbatim |

## Decision

Shipped:
- `configure-repo` 1.12.0: the Draft surface follow-up, and a sign-off role membership check
  before any binding.
- `plan-milestones` 1.3.0: `notion-draft.md`, which holds the REQUIRED `## Tickets on sign-off`
  section, plus description keywords.
- `refresh-roadmap-status` 1.3.0: pass 7.
- The issue-tracker template's binding fields.

`publish-issues` is unchanged.

The multi-project concern rests on the data source ID: the same ID on every machine,
whatever the server is called. A setup that cannot reach the project's workspace binds
nothing. Area choice, parentless pages, the sign-off fields, and relayed approvals were all
no-ops. They are recorded in `plan-milestones/TESTS.md` and written nowhere.

## Real setup for one person with several projects

1. **One workspace, many projects:** one server is enough. Each repo's
   `### Notion draft surface` block names its own drafts database by ID.
2. **Several workspaces:** Claude Code stores OAuth sign-ins "per endpoint". Two server
   names on `https://mcp.notion.com/mcp` may therefore share one sign-in and reach the same
   workspace. The docs neither confirm nor rule this out. `configure-repo` checks
   `notion-get-self` on every server and refuses to bind across workspaces, so a shared
   sign-in surfaces at setup. Two ways to keep each repo on its own workspace:
   - **Local scope per repo.** `claude mcp add --scope local --transport http notion https://mcp.notion.com/mcp`
     inside each repo, then `/mcp` → Re-authenticate, choosing that repo's workspace.
   - **User scope.** Keep one user-scoped server and rely on the binding check.

   The first real dogfood decides which one works.
3. **claude.ai connectors** load into Claude Code as `mcp__claude_ai_Notion__*` when you sign
   in with a claude.ai account. To keep one away from a project, toggle it off in `/mcp`.

Not covered:
- The real hosted server: its search ranking and its property shapes on create.
- A solo repo whose sign-off role is the user.
- A page edited after its sign-off.
