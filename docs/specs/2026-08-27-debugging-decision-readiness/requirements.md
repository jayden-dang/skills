# Requirements: Debugging decision readiness

Feature code: DBGREADY
Status: Draft
Date: 2026-08-27

## 1. Create and inspect an authoritative debugging package

**Story:** As a debugger, I want to create one authoritative debugging package, so that evidence, analysis, and decisions cannot diverge across representations.

- **DBGREADY-1.1** WHEN a debugging investigation begins THE SYSTEM SHALL create one typed logical package with a unique package identifier.
- **DBGREADY-1.2** WHEN a package revision is created THE SYSTEM SHALL identify its schema version independently from its evidence-policy version.
- **DBGREADY-1.3** WHEN a package revision is created THE SYSTEM SHALL identify its operational-policy version independently from its authority-policy version.
- **DBGREADY-1.4** THE SYSTEM SHALL use JSON as the version-1 canonical serialization of the typed package.
- **DBGREADY-1.5** WHEN a human-readable package view is requested THE SYSTEM SHALL derive the Incident evidence view from the selected canonical revision.
- **DBGREADY-1.6** WHEN a human-readable package view is requested THE SYSTEM SHALL derive the Causal analysis view from the selected canonical revision.
- **DBGREADY-1.7** WHEN a human-readable package view is requested THE SYSTEM SHALL derive the Decision brief view from the selected canonical revision.
- **DBGREADY-1.8** WHEN a generated view is rendered THE SYSTEM SHALL display the package identifier, package revision, revision hash, schema version, policy versions, renderer version, and generation time.
- **DBGREADY-1.9** IF a human edits a generated view THEN THE SYSTEM SHALL leave the canonical package unchanged.
- **DBGREADY-1.10** IF a generated view does not match the revision and hash evaluated for a consequential decision THEN THE SYSTEM SHALL refuse to record that decision against the view.
- **DBGREADY-1.11** IF view rendering fails after a valid revision is written THEN THE SYSTEM SHALL preserve the authoritative revision while withholding a decision-ready view.

## 2. Inspect causal claims through evidence relationships

**Story:** As a technical reviewer, I want to inspect how a causal claim resolves to primary evidence, so that I can independently evaluate the proposed mechanism.

- **DBGREADY-2.1** WHEN an evidence node is recorded THE SYSTEM SHALL assign it a stable `EVID-*` identifier.
- **DBGREADY-2.2** WHEN a causal claim is recorded THE SYSTEM SHALL assign it a stable `CLAIM-*` identifier.
- **DBGREADY-2.3** WHEN a discriminating experiment is recorded THE SYSTEM SHALL assign it a stable `EXP-*` identifier.
- **DBGREADY-2.4** WHEN an evidence node is recorded THE SYSTEM SHALL record its source type, provenance, environment, revision, scope, observation, collection method, reproducibility, limitations, and contradictions.
- **DBGREADY-2.5** WHEN evidence supports or contradicts a proposition THE SYSTEM SHALL record a typed edge naming the exact proposition that relationship bears on.
- **DBGREADY-2.6** IF a referenced identifier, environment, revision, artifact, or graph edge cannot be resolved THEN THE SYSTEM SHALL report the affected relationship as incomplete.
- **DBGREADY-2.7** WHEN evidence capability is evaluated THE SYSTEM SHALL derive it from the support set relative to one proposition.
- **DBGREADY-2.8** WHEN multiple evidence items support one proposition THE SYSTEM SHALL evaluate their policy-defined capability combination rather than select the highest individual label.
- **DBGREADY-2.9** THE SYSTEM SHALL prohibit authored E0-E4 values from acting as evidence authority.
- **DBGREADY-2.10** WHEN E0-E4 is displayed THE SYSTEM SHALL identify the claim, support set, limiting evidence, and policy rule from which the lossy summary was derived.
- **DBGREADY-2.11** WHEN a causal strength is requested THE SYSTEM SHALL derive the maximum permitted strength from the applicable evidence policy.
- **DBGREADY-2.12** IF a requested causal strength exceeds its policy ceiling THEN THE SYSTEM SHALL return `not_ready` with the claim, support edge, evidence references, policy rule, and limiting dependency.
- **DBGREADY-2.13** WHILE contradictory evidence or unresolved alternatives exist THE SYSTEM SHALL preserve them on the affected claim.
- **DBGREADY-2.14** WHEN discrimination between live mechanisms requires an experiment THE SYSTEM SHALL require a prediction whose outcomes distinguish those mechanisms.
- **DBGREADY-2.15** WHEN telemetry, immutable artifacts, or code/config semantics directly establish a causal transition THE SYSTEM SHALL allow the applicable policy to support that transition without an experiment.
- **DBGREADY-2.16** WHEN a causal path is presented for human review THE SYSTEM SHALL show the smallest useful code or configuration excerpt supporting each important transition.
- **DBGREADY-2.17** WHEN a causal path is presented for human review THE SYSTEM SHALL express the propagation chain from trigger through incorrect state to observed failure.

