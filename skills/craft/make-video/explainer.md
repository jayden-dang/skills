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

One `world` scene holds the things the film talks about. They stay on screen and change as the voice names the change, so the eye
never has to find its place again. Use several only for parts that share nothing. The world is 1800 by 840: fill it.

```json
{"id": "world", "kind": "world", "title": "How an offer gets a seat",
 "objects": [
   {"id": "old", "shape": "card", "head": true, "x": 0, "y": 0, "w": 820, "h": 840, "label": "08:15"},
   {"id": "lan", "shape": "row", "index": "01", "x": 36, "y": 200, "w": 748, "h": 128, "label": "Lan"},
   {"id": "new", "shape": "card", "head": true, "x": 1110, "y": 0, "w": 690, "h": 840, "label": "09:30", "sub": "Cat Ba"},
   {"id": "seat", "shape": "seat", "x": 1146, "y": 200, "w": 618, "h": 160, "label": "Free seat", "tone": "accent", "size": 40}
 ],
 "beats": [
   {"text": "Staff cancel the 08:15, so Lan needs another seat.", "ref": "docs/specs/rebooking/design.md:9",
    "world": {"set": {"old": {}, "lan": {}},
              "then": [{"at": "so Lan", "set": {"old": {"sub": "Cancelled", "subTone": "bad"}}}]}},
   {"text": "The offer holds the free seat on the 09:30 while she decides.", "ref": "REBOOK-2.1",
    "world": {"set": {"new": {}, "seat": {}}, "stats": {"Free seats": 1},
              "then": [{"at": "while she", "set": {"seat": {"label": "Lan", "sub": "Held", "tone": "warn", "timer": 1800}}, "arrows": [{"from": "lan", "to": "seat", "tone": "warn"}], "stats": {"Free seats": 0}}]}}
 ]}
```

| Slot | Means |
|---|---|
| `objects` | Everything in the world, hidden until a beat names it. `shape` is `card` (a frame, with `head: true` its `label` is large, top left, and `sub` is a tag beside it), `row` (a line of a list: `label`, `sub` at its right, optional `index`), `seat` (a place that can be taken; a new `label` turns it over like a card, `timer` in seconds counts down on it, and `timer: 0` takes it away), `code` or `note` (a short mono caption). `tone` and `subTone` are `ink`, `accent`, `warn`, `bad` or `muted` |
| `world.set` | Only what this moment changes: `{}` shows a thing, `hidden: true` removes it, a new `x`, `y`, `label`, `sub` or `tone` moves or morphs it |
| `world.arrows` | The arrows from this moment on, each `{from, to}`, with an optional `tone` and `label`. `[]` clears them |
| `world.camera` | The part of the world in frame, `h` = `w` x 840 / 1800. It carries over until set again. Nothing on screen may be cut by the frame, and the check fails one that is: hide it, or widen the camera |
| `world.stats` | Numbers worth keeping in view, such as `{"Free seats": 2}`. They sit in the top band and roll when they change. Two or three at most |
| `world.then` | More changes inside this line, each landing on the word it starts on: `{"at": "so Lan", "set": ...}`. It takes `set`, `arrows`, `camera` and `stats` |

Put a change on the word that names it, and let no more than 9 words pass without one (14 in Vietnamese): nine words run about 3.5 seconds. Two runs on the old text made one change a line, and 21 of their 25 world lines ran past that, which is what a slideshow is. The check fails such a line, and a line that changes nothing.

Draw it so that it reads at a glance. Each rule here answers something a contact sheet showed:

- List containers first and what moves last: `objects` order is depth, and a passenger moved onto a later ferry vanished behind it.
- Set `head: true` on a container, or what it holds sits on its name, and leave its top 190 for the name.
- Put parts far apart, `x` past 2000, and move the camera between them. Keep every label at 30 or larger at the widest view of its part.
- Place things so an arrow crosses nothing: it leaves the side of its box that faces its target.
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
