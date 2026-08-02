---
name: audit-trace
description: Use when checking that every requirement ID agrees across where it is
  defined and task-cited in docs/specs — the docs-only vertical integrity pass
  invoked by prove-claim, cut-release, realign-spec, and plan-tasks's coverage
  check, or whenever requirements and tasks may have drifted. Produces a
  traceability finding set — IDs cited but never defined, duplicate definitions,
  approved-but-uncited warnings, and optional architecture Respects integrity.
  Does not search application source or tests for requirement IDs.
---

# Audit Trace

The vertical traceability check. It answers one question with evidence: **does
every requirement ID agree across where it is defined and cited in the spec
triad (and optional architecture docs)?**

It is not a judgment call. Every input is gathered with `grep` and reads —
deterministic passes — and every finding follows a fixed rule. Two agents running
this on the same repo reach the same finding set.

**Docs-only:** this check never greps application source, test files, or commit
messages for requirement IDs. Coverage of behavior by tests is enforced by
execute-family Spec review, `test-first`, and prove-claim verify commands — not
by embedding `CODE-N.M` in code.

## What it produces

A finding set, each item an ERROR or a WARNING:

| Code | Tier | Condition |
|---|---|---|
| **E1** | error | A task cites an ID that no requirements file defines |
| **E3** | error | The same ID is defined (bold) in more than one file |
| **W1** | warn | An `Approved` requirement is cited by no task |
| **W2** | warn | A `requirements.md` is missing its `Status:` or `Feature code:` line |
| **E4** | error | A `Respects:` line cites an `ARCH-N` no `docs/architecture/` file defines |
| **E5** | error | A `Respects:` line cites a retired (struck-through) `ARCH-N` |
| **W3** | warn | A live `**ARCH-N**` invariant is cited by no `design.md` |
| **E6** | error | A `Security:` line cites a `TB-N`/`THR-N`/`CMP-N` with no live bold definition in the canonical Approved security docs |
| **E7** | error | A `Security:` line cites a retired (struck-through) `TB-N`/`THR-N`/`CMP-N` |
| **E8** | error | The same `TB-N`/`THR-N`/`CMP-N`/`SLO-N` is bold-defined in more than one canonical file |
| **E9** | error | A `Reliability:` line cites an `SLO-N` with no live bold definition in Approved `docs/ops/reliability.md` |
| **E10** | error | A `Reliability:` line cites a retired (struck-through) `SLO-N` |

E4/E5/W3 come from the invariant passes, which only run when a spine exists.
E6–E10 come from system-ID passes; skip when the defining docs are absent or
non-authoritative. **Do not** warn merely because a live system ID has no feature
citation. **Do not** judge semantic conformance. **Do not** grep application or
test source for these IDs.

**Retired:** **E2** (code-side ID presence for Implemented/Shipped) is not
emitted. Do not reintroduce a finding that greps the codebase for IDs.

Errors mean the audit-trace is broken. Warnings mean the audit-trace is incomplete but not
wrong. `prove-claim`/`cut-release` treat any error as a failing gate; warnings are reported,
not fatal, unless the caller says otherwise.

## Inputs

- **Specs** live under `docs/specs/` (or the `specsDir` named in
  `docs/agents/project.md`). Definitions come from files ending `requirements.md`
  or `fixes.md`; task citations from files ending `tasks.md`.
- **Architecture** (optional): when `docs/architecture/` exists, invariant
  passes read that tree and `Respects:` lines in feature `design.md` files.
- **Decision records** (optional): when `.skills/decisions/` exists, run the
  shipped validator (see below).
- Skip `node_modules .git dist build target coverage .next .skills vendor` and any
  dotfile/dot-dir when walking trees other than the intentional decision-record path.

Do **not** search application or test trees for requirement-ID coverage. Legacy
`/// REQ:` or test-title tags in a consumer repo are ignored by this check.

## The passes

Run these against the repo root and read the full output of each — under the
whole-tree rule in the NON-NEGOTIABLE section below.

**1. Definitions** — bold IDs in requirements/fixes files, minus retired ones.