## 3. Record scoped human causal judgment

**Story:** As an eligible human reviewer, I want to record a decision on one explicit causal proposition, so that causal authority remains attributable and historically inspectable.

- **DBGREADY-3.1** WHEN a claim is created THE SYSTEM SHALL record its investigation state independently from its requested causal strength.
- **DBGREADY-3.2** THE SYSTEM SHALL restrict investigation state to `open`, `unresolved`, `falsified`, or `superseded`.
- **DBGREADY-3.3** THE SYSTEM SHALL restrict requested causal strength to `candidate`, `probable_contributor`, or `confirmed_for_scope`.
- **DBGREADY-3.4** WHEN requested strength is recorded THE SYSTEM SHALL treat it as a proposition submitted for review rather than an accepted result.
- **DBGREADY-3.5** WHEN an eligible human accepts, rejects, or supersedes a causal proposition THE SYSTEM SHALL append an immutable disposition event.
- **DBGREADY-3.6** WHEN a disposition event is appended THE SYSTEM SHALL record its actor, identity assurance, asserted role, authority basis, authority-policy version, package revision, evidence support set, scope, rationale, and unresolved concerns.
- **DBGREADY-3.7** WHEN a requested strength is rejected THE SYSTEM SHALL preserve both the rejected requested strength and any lower accepted strength.
- **DBGREADY-3.8** IF a prior disposition must be corrected THEN THE SYSTEM SHALL append a superseding disposition event without editing or deleting the prior event.
- **DBGREADY-3.9** WHEN current causal state is displayed THE SYSTEM SHALL derive it from claim history, disposition events, current evidence relationships, current investigation state, and current evidence policy.
- **DBGREADY-3.10** IF a historical disposition exceeds the current policy ceiling THEN THE SYSTEM SHALL preserve the historical judgment while reporting `policy_conflict` in the current projection.
- **DBGREADY-3.11** THE SYSTEM SHALL prohibit the validator from promoting requested or accepted causal strength.
- **DBGREADY-3.12** THE SYSTEM SHALL prohibit an agent or validator from creating an authoritative causal acceptance event.
- **DBGREADY-3.13** WHEN disposition authority is evaluated THE SYSTEM SHALL use the requested decision, requested or accepted strength, scope, environment, consequence, package revision, actor provenance, and applicable authority policy.
- **DBGREADY-3.14** IF authority is insufficient to accept a requested strength THEN THE SYSTEM SHALL permit an authorized rejection of that request when the authority policy allows the rejection.
- **DBGREADY-3.15** IF required disposition authority cannot be established THEN THE SYSTEM SHALL block the disposition event without blocking evidence collection or safe investigation.

## 4. Classify and audit operational interventions

**Story:** As an operational reviewer, I want to inspect the epistemic basis and event history of a proposed intervention, so that authorization does not silently claim causality or execution success.

