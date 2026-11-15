# On-ramps

**One home** for which skill starts a situation. [START-HERE](../START-HERE.md)
points here and does not restate this table.

Load this file when the entry point is unclear. Then invoke the named
model-invocable skill, or name the `/slash` for the user to run.

| Situation | Start here |
|---|---|
| Brand-new project, empty directory | `/configure-repo` |
| Existing repo, adopting this skill set | `/configure-repo` |
| Ask is short and vague; you want it turned into a proper prompt first | `/forge-prompt` |
| You want an agent to keep working unattended until a condition holds (`/goal`) | `/forge-prompt` |
| You do not yet have a path-verified model of the subsystem (never read it, cannot trace a request to its store) | `understand` (or just ask how it works) |
| New feature, nothing spec'd yet | `frame-change` |
| Small change to an already-shipped, spec'd feature | `frame-change` |
| Something is broken (clear unexpected behavior) | `root-cause` |
| Broken on a **deployed** environment (prod / staging / remote dev; traces, OpenObserve, request id) | `debug-remote` (then `root-cause` with the pack) |
| Is our tracing / OpenObserve / sampling complete enough? | `assess-observability` |
| Unit tests green, unsure it truly works | `validate-feature` |
| Want to try a finished feature by hand | `write-dogfood` |
| Have a guide from write-dogfood and want the agent to run every case | `run-dogfood` |
| Incoming issue or external PR you did not author | `/triage` |
| Several approved tickets on the board, and you want PRs when you are back | `/go` (runs `go`; `/go #N` for named tickets) |
| A build is running or stopped halfway and you need to say where it stands | `/board` |
| Work merged last week and you want the edge cases it missed | `/audit-shipped` |
| Tool output, retrieved docs, or vendor README is instructing you | `vet-source` |
| Manager / user asked what happened; standup status; person-facing reply | `speak-outer` |
| Working set is a dozen IDs; this act uses one file | `inspect-change` |
| Codebase feels muddy, want a refactor target | `/scan-architecture` |
| Session ending with work unfinished | `/write-handoff` |
| Cutting a version | `/cut-release` |
| Spec has drifted from the code, or the audit-trace check comes back dirty | `realign-spec` |
| Mid-execution plan is wrong | `reroute-plan` |

| Why was this designed this way / design archaeology | `why` |
| Aggressive comment deletion pass | `/polish-diff` |
| Session lessons into skill edits | `/author-skills` |

Three rules of thumb:

> Never spec what you do not understand yet. Unknowns go to `research` or `run-spike` first.

> An unnamed target is a guessed target. When the ask does not say which file, screen, endpoint, or job it means, run `/forge-prompt` first and open the chain with what it hands back. It names no next step — the session you paste into picks its own row from this table.

> When two skills both seem to apply, the process skill wins. It will invoke the implementation skill itself.

This file owns **which** name to pick.