```bash
# every bold **CODE-N.M** in a requirements/fixes file, retired (~~struck~~) ones deleted first
grep -rnE '\*\*[A-Z][A-Z0-9]{1,11}-[0-9]+\.[0-9]+\*\*' docs/specs \
  --include='*requirements.md' --include='fixes.md' \
  | sed -E 's/~~[^~]*~~//g' \
  | grep -E '\*\*[A-Z][A-Z0-9]{1,11}-[0-9]+\.[0-9]+\*\*'
```

Each surviving line is `path:line:text`; every bold ID left on it is a definition,
owned by `path`. The `sed` deletes `~~ … ~~` spans, so a **retired** ID cannot reach
the result. A plain (non-bold) ID in a requirements file is prose, not a definition.

**2. Statuses and feature codes** — per requirements file.

```bash
grep -rnE '^(Status:|Feature code:)' docs/specs --include='*requirements.md'
```

`Status:` is one of `Draft | Approved | Implemented | Shipped` (first match wins).

**3. Task citations** — IDs on `_Requirements:` lines.

```bash
grep -roE '_Requirements:.*' docs/specs --include='*tasks.md' \
  | grep -oE '^[^:]+:|[A-Z][A-Z0-9]{1,11}-[0-9]+(\.[0-9]+)+' \
  | grep -E '^[^:]+:$|^[A-Z][A-Z0-9]{1,11}-[0-9]+\.[0-9]+$'
```

Only IDs on a line containing the literal `_Requirements:` are task citations. The
output alternates a `path:` line and the IDs cited in it — each ID belongs to the
`path:` above it. The trailing `grep` keeps only whole two-level tokens, so a
three-level `CODE-1.2.3` can never be read as a citation of `CODE-1.2`.

### Invariant passes — only when `docs/architecture/` exists

If the repo has no `docs/architecture/` directory, skip passes 4–5 entirely; the
finding set is passes 1–3, unchanged. When the spine exists, add:

**4. Invariant definitions** — bold `**ARCH-N**` in the spine, split into a *retired*
set (struck) and a *live* set (survivors), exactly as pass 1 handles requirements.

```bash
# retired invariants — the E5 set (struck-through, captured BEFORE deletion)
grep -rhoE '~~\*\*ARCH-[0-9]+\*\*~~' docs/architecture | grep -oE 'ARCH-[0-9]+' | sort -u
# live invariants — strike spans deleted first, then match (as in pass 1)
grep -rh '' docs/architecture --include='*.md' \
  | sed -E 's/~~[^~]*~~//g' \
  | grep -oE '\*\*ARCH-[0-9]+\*\*' | grep -oE 'ARCH-[0-9]+' | sort -u
```

The first grep is the **retired** set; the second (struck spans removed) is the
**live** set. An `ARCH-N` in neither is undefined.

**5. Respects citations** — each `ARCH-N` on a `Respects:` line in any `design.md`.

```bash
grep -rnE 'Respects:.*ARCH-[0-9]+' docs/specs --include='*design.md' \
  | grep -oE '^[^:]+:|ARCH-[0-9]+'
```

Each cited `ARCH-N` belongs to the `design.md` it sits in.

### System-ID passes — security and reliability (optional docs)

Skip entirely when the relevant canonical file is missing. Only extract
**definitions** from:

| Family | Definition file (canonical) |
|---|---|
| `TB-N`, `THR-N` | `docs/security/threat-model.md` |
| `CMP-N` | `docs/security/compliance.md` |
| `SLO-N` | `docs/ops/reliability.md` |

Definitions are bold `**TB-N**` / `**THR-N**` / `**CMP-N**` / `**SLO-N**` after
striking `~~…~~` spans (same retirement rule as requirements). Numbering is
repo-wide per family; never renumber or reuse.

**Citations** only from feature `design.md` lines:

```bash
# Security citations — only on Security: lines
grep -rnE '^Security:.*(TB|THR|CMP)-[0-9]+' docs/specs --include='*design.md' \
  | grep -oE '^[^:]+:|(TB|THR|CMP)-[0-9]+'

# Reliability citations — only on Reliability: lines
grep -rnE '^Reliability:.*SLO-[0-9]+' docs/specs --include='*design.md' \
  | grep -oE '^[^:]+:|SLO-[0-9]+'
```

