# foundation-note / v1

Optional copy-paste packet from `deepen-codebase` for another session (e.g.
`interpret-session` or the main work window). **Knowledge only** — never a
recommendation vehicle.

Emit only on explicit user request. Put the packet in a fenced block.

## Required shape

```text
schema: foundation-note/v1
subject: <topic name>
target_language: <code or name>
learner_familiarity: new | partial | strong
project_posture: <delivery intent + lifecycle, or unknown>

## Must-know (foundation cards)
- (<kind>) <card> — <one line>
  provenance: USER_VERBATIM | AGENT_SYNTHESIS | VERIFIED_EVIDENCE | SOURCE_CLAIM | INFERENCE

## Layers touched
- F0: <one line or none>
- F1: …
- F5: … (cite paths when present)
- F2/F3: … (name sources)
- Gap / Fail / Ops: …

## Open knowledge gaps
- <gap> — cheapest next deepen if known

## Live options (only if user supplied them)
For each option: technical delta surfaces only — no ranking, no pick.
provenance per row.

## Explicit exclusions
- no recommendation
- no stance
- no English ship reply
- no "learning complete"
```

## Rules

- Field-level provenance preferred; legend-only is insufficient.
- Preserve user-authored wording verbatim.
- Code, paths, identifiers unchanged.
- If an English copy is needed: keep original; label translations
  `AGENT_TRANSLATION_OF_USER_VERBATIM`; round-trip what the English commits them to.
- Empty sections: write `none` — do not invent cards to look complete.
