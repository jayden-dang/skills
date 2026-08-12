---
name: lang-mine-source
description: Use when authentic material — an article, video, podcast, meeting recording, or work document — should become practice rather than passive input; produces the source note carrying extracted chunks, a shadowing segment, mechanism-labelled comprehension gaps, and one production task.
---

# Mine source

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Contract

The source note carries five parts: what the material is and which theme slot it fills, the
learner's comprehension share on first pass, up to `limits.chunks_per_source` chunks filed
through `lang-build-lexicon`, one shadowing segment with its phonology rows, gaps each labelled
with the mechanism that caused them, and one production task reusing at least three chunks.

## Recipe

1. Record what the material is, why the learner chose it, and which slot of `config.themes` it fills.
2. **Comprehension check before anything else.** The learner reports roughly what share they understood on first pass. Below 70% → scaffold it: pre-teach the blocking chunks, replay in segments, give the topic frame. `config.materials_blend` is what governs how hard this cycle's input is; keep the source and add the scaffolding.
3. Extract at most `limits.chunks_per_source` **chunks**: collocations, functional phrases, whole clauses that carry a move. REQUIRED SUB-SKILL: use `lang-build-lexicon` to file them — it holds the rule for what counts as a chunk.
4. Choose one 30–60 second segment for shadowing. Note what makes it hard to say: linking, stress placement, reduction, rhythm. Each becomes or updates a `P-*` row.
5. Record the **gaps** — what could not be caught, each labelled with its mechanism: speed, unknown chunk, unfamiliar sound, or syntax the learner cannot parse. The mechanism is what turns a gap into a drill instead of a note-to-self.
6. Name one production task that reuses at least three of the extracted chunks in the learner's own context — their work, their week, their opinion. Not a comprehension quiz.
7. Write `sources/<slug>.md` and link it from the current cycle.

## Rationalizations

| Thought | Reality |
|---|---|
| "Too hard — pick something easier" | Scaffold it. The blend, not the moment's comfort, sets difficulty |
| "Pull out all the new vocabulary" | Over the cap nothing gets used |
| "They understood it, that's the win" | Comprehension without production leaves passive knowledge passive |
| "Note the gaps and move on" | An unscheduled gap repeats next month |

## Red flags

- More chunks than the cap
- Comprehension share unrecorded
- Source note with no production task
- Gaps recorded with no mechanism named

## Done when

Source note written with comprehension share, chunks filed through `lang-build-lexicon`, a shadowing segment with its phonology rows, mechanism-labelled gaps, and one production task reusing ≥3 chunks.
