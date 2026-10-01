# `/forge-goal`

> Outcome → one launch-ready **`/goal` block** for an unattended run: probed checks, guards, a bound, and `BLOCKED:` / `STOPPED:` lines a separate judge can settle. Works for Claude Code, Codex, or any agent CLI.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/forge-goal`) — agents must never auto-invoke it |
| **Reads** | the repository: scripts, tests, bench commands, contract comments — before asking anything |
| **Runs** | only checks that change nothing (tests, lint, bench, `grep`, `git diff`), once each, to prove they run and are not already green |
| **Writes** | the goal block in chat; edits no file |
| **Calls** | `clarify-decisions` for the interview channel |
| **Called by** | nobody — it sits outside every chain, like `/forge-prompt` |

## Why it exists

`/goal` in Claude Code keeps a session working until a condition holds, and a small model (Haiku
by default) decides after every turn whether it does. That judge "doesn't run commands or read
files independently" — it reads only what the session printed. Codex's `/goal` judges itself
instead, through a completion audit. Either way, a goal is a contract nobody can renegotiate
mid-run.

Without the skill, Sonnet wrote goals that could not end well: no turn or time bound (6 of 6),
"stop and tell me" written beside the condition where the judge never reads it (6 of 6), a mobile
criterion checked "by loading the page" in a repo with no browser, a 400 ms bar the user never
gave, a benchmark it would "build first" when `npm run bench` already existed, and three unrelated
tasks bundled into one run. Full record: `skills/discovery/forge-goal/TESTS.md`.

## What it hands back

```
<the outcome, one line>

Done when — each shown by command output in this session:
- `<command>` → <the output that proves it>

Must hold throughout:
- `<command>` → <the output that proves the guard held>

Stop early — the goal is also over when the last message starts with one of these:
- BLOCKED: <decision only a person can make> — when <situation>
- STOPPED: <progress and what is left> — after <N turns or H hours>

Read first: <paths>
```

Below it: one probe line per command (what it printed, or `[unprobed]` and why), a launch line
per runtime, and every goal it split off.

## How it differs from `/forge-prompt`

| | `/forge-prompt` | `/forge-goal` |
|---|---|---|
| Reader | a person-steered session | an unattended run and, on Claude Code, a tool-less judge |
| Open questions | travel as `Open — ask me` | must close, or become a `BLOCKED:` line |
| Method | never named | still never named — but *how done is proven* is the whole block |
| Done signal | what the user would look at | a command and the output it must print |

## Launching

- **Claude Code:** `/goal <block>` in auto mode (manual mode stops on every tool prompt); headless:
  `claude -p "/goal …"`.
- **Codex:** `/goal <block>` with `features.goals` enabled.
- **Other agent CLIs:** paste the block as the prompt; the `STOPPED:` bound is the only bound.
