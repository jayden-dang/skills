# A technical film of a spec

For the people who will build a spec and the people who review it: story by story, what each part will do, how it is
built, and why that design over what it rejected. It is the second film of a spec; the explainer (`explainer.md`) stays the
short one that makes someone understand the feature.

Two runs asked for this on 3.8.0 made an explainer instead. Each was one `world` of 21 and 19 lines on one view, with one
camera move or none; the call path, the offer states, the `Offer` type and the refusal table were spoken and never shown;
each decision was a small note box; both ran 114 to 119 seconds to fit a 120-second cap, one by cutting the state machine;
one jumped between stories and closed on "the five tasks". The shape below answers each of those.

In `src/script.json`, `source` is `{"kind": "spec", "ref": "<the commit>", "spec": "<the spec folder>", "cut": "technical"}`, and
`planned` is set as `explainer.md` says.

## 1. Read the spec for its design

- `requirements.md`: the stories, in order, and their SHALLs.
- `design.md`: every bullet under Decisions (the choice, what it rejected and why, the IDs it satisfies), and each part of the
  architecture: a call path, the states, a type or contract, a table of answers.
- Leave `tasks.md` out. Build order and task counts are for the agents who build it; the check fails a line that cites it.

*Done when: you can say, for each story, what it does, which design serves it and which decisions it rests on.*

## 2. Write it story by story

1. **The opening**, two or three lines: the problem on a named example, then the idea, in a `world` the stories come back to
   (`explainer.md` sections 1 and 2).
2. **Each story, in the order `requirements.md` gives**, as a chapter of three to five scenes:
   - *What it does*: the example moves on in the world, and the camera moves to the part this story is about.
   - *How it is built*: the design part that serves its IDs, on screen: `sequence` for a call path, `code` for a type copied
     from `design.md`, `table` for what each request answers, a world with arrows for the states.
   - *Why this design*: one `choice` scene for each Decisions bullet that satisfies this story's IDs.
   - *What goes wrong*: the edge its SHALLs guard (a late answer, a repeat, nothing free), back on the example.
3. **A closing `title`** saying where to read the spec.

Keep it readable for a reviewer who has not read the spec: the same example from start to end, one idea a line, one name
for one thing, and a term said plainly the first time it appears. A reason comes from the spec or the design.

Take the stories in order and never go back to an earlier one: a line that cites a story after a later one fails the check.
The film uses at least three kinds of scene besides titles, has a `choice` for every decision in `design.md`, and its world
moves the camera within 5 lines.

## 3. The `choice` scene

```json
{"id": "sweep", "kind": "choice", "title": "How a hold ends",
 "options": [{"label": "A sweep every 60 s", "why": "Survives a restart, and shows what it expired", "chosen": true},
             {"label": "A timer per offer", "why": "Lost on restart, with no record of what fired"}],
 "cost": "A hold can run up to 60 seconds over.",
 "beats": [{"text": "A hold can end by its own timer, or by a sweep.", "ref": "docs/specs/2026-11-rebooking/design.md:15"},
           {"text": "A sweep, because timers vanish on restart and nobody sees what fired.", "ref": "REBOOK-2.2"},
           {"text": "So a hold may overrun by up to a minute.", "ref": "docs/specs/2026-11-rebooking/design.md:15"}]}
```

| Slot | Means |
|---|---|
| `options` | 2 or 3 `{label, why, chosen?}`: the decision and what it rejected, exactly one `chosen`. They arrive through the first line |
| beats | The first line sets out the options, the second gives the verdict: the chosen one lights, the rest are struck through |
| `cost` | Optional: what the choice gives up, from `design.md`. It arrives on the third line, or with the verdict |

## 4. Length, language and report

Up to 300 seconds, about 45 a story. Cut a complication before a decision. `language`, `spoken` and the words kept exactly as
the spec has them follow `explainer.md` section 4. The report says what `explainer.md` section 5 asks, and how many decisions
the film shows of how many `design.md` holds.
