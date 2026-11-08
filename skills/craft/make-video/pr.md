# A film of a branch

Neither branch film made on 3.0.0 showed the change: `feat/quiet-hours` moves night alerts off the board, and one film
filmed only the night while the other filmed nothing. A reviewer sees a change best as the base and the branch side by
side.

## Shape

1. A `title` that says what the branch changes, for whom.
2. When the change shows in the app, a `compare` scene: the base on the left, the branch on the right.
   - Record each side from its own worktree, the base at `git merge-base main <branch>` and the branch at its head, on
     its own port, with the same steps, the same data and the same viewport. Name the clips for what they show, such as
     `day-base` and `day-branch`.
   - Set `labels` to the two refs as a reviewer knows them, such as `["main", "feat/quiet-hours"]`.
   - Give a line `"side": "before"` or `"side": "after"` when it is about one side; the other dims while it plays.
   - Give every line a `focus`, the rect it talks about in the page's CSS pixels, as a `clip` line does: it zooms both
     sides to the same place. The first compare film had none, and the board filled the top third of each side.
   - A state the app needs set up, such as a night clock, is staged on both sides the same way, and the scene's `staged`
     says so.
3. What no screen shows, such as a rule in the server or a new endpoint, in a `flow`, `world` or `code` scene.
   A change whose point is a number, such as a speed-up or a smaller reply, gets a `chart` read from the measured file
   (`data.md` beside this file).
4. A closing `title`.

```json
{"id": "night", "kind": "compare", "title": "A delay at night", "before": "night-base", "after": "night-branch",
 "labels": ["main", "feat/quiet-hours"], "staged": "Server clock set to 23:30 on both sides",
 "beats": [{"text": "On main, a delay at night goes straight to the board.", "ref": "alerts.js:4", "side": "before",
            "focus": {"x": 28, "y": 62, "w": 1544, "h": 260}},
           {"text": "On this branch, it waits in a held list instead.", "ref": "alerts.js:6", "side": "after",
            "focus": {"x": 1063, "y": 62, "w": 509, "h": 260}}]}
```

Something that stops appearing is a change a screen shows. One run left the `compare` out of `feat/quiet-hours`:
"The change has no visible effect on the board... showing night behaviour would mean changing the machine's clock",
though the whole change is a delay that reaches the board on `main` and does not on the branch. Stage the clock on both
sides and film it. Only a change whose two sides look the same in every state you can set up, such as a refactor, has
no `compare`, and the report says so.