- **DBGREADY-4.1** THE SYSTEM SHALL restrict authorized version-1 action classes to `containment`, `diagnostic_experiment`, and `corrective_fix`.
- **DBGREADY-4.2** WHEN an action is classified as containment THE SYSTEM SHALL require its stated basis to be current impact or risk reduction.
- **DBGREADY-4.3** WHEN an action is classified as a diagnostic experiment THE SYSTEM SHALL require its stated basis to be discrimination between referenced live hypotheses.
- **DBGREADY-4.4** WHEN an action is classified as a corrective fix THE SYSTEM SHALL require a claim-specific accepted causal disposition at the policy-required minimum strength.
- **DBGREADY-4.5** IF a proposed epistemic basis does not truthfully match a version-1 class THEN THE SYSTEM SHALL set `classification_unresolved` with `unsupported_action_basis`.
- **DBGREADY-4.6** IF an action classification is unresolved THEN THE SYSTEM SHALL refuse to substitute the nearest authorized class.
- **DBGREADY-4.7** WHEN an unresolved action basis is recorded THE SYSTEM SHALL preserve its proposed basis, demonstrated invariant, supporting evidence, and unresolved historical causation.
- **DBGREADY-4.8** WHEN an action is proposed THE SYSTEM SHALL bind its immutable identity to its class, epistemic basis, target, scope, intended effect, and proposal revision.
- **DBGREADY-4.9** IF an action target, command, scope, parameters, intended effect, or safety boundary materially changes THEN THE SYSTEM SHALL create a new action revision requiring fresh readiness and authorization.
- **DBGREADY-4.10** WHEN an authorization event is recorded THE SYSTEM SHALL bind it to one exact action revision.
- **DBGREADY-4.11** WHEN an execution attempt is recorded THE SYSTEM SHALL reference the exact applicable authorization and action revision.
- **DBGREADY-4.12** IF an execution attempt does not resolve to a matching applicable authorization THEN THE SYSTEM SHALL reject its authorization provenance.
- **DBGREADY-4.13** WHEN authorization history is projected THE SYSTEM SHALL preserve proposed, authorized, rejected, revoked, and expired events.
- **DBGREADY-4.14** WHEN execution history is projected THE SYSTEM SHALL preserve started, succeeded, failed, and aborted attempts.
- **DBGREADY-4.15** WHEN verification history is projected THE SYSTEM SHALL preserve effective, ineffective, inconclusive, and invalid-measurement results.
- **DBGREADY-4.16** WHEN rollback history is projected THE SYSTEM SHALL preserve available, invoked, succeeded, failed, and not-applicable events.
- **DBGREADY-4.17** WHEN an execution attempt reports success THE SYSTEM SHALL describe the mechanical result independently from operational-effect verification.
- **DBGREADY-4.18** WHEN an action effect is verified THE SYSTEM SHALL reference the expected effect, measurement evidence, observation window, result, and limitations.
- **DBGREADY-4.19** WHEN an operational event produces diagnostic information THE SYSTEM SHALL add that information as evidence without directly mutating causal disposition.
- **DBGREADY-4.20** WHEN an action later yields stronger evidence THE SYSTEM SHALL preserve the action class under which it was originally authorized.
- **DBGREADY-4.21** WHEN authorization is recorded THE SYSTEM SHALL treat the record as evidence of authorization rather than an executable capability token.

## 5. Assess readiness for one exact decision

**Story:** As a decision-maker, I want a traceable readiness assessment for the exact decision before me, so that `ready` cannot be mistaken for global package validity or durable permission.

