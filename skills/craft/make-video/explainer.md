# Explain it

A film of a spec makes someone understand the feature. It does not walk the spec. Five films built by following the spec's
files, rule then contract then decisions then plan, passed every check and read like a list: "Then offers." "The sweep."
"The routes." 0 to 9% of their lines said why anything was so, and their owner said they summarized and justified instead of
explaining. Two films built as below measured 42 to 64%, and the owner chose them.

Nothing a spec film shows exists yet, so it has no footage, and the film says so. In `src/script.json`, `source` is
`{"kind": "spec", "ref": "<the commit holding the spec>", "spec": "<the spec folder>"}`, and `planned` is a short label in the
film's language meaning "planned, not built". It prints on every frame.

## 1. Find the story first

Read the spec, then write these four down before any scene:

- **The problem.** What goes wrong today, for a named person, in one sentence. The design's context usually holds it.
- **The idea.** What this feature adds, in one sentence.
- **The example.** One or two named people and real values, followed through the whole film. Invented names and values are fine.
- **The complications.** Three to five "but what if" questions. Keep one only when the example visibly breaks without the rule
  that answers it.

*Done when: you can say the film aloud with no scene in mind.*

## 2. Write it in that order

1. The problem, shown on the example, as the film's first words. Four films opened on "This film explains how...", which tells nobody anything.
2. The idea.
3. The example moving forward, with each complication arriving as it happens: a line that opens the problem ("But Lan may answer late"), then a line that closes it ("So the offer holds the seat"). Time only runs forward. Two films let Lan accept her seat, then asked what if she answers late and took it back from her.
4. How the example ends, then a closing `title` saying where to read further.

Write each line as one idea, in the active voice, and call one thing by one name for the whole film. A reason comes from the
spec or the design, so leave it out when neither states one. One draft said a 409 stays "because that is a real error for a real
editor", which no file says.

Choose what explains the feature and leave the rest out: `check_video.py` writes it to `out/uncited.json`. Each line's `ref` names its IDs.

*Done when: at least a third of the lines give a reason. The check counts them.*

## 3. Draw one world

One `world` scene holds the things the film talks about. They stay on screen and change, so the eye never has to find its place
again. Use several only for parts that share nothing.

```json
{"id": "world", "kind": "world", "title": "Rebooking",
 "objects": [
   {"id": "ferry", "shape": "card", "head": true, "x": 70, "y": 90, "w": 470, "h": 300, "label": "08:15 to Cat Ba", "size": 40},
   {"id": "lan", "shape": "pill", "x": 190, "y": 170, "w": 230, "h": 86, "label": "Lan", "tone": "accent", "fill": true}
 ],
 "beats": [
   {"text": "Lan has a seat on the 08:15 ferry.", "ref": "docs/specs/rebooking/design.md:9",
    "world": {"set": {"ferry": {}, "lan": {}}, "camera": {"x": -140, "y": 40, "w": 900, "h": 374}}},
   {"text": "Staff cancel it, so she needs another seat.", "ref": "REBOOK-1.1",
    "world": {"set": {"ferry": {"label": "08:15 cancelled", "tone": "bad"}}, "arrows": [{"from": "lan", "to": "ferry"}],
              "then": {"after": 0.5, "set": {"lan": {"tone": "bad"}}}}}
 ]}
```

| Slot | Means |
|---|---|
| `objects` | Everything in the world, hidden until a beat names it. `shape` is `card`, `pill`, `seat`, `code` or `note`. `tone` is `ink`, `accent`, `bad` or `muted` |
| `world.set` | Only what this line changes: `{}` shows a thing, `hidden: true` removes it, a new `x`, `y`, `label` or `tone` moves or morphs it |
| `world.arrows` | The arrows from this line on. `[]` clears them |
| `world.camera` | The part of the world in frame, `h` = `w` x 740 / 1780. It carries over until set again. Nothing on screen may be cut by the frame, and the check fails one that is: hide it, or widen the camera |
| `world.then` | A second change, `after` a share of the line, for a line over about 5 seconds |

Draw it so that it reads at a glance. Each rule here answers something a contact sheet showed:

- List containers first and what moves last: `objects` order is depth, and a passenger moved onto a later ferry vanished behind it.
- Set `head: true` on a container, or what it holds sits on its name.
- Start the camera close on the first thing and widen as the world grows. A first draft sat small in one corner of an empty frame.
- Put parts far apart, `x` past 2000, and move the camera between them. Keep every label at 36 or larger at the widest view of its part.
- Change something on every line. The last line too: one film closed on the frame before it.
- Place things so an arrow crosses nothing: it runs straight between the two boxes.
- Give a route, a type or a code name as a `code` object, in the spec's own characters.

When exact words carry the point, an `ears` scene holds requirements, with `rules` of `{id, text}` copied from `requirements.md`, and
a `code` scene holds `file` and `lines` copied from that file at the pinned commit. A `table` scene holds `columns` and `rows`.
The check compares `rules` and `lines` with the files. These interrupt the world, so use one only when the film needs that text.

## 4. Length and language

As short as the story allows, 120 seconds at most. A world line costs about 0.3 seconds beyond its speech. Cut a complication before
you shorten every line.

`language` sets the narration, the labels and `planned`. `rules` and `lines`, IDs, routes and code names stay exactly as the spec has
them. When a line holds something a voice would misread, set `spoken` to how to say it, and `text` stays on screen:
`{"text": "It answers 409.", "spoken": "It answers four oh nine."}`.

## 5. Report

Add that the film describes planned behavior, that watching it approves nothing, and how many IDs `out/uncited.json` lists.

## A feature that is already built

Tell the same story with `source.kind` set to `feature`. Film what a person sees with `clip` scenes, and draw in a `world` what no
screen shows. Set `planned` to say what state it is in, such as "On dev, dogfood running". Check what you say about the server on the
running system. One film about a built feature nearly shipped with "Planned, not built" because its spec still read `In-progress`,
so read the code at `$REF` before you write a state.
