---
name: build-lexicon
description: Use when new words, phrases, collocations, or vocabulary must be saved or moved through the practice vault — produces chunk-first lexicon entries, each carrying its function, a source example, and a sentence the learner wrote.
---

# Build lexicon

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Contract

An entry is the phrase as the source actually used it, plus what it does in a conversation,
plus one authentic example with a link, plus one sentence the learner wrote about their own
work or life. The `lexicon.md` row has a column for each; a row with a blank column is not an
entry yet.

This is the home of the chunk rule: `mine-source` and `rehearse-transfer` file through here
rather than restating it.

## Recipe

1. Fill every column of the `lexicon.md` row. The `my sentence` column is the one that decides whether the entry exists — collect it in the same turn, while the chunk is still in play.
2. Capture the span as the source shows it. A single word is the entry only when the source shows that word standing alone; otherwise file the collocation it appears inside, because a word without its partners does not become speech.
3. State moves on the ladder in `capability-map.md` — R1 recognised → R2 used with preparation → R3 used unprompted — and that file holds the rules for earning each. `next_due` follows `config.due_buckets`: correct use promotes a bucket, failure resets to the first.
4. Cap live entries at `limits.lexicon_live`. Over cap → retire the **oldest R3** rows to the Retired section, keeping the newest in play.
5. Retire on R3 plus two unprompted sightings. Retired rows stay searchable and leave the due queue.
6. Link every entry to the capability or source it came from, so `review-practice-week` can see which themes are producing usable language and which are only producing notes.

## Rationalizations

| Thought | Reality |
|---|---|
| "File it now, they'll write a sentence later" | Later never happens, and the row stays a word list |
| "Just the word is enough, they know the rest" | The partners are the part they do not know |
| "They recognised it — that's R2" | Recognition is R1. R2 is production, with preparation |
| "Keep everything, storage is free" | Attention is not. Over the cap the due queue stops being workable |

## Red flags

- A `lexicon.md` row with a blank `my sentence` or `function` column
- A headword filed where the source showed it inside a collocation
- Live count over `limits.lexicon_live`
- A state promoted with no sighting recorded

## Done when

Every new row has all four columns filled; states follow `capability-map.md`'s ladder; live count within cap.
