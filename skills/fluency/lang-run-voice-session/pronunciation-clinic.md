# Pronunciation clinic

Load this file when the same `P-*` row has appeared in the voice debrief twice in a row, or
when the learner asks for pronunciation work directly. Conversation practice cannot fix a
sound the learner does not yet hear; the clinic can.

Run it as the second half of a voice session, after the conversation and its debrief.

## Contract

Each clinic item leaves a `P-*` row in `capability-map.md`, a ranking position by
intelligibility cost, one drill matched to that item's type, and two recordings — before and
after — both linked in the row. One recording is a sample; the pair is the evidence.

## Recipe

1. Anchor: `config.pronunciation.accent_anchor` for production, `config.pronunciation.listening_accents` for input. With `accent_erasure: false`, the target is being understood; keep every drill framed that way.
2. Diagnose from audio. If no recording of the item exists, ask for 30 seconds of speech on any cycle theme and work from that. Learners misdescribe their own sounds, so a description locates what to listen for — it is not the diagnosis.
3. Rank by intelligibility cost:
   - what actually broke comprehension for a listener;
   - what carries the target language's rhythm — word and sentence stress, linking, weak forms, reduction;
   - individual segments produced differently but intelligibly.
   Work top-down. A rhythm problem outranks a vowel almost every time.
4. **Perception check before production drilling.** Play the contrast and have the learner identify which one they heard, several times. If identification is unreliable, drill discrimination only — minimal pairs to hear, not to say. Production drilling on a contrast the learner cannot hear trains a guess.
5. Match the drill to the item:
   - segment contrast → minimal pairs;
   - rhythm, linking, reduction → a shadowing segment from a mined source;
   - word or sentence stress → a stress-marked read-aloud.
6. Re-record the same material after the drill. Link both recordings in the `P-*` row.
7. An item that survives two clinics goes into the next `lang-plan-cycle` as a focus capability — at that point it is a capability gap, not a session-level slip.

## Red flags

- A diagnosis with no recording behind it
- Segment work started while stress and linking are unaddressed
- Production drilling with no perception check
- A `P-*` row with only one recording linked
- The clinic run in place of the conversation rather than after it

## Done when

Items ranked by intelligibility cost; `P-*` rows created or updated; perception verified before production drilling; before and after recordings both linked.
