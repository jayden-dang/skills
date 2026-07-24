# Discovery Digest — Boundary Decision Records ("Own the Outer Loop" capability)

**Approved location (on adoption):** `docs/specs/2026-07-24-decision-records/discovery.md` — an optional, non-normative handoff artifact colocated with this feature's triad. `requirements.md` remains the normative specification; this file's existence sets no precedent requiring discovery records for future features.

## 1. Objective and primary failure

`[Agent-authored synthesis of user-ratified framing]`

Extend the skill set with an answerability backbone at production boundaries. Primary failure, as ratified `[User decision — verbatim]`:

> "Current verdicts leave no durable evidence that a human actually contributed the judgment that only the outer-loop owner can provide."

Supporting context:

- `[Verified evidence]` Source-article research: `docs/research/2026-07-23-own-the-outer-loop.md` (the X post is a cross-post of Osmani's Substack original, "Own the Outer Loop," 2026-07-09).
- `[Agent analysis — agent-authored repository inspection, no durable audit artifact]` An in-conversation gate inspection across the lifecycle skills reported eight points lacking a durable decision record — among them: finish-branch executes a four-option human verdict and records nothing; code-review's "Ready to merge?" verdict evaporates with the conversation; dogfood results persist only in browser localStorage; `.skills/` decision ephemera are git-ignored by design; `release` alone leaves a durable trail (tag + CHANGELOG + INDEX status). These findings were read from `skills/*/SKILL.md` sources during discovery but were not preserved as a citable audit artifact; requirements work should treat them as claims to re-verify against the skill files, not as evidence.

## 2. Ceremony tier

`[Agent analysis, user-adopted via exit ratification]`

**Tier 2 — full triad.** Multi-skill, multi-artifact work: one new skill (`record-decision` + `RECORD.md` + validator), edits to `finish-branch`, `release`, `trace`, `interpret`, a new durable artifact class (`docs/decisions/`), and mandated RED-baseline testing per component. Not reducible to a mini-spec.

## 3. Ratified decisions in final form

`[Agent-authored synthesis; each ratified by explicit user decision — verbatim cores in §4]`

**D1 — Backbone.** Answerability records at production boundaries, with comprehension/sampling as supporting mechanism and boundary generalization deferred. A valid record requires a human judgment contribution the agent's reports cannot supply.

**D2 — Two-tier assurance.** Record *absence* and malformation are caught mechanically (trace). Human *provenance* — not absolute authenticity — is held by a verbatim-only Iron Law: exact user-authored words, a pointer to the originating interaction where the harness permits, never summarized/improved/inferred/manufactured. A user replying "yes" to an agent-authored risk statement counts as verdict only, never as human-authored risk acceptance or response-if-wrong.

**D3 — Depth model.** Three depths: Minimal (verdict only), Guarded (verdict + one verbatim judgment element), Accountable (verdict + verbatim accepted risk + verbatim response-if-wrong). `depth = max(ceremony-tier floor, boundary-crossing floor, predicate escalation)`. Every actual crossing is at least Guarded; Minimal is reserved for work not yet affecting a dependent system — **and is therefore a reserved, non-emitting state in v1: because v1 records exist only at terminal boundary verdicts, `finish-branch` and `release` must never publish a Minimal record.** Tier 1 ≥ Guarded; Tier 2 and release ≥ Accountable. Three effect-predicates escalate to Accountable with OR semantics: **external audience** (recipient outside the group directly creating and approving the artifact), **no mechanical undo** (no known agent-runnable operation restoring prior externally observable state — attempted compensation doesn't count), **persistent stakeholder/dependent-system stakes** (permissions, availability, organizational data, money, obligations, downstream state). **Unknown is not false → Accountable**; no per-crossing risk interview exists anywhere. The record states: crossing-exists, boundary type, each predicate true/false/unknown with its supporting observable fact, ceremony floor, resulting depth, any user escalation. Consuming repos may pin actions to types or higher floors in `project.md`; nothing can lower core floors. User may escalate; agent may never de-escalate below the lookup result.

**D4 — Substrate.** `docs/decisions/`, one immutable file per record; the single global substrate and single logical trace target. Feature/requirement IDs are outward citations, never storage ownership. Each record splits into an **immutable payload** locked at human acceptance (boundary classification, human-authored contribution, verdict, accepted risk, response-if-wrong, evidence pointers as observed) and an **append-only provenance envelope** (publication ID + timestamp, storage disposition, reissue history, supersession/retirement references). Even typo fixes to the payload require an explicit correction/supersession event.

**D5 — Identity.** `DEC-YYYYMMDD-<token>`: date = acceptance date; token = 6-char Crockford base32 from local entropy, independently generatable on parallel branches, no semantic content. Semantics live in `Scope:` / `Boundary-Type:` fields. Content immutable from acceptance; ID immutable from publication; a collision reissue appends to the envelope (`Reissued-from:`) — recorded, never silent. Optional human-browsing index is a regenerable derived projection, never authoritative. **Mandatory pressure-test list** (no durable RED/GREEN evidence exists yet; in-conversation analysis only — the plan must test each): two parallel branches same day; two records for the same feature and boundary; orphan/global crossings; taxonomy renames; long-lived branches; collision detection at merge; reissue without mutation of the accepted payload.

**D6 — Storage classes.** `repo-verbatim` (default; standing policy where configured, explicit withhold mechanism, conditional confirmation for potentially sensitive prose — no per-gate storage quiz; exact payload visible before publication) / `withheld(<ref>)` (judgment off-record, but its existence and disposition on-record) / **blocked** (deterministic secret scan; on a hit the agent may only ask the user to rephrase, accept withhold, or stop — never redact or paraphrase and still label verbatim). The withheld-reference fork — whether every withheld judgment requires a durable opaque reference, or `withheld(unavailable)` is valid and necessarily produces W-opaque — is an explicit requirements/design decision (§9), not one the validator may invent.

**D7 — v1 emitters.** Exactly `finish-branch` and `release`. Emission rule `[User decision — verbatim]`: *"A v1 emitter creates one decision record when a human issues a terminal verdict at a production boundary"* — including terminal block/reject verdicts; excluding mechanical gate failure without a verdict, pause/defer, finish-branch "keep", and unfinished releases. finish-branch: merge, PR, discard, and explicit block emit; keep does not. release: at most one record; version/build/smoke/tag approvals are evidence inside it. Records may cite only evidence durable after publication (committed artifacts, immutable commit IDs, stable CI/PR/release refs, or evidence promoted into the record) — never `.skills/`, temp logs, local paths, or session history. **Evidence promotion**: an emitter may write an ephemeral artifact's substance into the record payload; promoted summaries remain **agent-authored evidence, never human judgment** ("digest" is reserved for interpret's end-of-session artifact). Spec approvals and correct-course are **not** emitters in v1.

**D8 — Pressure rulings (doctrine worked-examples).** A verdict issued against red evidence still emits — emission keys on the verdict, never the evidence's color. The finish-branch menu gains an explicit terminal block/reject option distinct from keep. Boundary-type vocabulary includes `disposal` (discard is Accountable via unknown-undo). The ledger covers **agent-mediated** crossings of agent-produced work only; a human acting directly by their own hand needs no agent record. Payload locks at the terminal verdict; post-verdict execution outcomes (tag hash, PR URL) append to the envelope. *(Exact PR boundary classification is open work — see §9; no universal ruling on the external-audience predicate for PR creation is ratified.)*

**D9 — Doctrine home.** `skills/ship/record-decision/` with `SKILL.md` (operational doctrine: valid-emitter gate, terminal-verdict rule, boundary lookup, depth computation, judgment elicitation, verbatim law, storage handling, acceptance lock, ID minting, reissue, write, validation) and `RECORD.md` (sole grammar: fields, allowed values, payload/envelope split, syntax, storage classes, evidence-pointer rules, reissue/supersession entries) behind a strong sibling pointer; no grammar duplication in SKILL.md. Emitters carry no copied doctrine — `REQUIRED SUB-SKILL: use record-decision`, handing over the terminal verdict plus durable evidence. Model-invoked with a trigger-narrow description (*"Use when a named production-boundary emitter has obtained a terminal human verdict and hands off durable evidence for publication"* — no generic "important decision"/"approval" triggers). Runtime caller gate: v1 emitters are a closed set; no terminal human verdict → no record; evidence producers cannot self-promote to emitters; invalid invocation returns without an artifact. No root template; if ever needed, a generated projection with an equivalence check.

**D10 — Trace extension.** Errors: **E-dup** (duplicate DEC ID), **E-grammar** (missing/invalid required field for declared depth, illegal enum values, missing Storage, empty Accountable judgment fields), **E-spine** (citation of unknown feature/requirement IDs; also owns syntactically-valid-but-broken durable pointers) — **E-spine applies only when the consuming repository has the relevant spine enabled; without that optional layer it no-ops rather than errors (ARCH-2).** Warnings: **W-uncited-tag** (post-adoption tag no record cites), **W-repeated-judgment** (≥3 byte-identical verbatim human-contribution fields across Guarded/Accountable records, exact equality after line-ending/boundary-whitespace normalization only — no fuzz, no LLM; reports IDs; advisory; never asks anyone to diversify the human's words; ignores verdict words and Minimal records), **W-opaque** (validly recorded but non-repo-auditable withheld judgment). Crossing-without-record stays warning-level — trace cannot distinguish agent-mediated from direct human action; emission enforcement lives in the emitters (ARCH-3-consistent). **Adoption anchor — ratified principles only:** exactly one anchor; an explicit and immutable cutoff; no earliest-record inference; zero or multiple anchors once adoption exists are errors. *(The cutoff's exact representation and the tag-comparison mechanism are open — see §9; no proposed value has yet been shown deterministic across shallow clones, rebases, cherry-picks, and backfill.)* A small shipped LLM-free validator (single file, stdlib-only) beside `RECORD.md`, invoked by trace with fixed diagnostics and exit rules, is preferred over shell pipelines.

**D11 — interpret upgrades.** (a) Compact visible ledger, updated only on decision events, showing Decided / Open / Rejected-deferred; full rationale reserved for the end-of-session digest. (b) Block-level claim labels: Source claim / Verified fact / Inference / Recommendation / User decision / Open question. (c) Rationale capture only when ≥2 live options exist AND the choice closes a meaningful branch or fixes a constraint AND the user hasn't already stated their reason — one short question; verbatim quote if already supplied; `Human rationale: not supplied` on decline; never inferred from an accepted recommendation. (d) End-of-session digest with seven provenance labels (User decisions / Human rationale — verbatim / Verified evidence / Interpret analysis — agent-authored / Open questions / Prepared reply — agent-authored / Transport-adoption status). Human-carried transport proves **adoption, not authorship**; agent analysis stays agent-authored after adoption. interpret remains read-only toward the project repo — never commits, never publishes, never an emitter. Risk-weighted depth compression deferred.

**D12 — Exit protocol.** This discovery record → user review and explicit adoption → fresh session reads it + repo context → invokes `write-requirements` directly. Ratified decisions reopen only on new evidence or genuine contradiction, never because the session is fresh.

## 4. Verbatim user decision cores

`[Human rationale — verbatim]`

- D1: *"The primary failure is not merely 'we lack durable decision records.' A record by itself can become accountability theater."*
- D2: *"A verbatim-only Iron Law establishes human provenance, not absolute authenticity. Name that trust tier honestly."*
- D3: *"Unknown is not false."* / *"The canonical ID should provide identity, not summarize mutable taxonomy."* (D5)
- D4: *"A single append-only ledger becomes a hot file in a skill set explicitly designed for parallel branches and agents."*
- D7: *"A v1 emitter creates one decision record when a human issues a terminal verdict at a production boundary."* / *"An evidence-producing skill cannot promote itself into an emitter."* (D9)
- D10: *"Call it `W-repeated-judgment`, because the mechanical observation is exact repetition, not proof of ritualization."* / *"'Fixed rg/git pass' should mean fixed deterministic commands with fixed diagnostics and exit rules, not necessarily one clever `rg` expression."*
- D11: *"Human-carried transport does not make the digest 'human provenance by construction.' It proves human transport or adoption, not human authorship."*

## 5. Agent-authored analysis and recommendations

`[Agent analysis — agent-authored]`

Contributed by the agent and adopted only as reflected in §3: the eight-point gate inspection (§1 caveat applies); the four-loops assessment (constraints strongest, sampling weakest); the three-architecture comparison (doctrine-edits / new-skill / spine-extension) and the observation that D9 is "Approach B minified and inverted"; the effect-predicate formulation; the self-describing-anchor idea (now open work per §9); the evidence-promotion default; the taxonomy-rename argument that eliminated semantic filenames; the agent-mediated-crossings scope line; the since-demoted PR-reviewers inference.

## 6. Rejected alternatives and why

`[Agent record of user rulings]`

Comprehension-as-backbone (supporting mechanism instead); boundary-generalization-as-backbone (no observed baseline failure; writing-skills forbids authoring for hypotheticals); single append-only ledger (hot file, tail conflicts, unbounded growth, neighbor-corrupting malformation); per-feature records + fallback (split chronology, two trace targets); YAML/JSONL substrate (hostile to verbatim human prose); sequential `DEC-N` (collision routine under parallel work); `DEC-date-slug` semantic IDs (collisions merely rare, orphans homeless, stale taxonomy fossilized in immutable filenames); semantic-filename variant (same taxonomy fossil); spec-approval emitters (not crossings; dilutes the boundary model); embed-doctrine-in-finish-branch (SSOT violation in slow motion); ARCH-invariant delivery (optional layer → absent doctrine); mandatory pin table (ARCH-2 violation); per-crossing risk assessment (silent under-escalation under pressure); per-gate storage quiz (quiz creep); uncited-tag as error (false-positives on legitimate direct human tags); dropping W-repeated-judgment (loses the one mechanical repetition signal); root record template (duplicated grammar or forbidden cross-folder link).

## 7. Deferred scope

`[User decision]`

Boundary generalization to publish/send/migrate/policy crossings (needs an observed baseline of the same failure there); `correct-course` as emitter (its ephemeral-history gap is a separate baseline to investigate); advisory derivability check on judgment fields (only if transcripts show an evasion the Iron Law misses); interpret risk-weighted depth (needs observed fatigue and a sharper predicate); generated record-template projection.

## 8. Cross-cutting constraints

`[Verified against AGENTS.md and docs/architecture]`

Project-agnostic: no assumptions of git branches, PRs, web apps, test frameworks, or deployment-shaped boundaries; git-dependent passes no-op without git (ARCH-2 pattern). Mechanical lane stays LLM-free (ARCH-1). No hard headless gates (ARCH-3) — enforcement is pressure-tested gate discipline; trace makes drift visible. Immutability via the payload/envelope split extends the ARCH-4 ID-immutability ethos. Model-invoked `record-decision` is reachable from both v1 emitter types: model-invoked `finish-branch` and user-invoked `release`. This is ARCH-5-consistent because both may invoke a model-invoked sub-skill; the prohibited direction is a model-invoked skill attempting to invoke a user-invoked skill. All authoring falls under the writing-skills Iron Law: RED baselines before any text, one skill at a time, trigger tests both directions, no-op sweep, token budgets.

## 9. Remaining open decisions (for the triad)

`[Open questions]`

Exact verdict enum (Osmani's six mapped onto the extended finish-branch menu); initial `Boundary-Type` table and pin-entry syntax for `project.md`; **exact PR boundary classification** (whether/when PR creation fires the external-audience predicate — repository readers, CI/bots, notifications, and public repos may all matter; the reviewers-inside-approval-group inference is context-dependent, not ratified); **adoption-anchor cutoff representation and tag-comparison mechanism** (must be shown deterministic across shallow clones, rebases, cherry-picks, backfill); **withheld-storage fork** (durable opaque reference required vs. `withheld(unavailable)` valid + necessarily W-opaque); validator language (python3 stdlib vs POSIX sh) and its fixture set; feature code for `docs/specs/INDEX.md` (candidate: `DREC`); `RECORD.md` field grammar in full; the "interaction pointer where the harness permits" format; the secret-scan pattern set; exact wording of the emitters' hand-off prose and the evidence-promotion recipe; **convention update** — if repository documentation states a spec directory contains exactly the three triad files, the plan must include the doc change admitting optional non-normative `discovery.md`.

## 10. Provenance

Labeled inline per section. Everything in §3 is agent-synthesized from decisions the user explicitly ratified across nine interview rounds; §4 is verbatim; §5 is agent-authored; §1's repository inspection is agent-authored analysis, not durable evidence. Adoption of this record does not convert any agent-authored content to human-authored.

## 11. Requirement-coverage checklist for write-requirements

Each must map to ≥1 EARS criterion: ☐ emission rule incl. terminal-block and red-evidence cases ☐ non-emission exclusions (keep/defer/mechanical-failure/unfinished-release) ☐ Minimal as reserved non-emitting state in v1 ☐ depth formula + floors + three predicates + unknown→Accountable ☐ verbatim law + yes-counts-as-verdict-only ☐ agent-never-de-escalates / user-escalate-only ☐ payload immutability + envelope append-only + supersession-for-typos ☐ ID format, two-phase immutability, recorded reissue + the seven-scenario pressure-test list ☐ three storage classes + secret-scan block + no-redact-as-verbatim + resolved withheld fork ☐ durable-evidence-only citation + evidence promotion (agent-authored, never human judgment) ☐ caller gate (closed set, no self-promotion, no-artifact return) ☐ three E-passes (E-spine ARCH-2-conditional) + three W-passes with exact semantics ☐ adoption-anchor principles + resolved cutoff mechanism ☐ validator determinism (fixed diagnostics, exit rules, LLM-free) ☐ finish-branch menu extension ☐ release single-record rule ☐ PR boundary classification resolved ☐ interpret ledger/labels/rationale-capture/digest + read-only posture ☐ ARCH-2 no-op behavior where layers absent.

## 12. Terminal handoff state

- **Discovery status: Complete**
- **Next required skill: `write-requirements`** (fresh session; read this record + current repo context; invoke directly)
- **Do not restart `brainstorm` without new evidence invalidating a ratified decision.**

---

## Correction 1 — Participant model (2026-07-24)

`[Ratified correction — new evidence, explicitly approved by the user during the write-requirements session; appended without rewriting the adopted text above]`

**New evidence.** Repository membership does not imply skill-set membership. A repository may contain people using this skill set, people using other workflows or none, bots and automation, and external contributors whose PRs enter without any of this methodology's trace, TDD, or decision-record discipline. This invalidates one clause of D8 and requires clarifications to D3 and D7; all other ratified decisions stand.

**C1 — Participant model and never-infer rule.** Three project-agnostic roles, defined once in a global SSOT: **skill-mediated actor** (a person acting through this skill set; only the workflow this set actually mediates may be enforced or recorded), **external contributor** (a person or bot supplying an artifact with no assumption this skill set produced it), **accountable reviewer** (the person using this skill set to independently verify an inbound contribution and issue the terminal accept/block/reject verdict). Skill-set membership is never inferred from repository membership, team roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts.

Runtime law `[User decision — verbatim]`:

> "Never infer use of this skill set from repository membership, team roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts. Enforce this set's process only for actions it mediates. Treat external contributions as untrusted input: author claims are supplied evidence, while the accountable reviewer independently verifies the contribution before issuing a terminal verdict. Record only explanations the author actually supplied; never certify that the author understands the whole contribution."

**Delivery surfaces (user-ratified).** Four separate enforcement surfaces, not permission to copy the doctrine into every skill: (a) **ARCH-6** as the citable architecture invariant in `docs/architecture/INDEX.md`; (b) the full three-role narrative in the appropriate architecture domain file; (c) a concise but semantically complete runtime law in `AGENTS.md` — not a blind pointer; (d) the smallest session-injected projection needed in `using-skills`, so the rule survives harnesses where AGENTS.md is never loaded. ARCH-6 alone is insufficient because the architecture layer is optional in consuming repos under ARCH-2. Only skills whose behavior changes operationalize the rule. The eventual plan must include drift/pressure checks for the alignment of these four surfaces.

**C2 — D8 amendment.** Ledger scope keys on **terminal verdicts mediated by this skill set, regardless of artifact provenance**; direct human action outside the workflow still requires no agent record. *Precedence: where this correction conflicts with D8's original artifact-provenance scope sentence ("agent-mediated crossings of agent-produced work only"), this correction supersedes that clause.*

**C3 — D3 clarification.** Approval-group membership for the external-audience predicate is never inferred from repository metadata (the never-infer rule applies). Absent a current, authoritative, and exhaustive mechanical source establishing every reader and notification recipient is inside the group, the predicate is UNKNOWN; UNKNOWN escalates to Accountable per D3, and predicate evaluation stays truthful and independent of the resulting depth.

**C4 — D7 clarification.** finish-branch's PR option is **outbound PR creation** of skill-mediated work. **Inbound PR acceptance has no v1 emitter.** External contributions do not violate this methodology merely by lacking DEC records, requirement IDs, or TDD reports.

**C5 — Deferred: `review-contribution` capability (extends §7).** Reviewing an inbound contribution created outside the trusted workflow — untrusted-input handling, author claims separated from reviewer observations, narrowly scoped author-authored rationale where comprehension matters, independent inspection and verification, standards/spec/acceptance checks where applicable, an evidence-backed recommendation for the accountable reviewer, and the terminal-verdict record — is a separate Tier-2 follow-up feature. `[Agent analysis — overlap audit, 2026-07-24, re-verifiable against the skill files]`: triage owns inbound PR orientation today but issues no verdict and leaves no record; code-review's "Ready to merge?" verdict evaporates and its Spec axis assumes the repo's own spine; receive-review handles the opposite direction; acceptance-check and finish-branch assume workflow-produced branches. Its evidence-provenance grammar (`supplied-by-author` vs `mediating-agent-observed`) is **deferred with it**: no v1 emitter accepts inbound PRs, so no v1 record needs the field, and the follow-up feature can add grammar fields for new records without mutating old payloads.

**Provenance.** C1–C5 ratified by explicit user decision on 2026-07-24; the runtime law is verbatim user-authored; the overlap audit in C5 is agent-authored analysis. This correction supersedes only the clause named in C2.
