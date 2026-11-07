# A film of a release

Both release films made on 3.0.0 came out as `title, clip, clip, title`: a feature film with a version number on it.
Nothing told the viewer how many things changed, which one they were watching, or what came next.

## Shape

1. A `title` that names the version and says how many things changed.
2. A map of the changes: a `timeline` from the previous tag to this one, one event per change, in the order the film
   takes them; or a `stat` when a number is the news, such as a measured gain. The check fails a release film with
   neither.
3. One scene per change, in the map's order, each in the kind that shows it best:

   | The change | Scene |
   |---|---|
   | Something a person sees and uses | `clip`, recorded at the tag |
   | Something that used to go wrong and now does not | `compare`, the previous tag beside this one (`pr.md` says how to record both) |
   | A rule no screen shows | `world` or `flow` |
   | A number that moved | `stat` |

4. A closing `title`.

```json
{"id": "map", "kind": "timeline", "title": "Since 1.2",
 "events": [{"label": "Countdown", "note": "minutes to boarding"}, {"label": "Delay alerts", "note": "one press"}],
 "beats": [{"text": "First, every sailing counts down to boarding.", "ref": "web/app.js:12"},
           {"text": "Then staff can report a delay with one press.", "ref": "web/app.js:30"}]}
```

| Slot | Means |
|---|---|
| `timeline.events` | 2 to 6 `{label, note?}`; each arrives on its line, or evenly through the last line when there are more events than lines |
| `stat.stats` | 1 to 3 `{value, label}`; a whole number counts up from zero on its line, any other value rolls in. 8 characters at most |
| `compare` | `before` and `after` name two clips added with `add_clip.py`, `labels` names the sides (default `Before`, `After`), and a beat's `side` dims the other side while that line plays, and its `focus` zooms both sides to the same rect |

Take the changes from the code at the tag against the previous tag (`git log <previous>..<tag>`), and leave out what the
code at the tag does not hold.
