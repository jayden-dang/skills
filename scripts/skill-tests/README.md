# Skill test fixtures

What the 2026-11-15 `TESTS.md` entries cite. Tracked, because the earlier fixtures lived in a
git-ignored folder and were lost.

| File | What it is |
|---|---|
| `make-quayside.sh` | A small billing repo: three features merged to `dev` this week, 9 tests, a github tracker behind a stateful `bin/gh`. `GATE=1` adds a ticket approver, `FILING=draft` sets Follow-up filing, `DUP=1` and `SHAPE=1` pre-file tickets. Installs the named skills in `.claude/skills/` |
| `make-tidewater.sh` | A ferry-booking repo with a roadmap layer: MILE-1 closed, MILE-2 to MILE-4 committed with every member shipped in v0.3.0, MILE-5 planned. Used for the milestone close and assessment runs |
| `make-fernhollow.sh` | The `evolve-system` fixture with the same tracker shim |
| `gh-shim.py` | The stateful `gh` stand-in; its state lives in `.git/gh.json` |
| `score-inbox.py`, `score-evolve.py` | Score a run from the tracker state, the working tree and what `board.py` prints |
| `routing/listing.py` | The skill listing a session sees |
| `routing/suite.py` | The frozen routing suite: 153 first messages and the skill each should reach |
| `routing/cluster-*.md`, `routing/older-trigger-evals.md` | The messages |
| `retire.py`, `scrub.py`, `dropsent.py`, `routing/unflag.py`, `routing/record.py` | The one-off tools used to unflag, merge and delete skills. `dropsent.py` is blunt: review what it changes |
| `baselines/` | One ticket run from `/idea` through `/shape` and `/go`, before and after the merges |

Throwaway repos set `core.fsmonitor false`: a global fsmonitor stalls git in them.
