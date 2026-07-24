# Quiz quality rules

Load when authoring the five quiz items for a comprehension packet.

## Contract

- Exactly **five** medium-difficulty multiple-choice questions — **never omit** for “trivial” changes.
- Each question: prompt + **four** options + one correct index + feedback for correct and for each wrong option.
- Target **behavior, causality, contracts, edge cases, trade-offs** of *this* change — not trivia or bare API-name recall.
- Distractors = **plausible misconceptions**, not jokes or “all/none of the above” as the default pattern.
- Keep options **comparable** in length, grammar, and specificity so the correct answer is not the longest/most confident.
- Shell **shuffles** option order from a per-page seed; do not rely on source order.
- No answer-leak in stems, option labels, or pre-click ARIA text.

## Done when

Five items meet the rules above and map to the resolved change (and any cited DECs).
