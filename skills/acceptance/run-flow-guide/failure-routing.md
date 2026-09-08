# Failure routing

WHEN a driven case is not `pass` — read from `run-flow-guide/SKILL.md` § 4.

Re-drive the failed case once from a clean setup, then classify by observation.
**Master** (this controller) owns case selection, evidence slots, `mark`
pass/fail/blocked, and **re-test** after a fix — never hand those to a fix
subagent.

| Observation | Action |
|---|---|
| Deterministic fail on a real Expect / backend assertion | **Product defect.** Master marks `fail` with full evidence (`saw`/`server`). Dispatch an isolated **subagent** with a red-capable brief only: case id, `req`, try/expect, saw/server, repro — **not** the full session history or long dogfood context. Master does **not** patch product code in the walkthrough session. Subagent **REQUIRED SUB-SKILL: use `root-cause`** (and **test-first**); isolation is **not** a free patch without root-cause. |
| Flaky, or guide wrong (stale label, missing seed, bad Expect) | Fix the case's authored slots in the **run file** (re-`render` the HTML if the human has it open); re-drive. Do not send guide bugs to `root-cause`. |
| Shared precondition broken (login, server down, seed missing) | Stop the run. Leave remaining cases `pending`/`blocked`. Downstream is untested, not passing. |

**On DONE** (subagent reports fixed): control returns to the **master**. Restart
the app if needed, re-drive the failed case from a clean setup, **and** re-drive
every already-`pass` case whose `req` the product fix touched (grep the diff for
requirement IDs or the modules those cases exercise).

**Loops stay separate.** The guide-gap fix loop (`vet-flow-guide`: patch run
file → re-vet) is **not** this product-defect dogfood loop. Guide-gap findings
are **not** routed here — the §2a gate should have blocked drive; if a missing
situation is discovered mid-run, treat it as guide wrong / re-enter vet, not as
a product defect. Product defects do not absorb missing-situation findings.

**Caps (D2):** 3 distinct fix attempts on the same case → stop and escalate.
5 product-defect fix cycles in the whole run → stop with a partial run file.
Do not mark untested cases `pass` to clear the board.

Durable asset for a product fix: the regression test `root-cause` already requires
under TDD — not a silent promotion of the whole guide into Playwright
(`validate-ui` is that path, only if the user asks).
