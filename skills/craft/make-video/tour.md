# A tour: how a project, a module or a change is built

A tour makes someone understand the code the way an engineer does: what the system is, what it is made of, how one
request moves through it, where each part lives, why it is that way, and how to change it safely. Both runs asked to
explain a whole project on 3.5 made one film of layers and a request path, then told the design system and the folder
layout as bullet points, and never moved from the whole system into a part.

`source` is `{"kind": "tour", "ref": "<the commit>"}`. Every line cites a `file:line` at that commit, or an ADR or design
doc. The check fails a tour with no `world`, a first `world` whose camera never moves, or no `tree`, and asks a third of
the lines to give a reason.

## Shape

1. **The map**, one `world` that zooms like the C4 model's "maps of your code": open on the system as one box among the
   people and systems around it, then move the camera into its containers (apps and data stores), then into the one
   container this film is about. C4's author finds the context and container levels "sufficient for most software
   development teams" (c4model.com/diagrams): go down to components only where the film needs them.
2. **One request end to end**, on the same map: arrows and changes on the words, or a `code` scene for the one hop that
   matters.
3. **Where it lives**, a `tree` scene: `paths` lists the files and folders the film names, each `{path, note, at?}`; a
   folder ends in `/`. The check fails a path that is not at the commit.
4. **Why it is this way**: the decisions from `docs/adr/` and the design doc, as lines or an `aside`.
5. **The design system**, when the code has one: a `tokens` scene with `file` and `tokens` of `{name, value, role}`,
   copied from that file; each is drawn as what it is (a colour as a swatch, a radius on a corner, a shadow under a
   card, a face as type), and the check fails a value the file does not hold. Show the components in the running app
   with a `clip` when it runs.
6. **How to change it safely**: the tests that guard it, the place to start, what breaks easily.

A tour of a module or a change takes the same steps at its own scale: the map opens on the module, or on the part the
change touches.
