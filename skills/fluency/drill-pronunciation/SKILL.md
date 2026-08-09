---
name: drill-pronunciation
description: Use when a sound, accent, stress pattern, rhythm, or intonation contour needs targeted work — produces phonology capability rows ranked by intelligibility cost, a matched drill, and the before/after recordings that evidence them.
---

# Drill pronunciation

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Contract

Each item leaves a `P-*` row in `capability-map.md`, a ranking position by intelligibility
cost, one drill matched to that item's type, and two recordings — before and after — both
linked in the row. One recording is a sample; the pair is the evidence.

## Recipe

1. Anchor: `config.pronunciation.accent_anchor` for production, `config.pronunciation.listening_accents` for input. With `accent_erasure: false`, the target is intelligibility and rhythm; keep drills framed on being understood.
2. If no recording exists for the item, ask for 30 seconds of speech on any cycle theme and diagnose from that. Learners misdescribe their own sounds, so a written description is a starting point for what to listen for, never the diagnosis itself.
3. Rank findings by intelligibility cost:
   - what actually broke comprehension for a listener;
   - what carries the target language's rhythm — word and sentence stress, linking, weak forms, reduction;
   - individual segments the learner produces differently but intelligibly.
   Work top-down. A rhythm problem outranks a vowel almost every time.
4. **Perception check before drilling production.** Play the contrast and have the learner identify it. If identification is unreliable, drill discrimination first — minimal pairs to hear, not to say. Production drilling on a contrast the learner cannot hear trains a guess.
5. Each item → a `P-*` row plus one matched drill: minimal pairs, a shadowing segment from a mined source, or a stress-marked read-aloud.
6. Re-record after the drill. Link both recordings in the row.
7. Items that persist across two sessions become focus in `run-voice-session`, where they meet real speaking pressure.

## Rationalizations

| Thought | Reality |
|---|---|
| "They described the problem, that's enough to work with" | Listen to audio. Descriptions locate the item, they do not diagnose it |
| "Fix the individual sounds first, then rhythm" | Rhythm and stress carry more intelligibility than any single segment |
| "Drill it until they say it right" | If they cannot hear the contrast, repetition trains the wrong target |
| "Their accent should sound native" | Config says intelligibility. Frame the drill that way |
| "One recording is enough" | Without the before, the after proves nothing |

## Red flags

- A diagnosis with no recording behind it
- Segment work started while stress and linking are unaddressed
- Production drilling with no perception check
- A `P-*` row with only one recording linked

## Done when

Findings ranked by intelligibility cost; `P-*` rows created or updated; perception verified before production drilling; before and after recordings both linked.