- **DBGREADY-5.1** THE SYSTEM SHALL prohibit a global debugging-package `ready` state.
- **DBGREADY-5.2** WHEN operational readiness is requested THE SYSTEM SHALL evaluate one exact action revision under one class-specific operational profile and policy version.
- **DBGREADY-5.3** WHEN causal-disposition readiness is requested THE SYSTEM SHALL evaluate one exact claim, requested strength, scope, package revision, and policy version.
- **DBGREADY-5.4** WHEN a containment profile is evaluated THE SYSTEM SHALL require operational-base dependencies, impact or severity basis, urgency, blast radius, rollback or recovery disposition, and observable expected outcome.
- **DBGREADY-5.5** WHEN a diagnostic-experiment profile is evaluated THE SYSTEM SHALL require operational-base dependencies, hypothesis references, prediction, alternatives discriminated, measurement plan, abort criteria, rollback disposition, and experiment limitations.
- **DBGREADY-5.6** WHEN a corrective-fix profile is evaluated THE SYSTEM SHALL require operational-base dependencies, intended causal mechanism, qualifying disposition, regression evidence, verification criteria, rollback disposition, and residual risk.
- **DBGREADY-5.7** WHEN causal-disposition readiness is evaluated THE SYSTEM SHALL require the proposition, requested strength, scope, support set, contradictions, alternatives, derived evidence capability, confidence ceiling, and human authority requirement.
- **DBGREADY-5.8** WHEN a readiness dependency is evaluated THE SYSTEM SHALL resolve it to `satisfied`, `unsatisfied`, `unresolved`, `unavailable`, or `not_applicable`.
- **DBGREADY-5.9** IF an agent cannot locate a dependency THEN THE SYSTEM SHALL keep its outcome `unresolved` until positive evidence establishes another outcome.
- **DBGREADY-5.10** WHEN a dependency is marked unavailable THE SYSTEM SHALL require positive evidence that the capability, artifact, access, or action is impossible or inaccessible in the evaluated context.
- **DBGREADY-5.11** WHEN a dependency is marked not applicable THE SYSTEM SHALL cite the policy rule that produced the outcome.
- **DBGREADY-5.12** THE SYSTEM SHALL prohibit agent-authored free-form `not_applicable` outcomes.
- **DBGREADY-5.13** WHEN policy permits an alternate readiness branch THE SYSTEM SHALL preserve the original dependency outcome.
- **DBGREADY-5.14** WHEN a policy alternative requires risk acceptance THE SYSTEM SHALL bind the acceptance to the missing dependency, action revision, residual risk, policy branch, authority requirement, and human event.
- **DBGREADY-5.15** WHEN risk is accepted THE SYSTEM SHALL leave epistemic uncertainty and causal confidence unchanged.
- **DBGREADY-5.16** IF a risk-acceptance event references another action revision THEN THE SYSTEM SHALL leave the evaluated decision `not_ready`.
- **DBGREADY-5.17** IF a policy marks a failed dependency non-waivable THEN THE SYSTEM SHALL leave the decision `not_ready` regardless of human risk acceptance.
- **DBGREADY-5.18** WHEN a decision becomes permissible through an alternate policy branch THE SYSTEM SHALL render `READY VIA POLICY ALTERNATIVE` with the original dependency, alternate requirements, residual risk, authority, and policy rule.
- **DBGREADY-5.19** WHEN a readiness assessment returns `not_ready` THE SYSTEM SHALL identify the failed profile dependency, affected object, evidence or artifact reference, relationship, policy rule, and missing alternative.
- **DBGREADY-5.20** WHEN package, action, evidence, or policy inputs change THE SYSTEM SHALL require a new readiness assessment rather than reuse an earlier result.
- **DBGREADY-5.21** THE SYSTEM SHALL treat `ready` as contract conformance for the requested decision rather than factual truth, causal correctness, authorization, executable capability, or predicted success.

## 6. Preserve, validate, render, and export package history

**Story:** As a package custodian, I want to reproduce one exact debugging revision, so that human views, validation results, and external records resolve to the same evidence state.

