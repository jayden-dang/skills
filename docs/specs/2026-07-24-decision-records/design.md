# Design: Boundary Decision Records

Feature code: DREC
Status: Implemented
Date: 2026-07-24
Requirements: ./requirements.md

## Context

Today the skill set's production boundaries execute human verdicts and record
nothing durable: finish-branch runs a four-option menu and discards the
decision with the conversation; release leaves a tag, a CHANGELOG entry, and an
INDEX status, but no record of the human judgment behind them; trace has no
concept of a decision record. The repository is confirmed greenfield for this
feature — no `docs/decisions/`, no `record-decision` skill, no validator, no
`ARCH-6` (scan digest: `.skills/drec-scan.md`).

Three constraints shape everything. First, ARCH-1/ARCH-3: the mechanical lane
must be LLM-free and must not mandate tooling consumers don't have — ARCH-3
names Python explicitly as non-mandatable, which together with DREC-11.23
forces the validator into POSIX sh + POSIX utilities. Second, distribution:
repo `scripts/` are not shipped by the plugin (no `scripts` key in
`.claude-plugin/plugin.json`), so the validator must live inside
`skills/ship/record-decision/` to reach consumers at all. Third, the verbatim
law: human prose must survive byte-exact inside a machine-checkable file, so
the grammar wraps prose in framing the writer controls and content can never
spoof.

One discovery-note premise did not survive contact with the repo: the research
digest (`docs/research/2026-07-23-own-the-outer-loop.md`) contains no
"six verdicts" list to map — Osmani's article names three responsibilities,
not a verdict taxonomy. The verdict enum is therefore derived from the ratified
emission cases in requirements story 6/7, which happen to yield exactly six
emitting verdicts. No requirement text depended on the Osmani mapping, so no
upstream sync-back is needed; this is recorded here so nobody goes hunting for
a list that doesn't exist.

## Decisions

