# `inspect-change` — Standards axis: production readiness (items 19–24)

Model roster: Sonnet. Fixture: a diff adding tier-aware pricing behind an env
flag — an uncapped retry loop, a swallowed fallback to the old path, an
opt-*out* flag, a migration dropping `NOT NULL` on a column two external
webhook partners read, and three callers left on the old path **in files the
diff does not touch**.

## RED — S-PROD (frame gap)

**Observed (1/1).** Twelve findings, all twelve smells walked with explicit
HIT verdicts, plus one security finding. Strong code review.

Zero hits across the operational frame — grep over the report:

| rollback | down migration | observability | metric | monitor | alert | unsafe default | opt-in/out | feature flag | webhook | partner | blast radius |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The uncapped retry was reported as **"comment compensating for bad code"** — a
comment smell — not as a checkout request that hangs forever when the config
service is down. The migration was reported as **"dead code"**, never as an
irreversible constraint drop on an externally-read column.

**Failure class.** Reads the hunk, not the running system.

## GREEN v1 — production-readiness section added → **regression**

**Observed.** All six operational items fired correctly. But part (b) collapsed:
only 4 of 12 smells evaluated, no per-smell verdicts. Adding a fourth
obligation to an already-dense run-on brief crowded out the "in turn" walk.

**Failure class changed** to *output has the wrong shape* → per the failure
table the form is a contract, not a longer sentence.

## REFACTOR — brief restructured into a four-part output contract

Parts (a)–(d) in order, each complete before the next; part (b) requires a
verdict line per smell **including non-hits**; the loophole named explicitly:
"Adding a later part never licenses shortening an earlier one."

**Observed (post-refactor).** 14 findings. All 12 smells carry verdict lines;
all 6 production items fire. Both axes hold simultaneously.

**Meta-test:** "the text was clear." Agent quoted the loophole-closing line as
what kept it walking all twelve, and the item-24 "a diff-only reading always
returns a false clean" clause as what sent it to read the three untouched files.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Production-readiness section, scoped to diffs changing runtime behavior/storage/contract/config | RED: 0 operational findings; GREEN: 6 |
| Item 24 MUST be answered from a search **beyond the diff** | RED missed 3 unmigrated callers; GREEN found all 3 in untouched files |
| Part (b) needs a verdict line per smell, non-hits included | GREEN v1 regressed to 4/12; post-refactor 12/12 |
| "Adding a later part never licenses shortening an earlier one" | The exact regression v1 exhibited; agent cited this line as the fix |
| Two-axis verdict preserved — production readiness sits inside Standards, like Security | No description change; no third hard axis introduced |

## Known open (not fixed — no baseline failure recorded)

Meta-test surfaced a *pre-existing* ambiguity in the Security section's
trigger: whether an unvalidated response from an internal service URL counts
as "untrusted input". The agent judged correctly but re-read the trigger to
confirm. Needs its own RED before any edit.
