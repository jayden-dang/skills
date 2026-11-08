# Recorded scenes: a terminal and a chart

Both scenes play back what really happened; neither takes its content from the script.

## A terminal

Both runs asked to film a command-line tool on 3.5 drew `points` instead: "the skill's `clip` scene records a browser.
Putting terminal text in a browser page would be staging." Record the real command:

```bash
python3 "$SKILL/scripts/record_terminal.py" <project> sailings --cwd <worktree> \
  --env TIDEGATE_URL=http://localhost:$PORT --show "tidegate sailings" -- node bin/tidegate.js sailings
```

It runs the command and keeps what it printed in `src/terminals.json`. `--show` is the command as a reader should see
it. In a `terminal` scene, a line with `"run": "sailings"` types that command and prints its output; earlier runs stay
above. Its `ref` is `run: sailings`. The check fails a run that was never recorded.

## A chart

Both runs asked to show how much faster a branch is drew two `stat` scenes with numbers typed into the script, and one
showed a median of 0.47 ms while the `bench/results.json` it cited said 0.51. A `chart` reads its numbers from a file
at the pinned commit:

```json
{"id": "speed", "kind": "chart", "title": "One poll, 5000 alerts", "unit": "ms", "data": "bench/results.json",
 "series": ["main", "perf/board-refresh"],
 "groups": [{"label": "median", "values": ["before.median_ms", "after.median_ms"]},
            {"label": "p95", "values": ["before.p95_ms", "after.p95_ms"]}], "beats": [...]}
```

`values` are dot paths into a JSON file (array indexes are numbers) or `row.column` into a CSV, one per series. Run
`python3 "$SKILL/scripts/chart_data.py" <project> <repo>` before the preview: it writes the numbers to `src/data.json`,
and the check fails a path the file lacks and a `src/data.json` that no longer matches. Bars start at zero on one axis,
one unit a chart, 1 to 4 series in the look's own validated colours, a legend past one series, the value on each bar;
each group grows on its line. Measure first when the file is not in the repo: commit the numbers, then chart them.
