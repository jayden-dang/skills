---
name: record-decision
description: Use when a named production-boundary emitter (finish-branch or
  release) has obtained a terminal human verdict and hands off durable evidence
  for publication.
---

# Record a Boundary Decision

Publish one immutable decision record under `docs/decisions/` for a skill-mediated
terminal verdict — **before** the production crossing executes.

Grammar is defined solely in sibling `RECORD.md`. Do not restate field lists here.

## HARD-GATE — Caller gate

| Required | Reality if missing |
|---|---|
| Caller ∈ {`finish-branch`, `release`} | Return **without** creating an artifact |
| Terminal human verdict in the handoff | Return **without** an artifact |
| Durable evidence (or empty set with explicit none) handed **inline as text** | Do not accept `.skills/`, temp paths, or session-history locators |

Evidence-producing skills cannot self-promote into emitters. Records are emitted
only for verdicts this skill set mediated (ARCH-6) — never for actions a human
took directly outside the workflow.

| Thought | Reality |
|---|---|
| "This approval is important enough to record" | Only finish-branch / release handoffs with a terminal verdict |
| "I have a log path under .skills/" | Promote substance inline first; never cite the path |
| "Skip the record; the merge is urgent" | No crossing without a published valid record (when a record is required) |

**Done when:** caller, verdict, and durable citations are present — or you returned with no file.

## Handoff interface (from emitter)

Accept **inline text only**:

- Verdict: `merge` \| `pr` \| `discard` \| `block` \| `release-approve` \| `release-reject`
- Boundary type, ceremony tier inputs, predicate facts the emitter already knows
- Durable citations (commit IDs, PR refs, `tag name@object-id`)
- Any promotion substance (ephemeral content rewritten as text)

## Depth computation (fixed lookup — no per-crossing interview)

```
depth = max(ceremony-tier floor, boundary-crossing floor, predicate escalation)
```

| Source | Floor |
|---|---|
| Tier 1 / mini-spec | Guarded |
| Tier 2 / full triad | Accountable |
| release | Accountable |
| boundary `disposal` (discard) | Accountable |
| any predicate true **or unknown** | Accountable escalation |

- Every actual boundary crossing is at least Guarded.
- **Minimal is never published** (reserved non-emitting).
- Evaluate all three predicates truthfully even when a floor already fixes depth:
  external audience, no mechanical undo, persistent stakes.
- External audience **TRUE** only when output is mechanically established to reach
  outside the creating-and-approving group; **FALSE** only from a current,
  authoritative, exhaustive mechanical source; otherwise **unknown**. Repo
  privacy, roster, CODEOWNERS, branch ownership, PR authorship, or workflow band
  alone never prove FALSE. No network probes or interviews to lower a value.
  Unprompted user statements may escalate or supply context — never establish
  external-audience FALSE.
- User may escalate depth; agent **never** de-escalates.
- Write every lookup input and result into the record classification fields.

**Pins:** if `docs/agents/project.md` has `## Decision boundaries`, apply rows that
raise a floor or bind an action to a type; ignore any row that would lower a core
floor (one-line notice). Absent section → core table only.

**Done when:** Depth is Guarded or Accountable and all classification fields are filled.

## Judgment elicitation (verbatim law)

| Depth | Require |
|---|---|
| Guarded | Terminal verdict + ≥1 verbatim human judgment element |
| Accountable | Verdict + verbatim accepted risk + verbatim response-if-wrong |

**Iron Law:** store exact user-authored words only — never summarized, improved,
inferred, or manufactured. A bare "yes"/"ok" to an agent-authored risk statement
is a **verdict only**, never risk or response-if-wrong text.

Attach interaction pointers where the harness permits; else `unavailable`.

| Thought | Reality |
|---|---|
| "The user obviously meant this risk" | If they did not type it, it is not human judgment |
| "I'll polish their wording" | Verbatim only — polish is fabrication |

