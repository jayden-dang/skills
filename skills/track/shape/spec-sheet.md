# The spec sheet

One self-contained `RUN/sheet.html`, written when the spec is closed, with or without a film. It is a technical sheet: one page of
lettered panels inside a ruled frame, so the whole spec is in view at once, like an engineering drawing. The operator reads it, then
types `approve` or says what to change. It stays in `RUN`, uncommitted, and is written again whenever the spec changes.

Two runs on the earlier form, Sonnet and Haiku, each gave 0 figures and nothing to step through, and listed the requirements the film
left out as bare IDs, with no word of what they ask. A film explains and does not cover, so this sheet carries what the film cannot.

REQUIRED SUB-SKILL: use `craft-page`, treatment Utilitarian. Write it in `LANG` from `auto.md`. Code identifiers and IDs stay verbatim.
Every value comes from a file or a command output you read. A name or a value in the example may be invented, and comes from the film when there is one.
Sentences: one idea, at most 20 words, active voice, one word per thing, the example before the rule.

## The frame

- A thin double rule around the page, with column numbers along the top and bottom edges and row letters down the sides.
- Panels on a grid, with these rows at 1400 wide: A and B, half each; C alone; D and E, half each; F and G, half each; H two thirds and I one third. All one column below 900. Each panel opens with its letter in a filled square, its title, and at its right a small mono tag naming its source file.
- Hairline tables. Mono for rules, values and code. One accent for what holds, one warning color for what needs the operator.
- Each SVG has a `viewBox` no wider than its panel's width in pixels, and its text is at least 12px, so it shows at 12px or more. Five of the first six figures scaled their labels down to 6 to 8.5px, which nobody can read.
- The only controls are the walk's two buttons: no radio button, no checkbox, no text box to copy.

## The panels, in order

**A. The film.** With a film: `<video controls src="film.mp4">`, its length, and that it describes planned behavior and approves nothing. Under it,
one sentence for the problem and one for the idea. A film that was refused or never reached `PASS`: say so and why, then the two sentences.
Without `--video`: the two sentences alone.

**B. The map.** An inline SVG tree: the feature, its stories, and every live requirement ID written in full, each with a gloss of at most six words. With a film,
mark each ID as in the film or not, from the film's `out/uncited.json`.

**C. Walk one example.** One named person and real values, through the normal path and at least one thing going wrong, 5 to 9 steps, with
buttons to step back and forward. One inline SVG holds the same places on every step, and only what the step changes moves or changes color. Each step gives one sentence, its IDs,
what the data holds at that moment, and with a film a link to `film.mp4#t=<seconds>`. Without JavaScript the first step still shows.

**D. Anatomy of the rules.** The 2 to 4 requirements with the most consequence, each copied exactly from `requirements.md` in mono. Each clause is an
`inline-block` box holding its words with its label under them: trigger, response or value. Absolute positions put one run's labels on top of the next line.

**E. When something fails.** A table: situation, what the person sees, ID.

**F. Decided for you.** A table of every `agent-decided` and Weigh value: value, IDs, label. A number with a limit the spec states is also a small bar.

**G. The plan.** The tasks as a timeline in dependency order, each with the IDs it covers.

Each ID the film leaves out has its meaning in panel C, D or E: a bare ID in the map tells nobody what it asks.

**H. Needs you.** At most 5 items of at most 50 words, biggest consequence first, from `agent-decided` lines where reversing changes what the person sees or does, or where the
final review could not settle it. Each: what was picked, the risk, what reversing changes, your lean labelled as yours. When `work` declined any OPTIONAL cut, one item is
always the largest it declined, by plan lines, with its IDs: authors judged their own text, and one run declined all 7. None → say so.

**I. The title block**, at the sheet's bottom right, as on a drawing: feature, ticket, branch at commit, `Status: Draft`, spec paths linked to `requirements.md`, `design.md`
and `tasks.md`, and in one sentence: agents closed this spec, the operator has not read it. The receipt's `missing` line sits here when it names anything.

## Below the frame, collapsed

- **What the final review changed.** From `RUN/final-review.md`: how many items, how many applied or rejected, every item with its outcome.
- **What it touches.** Files outside the repo, with what each holds today from reading it, and when it changes. Repo areas with the guard protecting each. What it leaves alone. What it does not do.
- **How far to trust this.** Each gate's rounds; the receipt's `ran`, `subagents`, `missing` lines verbatim; Lock-required items the advisor would cut, one line each; the limits (same model, picks it approved itself); what nobody has verified.

The sheet ends on one line: type `approve`, or say what to change in plain words.

## Look at it

Render it at 1400 wide and read the image: a browser tool, or headless Chrome with `--window-size=1440,3000 --screenshot=<path>`. Then press the walk's
Next through to the last step, where a browser tool can. Neither first-draft run looked, and their overlaps and 7px labels shipped. Fix any overlap, cut-off text,
empty cell or label you cannot read, and look again. No browser on the machine → say so in panel I.

*Done when: you have read a render with no such fault, and the words outside the collapsed parts number under 1,500.*
