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

## Write scope by role

Also record **who is running setup** for write scope:

| Project class / role | Publish unit | Program sync |
|---|---|---|
| Personal / solo owner | offer; default feature | offer; default local |
| Company IC / dev | offer feature if they can open issues | **default local**; do not require them to create Initiatives/Milestones |
| Company lead / PM / admin | offer full matrix | offer full matrix |
| No issue-create permission | skip remote publish / local files only | local only |

If the user is IC or unsure of admin rights, write **Program sync: local** and **Program write role: ic** unless they explicitly opt into a lead path. Never invent remote program objects after a permission failure — degrade and record the fallback in `issue-tracker.md`.