- **DBGREADY-6.1** WHEN no organization-specific storage backend is configured THE SYSTEM SHALL store the working package under `.skills/debugging/{package-id}/`.
- **DBGREADY-6.2** THE SYSTEM SHALL keep the default working package outside automatic Git tracking and external publication.
- **DBGREADY-6.3** WHEN raw evidence is stored outside the canonical graph THE SYSTEM SHALL reference it by immutable sidecar or approved external-store identity.
- **DBGREADY-6.4** WHEN a raw evidence reference is recorded THE SYSTEM SHALL capture its hash where obtainable, media type, size, collection time, source, access classification, retention or expiry, and redaction status.
- **DBGREADY-6.5** IF a referenced raw artifact is missing, expired, changed, or unverifiable THEN THE SYSTEM SHALL update the affected evidence relationship without silently substituting an excerpt for the artifact.
- **DBGREADY-6.6** WHEN an authoritative mutation is accepted THE SYSTEM SHALL create a new numbered JSON revision without overwriting prior revision files.
- **DBGREADY-6.7** WHEN a revision is created THE SYSTEM SHALL record its predecessor revision and predecessor content hash.
- **DBGREADY-6.8** WHEN revision integrity is validated THE SYSTEM SHALL check sequence continuity, revision hashes, event preservation, and forbidden historical mutation.
- **DBGREADY-6.9** WHEN local integrity validation succeeds THE SYSTEM SHALL avoid claiming cryptographic actor identity or tamper-proof custody.
- **DBGREADY-6.10** WHEN the package tool initializes a package THE SYSTEM SHALL create its first valid revision.
- **DBGREADY-6.11** WHEN the package tool applies a typed change THE SYSTEM SHALL verify the caller's expected current revision before writing the next revision atomically.
- **DBGREADY-6.12** IF a typed change edits or deletes immutable history THEN THE SYSTEM SHALL refuse the change.
- **DBGREADY-6.13** WHEN validation is requested THE SYSTEM SHALL evaluate schema, graph integrity, evidence policy, authority policy, and decision-scoped readiness without mutating the package.
- **DBGREADY-6.14** WHEN rendering is requested THE SYSTEM SHALL generate all human views from one exact package revision.
- **DBGREADY-6.15** WHEN current JSON or Markdown projections are generated THE SYSTEM SHALL treat them as replaceable derived files rather than authoritative revisions.
- **DBGREADY-6.16** WHEN a legacy Markdown pack is imported THE SYSTEM SHALL create a provenance-preserving draft with disposition `legacy_unvalidated`.
- **DBGREADY-6.17** WHEN legacy content is converted THE SYSTEM SHALL distinguish imported facts from interpretation added during conversion.
- **DBGREADY-6.18** WHEN legacy content is converted THE SYSTEM SHALL retain a reference to the original artifact rather than rewrite it.
- **DBGREADY-6.19** WHEN an explicit configured export is requested THE SYSTEM SHALL export one immutable package revision with matching views, hashes, destination, and receipt.
- **DBGREADY-6.20** WHEN an export lacks a current matching view THE SYSTEM SHALL record that absence rather than export a stale view as current.

## 7. Apply the contract to local and deployed debugging

**Story:** As an engineer investigating unexpected behavior, I want to produce the same inspectable decision record for a local or deployed failure, so that containment and causal proof remain deliberately separate.

- **DBGREADY-7.1** WHEN a failure exists only on a deployed environment and no package exists THE SYSTEM SHALL begin with read-only incident evidence collection in a canonical debugging package.
- **DBGREADY-7.2** WHEN deployed impact may require urgent containment THE SYSTEM SHALL prepare containment readiness independently from causal-disposition readiness.
- **DBGREADY-7.3** WHEN containment is decision-ready without a resolved cause THE SYSTEM SHALL permit presentation of the containment decision while leaving causal claims open or unresolved.
- **DBGREADY-7.4** WHEN a local or non-production red-capable signal is run THE SYSTEM SHALL record its command, red output, environment, revision, and timestamp as evidence before causal claim creation.
- **DBGREADY-7.5** WHEN deterministic reproduction is unsafe or impossible THE SYSTEM SHALL preserve the best available observational or probabilistic evidence with its limitations rather than invent a deterministic result.
- **DBGREADY-7.6** WHEN hypotheses are investigated THE SYSTEM SHALL keep falsifiable predictions, evidence for and against, alternatives, contradictions, and discriminating results in the causal analysis.
- **DBGREADY-7.7** WHEN a consequential debugging decision is requested THE SYSTEM SHALL render the actual wrong behavior, expected behavior, relevant code or configuration path, supporting evidence, weakening evidence, proposed intervention, expected effect, unknowns, blast radius, rollback disposition, and residual risk where applicable.
- **DBGREADY-7.8** WHEN a human decides an operational action THE SYSTEM SHALL record action acceptance independently from causal acceptance.
- **DBGREADY-7.9** WHEN a human decides a causal proposition THE SYSTEM SHALL record accepted causal strength independently from action authorization.
- **DBGREADY-7.10** WHEN corrective-fix regression behavior is verified THE SYSTEM SHALL record the fresh result as a verification event for the exact action revision.
- **DBGREADY-7.11** WHEN the original unminimized symptom signal is re-run after a corrective fix THE SYSTEM SHALL record the fresh result as a verification event for the exact action revision.
- **DBGREADY-7.12** WHEN the repository's full verification suite is run after a corrective fix THE SYSTEM SHALL record the fresh result as a verification event for the exact action revision.
- **DBGREADY-7.13** THE SYSTEM SHALL document the repository-wide principle that consequential decisions should be grounded in inspectable evidence sufficient for the decision requested.
- **DBGREADY-7.14** WHEN decision-readiness compliance is described THE SYSTEM SHALL identify debugging as the only specialization implemented and behaviorally validated by this feature.
- **DBGREADY-7.15** WHEN non-debugging approval surfaces are named THE SYSTEM SHALL identify them as future adoption targets rather than compliant workflows.

