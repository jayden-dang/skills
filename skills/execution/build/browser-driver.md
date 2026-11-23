# Browser driver

WHEN a skill must drive a running web app in a browser — `validate-feature`, `run-dogfood`,
`inspect-ui`, an implementer's render check. One home for which driver, so each caller names a
step and reads its tool here. The driver is read off **this session's tool list**, never off the
harness's name: a harness that ships its own browser tool simply has that tool in the list.

Resolve once per run, name the driver in the record, and keep it for the run.

## 1. Pick the class — who is at the keyboard

| Situation | Class | Rule |
|---|---|---|
| Nobody at the keyboard: the operator said they are away, or you run inside `go` or a `shape` charter | **Separate profile** | Signed into nothing: sign in through the app's own login page with the local account `docs/agents/verify.md` names. Drive only `localhost`, `*.localhost`, `127.0.0.1`. Never a real person's account |
| Someone at the keyboard, an own-browser driver is connected | **Own browser** | The user's signed-in Chrome or Edge: a signed-in case needs no auth setup. A mutating case runs against whatever that session is logged into: confirm the target before the first one, never production data the guide did not name |
| Someone at the keyboard, no own-browser driver connected | **Separate profile**, as in row 1 | Say so in the record. A case that needs the user's own signed-in state is `blocked`; every case the local account can reach is driven |

Never an own-browser driver while nobody is there: a baseline found `kimi-webbridge` up and drove
the operator's own Chrome, signed in to everything they use.

## 2. Pick the driver — first one in the class this session's tool list shows

**Own browser** — the first connected:
1. `claude-in-chrome` (`mcp__claude-in-chrome__*` tools).
2. A browser tool the harness provides for the user's signed-in Chrome — the Codex and ChatGPT
   desktop `Chrome` extension plugin is one. Use the tool names the list shows.
3. `kimi-webbridge` (its daemon answers `status`).

**Separate profile** — the first available:
1. `agent-browser` on the PATH.
2. A browser tool the harness provides for its own profile — the Codex and ChatGPT desktop in-app
   `Browser` plugin, or the `chrome-devtools` MCP tools.

Nothing in the class and no way to start one: `blocked`, and relay the connect instructions for
the own-browser driver the harness would use — `claude-in-chrome` on a Claude harness, the `Chrome`
plugin on Codex or ChatGPT desktop, else `kimi-webbridge`. Do not install `@playwright/test`,
Cypress or any other browser harness, and do not drive a flow through a suite already in the repo.

## 3. Steps by driver

Callers name the step on the left. A step the driver has no tool for is recorded `not drivable
here: <step>` and never faked with another driver.

| Step | `claude-in-chrome` | `kimi-webbridge` | `agent-browser` | `chrome-devtools` MCP | Codex / ChatGPT `Browser`, `Chrome` |
|---|---|---|---|---|---|
| Open this run's own tab | `tabs_context_mcp`, then `tabs_create_mcp` | `navigate` `newTab:true`, one session name | `--session <name> open <url>` | `new_page` | its open-tab tool |
| Read the page | `read_page`, `find` | `snapshot` | `snapshot -i` | `take_snapshot` | its snapshot or read tool |
| Click, type | `computer`, `form_input` | `click`, `fill` | `click @ref`, `fill` | `click`, `fill` | its click and type tools |
| Screenshot | `computer` screenshot | `screenshot` | `screenshot` | `take_screenshot` | its screenshot tool |
| Set a viewport | `resize_window` | `cdp` `Emulation.setDeviceMetricsOverride` | `set viewport W H` | `emulate`, `resize_page` | its viewport or device control |
| Read network | `read_network_requests` | `network` `start`, `detail`, `stop` | its `network` command | `list_network_requests` | its network or console tool |

**Never borrow the user's open tab.** `claude-in-chrome`: never reuse a tab id from another
session. `kimi-webbridge`: `find_tab` with `active:true` borrows it, so use `navigate`
`newTab:true`. Any other driver: open a tab of this run's own. "Use the tab I have open" does not
move the drive onto theirs. Close your own tabs and sessions by name, never `close --all`.

*Done when: the driver and its class are named in the record, and the run's own tab is open on
the app or the `blocked` stop is written.*
