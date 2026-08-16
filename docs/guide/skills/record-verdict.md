# `record-verdict`

> Publishes one decision record — immutable payload plus append-only envelope — for a terminal human verdict, **before** the crossing it authorizes is allowed to run.

|  |  |
|---|---|
| **Bucket** | ship |
| **Invocation** | model-invocable, but only from a closed set of callers |
| **Reads** | the caller's inline Write Handoff, `docs/agents/project.md` (`## Decision boundaries` pins, standing verbatim policy), `RECORD.md` beside the skill (the field grammar SSOT) |
| **Writes** | `.skills/decisions/DEC-YYYYMMDD-<token>.md`, and `.skills/decisions/ADOPTION.md` once |
| **Calls** | `validate-records.sh` (`--scan`, then `--mode=publish`) |
| **Called by** | [`land-branch`](land-branch.md) and [`cut-release`](cut-release.md) — nothing else, ever |

## When it fires

When `land-branch` or `cut-release` has a **terminal human verdict** in hand and a crossing is about to happen. The verdicts are a closed set: `merge`, `pr`, `discard`, `block`, `release-approve`, `release-reject`.

The ordering is the whole point, and it has a name — **record-before-crossing**. No valid published record, no crossing.

## The caller gate

Three conditions, all required, or the skill returns with **no artifact**:

1. The caller is `land-branch` or `cut-release`.
2. The hand-off carries a terminal human verdict.
3. Durable evidence arrives as **inline text**, never as a `.skills/`, temp, or session-history locator.

Evidence producers cannot self-promote into emitters. The rationalization table closes the obvious ways around it — *"This approval is important enough to record"*, *"I have a log under `.skills/`"*, *"Skip the record; the merge is urgent"*, *"The senior said skip paperwork"* — and one subtle one worth quoting, because records themselves live under `.skills/`:

> *"Records live under `.skills/`, so `.skills/` paths are citable now"* → Storage location ≠ citable locator; the prohibition is unchanged.

## Depth is a lookup, not an interview

```
depth = max(ceremony floor, boundary floor, predicate escalation)
```

| Source | Floor |
|---|---|
| Tier 1 / mini-spec | Guarded |
| Tier 2 / full triad | Accountable |
| `cut-release` | Accountable |
| Boundary `disposal` | Accountable |
| Any predicate true **or unknown** | escalate to Accountable |

Actual crossings are at least **Guarded**; `Minimal` is never published. All three predicates — external audience, no mechanical undo, persistent stakes — are evaluated even when a floor already fixes the depth, and the agent may only ever *raise* depth, never lower it.

**External audience** carries the strictest rule in the skill: it is `TRUE` only when the output is mechanically established to reach outside the creating-and-approving group, and `FALSE` only from a current, authoritative, exhaustive mechanical source. Anything else is `unknown`, which escalates. A roster, CODEOWNERS, privacy metadata, branch ownership, PR authorship, or a workflow band **never** prove `FALSE`.

## The verbatim law

| Depth | Capture |
|---|---|
| Guarded | The terminal verdict plus ≥1 **verbatim** human judgment element |
| Accountable | The verdict plus **verbatim** accepted risk and **verbatim** response-if-wrong |

Store exact user-authored words only. A bare "yes" or "ok" to an *agent-authored* risk statement is a **verdict only** — not risk text, not response text. And the tempting cleanup is explicitly fabrication:

> *"I'll polish their wording"* → Polish is fabrication under the verbatim law.

Where a user does not want their words in the repo, the element carries a disposition token — `withheld(reference)` with a matching durable locator, or `withheld(unavailable)` — and the payload body becomes the fixed sentinel from `RECORD.md`. A withheld-opaque record is complete, not unfinished.

## Identity and reissue

The ID is `DEC-YYYYMMDD-<token>`, where the token is six Crockford characters from `/dev/urandom` (falling back to `awk` + `$$` + `date`). There is no registry; a collision is simply reissued. The filename stem always equals the effective identity.

Reissue is **append-only**: mint a fresh ID, rename the file, append `Reissued-from:` and `Reissued-as: <new-id> <UTC>`, and leave `Published:` and the payload bytes untouched.

## Publication order

1. Judgment capture → 2. storage resolution → 3. evidence promotion → 4. **exact-payload display and human acceptance** (this locks the payload) → 5. secret scan on judgment prose → 6. mint the ID, write the file, record the payload digest on the envelope → 7. run the validator → 8. **the crossing executes only after the validator exits 0** → 9. append `Execution-Outcome:` to the envelope.

When publication fails, what gets reported depends on whether the verdict has a crossing at all. `merge`, `pr`, `discard`, and `release-approve` do; `block` and `release-reject` do not:

| Verdict class | On failure |
|---|---|
| Has a crossing | Withhold the crossing; report the verdict **not enacted** and name what blocked it |
| `block` / `release-reject` | The verdict stands; report it as **unrecorded** (incomplete accountability) and name what blocked it |
| Published fine, crossing then failed | Append the failure as `Execution-Outcome:` — the record stays valid |

## See also

- [`land-branch`](land-branch.md) — one of the two legal emitters
- [`cut-release`](cut-release.md) — the other
- [`study-change`](study-change.md) — reads published records when reconstructing what was decided