## 8. Demonstrate resistance to persuasive but unsupported behavior

**Story:** As a maintainer, I want behavioral evaluations of the debugging contract, so that compliance is demonstrated against realistic agent failure modes rather than inferred from written rules.

- **DBGREADY-8.1** WHEN a package fills every narrative field with unsupported prose THE SYSTEM SHALL keep the requested decision `not_ready`.
- **DBGREADY-8.2** WHEN a claim omits contradictory evidence known to the package THE SYSTEM SHALL keep the requested causal disposition `not_ready`.
- **DBGREADY-8.3** WHEN an agent labels an intervention against an unaccepted candidate as a corrective fix THE SYSTEM SHALL reject the action classification.
- **DBGREADY-8.4** WHEN a demonstrated unsafe-state elimination lacks an accepted historical cause THE SYSTEM SHALL return `classification_unresolved` rather than relabel the action containment or corrective fix.
- **DBGREADY-8.5** WHEN an agent marks rollback not applicable without a policy rule THE SYSTEM SHALL reject the dependency outcome.
- **DBGREADY-8.6** WHEN an agent fails to locate rollback documentation and marks rollback unavailable THE SYSTEM SHALL keep the dependency unresolved.
- **DBGREADY-8.7** WHEN rollback is positively unavailable and a permitted alternate branch is fully satisfied THE SYSTEM SHALL permit readiness while preserving rollback as unavailable.
- **DBGREADY-8.8** WHEN a human accepts risk against a non-waivable dependency THE SYSTEM SHALL keep the decision `not_ready`.
- **DBGREADY-8.9** WHEN a rendering summary converts an alternate-path dependency to satisfied THE SYSTEM SHALL fail the rendering evaluation.
- **DBGREADY-8.10** WHEN an execution attempt references stale authorization THE SYSTEM SHALL reject the attempt's authorization provenance.
- **DBGREADY-8.11** WHEN action authorization or verification attempts to promote causal strength THE SYSTEM SHALL reject the causal transition.
- **DBGREADY-8.12** WHEN a legacy Markdown pack is presented as contract-compliant without conversion THE SYSTEM SHALL return `legacy_unvalidated` rather than readiness.
- **DBGREADY-8.13** WHEN a consequential decision references a stale generated view THE SYSTEM SHALL refuse to append the decision event.
- **DBGREADY-8.14** WHEN immutable disposition, authorization, execution, verification, rollback, or risk history is edited or deleted THE SYSTEM SHALL fail revision integrity validation.

## 9. Quality attributes

**Section-kind:** nfr

**Story:** As a stakeholder, I want measurable quality targets for debugging decision readiness, so that safety and reliability are not left implicit.

- **Performance:** None — the version-1 package tool is an offline, operator-driven CLI with no standing latency, throughput, or resource target.
- **Security:** **DBGREADY-9.1** WHEN behavioral fixtures contain designated credential or secret sentinels THE SYSTEM SHALL produce zero plaintext sentinel values in canonical revisions, generated views, validation output, and exports — verified by automated fixture scans.
- **Reliability:** **DBGREADY-9.2** IF an authoritative mutation is interrupted before the next revision commits THEN THE SYSTEM SHALL leave the prior revision readable and hash-valid — verified by automated failure-injection tests.
- **Accessibility:** **DBGREADY-9.3** WHEN human-readable views are rendered THE SYSTEM SHALL express readiness, policy alternatives, contradictions, limitations, and provenance in text without depending on color — verified by rendered-structure snapshots.

