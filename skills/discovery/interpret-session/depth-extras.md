# Normal/complex extras

The slots below only render on a **normal** or **complex** fork (see the depth table in `SKILL.md`). A **simple** fork or a no-choice paste never renders them.

## Before the stance

**4. Option deltas** (normal / complex) — one compact table of the dimensions on which viable options *actually differ*; then expand only the leading contenders. A table that restates the pasted card's own option paragraphs is padding; cut it.

**5. Picture or one scenario** (complex) — one ASCII diagram (topology / ownership / flow / boundary / lifecycle) **or** one walk of an actor through before / during / after (policy / failure / time). Not both unless they answer different questions.

## After the stance

**7. Pressure-test** (normal / complex) — 2–4 questions the user can ask to *attack* the pick: weakest assumption, irreversible cost, likely future requirement, or failure mode. Not a direction menu. Not "which do you want?"

**8. Decision boundary** (complex, or when adjacent constraints could ride in on one-word approval) — what locks if they accept the pick; what stays open.

## Then the detail behind the stance

Label blocks with these claim prefixes where they apply — **Source claim**, **Verified fact**, **Inference**, **Open question**. A **Verified fact** is not finished at the citation: end it with `→` and what the fact does to the live choice. A fact whose consequence the reader must assemble themselves is homework, not analysis. Cover:

| Element | Covers |
|---|---|
| **Map vs territory** | where the paste is a model of the work (prompt/spec/plan) and where the codebase or reality may disagree; cite `file:line` when you checked |
| **Knowns sketch** | when a real choice is open: what is locked, what is still unknown, what is an assumption dressed as a decision, and whether the user has **evaluation criteria** to judge the options (if not, say so and teach or research the criteria before piling on alternatives) |
| **Alternatives** | at least one genuinely different approach the other session did not lead with. The strongest runner-up already lives in the stance; do not repeat it here unless the causal mechanism needs expansion |
| **Trade-offs** | side by side only where they add evidence or mechanism beyond **Runner-up** and **Cost I accept**. Padding tables: same cut as step 4 |
| **Hidden assumptions** | what the pasted response takes for granted that may not hold here |
| **Risks** | where each option bites later |
| **When each wins** | the conditions that make each the right call, tied to the posture |
| **One concrete walk when the territory leaves the repo** | a card argued on an external standard, library, or protocol gets one real-shaped artifact: a sample log line, a two-node trace sketch, the query the user would actually run. The walk does for external territory what `file:line` does for the repo. Skip if step 5 already walked the consequence |
| **References** | when prose cannot carry the intent, name code, components, or external implementations to point at instead of more description |

Implementation-grade constraints the analysis surfaces — version pins, shutdown ordering, test lists — do not sit mid-analysis: collapse them into a short *for the spec* tail at the end, or carry them as **Weigh** items in the reply. The user is deciding direction; the implementing session consumes that grade of detail later.
