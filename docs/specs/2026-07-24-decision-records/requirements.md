# Requirements: Boundary Decision Records

Feature code: DREC
Status: Approved
Date: 2026-07-24

Discovery handoff (non-normative): [`discovery.md`](./discovery.md) including
**Correction 1 — Participant model (2026-07-24)**. This file is the normative
specification. Depth names (`Minimal` / `Guarded` / `Accountable`), storage
dispositions, and pass names (`E-dup`, `E-grammar`, `E-spine`, `W-uncited-tag`,
`W-repeated-judgment`, `W-opaque`) are ratified vocabulary; exact field tokens
and enum members beyond those named here are design-level (see "Carried to
design").

## 1. Record substrate and immutability

**Story:** As an auditor of production decisions, I want each decision record
stored as one immutable file in a single global substrate, so that human
judgments stay durable, tamper-evident, and mergeable across parallel branches.

- **DREC-1.1** THE SYSTEM SHALL store every decision record as exactly one file under `docs/decisions/`, the single global substrate and single logical trace target for decision records.
- **DREC-1.2** THE SYSTEM SHALL structure every decision record as an immutable payload plus an append-only provenance envelope, as defined solely in `RECORD.md`.
- **DREC-1.3** WHEN a human accepts a record THE SYSTEM SHALL lock the payload (boundary classification, human-authored contribution, verdict, accepted risk, response-if-wrong, evidence pointers as observed) against any subsequent in-place edit.
- **DREC-1.4** IF a payload defect is discovered after acceptance (including a typo) THEN THE SYSTEM SHALL correct it only through an explicit correction/supersession event that identifies exactly what it supersedes, appends to the envelope, and leaves the accepted payload bytes unchanged.
- **DREC-1.5** WHEN a post-verdict execution outcome becomes known (for example a tag hash or PR URL) THE SYSTEM SHALL append it to the provenance envelope, never to the locked payload.
- **DREC-1.6** THE SYSTEM SHALL treat feature and requirement IDs inside records as outward citations only, never as storage ownership or file-location keys.
- **DREC-1.7** WHERE a human-browsing index of decision records exists THE SYSTEM SHALL treat it as a regenerable derived projection, never as an authoritative source.
- **DREC-1.8** WHEN a record carries correction/supersession events THE SYSTEM SHALL let readers and the validator derive exactly one deterministic effective view of the record while the original payload bytes remain preserved.

## 2. Record identity and reissue

**Story:** As a maintainer running parallel branches and agents, I want record
identity minted locally with collisions handled loudly, so that identity never
requires coordination and never mutates silently.

- **DREC-2.1** WHEN publishing an accepted record THE SYSTEM SHALL mint its ID as `DEC-YYYYMMDD-<token>`, where `YYYYMMDD` is the payload acceptance date and the token is a 6-character Crockford base32 value from local entropy carrying no semantic content.
- **DREC-2.2** THE SYSTEM SHALL keep record semantics in payload fields (`Scope:`, `Boundary-Type:`), never encoded in the ID or the filename.
- **DREC-2.3** WHILE parallel branches mint records on the same day THE SYSTEM SHALL require no coordination, counter, or registry for ID generation.
- **DREC-2.4** WHEN a merge surfaces two records bearing the same ID THE SYSTEM SHALL reissue one under a fresh ID with a `Reissued-from:` entry appended to its envelope, leaving the accepted payload unmutated.
- **DREC-2.5** THE SYSTEM SHALL treat a record ID as immutable from publication: a collision is resolved only by recorded reissue, never by silent rename or in-place mutation.
- **DREC-2.6** THE SYSTEM SHALL accept multiple valid records citing the same feature and the same boundary type.
- **DREC-2.7** THE SYSTEM SHALL accept records for orphan or global crossings that cite no feature or requirement ID.
- **DREC-2.8** WHEN the boundary-type vocabulary is later renamed THE SYSTEM SHALL continue to treat previously accepted records as grammar-valid without payload mutation.
- **DREC-2.9** WHEN a record minted on a long-lived branch is merged later THE SYSTEM SHALL preserve its original acceptance-dated ID without re-dating.

*The seven ratified pressure scenarios map: parallel same-day → 2.3; same
feature+boundary → 2.6; orphan/global → 2.7; taxonomy renames → 2.2/2.8;
long-lived branches → 2.9; collision detection at merge → 2.4 and 11.1; reissue
without payload mutation → 2.4/2.5.*

## 3. Boundary classification and depth

**Story:** As the outer-loop owner, I want record depth computed from ratified
floors and effect predicates with unknowns escalating, so that ceremony can
never be silently under-scoped.

- **DREC-3.1** WHEN an emitter hands off a terminal verdict THE SYSTEM SHALL compute record depth as `max(ceremony-tier floor, boundary-crossing floor, predicate escalation)`.
- **DREC-3.2** THE SYSTEM SHALL assign at least Guarded depth to every actual boundary crossing.
- **DREC-3.3** THE SYSTEM SHALL apply depth floors of Guarded for Tier 1 work, Accountable for Tier 2 work, and Accountable for release.
- **DREC-3.4** THE SYSTEM SHALL treat Minimal as a reserved, non-emitting depth in v1: neither `finish-branch` nor `release` ever publishes a Minimal record.
- **DREC-3.5** WHEN classifying a crossing THE SYSTEM SHALL evaluate three effect predicates with OR semantics — external audience, no mechanical undo, persistent stakeholder/dependent-system stakes — escalating the depth to Accountable when any is true.
- **DREC-3.6** WHEN a predicate cannot be established true or false from the sources DREC-3.8 permits THE SYSTEM SHALL record it as unknown and escalate to Accountable (unknown is not false).
- **DREC-3.7** THE SYSTEM SHALL state in every record: that a crossing exists, its boundary type, each predicate's value (true/false/unknown) with its supporting observable fact, the ceremony floor, the resulting depth, and any user escalation.
- **DREC-3.8** THE SYSTEM SHALL conduct no per-crossing risk interview; predicate values come from mechanically available facts, standing configuration, and statements the user made unprompted (bounded by DREC-3.20).
- **DREC-3.9** THE SYSTEM SHALL evaluate the external-audience predicate as TRUE when the crossing's output is mechanically established to reach a recipient outside the group directly creating and approving the artifact (for example, a mechanically established public repository).
- **DREC-3.10** THE SYSTEM SHALL evaluate the external-audience predicate as FALSE only when a current, authoritative, and exhaustive mechanical source establishes that every repository reader and every notification recipient belongs to the creating-and-approving group.
- **DREC-3.11** IF neither the TRUE nor the FALSE evidence bar is met THEN THE SYSTEM SHALL record the external-audience predicate as unknown.
- **DREC-3.12** THE SYSTEM SHALL never treat repository privacy, team roster, CODEOWNERS, branch ownership, PR authorship, or workflow band, alone or combined, as sufficient FALSE evidence for the external-audience predicate.
- **DREC-3.13** THE SYSTEM SHALL evaluate predicates without requiring network access, API probes, or a user interview to lower a predicate's value.
- **DREC-3.14** WHILE the resulting depth is already fixed by a floor THE SYSTEM SHALL still evaluate and record every predicate truthfully, never forcing or skipping evaluation.
- **DREC-3.15** WHERE `docs/agents/project.md` pins actions to boundary types or higher floors THE SYSTEM SHALL apply those pins.
- **DREC-3.16** IF a configuration attempts to lower a core floor THEN THE SYSTEM SHALL ignore that entry and apply the core floor.
- **DREC-3.17** WHEN the user escalates depth above the computed result THE SYSTEM SHALL apply the escalation and record it.
- **DREC-3.18** THE SYSTEM SHALL never publish a record below the computed depth (the agent may never de-escalate).
- **DREC-3.19** WHEN `finish-branch` executes a discard verdict THE SYSTEM SHALL classify the crossing as boundary type `disposal` at Accountable depth (no-mechanical-undo never established false for disposal).
- **DREC-3.20** WHEN an unprompted user statement bears on a predicate THE SYSTEM SHALL use it only to escalate the predicate's value or to supply recorded supporting context — never to establish external-audience FALSE, which requires the current, authoritative, exhaustive mechanical evidence of DREC-3.10.

## 4. Verbatim human provenance

**Story:** As a future reader of a record, I want the human contribution held to
a verbatim-only law, so that the record proves human provenance rather than
manufacturing accountability theater.

- **DREC-4.1** THE SYSTEM SHALL require for a Guarded record a human verdict plus at least one verbatim human-authored judgment element.
- **DREC-4.2** THE SYSTEM SHALL require for an Accountable record a human verdict plus verbatim accepted risk plus verbatim response-if-wrong.
- **DREC-4.3** THE SYSTEM SHALL store human judgment elements only as exact user-authored words — never summarized, improved, inferred, or manufactured.
- **DREC-4.4** WHERE the harness permits THE SYSTEM SHALL attach a pointer to the originating interaction alongside each verbatim element.
- **DREC-4.5** IF the user replies with bare affirmation (for example "yes") to an agent-authored risk statement THEN THE SYSTEM SHALL count the reply as a verdict only, never as human-authored risk acceptance or response-if-wrong.
- **DREC-4.6** THE SYSTEM SHALL describe the verbatim guarantee in `RECORD.md` as human provenance, not absolute authenticity.

## 5. Storage classes and the secret scan

**Story:** As a user whose judgment may be sensitive, I want deterministic
storage dispositions with an honest off-record path, so that completing a
terminal verdict never forces disclosure and never falsifies verbatimness.

- **DREC-5.1** THE SYSTEM SHALL publish every human judgment element under exactly one storage disposition: `repo-verbatim`, `withheld(reference)`, or `withheld(unavailable)`.
- **DREC-5.2** WHERE a standing repo-verbatim policy is configured THE SYSTEM SHALL apply it without a per-gate storage quiz.
- **DREC-5.3** THE SYSTEM SHALL offer an explicit withhold mechanism at judgment capture.
- **DREC-5.4** WHEN a judgment element contains potentially sensitive prose THE SYSTEM SHALL obtain conditional confirmation before the element is accepted into a repo-verbatim payload.
- **DREC-5.5** WHEN a record will publish repo-verbatim THE SYSTEM SHALL show the user the exact payload before acceptance locks it (DREC-1.3).
- **DREC-5.6** WHEN the user has already supplied a durable opaque reference for a withheld judgment THE SYSTEM SHALL record `Storage: withheld(reference)` with `Storage-Reference: <exact locator>`.
- **DREC-5.7** WHEN a judgment is withheld and no reference was supplied THE SYSTEM SHALL ask exactly once whether one exists.
- **DREC-5.8** IF the user cannot or declines to provide a reference THEN THE SYSTEM SHALL record `Storage: withheld(unavailable)` with `Storage-Reference: unavailable` and continue publication.
- **DREC-5.9** THE SYSTEM SHALL never re-ask for a reference on that record, never block publication over an unavailable reference, and never treat the resulting `W-opaque` warning as unfinished work.
- **DREC-5.10** WHEN the deterministic secret scan hits on judgment prose THE SYSTEM SHALL offer only three continuations: ask the user to rephrase, accept withhold, or stop.
- **DREC-5.11** THE SYSTEM SHALL never redact or paraphrase user prose and still label it verbatim.

## 6. Emission — finish-branch

**Story:** As the outer-loop owner finishing a branch, I want every terminal
integration verdict I issue through the workflow captured as one record, so
that the judgment only I can contribute leaves durable evidence.

- **DREC-6.1** WHEN a human issues a terminal verdict at a production boundary through a v1 emitter THE SYSTEM SHALL create exactly one decision record, published under the ordering of DREC-15.1; a stopped or failed publication follows DREC-15.2–15.5, never silent unrecorded enactment.
- **DREC-6.2** THE SYSTEM SHALL limit v1 emitters to exactly `finish-branch` and `release`.
- **DREC-6.3** WHEN `finish-branch` executes a merge, outbound-PR-creation, or discard verdict THE SYSTEM SHALL emit a decision record.
- **DREC-6.4** THE SYSTEM SHALL extend the `finish-branch` menu with an explicit terminal block/reject option distinct from keep.
- **DREC-6.5** WHEN the user issues the terminal block/reject verdict THE SYSTEM SHALL emit a decision record for it.
- **DREC-6.6** WHEN the user selects keep THE SYSTEM SHALL NOT emit a decision record.
- **DREC-6.7** IF a mechanical gate fails without a human verdict THEN THE SYSTEM SHALL NOT emit a decision record.
- **DREC-6.8** WHEN a human issues a terminal verdict against red evidence THE SYSTEM SHALL still emit the record — emission keys on the verdict, never on the evidence's color.
- **DREC-6.9** WHEN the user pauses or defers without a terminal verdict THE SYSTEM SHALL NOT emit a decision record.
- **DREC-6.10** WHILE the verify gate is red THE SYSTEM SHALL still accept an explicit terminal block or discard verdict from the user (and emit per DREC-6.8).
- **DREC-6.11** THE SYSTEM SHALL emit records only for terminal verdicts mediated by this skill set, never for actions a human took directly outside the workflow (Correction 1, C2).
- **DREC-6.12** (guard) WHEN `finish-branch` runs THE SYSTEM SHALL CONTINUE TO withhold the merge and PR options while any verify, trace, or required acceptance check fails. (Today the entire menu is withheld on failure; DREC-6.10 deliberately narrows that stop to admit terminal block/discard verdicts on red — integration options stay withheld.)
- **DREC-6.13** (guard) WHEN the user selects discard THE SYSTEM SHALL CONTINUE TO require the literally typed word `discard` as the only valid confirmation.
- **DREC-6.14** (guard) WHEN `finish-branch` presents its menu THE SYSTEM SHALL CONTINUE TO offer merge, PR, keep, and discard — the block/reject extension adds an option, never removes or renames one.

## 7. Emission — release

**Story:** As the outer-loop owner cutting a release, I want any terminal
release verdict captured as exactly one record with the intermediate approvals
folded in as evidence, so that the release trail stays single-threaded and
complete.

- **DREC-7.1** WHEN a release reaches a successful terminal human verdict THE SYSTEM SHALL create exactly one decision record for the entire release.
- **DREC-7.2** THE SYSTEM SHALL fold version, build, smoke, and tag approvals into the release record as evidence, never as separate records.
- **DREC-7.3** IF a release ends by mechanical stop, abandonment, or defer without a terminal human verdict THEN THE SYSTEM SHALL NOT emit a decision record.
- **DREC-7.4** (guard) IF any release step fails THEN THE SYSTEM SHALL CONTINUE TO stop and leave the repo un-released, with no partial release.
- **DREC-7.5** (guard) WHEN cutting a release THE SYSTEM SHALL CONTINUE TO require explicit user approval for the version string and for tag creation/push.
- **DREC-7.6** WHEN the user issues an explicit terminal block/reject verdict on a release THE SYSTEM SHALL emit exactly one decision record for it.

## 8. Evidence citation and promotion

**Story:** As an auditor reading a record years later, I want every citation to
resolve to something durable, so that the record's evidence outlives sessions,
worktrees, and scratch files.

- **DREC-8.1** THE SYSTEM SHALL cite in records only evidence durable after publication: committed artifacts, immutable commit IDs, stable CI/PR/release refs, or evidence promoted into the record.
- **DREC-8.2** THE SYSTEM SHALL never cite `.skills/` paths, temporary logs, local absolute paths, or session history as record evidence.
- **DREC-8.3** WHEN an emitter promotes an ephemeral artifact THE SYSTEM SHALL complete the promotion — its substance written into the payload labeled as agent-authored evidence — before the exact payload is shown for acceptance (DREC-5.5) and before the acceptance lock (DREC-1.3).
- **DREC-8.4** THE SYSTEM SHALL never present promoted evidence as human judgment.
- **DREC-8.5** THE SYSTEM SHALL reserve the term "digest" for interpret's end-of-session artifact; promoted summaries use different naming.
- **DREC-8.6** IF evidence emerges after the payload lock THEN THE SYSTEM SHALL record it only as a permitted provenance-envelope append, never by payload mutation.

## 9. The record-decision skill and its caller gate

**Story:** As a maintainer of the skill set, I want the doctrine housed once
behind a hard caller gate, so that no skill can quietly promote itself into an
emitter and no emitter carries copied doctrine.

- **DREC-9.1** THE SYSTEM SHALL house operational doctrine in `skills/ship/record-decision/SKILL.md` and the sole record grammar in its sibling `RECORD.md`.
- **DREC-9.2** THE SYSTEM SHALL NOT duplicate grammar in `SKILL.md` — a strong sibling pointer only.
- **DREC-9.3** THE SYSTEM SHALL have emitters invoke `record-decision` via `REQUIRED SUB-SKILL:` prose, handing over the terminal verdict and durable evidence, with no copied doctrine in the emitter.
- **DREC-9.4** THE SYSTEM SHALL give `record-decision` a trigger-narrow description — a named production-boundary emitter with a terminal human verdict and durable evidence — with no generic "important decision" or "approval" trigger.
- **DREC-9.5** IF `record-decision` is invoked without a terminal human verdict THEN THE SYSTEM SHALL return without creating an artifact.
- **DREC-9.6** IF `record-decision` is invoked by a caller outside the closed v1 emitter set THEN THE SYSTEM SHALL return without creating an artifact.
- **DREC-9.7** THE SYSTEM SHALL never allow an evidence-producing skill to promote itself into an emitter.
- **DREC-9.8** THE SYSTEM SHALL ship no root-level record template.
- **DREC-9.9** THE SYSTEM SHALL mark `record-decision` model-invoked, reachable from model-invoked `finish-branch` and user-invoked `release` (ARCH-5-conformant direction).

## 10. Participant-model SSOT

**Story:** As a user of this skill set in a mixed repository, I want the
participant boundary defined once and projected to every runtime surface, so
that skill-set membership is never inferred and external contributors are never
policed by a process they never adopted.

- **DREC-10.1** THE SYSTEM SHALL add **ARCH-6** to `docs/architecture/INDEX.md` stating, as one greppable invariant, the never-infer/mediation-scope rule.
- **DREC-10.2** THE SYSTEM SHALL place the full three-role participant narrative (skill-mediated actor, external contributor, accountable reviewer) in an architecture domain file.
- **DREC-10.3** THE SYSTEM SHALL add the ratified runtime law to `AGENTS.md` as concise, semantically complete text — not a bare pointer.
- **DREC-10.4** THE SYSTEM SHALL add the smallest sufficient session-injected projection of the runtime law to `using-skills`.
- **DREC-10.5** THE SYSTEM SHALL NOT duplicate the full participant narrative into individual skills; only skills whose behavior changes operationalize the rule.
- **DREC-10.6** THE SYSTEM SHALL treat the absence of decision records, requirement IDs, or TDD reports on an external contribution as no violation of this methodology.
- **DREC-10.7** (guard) WHEN `using-skills` is injected THE SYSTEM SHALL CONTINUE TO carry its subagent exemption and its 1%-rule gate unchanged.
- **DREC-10.8** (guard) WHEN `AGENTS.md` is amended THE SYSTEM SHALL CONTINUE TO present the Four Iron Laws and the orchestration rule unchanged.

## 11. Trace extension, adoption anchor, and validator

**Story:** As anyone running `trace`, I want record absence and malformation
caught by deterministic LLM-free passes, so that the mechanical lane holds the
assurance the verbatim law cannot.

- **DREC-11.1** WHEN decision records exist THE SYSTEM SHALL report **E-dup** (error) for any DEC ID defined by more than one record file.
- **DREC-11.2** WHEN decision records exist THE SYSTEM SHALL report **E-grammar** (error) for a record with a missing or invalid required field for its declared depth, an illegal enum value, a missing `Storage:` field, or an empty Accountable judgment field.
- **DREC-11.3** WHERE the consuming repo has the requirements spine enabled THE SYSTEM SHALL report **E-spine** (error) for a record citing an unknown feature/requirement ID, or carrying a mechanically resolvable durable pointer whose target is demonstrably absent.
- **DREC-11.4** WHERE the spine layer is absent THE SYSTEM SHALL no-op the E-spine pass rather than report errors (ARCH-2).
- **DREC-11.5** WHEN decision records exist THE SYSTEM SHALL report **W-uncited-tag** (warning) for each candidate post-adoption tag (per DREC-11.22) cited by no record.
- **DREC-11.6** WHEN three or more Guarded/Accountable records carry byte-identical verbatim human-contribution fields — equality after line-ending and boundary-whitespace normalization only, no fuzzy or LLM matching — THE SYSTEM SHALL report **W-repeated-judgment** (warning) listing the record IDs.
- **DREC-11.7** THE SYSTEM SHALL exclude verdict words and Minimal records from W-repeated-judgment and never ask anyone to diversify the human's words (advisory only).
- **DREC-11.8** THE SYSTEM SHALL report **W-opaque** (warning) for every record with `Storage: withheld(unavailable)`; a syntactically valid `withheld(reference)` is never W-opaque merely because the current environment cannot inspect its locator.
- **DREC-11.9** THE SYSTEM SHALL NOT treat an external locator the current environment cannot inspect as broken.
- **DREC-11.10** THE SYSTEM SHALL keep crossing-without-record at warning level, never error — trace cannot distinguish skill-mediated verdicts from direct human action or external contribution.
- **DREC-11.11** THE SYSTEM SHALL represent adoption as exactly one anchor in the decision substrate carrying an explicit, immutable UTC cutoff timestamp.
- **DREC-11.12** IF zero or multiple adoption anchors exist while any decision record exists THEN THE SYSTEM SHALL report an error.
- **DREC-11.13** THE SYSTEM SHALL never infer adoption from the earliest record.
- **DREC-11.14** WHEN adoption is declared THE SYSTEM SHALL record in the anchor an explicit baseline mapping each tag ref name existing at the adoption moment to its referenced object ID.
- **DREC-11.15** IF tags are not visible in the current clone THEN THE SYSTEM SHALL no-op the W-uncited-tag pass rather than guess.
- **DREC-11.16** THE SYSTEM SHALL implement the decision-record passes as a single-file, stdlib-only, LLM-free validator shipped beside `RECORD.md` — the same validator invoked by `trace` and by `record-decision` at publication time (DREC-15.6) — with fixed diagnostics and fixed exit rules.
- **DREC-11.17** THE SYSTEM SHALL limit validator judgment on external references to syntax, prohibited ephemeral locator classes, and deterministic secret patterns — never asserting an external reference exists, is accessible, contains the judgment, or is authentic unless a configured mechanical resolver proves it.
- **DREC-11.18** WHERE a repo has no decision-record adoption (no anchor and no records) THE SYSTEM SHALL no-op all decision-record passes (ARCH-2).
- **DREC-11.19** IF the validator cannot run in the current environment THEN THE SYSTEM SHALL report the decision-record passes as not-run, never as passed.
- **DREC-11.20** (guard) WHEN `trace` runs THE SYSTEM SHALL CONTINUE TO produce the existing E1–E5 / W1–W3 finding set with unchanged semantics.
- **DREC-11.21** (guard) WHEN `trace` evaluates coverage THE SYSTEM SHALL CONTINUE TO apply textual presence without judgment (ARCH-1).
- **DREC-11.22** WHEN evaluating W-uncited-tag THE SYSTEM SHALL treat a currently visible tag as a candidate post-adoption tag exactly when its name is absent from the anchor baseline or its referenced object ID differs from the baseline entry — using no history traversal, ancestry inference, tag-date reading, or commit-date fallback.
- **DREC-11.23** THE SYSTEM SHALL implement the validator to require no runtime installation beyond capabilities the skill set already guarantees to consuming repos (ARCH-3) — an unavailable validator reports not-run per DREC-11.19, but the chosen implementation must not make that the expected consumer experience.
- **DREC-11.24** WHEN reporting W-uncited-tag THE SYSTEM SHALL state the mechanical fact — the tag is absent from, or changed since, the adoption baseline — never a chronology claim the repository snapshot cannot prove.

## 12. interpret upgrades

**Story:** As a user deciding in my own language, I want decisions, claims, and
rationale labeled by provenance throughout the session, so that what I decided,
what I authored, and what the agent authored never blur.

- **DREC-12.1** WHEN a decision event occurs in an interpret session THE SYSTEM SHALL update a compact visible ledger showing Decided / Open / Rejected-deferred — and only on decision events.
- **DREC-12.2** THE SYSTEM SHALL reserve full rationale for the end-of-session digest, keeping the ledger compact.
- **DREC-12.3** THE SYSTEM SHALL label blocks in interpret analysis output with exactly these claim labels: Source claim / Verified fact / Inference / Recommendation / User decision / Open question.
- **DREC-12.4** WHEN at least two live options exist, the choice closes a meaningful branch or fixes a constraint, and the user has not already stated their reason THE SYSTEM SHALL ask one short rationale question.
- **DREC-12.5** WHEN the user has already supplied a reason THE SYSTEM SHALL quote it verbatim without re-asking.
- **DREC-12.6** IF the user declines to give a rationale THEN THE SYSTEM SHALL record `Human rationale: not supplied`.
- **DREC-12.7** THE SYSTEM SHALL never infer rationale from an accepted recommendation.
- **DREC-12.8** WHEN an interpret session ends THE SYSTEM SHALL produce a digest carrying exactly these seven provenance labels: User decisions / Human rationale — verbatim / Verified evidence / Interpret analysis — agent-authored / Open questions / Prepared reply — agent-authored / Transport-adoption status.
- **DREC-12.9** THE SYSTEM SHALL treat human-carried transport of the digest as proof of adoption, never authorship — agent analysis stays agent-authored after adoption.
- **DREC-12.10** WHILE an interpret session runs THE SYSTEM SHALL remain read-only toward the project repo — never committing, publishing, or emitting decision records.
- **DREC-12.11** (guard) WHEN the user pastes a response THE SYSTEM SHALL CONTINUE TO produce interpret's five sections in order (translate, simplify, Feynman, independent analysis, reply-to-send-back).
- **DREC-12.12** (guard) WHILE running beside another session THE SYSTEM SHALL CONTINUE TO act as a companion that does not drive spec or code.

## 13. Documentation convention

**Story:** As a future feature author, I want the spec-folder convention to
admit this feature's discovery handoff without normalizing it, so that the
repository documentation and the repository agree.

- **DREC-13.1** THE SYSTEM SHALL update the spec-folder layout documentation in `docs/architecture/artifacts.md` to admit an optional, non-normative `discovery.md` beside the triad.
- **DREC-13.2** THE SYSTEM SHALL state in that convention that `requirements.md` remains the sole normative specification and that a discovery record is never required for a feature.

## 14. Non-functional requirements

- **Performance:** None — every new pass is an offline, single-shot file
  read/grep at skill runtime; no latency-sensitive surface exists.
- **Security:**
  - **DREC-14.1** WHEN a repo-verbatim judgment payload is about to publish THE SYSTEM SHALL run the deterministic secret scan before the write — verified by RED/GREEN fixtures seeded with known secret patterns.
- **Reliability:**
  - **DREC-14.2** WHEN the validator runs twice on identical input THE SYSTEM SHALL produce identical diagnostics and identical exit codes — verified by a repeated-run fixture test.
- **Accessibility:** None — outputs are markdown artifacts and terminal text;
  no UI surface.

## 15. Record-before-crossing ordering and publication failure

**Story:** As the outer-loop owner, I want the record published before the
crossing executes, so that no production crossing can outrun its
accountability record and no failure is papered over as compliant completion.

- **DREC-15.1** WHEN enacting a terminal verdict whose crossing requires a record THE SYSTEM SHALL follow this order: judgment capture → storage resolution → evidence promotion (DREC-8.3) → exact-payload display → human acceptance → successful valid-record publication → crossing execution → execution outcome appended to the envelope.
- **DREC-15.2** IF required record publication is stopped (including a secret-scan stop per DREC-5.10) or fails (including a filesystem write failure) THEN THE SYSTEM SHALL NOT execute the crossing action — no merge, PR creation, discard, release step, or any other crossing side effect.
- **DREC-15.3** WHEN a crossing was withheld because publication stopped or failed THE SYSTEM SHALL report that the verdict was not enacted and the crossing did not occur — never claiming compliant completion.
- **DREC-15.4** WHEN retrying after a stopped or failed publication THE SYSTEM SHALL reuse only the human contributions actually captured, never manufacturing or altering human judgment.
- **DREC-15.5** IF a block/reject record cannot publish THEN THE SYSTEM SHALL report an unrecorded terminal verdict and an incomplete accountability workflow, never treating it as a valid recorded completion (block/reject has no crossing side effect to withhold).
- **DREC-15.6** IF the record cannot be validated at publication time (validator not-run or failing) THEN THE SYSTEM SHALL treat it as a publication failure under DREC-15.2.
- **DREC-15.7** WHEN publication succeeds and the subsequent crossing execution fails THE SYSTEM SHALL append the failure outcome to the provenance envelope and report the crossing as failed — the published record remains valid.

*Pressure cases the plan must RED-test: secret hit + user stops (15.2); missing
required human judgment, which makes the record invalid at its depth (15.6 via
11.2 semantics); validator not-run/failure at publication (15.6); filesystem
write failure (15.2); successful publication followed by crossing failure
(15.7); block/reject record-publication failure (15.5).*

## Out of Scope

- Inbound PR acceptance and the `review-contribution` capability, including its
  evidence-provenance grammar (`supplied-by-author` vs
  `mediating-agent-observed`) — deferred Tier-2 follow-up (Correction 1, C5).
- Boundary generalization to publish/send/migrate/policy crossings (no observed
  baseline failure there).
- `correct-course` and spec approvals as emitters (not crossings in v1).
- Advisory derivability check on judgment fields (only if transcripts show an
  evasion the Iron Law misses).
- interpret risk-weighted depth compression (needs observed fatigue and a
  sharper predicate).
- A generated record-template projection or any root-level record template.
- Per-crossing risk interviews, mandatory pin tables, and per-gate storage
  quizzes (rejected in discovery).
- Enforcing decision-record discipline on external contributors or on any
  action this skill set did not mediate.
- Any hard headless gate (CI job, git hook) for decision records — the
  validator runs via `trace` where an agent is present (ARCH-3).

## Carried to design (non-normative)

Deliberately not fixed at requirements level: exact verdict enum tokens and the
mapping of Osmani's six verdicts onto the extended finish-branch menu; the
initial `Boundary-Type` table and `project.md` pin-entry syntax; the full
`RECORD.md` field grammar, including the anchor's baseline-set syntax; the
interaction-pointer format "where the harness permits"; the secret-scan pattern
set; validator implementation language and its fixture set (constrained by
DREC-11.23); exact emitter hand-off prose and the evidence-promotion recipe;
whether `release` should create annotated tags as an explicit behavior change
(no requirement currently depends on tag dates); the alignment drift/pressure
checks across the four participant-model surfaces (plan must include them per
Correction 1); RED/GREEN pressure tests for the anchor baseline across shallow
clones, rebases, cherry-picks, backfill, a new tag name, an existing name
force-moved to a new object, and a pre-existing remote tag becoming visible
after adoption (a warning-lane candidate by design, not a defect) — with
delete/recreate to the identical object documented as an acknowledged
undetectable limitation. No determinism claim is made here until that evidence
exists.

## Discovery coverage map (non-normative)

| Digest §11 checklist item | Criteria |
|---|---|
| Emission rule incl. terminal-block, red-evidence | 6.1, 6.3, 6.5, 6.8, 6.10, 7.6 |
| Non-emission exclusions | 6.6, 6.7, 6.9, 7.3 |
| Minimal reserved non-emitting in v1 | 3.4 |
| Depth formula + floors + predicates + unknown→Accountable | 3.1–3.6, 3.20 |
| Verbatim law + yes-counts-as-verdict-only | 4.1–4.5 |
| Agent-never-de-escalates / user-escalate-only | 3.17, 3.18 |
| Payload immutability + envelope + supersession-for-typos | 1.2–1.5, 1.8 |
| ID format, two-phase immutability, recorded reissue, 7 scenarios | 2.1–2.9 |
| Storage classes + secret-scan block + no-redact + withheld fork | 5.1–5.11 |
| Durable-evidence-only + promotion | 8.1–8.6 |
| Caller gate | 9.5–9.7 |
| Three E-passes (E-spine conditional) + three W-passes | 11.1–11.10 |
| Adoption-anchor principles + resolved baseline mechanism | 11.11–11.15, 11.22, 11.24 |
| Validator determinism + consumer-dependency constraint | 11.16, 11.17, 11.19, 11.23, 14.2 |
| Record-before-crossing ordering + publication failure | 15.1–15.7 |
| finish-branch menu extension | 6.4 |
| Release single-record rule | 7.1, 7.6 |
| PR boundary classification resolved | 3.9–3.13 (outbound; inbound deferred per C4/C5) |
| interpret ledger/labels/rationale/digest + read-only | 12.1–12.12 |
| ARCH-2 no-op where layers absent | 11.4, 11.15, 11.18 |
| Correction 1: participant model SSOT + scope | 10.1–10.6, 6.11 |
