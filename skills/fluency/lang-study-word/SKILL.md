---
name: lang-study-word
description: Use when the learner meets a new word, phrase, or expression and wants to actually use it — "what does X mean", "how do I use X", "teach me this word", "what's the difference between X and Y" — produces the word study note carrying a target-language meaning, word family, near-synonym contrasts, collocations, register, authentic contexts, and the learner's own sentences.
---

# Study word

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Contract

A word is learned when the learner can **produce it in the right place**, not when they can
recall its translation. The study note has seven REQUIRED slots, and a note missing any of
them is not finished:

1. **Meaning, in the target language** — defined with words simpler than the headword itself.
2. **Word family** — the forms that actually occur, each marked *produce* or *recognise only*.
3. **Near-synonyms, each with what separates it** — never a bare list.
4. **Collocations** — what it habitually combines with.
5. **Register and constraints** — where it fits, and where it would be wrong.
6. **Authentic contexts** — 2–3 real uses, from a source, not invented.
7. **The learner's own sentences** — one per context type, in their own work or life.

## Recipe

1. Define in the target language first, using words below the headword's level. Reach for the support language only after the learner has stalled twice on the same definition, and then gloss the concept, not the word — `config.language_policy` governs this.
2. **Word family**: list the forms that occur in real use, and mark each *produce* or *recognise only*. Most derivations are rare; teaching every form as equally usable is the commonest way vocabulary study wastes time.
3. **Near-synonyms with a distinguishing axis on every row.** A synonym list without contrasts is worse than no list — it licenses free substitution, which is exactly how a learner produces a word that is technically correct and audibly wrong. Each row names the axis: register, strength, connotation, or what it collocates with.

   | word | axis | when it, not the others |
   |---|---|---|

4. **Collocations**: the verbs, nouns, prepositions, and adverbs it habitually appears with. This is what turns a known word into a usable one — the learner already knows a word they cannot combine.
5. **Register and constraints**: formal / neutral / informal, spoken / written, and one place where the word would be wrong. The wrong case teaches the boundary faster than three more right ones.
6. **Authentic contexts**: 2–3 real examples with source links, spread across different situations. Invented example sentences hide the collocations that make the word work.
7. **The learner writes their own sentences** — one per context type, about their own work or life. Do not draft these; diagnose them. REQUIRED SUB-SKILL: use `lang-diagnose-output` if any sentence needs correcting.
8. Write `lexicon/<slug>.md`. REQUIRED SUB-SKILL: use `lang-build-lexicon` to file the ledger row, link the study note from it, and set the first `next_due` bucket.

## Review, later

The study note is the depth; the ledger row is what brings it back. `lang-run-session` pulls due
rows into production tasks and `lang-run-voice-session` steers them into conversation. Neither
asks for a definition — a word recalled is not a word used, and only unprompted use moves
the state.

## Rationalizations

| Thought | Reality |
|---|---|
| "Give the translation, it's faster" | The translation is the thing that has to be unlearned later |
| "List the synonyms, they'll work out the difference" | They will substitute freely and be wrong. Every row needs its axis |
| "All the word forms, for completeness" | Rare forms crowd out the two they will actually say |
| "Write them a few example sentences" | The coach's sentences prove nothing. Theirs are the evidence |
| "Made-up examples are clearer" | Invented examples quietly drop the collocations |
| "They understood the explanation — done" | Understanding is R1. The note is not finished until their own sentences exist |

## Red flags

- A study note with an empty slot among the seven
- A synonym row with no distinguishing axis
- Example sentences written by the coach and filed as the learner's
- A support-language gloss offered before two stalls
- Note written but no ledger row filed, so it never comes back

## Done when

`lexicon/<slug>.md` has all seven slots filled, the learner's own sentences are diagnosed, and the `lexicon.md` row links the note and carries a `next_due`.
