# Question card recipe

Load this file with the first card when the required output shape is uncertain.
`SKILL.md` remains authoritative for which slots are required.

## Contents

- Slot expansion (Radius through Stop)
- Recommendation argument
- Shape sub-slot
- Reference (a feature shipped products already have)
- Extra rationalizations (coverage / compat restatements)

## Slot expansion

Exactly **one** decision per message. Write cause-and-effect sentences in the
user's domain language. Preserve exact technical terms.

1. **Radius** — `architecture` · `data` · `auth/security` · `UX flow` ·
   `polish-diff`. Coverage ON adds `reliability` · `failure` · `operate`.
2. **Thread** — *Locked so far* · *This card* · *Still open after* (names, never
   "3 of 5").
3. **Territory** — grounded repo facts. Teach a blocking blindspot here. Do not
   invent. Do not ask the user to recall what you can read.
4. **Question** — the decision in plain language.
5. **Why it matters** — blast only (what rewrites if the answer flips). Graders
   are slot 7.
6. **Closes** — `known-unknown` · `unknown-known` · `blindspot-confirm`.
7. **Criteria (graders)** — 1–2 named pass/fail graders **above** Options on
   every high-blast radius. Recommendation cites them by name.
8. **Options (2–4)** — gains, pays, can break, better-fit. Bare labels are not
   options. **Shape** on `architecture` or `data`: caller-facing difference
   (signature, type, column, route, payload), ≤6 lines, no bodies, every option
   (not only the recommended one). **Reference** on a feature shipped products
   already have: see below.
9. **Recommendation** — Pick · Decisive factors (Territory + named Criteria) ·
   Runner-up · Accepted trade-off · Confidence / evidence gap · Reopen trigger
   (observable; “if requirements change” is not a trigger).
10. **Stop.** Wait. Recompute the open set, then next card or close package.

Visible order: `Radius → Thread → Territory → Question → Why it matters →
Closes → Criteria → Options → Recommendation → Stop`.

## Reference

WHEN the card decides a feature that shipped products already have — undo on
delete, sharing and access, invites, retries, notifications, search — one
option is **the proven reference, cut to fit**:

- **Reference** — the product that ships it, and why it is known to work (years
  in use, scale, a published guideline). REQUIRED SUB-SKILL: use `research` to
  confirm how it behaves. No lookup in reach → name it as recalled and
  unverified, with the page that would confirm it.
- **Pieces** — every piece it ships, in the order a user meets them, the first
  one included.
- **Cut** — each piece this repo's code and posture do not need, one reason
  each. What is left is the option, with its Shape like any other.

Draw it **first**, before any option of your own. It is where an option comes
from, not a citation added to ones you already drew. When two references split
on the very question the card asks — one does it on the server, one on the
device — that split is the evidence: say which reference this repo resembles,
and why. Judge it by the same Criteria, with no head start. It shows the feature
works for users, not that it fits this code.

Measured, two interviews — accidental note deletion, and sharing a note to
co-edit — drew every option from scratch and named no product. The sharing card
recommended a single `editor_id` column, a hard limit of one collaborator, where
the products people share notes in keep a list of them. The delete card offered
Undo as a standalone option and rejected it, where those products pair it with a
Trash. With this section in place, a reminders card drew two options of its own
first, then added the reference as a third, called it "the same as A", and named
two products that split on its exact question without using the split.

Not on a card whose decision lives inside the repo — where a check sits, which
module owns a field. No product ships that.

## Extra rationalizations

These restated coverage/compat counters live here so the root table stays
short. They still bind when Coverage ON or Compat obligation is in play.

| Thought | Reality |
|---|---|
| "Production intent means treat every schema change as if users were on it" | Delivery intent is the quality bar; Compat obligation names who is committed. On None the clean in-place rewrite is the Production answer. |
| "Nothing in the repo confirms that migration never ran — stay additive" | Compat obligation None is that confirmation. |
| "Additive is bounded debt — one follow-up migration retires the old column" | The follow-up is the debt. On None ship one shape. |
| "Reliability is later / skip the map" | When Coverage ON, Missing cells stay open. |
| "TBD is fine — Open Questions will catch it" | When ON: unowned TBD blocks close; signer required. |
| "Absent/MVP/Early = Production coverage" | ON needs all three gate parts. |
| "Parent tier-0 brief still needs full coverage" | Brief / tier-0 ⇒ OFF. |
| "OFF — keep a partial coverage map anyway" | OFF omits the map. Core close is slots 4–6 + problem lock. |
| "Put TBD and accepted risk in one bucket" | When ON: three distinct close slots. See `production-coverage.md`. |
