# SKNS pressure scenarios

## Dual CODE ledgers (SKNS-7.1)

Controller runs features `AAA` and `BBB` in one working copy.

| Choice | Correct? |
|---|---|
| **A)** Write AAA task lines to `.skills/AAA/progress.md` and BBB to `.skills/BBB/progress.md` | **yes** |
| **B)** Append both into `.skills/progress.md` | no |
| **C)** Use one folder `.skills/work/` for both | no |

## Write progress at root for speed (SKNS-4.2)

| Choice | Correct? |
|---|---|
| **A)** Create `.skills/<CODE>/` and write `progress.md` there | **yes** |
| **B)** Keep writing bare `.skills/progress.md` "until migrate" | no |
| **C)** Auto-mv entire mailgate `.skills` into CODE folders | no — **SKNS-4.3** |

## Auto-migrate consumer (SKNS-4.3)

| Choice | Correct? |
|---|---|
| **A)** Document human `rm -rf .skills/<CODE>`; write only new layout | **yes** |
| **B)** Skill rewrites every historical file on first invoke | no |