Do **not** treat these IDs as task-footer citations. Do **not** emit a warning
solely because a live system ID is uncited by any design.

Rules when defining files exist:

- **E6** — Security: cites TB/THR/CMP not in live definition set
- **E7** — Security: cites retired TB/THR/CMP
- **E8** — same system ID bold-defined in two or more distinct definition files
- **E9** — Reliability: cites SLO not in live definition set in reliability.md
- **E10** — Reliability: cites retired SLO

## The rules

With the sets in hand — `defined` (ID → {file, status}), `taskCited` — apply:

- **E1** — for each ID in `taskCited` not in `defined`: report it and the citing
  task file(s). (IDs that appear only in application or test source are not
  task citations and never feed E1.)
- **E3** — for each ID bold-defined in two or more distinct files: report the files.
  (Two bold occurrences in the *same* file are not a duplicate.)
- **W1** — for each `defined` ID whose status is exactly `Approved` and not in
  `taskCited`: report it.
- **W2** — for each `requirements.md` (never `fixes.md`) missing a `Status:` or a
  `Feature code:` line: report which line is missing.

When `docs/architecture/` exists, also — with `liveArch`, `retiredArch`, and
`respectsCited` (ARCH-N → citing design) in hand:

- **E4** — for each `ARCH-N` in `respectsCited` that is in neither `liveArch` nor
  `retiredArch`: report it and the citing `design.md`.
- **E5** — for each `ARCH-N` in `respectsCited` that is in `retiredArch`: report it
  and the citing `design.md`.
- **W3** — for each `ARCH-N` in `liveArch` not in `respectsCited`: report it.

Status obligations at a glance:

| Status | Needs a task (W1) |
|---|---|
| Draft | no |
| Approved | **yes** |
| Implemented / Shipped | no (task history may remain; no code-side ID gate) |

`Status: Implemented` / `Shipped` evidence is process (tasks checked, verify green,
Spec review) — not a greppable ID in a test file.

## <NON-NEGOTIABLE> Task citation integrity is textual — do not judge it

An ID is **task-cited** when its string appears on a `_Requirements:` line. Full
stop. Do not read the task steps to decide whether the task "really" implements
the requirement. That judgment is Spec review / prove-claim, not this check.

Gather **every** matching requirements and tasks file under the specs tree.
Missing one requirements file invents a false E1; missing one tasks file invents
a false W1. Grep the specs tree; do not sample.

The same rule binds the invariant passes: E4/E5/W3 check only that a `Respects: ARCH-N`
citation names a *live* invariant — existence and liveness. Never judge whether the
design *actually* respects the invariant; that semantic call is `review-invariants` /
`inspect-change`, not `audit-trace`.

### Decision-record passes — only when `.skills/decisions/` exists

If the repo has no `.skills/decisions/` directory, skip this section entirely; the
finding set remains passes 1–3 (or 1–5) unchanged.

When `.skills/decisions/` exists, run the shipped validator (path relative to this
skill set install, beside `record-verdict`):

```bash
sh skills/ship/record-verdict/validate-records.sh --mode=audit-trace
```

Merge its diagnostic lines into the report **verbatim**. Exit code 1 → treat as
audit-trace errors (gate fail). Exit code 2 → decision-record passes **not-run**
(never "passed"). Exit 0 → no decision-record errors (warnings may still appear).

Do not reinterpret validator findings. **Crossing-without-record:** the validator
does not emit an automated finding for “a production crossing lacks a record,”
because it cannot tell skill-mediated verdicts from direct human action or
external contribution. If an agent or human notes such an absence, treat it as a
**warning-level concern only — never an error and never a cut-release/prove-claim gate
fail**. Existing E1 / E3–E5 / W1–W3 semantics are unchanged by decision-record passes.

## Output

Report the counts, then the findings:

```
trace: 24 requirements · 24 task-cited
  ERROR E1 task cites unknown requirement SHELL-9.9 (docs/specs/…/tasks.md)
  warn  W1 NOTES-2.1 (…/requirements.md, Approved) is not cited by any task
```

Exact wording and ordering are not contractual — the **finding set** is. If
`docs/specs/` does not exist, say there is nothing to check and stop. When a caller
(prove-claim, cut-release) needs a pass/fail, the gate is: zero errors.
