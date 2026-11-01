# Issue-tracker follow-up questions

Load this file **only when Decision A's tracker is chosen**. The option
definitions, follow-up questions, the write-scope table, and the IC-default
rule all live here so Decision A itself stays short.

## Option definitions

- **github** — repo issues via the `gh` CLI
- **gitlab** — repo issues via the `glab` CLI
- **linear** — issues in Linear, via a connected Linear MCP server (preferred) or the Linear GraphQL API; for teams that track work in Linear rather than in the code host
- **local** — markdown files under `.scratch/<feature>/`, each carrying a `Status:` line; good for solo repos or repos without a remote
- **other** — the user describes their workflow in a paragraph; record it as freeform prose

## PR surface (github/gitlab only)

Follow-up (github/gitlab only): **are external pull requests a request surface?** Explainer: open-source repos often receive feature requests as PRs — a PR is an issue with attached code. If yes, `triage` pulls external PRs into the same queue and state machine. Default: no. Skip the question entirely for linear/local/other — for a Linear shop, requests arrive as Linear issues and any PRs stay in the linked code host, not the triage queue.

## Publish unit (all remote trackers + local)

Follow-up (all remote trackers + local): **Publish unit for approved plans?** Explainer: after `plan-tasks`, the triad can open tracker work. Default **`feature`** — one issue per feature/plan; tasks stay in `tasks.md` (not issues, not default sub-issues). Legacy **`tasks`** (one issue per plan task) is opt-in only — noisy. Recommend **feature**.

## Program sync (when tracker is not `local` / `other`)

Follow-up (when tracker is not `local` / `other`): **Program sync for milestones and roads?** Explainer: `MILE-N` / `ROAD-N` already live in `docs/roadmap/` (optional, local-first). Remote mirrors are optional and easy to spam.

- **local** (default) — no remote milestones/initiatives/Projects for program IDs; feature issues may *cite* ROAD/MILE in the body only.
- **labels** / **project_fields** — put ROAD/MILE as metadata on the feature issue only.
- **initiatives** (or org Project as program board) — for leads who want a remote program view.

## Draft surface (all trackers)

Follow-up: **where do milestone drafts wait for sign-off?** Explainer: `plan-milestones`
drafts each milestone in `docs/roadmap/INDEX.md`. With `notion`, it also writes a page in
one Notion database, the sign-off role signs that page off, and only then do its tickets
reach the tracker.

- **repo** (default): the roadmap file only.
- **notion**: needs a connected Notion MCP server.
  1. Run `notion-get-self` on every connected Notion server, and note the workspace each
     one reaches. Two servers can be signed in to the same workspace: Claude Code keeps
     one sign-in per server URL.
  2. Find the project's drafts database and `notion-fetch` it. Bind it only when
     `notion-get-users` lists the sign-off role in that workspace. Then fill the template's
     `### Notion draft surface` block from what those calls returned.
  3. If the sign-off role is not listed, write **Draft surface** `repo`. Tell the user which
     workspace each server reached, and that the project's own workspace needs a sign-in:
     `/mcp`, then the server, then **Re-authenticate**, choosing that workspace.

  Why step 3 is there: one test made Klynt Labs the only workspace either server could reach.
  All six setups then bound harbor-ledger to Klynt's "Ledger / Roadmap drafts", another
  company's database. Two of them saw that Quang was not a member of that workspace, and
  still wrote him in as the sign-off person.

`plan-milestones` and `refresh-roadmap-status` read only the **Draft surface** row and that
block in `docs/agents/issue-tracker.md`. They never read a Notion binding written anywhere
else. One baseline setup recorded it in a new `project.md` section, and that repo's
drafts would have stayed out of both skills.

## Issue fields (all trackers)

Fill the `Issue fields` table in `docs/agents/issue-tracker.md`. Every row names a write and a read.

On GitHub, run `gh repo view --json isInOrganization`. All four baseline setups wrote "none" for
priority, estimate or both, and a `Blocked by:` line for blocking, so issues on those repos could
never carry the fields. These rows hold on both owner types:

| Field | Write | Read |
|---|---|---|
| Assignee | `gh issue create --assignee <login>` | `gh issue view <n> --json assignees` |
| Status | `gh issue create --label <role string>` | `gh issue view <n> --json labels` |
| Blocking | `gh issue create --blocked-by <n>,<n>` | `gh issue view <n> --json blockedBy` |

**`isInOrganization` true:** priority and estimate are the organization's issue fields. Read their IDs:

```bash
gh api graphql -f query='{organization(login:"<org>"){issueFields(first:20){nodes{... on IssueFieldSingleSelect{id name options{id name}}}}}}'
```

Use these global IDs. The REST list's numeric option IDs are rejected. Write each value after the create,
with the issue's ID from `gh issue view <n> --json id`, and list every option's ID in the row:

```bash
gh api graphql -f query='mutation{setIssueFieldValue(input:{issueId:"<issue id>",issueFields:[{fieldId:"<field id>",singleSelectOptionId:"<option id>"}]}){clientMutationId}}'
```

Read both with `gh api repos/<owner>/<repo>/issues/<n> --jq .issue_field_values`.

The estimate scale is 1, 2, 3, 5, 8. Where `Effort` offers other options, name the change for the
operator, since it reaches every repo in that organization. Until they agree, the estimate row uses
`size:<n>` labels.

**`isInOrganization` false:** `--label priority:<urgent|high|medium|low>` and `--label size:<n>`, read
with `gh issue view <n> --json labels`.

**Labels that do not exist yet:** list them for the operator and create them on their yes.

**Local tracker:** each field is a line in the issue file: `Assignee:`, `Status:`, `Priority:`,
`Estimate:`, and `Blocked by:`.

## Write scope by role

Also record **who is running setup** for write scope:

| Project class / role | Publish unit | Program sync |
|---|---|---|
| Personal / solo owner | offer; default feature | offer; default local |
| Company IC / dev | offer feature if they can open issues | **default local**; do not require them to create Initiatives/Milestones |
| Company lead / PM / admin | offer full matrix | offer full matrix |
| No issue-create permission | skip remote publish / local files only | local only |

If the user is IC or unsure of admin rights, write **Program sync: local** and **Program write role: ic** unless they explicitly opt into a lead path. Never invent remote program objects after a permission failure — degrade and record the fallback in `issue-tracker.md`.
