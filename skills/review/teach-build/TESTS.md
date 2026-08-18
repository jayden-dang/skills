# teach-build — test evidence

Model roster: **Sonnet only** (user directive 2026-08-18: every subagent this
skill is tested on and dispatches runs Sonnet). All transcripts below are
Sonnet, fresh context per rep, via general-purpose subagents.

Fixture: `fixture-expd` — a two-commit repo (commit 1: platform substrate
`store.py` / `http.py` / `worker.py` / `notify.py`; commit 2: feature EXPD
`export_api.py` / `exports.py` + 2 committed tests + `requirements.md` with
6 EARS IDs) plus `.skills/EXPD/` ephemera: `progress.md` (6-task wave
ledger), `implementation-notes.md` (two nine-field deviations:
unknown-unknown retry-decorator, assumption-break async notify),
`acceptance.md` (14/14 ledger, 2 tests promoted). Deliberate teachables the
fixture buries: the shared `notify._PENDING` flush coupling, the assumed
`jobs` UNIQUE constraint no schema defines, 4/6 requirements with no
committed regression test.

## RED — baseline, no skill (2026-08-18)

Shape criteria fixed before the runs: S1 journey grounded in
implementation-notes; S2 operation explained across pre-existing components
outside the diff; S3 one systematized artifact with real diagrams; S4 no
invented process facts; S5 ranked importance.

Two prompt arms, two reps each:

**Rich arm** (prompt itself asked for "how it operates inside the system…
systematize it, diagrams welcome"):

- Rep 1: wrote a local HTML page AND published a claude.ai artifact
  (unrequested). S1/S2/S4/S5 pass.
- Rep 2: published a claude.ai artifact **only** — no local file at all;
  deliverable existed solely on an external service nobody asked for.
  S1/S2/S4 pass.

**Terse arm** (realistic invocation: "Teach me this build before I decide on
the merge."):

- Rep 3: chat-only markdown dump. **No file, no artifact, zero diagrams.**
  S1/S2/S4 pass; S3 fail.
- Rep 4: chat-only markdown dump. Same: no file, zero diagrams. S3 fail.

**Recorded conclusion:** content is not the failure — all four reps found
the deviations, crossed the diff boundary, and cross-checked the record
against the tree unprompted, so content rules would be no-op text. The
failure is **deliverable shape variance**: four runs produced three shapes
(chat dump / external-artifact-only / local file + unrequested publish),
none at a predictable path, and diagrams appeared only when the prompt
asked. Classification per author-skills: "complies, but the output has the
wrong shape" → positive recipe/contract, not prohibitions.

## GREEN — v1.0.0 contract, terse arm (2026-08-18)

Same terse scenario, skill body loaded verbatim in the prompt, one fixture
copy per rep (parallel reps would collide on
`.skills/EXPD/teach-build.html`). Every packet was verified mechanically by
the author (section greps, SVG count, external-URL scan, HTML parse) — not
by trusting the rep's report.

- Rep A: `.skills/EXPD/teach-build.html`, five sections in order, one
  inline-SVG sequence figure, zero external references, both notes entries +
  Revisit lines, operation map crosses `http.py` / `worker.py` / `store.py`
  / `notify.py` (all pre-existing), no external publish, final message =
  path + five-line summary. Contract holds.
- Rep B: same shape (plus a "Sources read / not found" preamble heading,
  which the body prescribes); single deliverable file; contract holds.
- Rep C (run with the meta-test appended): same shape; contract holds.

Edge rep (conditional branch): `/teach-build` on a clean single-commit repo
with no `.skills` artifacts — the rep stopped, wrote **no** HTML, quoted the
stop rule, and refused to fabricate Journey/Operation sections. Wobble: it
explained the stop but did not cleanly *name* `/study-change` as the
hand-off in its final line; transcript shows harness noise (it treated the
pasted skill body as untrusted, which a real Skill-tool load does not
trigger). Counted pass on the load-bearing assertion (no invented packet).

## REFACTOR / meta-test (2026-08-18)

No new rationalizations in any GREEN transcript. Rep C's meta-test answers,
verbatim in class:

- "CHAT PROSE IS A POINTER … NEVER THE DELIVERABLE" — named as the line that
  killed answering-in-chat; "that line is unambiguous."
- Publish-to-artifact "considered briefly … so I didn't" — stopped by the
  stays-local line plus the red flag.
- ASCII figure "rejected" — stopped by the ASCII red flag + craft-page
  requirement.
- "It should have said X" items: (1) tone for damning Record-vs-tree
  findings under "never a ship gate" — fixed in v1.0.0 by adding "A finding
  states fact plus citation; its consequence goes to Open questions" (all
  three reps had already converged on this behavior; the line pins it);
  (2) requirement-map row granularity for multi-file satisfaction chains —
  not fixed: reps A/B/C all converged on one row per ID unprompted, so
  added text would fail the no-op test.

Untested branch, recorded honestly: the `(session)` labeling rule for
orchestration facts fires only when the packet is built in the same session
that ran the build; every rep here was a fresh subagent, so the branch never
executed. It stays in the body as a conditional on an observable predicate;
first live close-time run should watch it.