1. **Grammar committed via design-twice.** Two divergent candidates were
   produced (A: minimal interface, 10 parser rules; B: maximal mechanical
   verifiability, 62 rules, count-and-skip framing, digests everywhere). The
   committed design is A's grammar with four B elements grafted on: envelope
   placement of storage dispositions (ratified D4 puts "storage disposition"
   in the envelope — A had it in the payload), a payload digest recorded at
   publication (tamper evidence at one rule's cost), the fixed
   withheld-sentinel (DREC-5.11 by construction), and the bidirectional
   supersession cross-check. Reason: B's full framing needs pass names outside
   the ratified vocabulary (E-digest/E-chain/E-anchor) and a validator too
   large for "small single file"; A alone lacks D4 conformance and any
   mutation evidence.
2. **Validator language: POSIX sh + POSIX utilities.** Compelled by ARCH-3
   ("never mandate Python") + DREC-11.23. Capability-dependent behavior
   follows the explicit ordered floors of decision 13: the digest can fail
   honestly (publication failure / validator not-run), while entropy has a
   guaranteed POSIX floor and never blocks — in neither case a silent pass.
3. **Verdict enum (closed, six):** `merge`, `pr`, `discard`, `block`
   (finish-branch), `release-approve`, `release-reject` (release). `keep`,
   pause/defer are non-emitting and outside the enum. Derived from DREC-6.3,
   6.5, 7.1, 7.6.
4. **Boundary-Type (open, syntax-only):** validated as `^[a-z][a-z0-9-]*$`,
   never against a membership list — this makes DREC-2.8 rename-safety
   structural. Initial documented table: `integration` (merge),
   `publication` (outbound PR), `disposal` (discard), `release`. A block
   verdict carries the boundary type of the crossing it blocked. Typos are
   undetectable by construction; accepted because emitters, not humans, write
   the tokens.
5. **Storage dispositions live in the envelope** (D4), keyed by element type
   (`Storage-Judgment:`, `Storage-Accepted-Risk:`, `Storage-Response-If-Wrong:`),
   since each type occurs at most once per record. The payload carries the
   verbatim block or the fixed withheld sentinel; the envelope carries the
   disposition and `Storage-Reference`.
6. **Corrections are new records, never edits.** Supersession = publish a new
   `DEC-*.md` with `Supersedes:`, append one `Superseded-by:` line to the old
   envelope. Effective view = follow `Superseded-by:` to the chain's end;
   linearity is E-grammar-enforced (no fork, no cycle, bidirectional match).
7. **Anchor identified by content marker, not filename** — first non-blank
   line `# Decision-Record Adoption Anchor` — so zero/multiple detection
   (DREC-11.12) is a real check. Conventionally written as
   `docs/decisions/ADOPTION.md`. DREC-11.11's immutability is a doctrine rule
   about skill behavior: no skill ever edits an anchor after writing it. A
   wrong anchor has no in-band correction path — repairing one is a direct
   human act outside the workflow (needing no record, per ARCH-6's mediation
   scope), with git history as the audit trail (accepted limitation).
8. **Tag citations carry name AND object ID** (`<ref-name>@<object-id>`) in
   both `Evidence: tag` lines and anchor `Baseline-Tag:` lines — one `@`-split
   rule, and the user-ratified tag-citation identity rule: a record cites a
   tag only if both name and object ID match; name-only never matches.
9. **No new ADRs.** Decision 2 is compelled by a live invariant (not
   surprising given ARCH-3); decision 6 restates approved requirement text
   (DREC-1.4/1.8). Nothing here is simultaneously hard-to-reverse, surprising
   without context, and a live trade-off, so the domain-modeling ADR gate is
   not triggered.
10. **No new dependencies.** Everything builds on POSIX utilities, git, and
    existing repo patterns; there is no third-party adoption to put to the
    user.
11. **Two-phase identity is structural.** The payload carries `Accepted:` and
    no publication ID; identity lives only in the envelope (`Published:`,
    `Reissued-as:`) and the filename. Nothing about minting or reissue can
    touch locked payload bytes, because the payload simply has no identity
    field to touch.
12. **Typed envelope outcomes are citations.** `Execution-Outcome: tag
    <ref-name>@<object-id> <note>` is a first-class tag citation for
    W-uncited-tag, equal in standing to a payload `Evidence: tag` line —
    required because a release record publishes before its tag exists.
    Name-only matching remains invalid in both positions.
13. **Capability floors are explicit, never assumed.** Entropy:
    `/dev/urandom` opportunistically, POSIX `awk`/`$$`/`date` as the
    guaranteed floor — degraded entropy is repaired by the ratified
    collision/reissue path and never blocks publication. Payload digest:
    ordered probe `sha256sum` → `shasum -a 256` → `openssl dgst -sha256`
    (recorded as `Payload-Digest-Algorithm: sha256`) → `git hash-object
    --stdin` (recorded as `git-blob`; git is already required by the emitters
    themselves, so this floor is always reachable at publication). If no
    probe succeeds at publication, publication fails honestly (DREC-15.2 via
    15.6). At verification time, a declared algorithm whose capability is
    absent makes the validator exit 2 (not-run, DREC-11.19) — digest
    verification is a required check, never silently skipped, so the tamper-
    evidence claim is never quietly vacuous. This satisfies DREC-11.23: every
    floor is a POSIX utility or git, nothing to install.

Invariants relied on: ARCH-1 (deterministic passes), ARCH-2 (optional layers
no-op), ARCH-3 (no mandated tooling), ARCH-4 (ID immutability), ARCH-5
(invocation direction). New: ARCH-6 (participant boundary, added by this
feature).

## Architecture

### 1. Record grammar — `skills/ship/record-decision/RECORD.md`

Satisfies: DREC-1.1, DREC-1.2, DREC-1.6, DREC-1.7, DREC-2.2, DREC-4.4, DREC-4.6, DREC-5.1, DREC-8.5
Respects: ARCH-4
Reuse: none — new grammar (rung 7); no existing artifact class represents locked-payload + append-only-envelope records

The sole grammar document. One record = one file
`docs/decisions/DEC-YYYYMMDD-XXXXXX.md`. Everything before the line exactly
`## Envelope` is payload; that line and after is envelope — one string
comparison splits the file. Fields are `Name: value` at column 0. Multi-line
fields — the three `Human-*` judgment fields, every `Predicate-*-Fact:` that
needs more than a line, and `Promoted-Evidence:` alike — put nothing after
the colon; each content line is prefixed `| ` (bare `|` for blank lines) and
the block ends at the first unprefixed line. The prefix rule is universal for
block content, human- or agent-authored, so no line of any block can sit at
column 0 and spoof structure (including a literal `## Envelope`); stripping
the prefix recovers exact bytes (DREC-4.3's mechanical substrate).

Payload fields — the payload carries **no publication identity**, because it
locks at acceptance while the ID is minted at publication: `Accepted:` (UTC
timestamp recorded before lock; its date is the ID's `YYYYMMDD` source),
`Emitter:`, `Verdict:`,
`Boundary-Type:`, `Scope:` (feature/requirement IDs or `none` — outward
citations only, DREC-1.6), `Crossing-Exists: true`, `Ceremony-Floor:`,
`User-Escalation:`, `Depth:` (`Guarded|Accountable` — `Minimal` illegal in a
published record), three `Predicate-*:` + `Predicate-*-Fact:` pairs,
`Human-Judgment:` / `Human-Accepted-Risk:` / `Human-Response-If-Wrong:`
(verbatim blocks or the fixed withheld sentinel line
`[[withheld — see envelope]]`), per-element `*-Pointer:` fields (interaction
pointer or `unavailable`, DREC-4.4), `Evidence:` lines (repeatable,
`<kind> <value>`; kind ∈ `commit|tag|pr|ci|release`; `tag` value is
`<ref-name>@<object-id>`), `Promoted-Evidence:` blocks (agent-authored; the
name deliberately avoids "digest", DREC-8.5).

Envelope fields: `Published:` (`<id> <UTC>` — the minted publication
identity; never rewritten), `Payload-Digest-Algorithm:` + `Payload-Digest:`
(recorded at publication, decision 13), `Storage-Judgment:` /
`Storage-Accepted-Risk:` / `Storage-Response-If-Wrong:`
(`repo-verbatim|withheld(reference)|withheld(unavailable)`),
`Storage-Reference-*:` (`<locator>|unavailable|n/a`), `Reissued-from:` +
`Reissued-as:` (appended as a pair at reissue, section 2),
`Supersedes:`, `Superseded-by:`, `Retired:`, `Execution-Outcome:` (repeatable,
append-only; the `tag` -typed form `Execution-Outcome: tag
<ref-name>@<object-id> <note>` is a first-class tag citation, decision 12).

Identity checks the validator derives from this: **effective identity** = the
last `Reissued-as:` value, else the `Published:` ID; the filename stem must
equal the effective identity; and the effective ID's `YYYYMMDD` must equal the
locked `Accepted:` date.

RECORD.md documents the boundary-type table as author guidance (never a
machine whitelist), states the verbatim guarantee as human provenance, not
authenticity (DREC-4.6), and defines the optional human-browsing index as a
regenerable projection that is never authoritative (DREC-1.7).

### 2. Identity, minting, and reissue

Satisfies: DREC-2.1, DREC-2.3, DREC-2.4, DREC-2.5, DREC-2.6, DREC-2.7, DREC-2.8, DREC-2.9
Respects: ARCH-4
Reuse: existing — POSIX `od`/`awk`/`date` for local entropy (rung 3)

Minting happens at publication (never acceptance): token = 6 chars mapped into
the Crockford alphabet from local entropy; date = the payload's locked
`Accepted:` date, preserved unchanged across late merges (DREC-2.9/2.1).
Entropy is an ordered capability probe (decision 13): `/dev/urandom` read via
`od` where readable; otherwise POSIX `awk` `srand()` mixed with `$$` and
`date +%s` — always available, weaker, and acceptable because collisions are
detectable (E-dup) and repairable (reissue) by ratified design; entropy
quality never blocks publication. No registry, no counter (DREC-2.3).

**Reissue is a pure append transition — no field is ever rewritten.** A
collision surfaces at merge as two files whose effective identities are equal
(E-dup). Resolution, on exactly one of the two files: mint a fresh ID, rename
the file to it, and append the pair `Reissued-from: <old-id>` (DREC-2.4's
ratified entry) and `Reissued-as: <new-id> <UTC>` to its envelope. The
original `Published:` line — the original publication identity — stays
untouched forever; payload bytes stay untouched; the other file changes not
at all. **Identity resolution is mechanical:** a file's identity chain is its
`Published:` ID followed by its `Reissued-as:` IDs in order; its effective
identity is the chain's last element; the filename stem must equal it.
A citation of ID Z resolves to the unique file whose effective identity is Z,
else to the unique file whose chain contains Z; if no unique holder exists the
validator reports it (E-dup family) — so after the standard
publication → collision → reissue sequence, citations of the contested old ID
deterministically resolve to the file that kept it, and the reissued file's
chain records both IDs for auditors. A re-collision on an already-reissued
file appends a second `Reissued-from:`/`Reissued-as:` pair, where
`Reissued-from:` names the immediately prior effective identity (the last
`Reissued-as:` value, not the original `Published:` ID) — the chain stays a
simple ordered list and the same rules apply unchanged. E-dup itself operates on effective
identities. Multiple records per feature+boundary and feature-less
(`Scope: none`) records are valid by construction (DREC-2.6/2.7).
Boundary-type renames touch only RECORD.md's guidance table, never filenames
or old records (DREC-2.2/2.8, decision 4).

### 3. Payload lock, supersession, and effective view

Satisfies: DREC-1.3, DREC-1.4, DREC-1.5, DREC-1.8, DREC-8.6
Respects: ARCH-4
Reuse: existing — mirrors the spec-spine retire-by-strikethrough ethos (rung 2, pattern)

At human acceptance the payload is locked; publication records its payload
digest — computed by decision 13's ordered capability probe and named in
`Payload-Digest-Algorithm:` — in the envelope, making later in-place edits
mechanically evident. A payload
defect — typo included — is corrected only by publishing a new record whose
envelope carries `Supersedes: <old-id>` (naming exactly what it supersedes,
DREC-1.4) plus one appended `Superseded-by: <new-id>` line on the old record.
Effective view (DREC-1.8): follow `Superseded-by:` forward; the record with
none is the single effective view. The validator enforces chain linearity —
at most one `Supersedes:` targeting any ID, at most one `Superseded-by:` per
envelope, bidirectional consistency, no cycles — all as E-grammar conditions.
Post-verdict outcomes and late evidence append as `Execution-Outcome:` lines
(DREC-1.5, 8.6); nothing after the lock touches payload bytes.

### 4. The record-decision skill — caller gate and emission contract

Satisfies: DREC-6.1, DREC-6.2, DREC-6.11, DREC-9.1, DREC-9.2, DREC-9.3, DREC-9.4, DREC-9.5, DREC-9.6, DREC-9.7, DREC-9.8, DREC-9.9
Respects: ARCH-5
Reuse: existing — `REQUIRED SUB-SKILL:` prose convention and skill-directory layout (rung 2)

New model-invoked skill at `skills/ship/record-decision/` (SKILL.md +
RECORD.md + validator; registered in `.claude-plugin/plugin.json`, which
`test_plugin_manifest.py` will enforce). Frontmatter description is
trigger-narrow: "Use when a named production-boundary emitter (finish-branch
or release) has obtained a terminal human verdict and hands off durable
evidence for publication" — no generic approval language (DREC-9.4). SKILL.md
opens with the caller gate as a HARD-GATE block: caller must be in the closed
set {finish-branch, release}; a terminal human verdict and durable evidence
must be in the handoff; anything else returns without an artifact
(DREC-9.5/9.6), and evidence producers cannot self-promote (DREC-9.7) — with a
rationalization table from the RED baselines. Records are emitted only for
verdicts this skill set mediated (DREC-6.11, citing ARCH-6). SKILL.md holds
doctrine only and points to RECORD.md for all grammar (DREC-9.1/9.2); emitters
carry a one-line `REQUIRED SUB-SKILL: use record-decision` handoff
(DREC-9.3). No root template exists or is generated (DREC-9.8). The skill is
model-invoked, reachable from model-invoked finish-branch and user-invoked
release (DREC-9.9, ARCH-5's permitted direction).

### 5. Depth computation and boundary lookup (record-decision doctrine)

Satisfies: DREC-3.1, DREC-3.2, DREC-3.3, DREC-3.4, DREC-3.5, DREC-3.6, DREC-3.7, DREC-3.8, DREC-3.9, DREC-3.10, DREC-3.11, DREC-3.12, DREC-3.13, DREC-3.14, DREC-3.17, DREC-3.18, DREC-3.19, DREC-3.20
Reuse: existing — reads posture/tier context from spec status + `docs/agents/project.md` exactly as other skills do (rung 2)

A fixed lookup, no per-crossing interview (DREC-3.8): ceremony floor from the
feature's spec tier (full triad → Tier 2 → Accountable; mini-spec → Tier 1 →
Guarded; release → Accountable), boundary floor from the boundary-type table
(disposal → Accountable, DREC-3.19), predicate escalation per DREC-3.5/3.6
with `depth = max(...)` (DREC-3.1–3.3), Minimal never published (DREC-3.4).
The external-audience bar is spelled out with the ratified evidence rules
(TRUE: mechanically established public; FALSE: only a current, authoritative,
exhaustive mechanical source; otherwise unknown; repo metadata never FALSE
evidence; no probes or interviews to lower; DREC-3.9–3.13) and the
unprompted-statement bound (DREC-3.20). Predicates are always evaluated and
recorded truthfully even when a floor already fixes depth (DREC-3.14). User
may escalate, agent never de-escalates (DREC-3.17/3.18); every lookup input
and result is written into the record's classification fields (DREC-3.7).

### 6. Judgment elicitation and the verbatim law (record-decision doctrine)

Satisfies: DREC-4.1, DREC-4.2, DREC-4.3, DREC-4.5
Reuse: none — new doctrine (rung 7); no existing skill elicits verbatim human judgment

Depth determines what is asked: Guarded → verdict + one judgment element;
Accountable → verdict + accepted risk + response-if-wrong (DREC-4.1/4.2).
The Iron Law block: store exact user-authored words only — never summarized,
improved, inferred, or manufactured (DREC-4.3); a bare "yes" to an
agent-authored risk statement is a verdict and nothing more (DREC-4.5), with
the rationalization table for the "the user obviously meant…" failure modes.
Interaction pointers attach where the harness permits, else `unavailable`
(grammar field per section 1).

### 7. Storage resolution and the secret scan (record-decision doctrine + validator `--scan`)

Satisfies: DREC-5.2, DREC-5.3, DREC-5.4, DREC-5.5, DREC-5.6, DREC-5.7, DREC-5.8, DREC-5.9, DREC-5.10, DREC-5.11, DREC-14.1
Respects: ARCH-2
Reuse: existing — the validator file also hosts the scan patterns, one shipped artifact (rung 2 within this feature)

Deterministic branch, exactly as ratified: standing repo-verbatim policy in
`project.md` applies without a quiz (DREC-5.2); explicit withhold always
offered (DREC-5.3); potentially sensitive prose gets one conditional
confirmation before acceptance (DREC-5.4); the exact payload is displayed
before acceptance locks it (DREC-5.5); withheld with a supplied locator →
`withheld(reference)` + locator; otherwise ask once; declined/unavailable →
`withheld(unavailable)` + `Storage-Reference: unavailable`, publication
continues, no re-asking, no blocking, W-opaque is not unfinished work
(DREC-5.6–5.9). The secret scan runs as `validate-records.sh --scan` over
judgment prose before any write (DREC-14.1): a fixed, documented pattern list
(private-key blocks, AWS `AKIA…`, GitHub `ghp_`/`github_pat_`, Slack `xox…`,
generic high-entropy `key/token/secret/password =` assignments) shipped inside
the validator so there is exactly one deterministic implementation. On a hit:
rephrase / withhold / stop — the only three continuations; redact-and-label-
verbatim is structurally impossible because a withheld element is the fixed
sentinel, never edited prose (DREC-5.10/5.11).

### 8. Publication ordering and failure semantics (record-decision doctrine)

Satisfies: DREC-15.1, DREC-15.2, DREC-15.3, DREC-15.4, DREC-15.5, DREC-15.6, DREC-15.7
Reuse: existing — stop-rule prose idiom from release's "The stop rule" (rung 2, pattern)

SKILL.md encodes the DREC-15.1 chain as a numbered checklist ending in
"crossing executes only after the validator exits 0 on the published file."
Publication failure of any kind — secret-scan stop, missing judgment (record
invalid at depth), validator exit 1 or 2 (DREC-15.6), filesystem write failure
— withholds the crossing and reports "verdict not enacted; crossing did not
occur" (DREC-15.2/15.3). Retry reuses captured contributions verbatim, never
regenerates them (DREC-15.4). Block/reject with failed publication reports an
unrecorded terminal verdict and an incomplete accountability workflow
(DREC-15.5). Post-publication crossing failure appends the failure as
`Execution-Outcome:`; the record stays valid (DREC-15.7).

### 9. Evidence rules (record-decision doctrine)

Satisfies: DREC-8.1, DREC-8.2, DREC-8.3, DREC-8.4
Reuse: existing — durable-ref vocabulary already used by release/finish-branch (tags, PRs, commits) (rung 2)

Citable kinds are the grammar's evidence kinds only; `.skills/`, temp logs,
local absolute paths, and session history are prohibited locator classes the
validator rejects mechanically (DREC-8.1/8.2). Promotion writes an ephemeral
artifact's substance into a `Promoted-Evidence:` block — agent-authored by
type, structurally excluded from ever satisfying a judgment field
(DREC-8.3/8.4) — and completes before payload display per section 8's chain.
Tag citations use `<ref-name>@<object-id>` — in payload `Evidence: tag` lines
for tags that exist before acceptance, and in typed `Execution-Outcome: tag`
envelope lines for tags the crossing itself creates (decision 12); in both
positions a citation matches a tag only when both halves match (user-ratified
identity rule).

**Handoff interface:** the emitter hands record-decision the verdict, the
classification inputs (tier, boundary type, predicate facts), durable
citations (commit IDs, PR refs, tag name@id), and any promotion content
**inline as text** — never a path under `.skills/`, a temp location, or a
session-history reference. Emitters may read ephemeral artifacts to compose
that inline substance, but nothing published, and nothing in the handoff the
record depends on, references an ephemeral location (DREC-8.2/8.3).

### 10. Adoption anchor

Satisfies: DREC-11.11, DREC-11.12, DREC-11.13, DREC-11.14, DREC-11.15, DREC-11.22
Respects: ARCH-2
Reuse: none — new artifact (rung 7); nothing existing represents an adoption baseline

Content-marked file (decision 7) carrying `Cutoff:` (ISO-8601 UTC, immutable)
and repeatable `Baseline-Tag: <ref-name>@<object-id>` lines snapshotting tags
at adoption (DREC-11.11/11.14). Written once by record-decision on first
adoption; never inferred from earliest record (DREC-11.13). Validator counts
content-marked anchors: ≠ 1 while any record exists → error (E-grammar family,
DREC-11.12); no anchor and no records → all passes no-op (ARCH-2). Candidate
post-adoption tag = visible tag whose name is absent from the baseline OR
whose object ID differs (DREC-11.22); tags invisible (`git tag -l` empty while
baseline non-empty) → W-uncited-tag no-ops (DREC-11.15).

### 11. The validator — `skills/ship/record-decision/validate-records.sh`

Satisfies: DREC-11.1, DREC-11.2, DREC-11.3, DREC-11.4, DREC-11.5, DREC-11.6, DREC-11.7, DREC-11.8, DREC-11.9, DREC-11.10, DREC-11.16, DREC-11.17, DREC-11.18, DREC-11.19, DREC-11.23, DREC-11.24, DREC-14.2
Respects: ARCH-1, ARCH-2, ARCH-3
Reuse: existing — trace's fixed-pass/fixed-diagnostic contract and output style (rung 2); POSIX sh + git only (rung 3)

Single POSIX sh file, ~15 parser rules (candidate A's 10 plus digest,
storage-envelope cross-check, chain bidirectionality, anchor count, prohibited
locator classes). Passes, ratified names only: **E-dup** (one ID, two files);
**E-grammar** (field/enum/depth violations, missing Storage, empty Accountable
judgment, framing errors, digest mismatch, broken chains, anchor-count,
prohibited locators, filename ≠ effective envelope identity, effective ID's
`YYYYMMDD` ≠ locked `Accepted:` date); **E-spine** (unknown `Scope:` IDs or demonstrably absent
resolvable pointers; whole pass no-ops when `docs/specs/*/requirements.md`
glob is empty, DREC-11.4); **W-uncited-tag** (candidate per section 10; the citation set is the union of
payload `Evidence: tag <name>@<id>` lines and envelope `Execution-Outcome:
tag <name>@<id>` lines across all records — both halves must match, name-only
never counts (decision 12); diagnostic text states "absent from or
changed since the adoption baseline", DREC-11.24); **W-repeated-judgment**
(≥3 byte-identical judgment elements after CRLF→LF + boundary-whitespace trim;
withheld sentinels, verdict words excluded; reports IDs; advisory only,
DREC-11.6/11.7); **W-opaque** (`withheld(unavailable)` only; valid references
never flagged, DREC-11.8/11.9). Crossing-without-record is not a pass at all —
absence stays a trace-level warning concern, never an error (DREC-11.10).
Diagnostics use trace's severity-prefix convention — `ERROR <pass> …` /
`warn  <pass> …` with the record file named in the message — plus a final
count line; the exact fixed line format is defined once in the validator
itself and merged verbatim into trace's report (per trace's own rule, the
finding set is contractual, the prose around it is not). Exit 0 = no errors;
1 = errors; 2 = could not run (DREC-11.19 → callers treat as not-run/failure,
never pass). Digest verification is a required check: a record declaring a
digest algorithm the environment cannot compute yields exit 2, so the
tamper-evidence claim is never silently vacuous (decision 13).
No LLM anywhere, external references judged only on syntax/locator-class/
secret patterns (DREC-11.17), byte-identical output on identical input
(DREC-14.2). Modes: `--mode=trace` (whole substrate), `--mode=publish
--record <file>` (whole substrate + the candidate; same rule set), `--scan`
(secret patterns on stdin, section 7).

### 12. trace integration

Satisfies: DREC-11.20, DREC-11.21
Respects: ARCH-1, ARCH-2
Reuse: existing — extends trace's conditional-pass pattern (passes 5–6 fire only when `docs/architecture/` exists) (rung 2)

trace SKILL.md gains one section, "Decision-record passes — only when
`docs/decisions/` exists," which shells to the validator and merges its
finding lines into the report. Existing passes 1–6 and findings E1–E5/W1–W3
are untouched (DREC-11.20), and the textual-presence coverage law is untouched
(DREC-11.21). Absent `docs/decisions/` → the section no-ops exactly like the
invariant passes. sync-spec and verify invoke trace already, so the new passes
propagate with zero edits to either.

### 13. finish-branch integration

Satisfies: DREC-6.3, DREC-6.4, DREC-6.5, DREC-6.6, DREC-6.7, DREC-6.8, DREC-6.9, DREC-6.10, DREC-6.12, DREC-6.13, DREC-6.14
Respects: ARCH-5
Reuse: existing — extends the existing menu/gate structure in place (rung 2)

Menu grows a fifth option, "Block: reject this work at this boundary
(records a terminal block verdict)" — existing four options unchanged in text
and order (DREC-6.4/6.14). Step 4 gains, per option: merge/PR/discard →
`REQUIRED SUB-SKILL: use record-decision` with the verdict, boundary type
(integration/publication/disposal), tier, and durable evidence — record
publishes before the git/gh action executes (section 8 ordering); keep →
explicitly no record (DREC-6.6). The gate STOP path is amended: while red, no
integration menu, but the user may still issue an explicit terminal block or
discard verdict, which emits against red evidence (DREC-6.8/6.10/6.12);
mechanical failure alone, or pause/defer, emits nothing (DREC-6.7/6.9).
Discard keeps the typed-`discard` confirmation (DREC-6.13) and always
classifies as `disposal` (section 5).

### 14. release integration

Satisfies: DREC-7.1, DREC-7.2, DREC-7.3, DREC-7.4, DREC-7.5, DREC-7.6
Respects: ARCH-5
Reuse: existing — extends the existing gate sequence in place (rung 2)

One record per release, created at the terminal verdict: after the smoke gate
and the user's explicit tag approval (step g's approval IS the successful
terminal verdict), release invokes record-decision with verdict
`release-approve`, folding the version/build/smoke/tag approvals in as
evidence lines (DREC-7.1/7.2); the record publishes before the tag is created
and pushed (section 8 ordering), and the created tag appends afterward as the
typed outcome `Execution-Outcome: tag <ref-name>@<object-id> pushed <UTC>` —
which is itself the tag's citation for W-uncited-tag (decision 12), so a
successfully released tag can never warn as uncited. An explicit user verdict to kill the release emits
`release-reject` (DREC-7.6); the stop rule firing without a verdict emits
nothing (DREC-7.3). The stop rule and both approval gates are unchanged
(DREC-7.4/7.5).

### 15. project.md pins

Satisfies: DREC-3.15, DREC-3.16
Respects: ARCH-2
Reuse: existing — new optional section in the existing `docs/agents/project.md` pattern (rung 2)

An optional `## Decision boundaries` section: a table of
`| Action | Boundary-Type | Floor |` rows. record-decision reads it when
present; pins may raise a floor or bind an action to a type; any entry whose
floor is below the core table's is ignored with a one-line notice
(DREC-3.16). Absent section → core table only (ARCH-2).

### 16. Participant-model surfaces

Satisfies: DREC-10.1, DREC-10.2, DREC-10.3, DREC-10.4, DREC-10.5, DREC-10.6, DREC-10.7, DREC-10.8
Respects: ARCH-2, ARCH-6
Reuse: existing — each surface extends an existing document in place (rung 2)

Four surfaces, one doctrine (Correction 1): (a) `docs/architecture/INDEX.md`
gains `**ARCH-6**` — one greppable sentence: skills MUST enforce and record
only actions this skill set mediates; membership is never inferred from
repository membership, roster, CODEOWNERS, branch ownership, PR authorship,
or supplied artifacts. (b) `docs/architecture/artifacts.md` gains the
three-role narrative (skill-mediated actor / external contributor /
accountable reviewer) — chosen over system.md because artifacts.md already
owns the consumer-artifact and trace model the roles qualify. (c) AGENTS.md
gains a short "Participant boundary" subsection carrying the ratified runtime
law verbatim — semantically complete, not a pointer (DREC-10.3), beside the
existing orchestration rules; Iron Laws and orchestration text untouched
(DREC-10.8). (d) using-skills gains the smallest projection — two sentences
distilling never-infer + supplied-evidence — because the session hook injects
the whole file every session and every token recurs (DREC-10.4); the
subagent-exemption and 1%-rule blocks are untouched (DREC-10.7). No other
skill copies the narrative; only record-decision, finish-branch, and trace
operationalize it where their behavior changes (DREC-10.5), including the
external-contribution non-violation rule stated once in ARCH-6's narrative
(DREC-10.6). The plan adds a drift check: a fixture test greps all four
surfaces for the load-bearing phrases so they cannot silently diverge.

### 17. interpret upgrades

Satisfies: DREC-12.1, DREC-12.2, DREC-12.3, DREC-12.4, DREC-12.5, DREC-12.6, DREC-12.7, DREC-12.8, DREC-12.9, DREC-12.10, DREC-12.11, DREC-12.12
Reuse: existing — extends interpret's existing loop and "Maintain the thread" section in place (rung 2)

Three additions to `skills/discovery/interpret/SKILL.md`: (a) a **ledger
block** — after any loop turn containing a decision event, render a compact
fenced ledger (`Decided / Open / Rejected-deferred`, one line each); no
decision event, no ledger render (DREC-12.1/12.2). (b) **Claim labels** — the
six bold prefixes on section-4 blocks (DREC-12.3), and the **rationale rule**:
when ≥2 live options existed, the choice closed a branch or fixed a
constraint, and no reason was given — one short question; verbatim quote if
already supplied; `Human rationale: not supplied` on decline; never inferred
(DREC-12.4–12.7). (c) an **end-of-session digest** section with the seven
ratified provenance labels and the transport-proves-adoption-not-authorship
rule (DREC-12.8/12.9). The read-only posture becomes explicit prose: interpret
never commits, publishes, or emits records (DREC-12.10); the five-section loop
and companion framing are untouched (DREC-12.11/12.12). interpret is
user-invoked, so no frontmatter change.

### 18. Documentation convention update

Satisfies: DREC-13.1, DREC-13.2
Reuse: existing — one-line addition to the existing layout block (rung 2)

`docs/architecture/artifacts.md`'s spec-folder layout gains one line —
`discovery.md  # optional, non-normative discovery handoff` — plus one
sentence: requirements.md remains the sole normative specification and a
discovery record is never required.

## Seams for testing

Existing seam patterns: python unittest under `tests/` (repo-internal, per
`docs/agents/project.md`) and the `tests/<feature>/scenarios.md` +
`red-baselines.md` fixture pair already used for skill-text behavior. One new
seam: the validator CLI.

| Seam | Kind | Covers |
|---|---|---|
| `validate-records.sh` CLI over fixture substrates (`tests/decision-records/fixtures/`) — NEW seam | unit | DREC-1.1, 1.2, 1.4, 1.8, 2.1, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.4, 5.1, 8.1, 8.2, 11.1–11.19, 11.22, 11.23, 11.24, 14.2 |
| `validate-records.sh --scan` with seeded-secret fixtures | unit | DREC-5.10 (scan trigger), 14.1 |
| Skill-text scenario fixtures `tests/decision-records/scenarios.md` + `red-baselines.md` (existing pattern) | integration (agent-run doctrine scenarios) | DREC-1.3, 1.5, 1.6, 1.7, 2.2, 2.3, 3.1–3.3, 3.5–3.20, 4.1–4.6, 5.2–5.9, 5.11, 6.1–6.11, 7.1–7.3, 7.6, 8.3–8.6, 9.3–9.7, 15.1–15.7 |
| Doc-content greps in unittest (existing textual-check pattern) | unit | DREC-9.1, 9.2, 9.4, 9.8, 9.9, 10.1–10.8 (incl. four-surface drift check), 12.1–12.12 (doctrine text presence), 13.1, 13.2, 6.12–6.14 (guard text), 7.4, 7.5, 11.20, 11.21 |

## Coverage check

Every DREC ID from requirements.md appears in exactly one `Satisfies:` line
above: 1.1–1.8 (§1, §3), 2.1–2.9 (§2, §1 for 2.2), 3.1–3.20 (§5, §15 for
3.15/3.16), 4.1–4.6 (§6, §1 for 4.4/4.6), 5.1–5.11 (§7, §1 for 5.1), 6.1–6.14
(§4 for 6.1/6.2/6.11, §13 for the rest), 7.1–7.6 (§14), 8.1–8.6 (§9, §3 for
8.6, §1 for 8.5), 9.1–9.9 (§4), 10.1–10.8 (§16), 11.1–11.24 (§10, §11, §12),
12.1–12.12 (§17), 13.1–13.2 (§18), 14.1 (§7), 14.2 (§11), 15.1–15.7 (§8).
Deliberately unmapped: none.
