# Skill test fixtures

What the 2026-11-15 `TESTS.md` entries cite. Tracked, because the earlier fixtures lived in a
git-ignored folder and were lost.

| File | What it is |
|---|---|
| `make-quayside.sh` | A small billing repo: three features merged to `dev` this week, 9 tests, a github tracker behind a stateful `bin/gh`. `GATE=1` adds a ticket approver, `FILING=draft` sets Follow-up filing, `DUP=1` and `SHAPE=1` pre-file tickets. Installs the named skills in `.claude/skills/` |
| `make-tidewater.sh` | A ferry-booking repo with a roadmap layer: MILE-1 closed, MILE-2 to MILE-4 committed with every member shipped in v0.3.0, MILE-5 planned. Used for the milestone close and assessment runs |
| `make-harbourline.sh` | A ferry seat-booking API in Node, with JSON files as the store. `main` has a platform layer whose helpers carry seven defects that `feat/booking` inherits or adds; the comment at the top of the script lists them. Set `HL_PORT` to give each fixture its own port. `VARIANT=b` adds a 403 convention, a documented `stack` field, a race in seat reservation and a cron job that re-queues. `VARIANT=ui` adds a `/book` page. `GH=1` adds a bare origin and `bin/gh` = `gh-pr-shim.py`. `CONFLICT=1` (after `CI=1 GH=1`) opens PR #101 and then lands ACCT-2 on `main`, which conflicts with the branch on the auth method list; `CONFLICT=product` lands KIOSK-3 instead, a conflict whose sides cannot both hold. `CI=1` makes the feature clean, adds a close receipt and `.github/workflows/ci.yml` (`TZ: UTC`), and keeps one fault that only CI sees: the departure time follows the machine's zone. Used for `validate-feature` 1.4.0 to 1.5.0 |
| `gh-pr-shim.py` | A `gh` stand-in for pull-request work: create, view, edit, comment and ready, plus simulated CI. `pr checks`, `run view`, `run rerun` and the merge verdict all run the workflow's `- run:` lines on origin's head. The first run flakes with `ECONNRESET` unless `HL_FLAKE=0`. The first two reads of each head are pending (`HL_PENDING`). Mergeability comes from `git merge-tree`, and branch protection reads answer `required_linear_history` from `HL_LINEAR`. State lives in `.git/gh-pr.json`, and every call is logged to `.git/gh-calls.jsonl` |
| `score-conflict.sh` | `<dir> <start-sha>`: merge state, whether the old head is still in history (no force-push), CI on the tip, and whether both sides of the auth conflict survived |
| `score-tend.py` | `<dir>…`: per PR, the CI verdict on the pushed head, how many heads CI ran on, the forge calls the run made, and whether origin's `main` moved |
| `score-harbourline.py` | `<dir> <port> [start-sha]`: replays each defect against the repo as the run left it, on fresh seed data. Also reads the run's `logs/requests.log` to see which probes were sent |
| `make-fernhollow.sh` | The `evolve-system` fixture with the same tracker shim |
| `gh-shim.py` | The stateful `gh` stand-in; its state lives in `.git/gh.json` |
| `score-inbox.py`, `score-evolve.py` | Score a run from the tracker state, the working tree and what `board.py` prints |
| `routing/listing.py` | The skill listing a session sees |
| `routing/suite.py` | The frozen routing suite: 153 first messages and the skill each should reach |
| `routing/cluster-*.md`, `routing/older-trigger-evals.md` | The messages |
| `retire.py`, `scrub.py`, `dropsent.py`, `routing/unflag.py`, `routing/record.py` | The one-off tools used to unflag, merge and delete skills. `dropsent.py` is blunt: review what it changes |
| `baselines/` | One ticket run from `/idea` through `/shape` and `/go`, before and after the merges |

Throwaway repos set `core.fsmonitor false`: a global fsmonitor stalls git in them.