**Done when:** required elements are user-authored bytes or honestly withheld.

## Storage resolution

1. Standing repo-verbatim policy in `project.md` (if any) applies without a quiz.
2. Always offer an explicit withhold.
3. Potentially sensitive prose → one conditional confirmation before repo-verbatim.
4. Show the **exact payload** before acceptance locks it.
5. Withhold + supplied locator → `withheld(reference)` + locator.
6. Withhold without locator → ask **once**; if declined/unavailable →
   `withheld(unavailable)` + `Storage-Reference: unavailable`; continue; never
   re-ask; never block; W-opaque is not unfinished work.
7. Never redact or paraphrase user prose and still label it verbatim — withheld
   uses the fixed sentinel in `RECORD.md`.

**Secret scan:** before any write, pipe judgment prose to:

```bash
sh skills/ship/record-decision/validate-records.sh --scan
```

On hit, only three continuations: **rephrase**, **withhold**, or **stop**.

**Done when:** each judgment element has exactly one storage disposition.

## Evidence and promotion

Cite only durable kinds (`commit|tag|pr|ci|release`). Tag form:
`<ref-name>@<object-id>` (both halves required). Never cite `.skills/`, temp logs,
absolute local paths, or session history.

When promoting ephemeral substance, write it into `Promoted-Evidence:`
(agent-authored) **before** exact-payload display. Never present promoted text as
human judgment. Evidence after lock → `Execution-Outcome:` envelope append only.

## Minting (publication time)

1. Lock `Accepted:` UTC (date → `YYYYMMDD` for the ID).
2. Token = 6 Crockford chars from local entropy:
   - Prefer `/dev/urandom` via `od`
   - Else POSIX `awk` `srand()` mixed with `$$` and `date +%s`
3. ID = `DEC-YYYYMMDD-<token>`. No registry, no counter. Collisions → reissue.

**Reissue (append-only):** on E-dup collision, for exactly one file: mint a fresh
ID, rename the file, append `Reissued-from:` + `Reissued-as: <new-id> <UTC>`.
Never rewrite `Published:` or payload bytes.

## Adoption anchor (first write only)

If any record would publish and no content-marked anchor exists
(first non-blank line exactly `# Decision-Record Adoption Anchor`):

1. Write `docs/decisions/ADOPTION.md` once with `Cutoff:` (UTC now) and
   `Baseline-Tag: <name>@<object-id>` for each currently visible tag.
2. Never edit the anchor afterward. Never infer adoption from the earliest record.

## Publication checklist (record-before-crossing)

1. Judgment capture  
2. Storage resolution  
3. Evidence promotion (if any)  
4. Exact-payload display → human acceptance (locks payload)  
5. Secret scan on judgment prose  
6. Mint ID; write file; compute payload digest into envelope  
7. Run validator:

```bash
sh skills/ship/record-decision/validate-records.sh --mode=publish --record <file>
```

8. **Crossing executes only after the validator exits 0** on the published file  
9. Append execution outcomes to the envelope (`Execution-Outcome:`)

### Failure semantics

| Failure | Action |
|---|---|
| Secret-scan stop, missing judgment, validator exit 1 or 2, write failure | **Do not** execute the crossing; report verdict not enacted / crossing did not occur |
| Retry | Reuse captured human contributions **verbatim** — never regenerate them |
| Block/reject record cannot publish | Report unrecorded terminal verdict and incomplete accountability (no crossing side effect to withhold) |
| Publish OK, crossing later fails | Append failure as `Execution-Outcome:`; record stays valid |

**Done when:** a validator-clean file exists under `docs/decisions/` before any
merge/PR/discard/release side effect required for this verdict — or the crossing
was withheld with an honest report.

## Crossing-without-record (severity ceiling)

Absence of a record for a production action is never a mechanical **error** —
trace cannot prove skill mediation vs direct human/external action (ARCH-6).
If noted, treat as **warning-level only**, never a gate-failing error.