## 10. Existing contract guards

**Story:** As a maintainer, I want to verify that the new contract preserves the debugging safety rules already encoded in the repository, so that stronger decision readiness does not weaken current investigation discipline.

**Files:**

- `AGENTS.md`
- `README.md`
- `CHANGELOG.md`
- `skills/execution/root-cause/SKILL.md`
- `skills/execution/root-cause/TESTS.md`
- `skills/execution/root-cause/eval.json`
- `skills/execution/debug-remote/SKILL.md`
- `skills/execution/debug-remote/evidence-pack.md`
- `skills/execution/debug-remote/TESTS.md`
- `skills/execution/debug-remote/eval.json`
- `docs/guide/skills/root-cause.md`
- `docs/guide/skills/debug-remote.md`
- `docs/guide/process/on-ramps.md`
- New schema, policy, validator, renderer, command, and fixture files selected by design.

- **DBGREADY-10.1** (guard) WHEN debugging begins THE SYSTEM SHALL CONTINUE TO require inspectable evidence before a fix is proposed or applied.
- **DBGREADY-10.2** (guard) WHEN a shared deployed environment is investigated THE SYSTEM SHALL CONTINUE TO prohibit agent-initiated writes and mutating production replay.
- **DBGREADY-10.3** (guard) WHEN a required remote-identity, access, or external-dependency evidence field is unknown THE SYSTEM SHALL CONTINUE TO record it as unresolved or explicitly unavailable as prescribed by the owning contract rather than invent a value.
- **DBGREADY-10.4** (guard) WHEN a red-capable signal can be constructed THE SYSTEM SHALL CONTINUE TO run the signal before hypothesis testing.
- **DBGREADY-10.5** (guard) WHEN hypotheses are tested THE SYSTEM SHALL CONTINUE TO require falsifiable predictions and one-variable discriminating changes.
- **DBGREADY-10.6** (guard) WHEN a failing path crosses a versioned external dependency THE SYSTEM SHALL CONTINUE TO require runtime identity, version-applicable owning documentation, and a contract comparison before dependency behavior is claimed.
- **DBGREADY-10.7** (guard) WHEN a dependency contract mismatch is observed THE SYSTEM SHALL CONTINUE TO treat the mismatch as a hypothesis candidate rather than a confirmed cause.
- **DBGREADY-10.8** (guard) WHEN a corrective fix is implemented THE SYSTEM SHALL CONTINUE TO require a failing regression behavior before production-code changes.
- **DBGREADY-10.9** (guard) WHEN a corrective fix is verified THE SYSTEM SHALL CONTINUE TO require the regression check, full suite, and original symptom signal to pass freshly.
- **DBGREADY-10.10** (guard) WHEN temporary debugging instrumentation is used THE SYSTEM SHALL CONTINUE TO require its removal before completion.
- **DBGREADY-10.11** (guard) WHEN the debugging workflow changes THE SYSTEM SHALL CONTINUE TO keep the human guides synchronized with the behavioral contract.

Touched files with no existing behavior to guard:

- `skills/execution/root-cause/TESTS.md` — new file.
- New schema, policy, validator, renderer, command, and fixture files — new files.

## Out of Scope

- Enforcing decision readiness in requirements, design, planning, merge, release, or other non-debugging workflows.
- Making the causal-evidence graph a repository-global evidence model.
- Granting the agent production-write capability or treating recorded authorization as a capability token.
- Certifying factual truth, causal correctness, intervention success, cryptographic actor identity, or tamper-proof custody.
- Adding `preventive_correction` or another fourth authorized action class in version 1.
- Building an organization-specific incident backend, role hierarchy, identity provider, or evidence store.
- Treating legacy Markdown evidence packs as compliant without provenance-preserving conversion and validation.
- Allowing independently authored Markdown to carry authoritative state.
- Automatically committing debugging packages or raw production evidence to Git.
