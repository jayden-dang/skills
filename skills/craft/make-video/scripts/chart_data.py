#!/usr/bin/env python3
"""Read every chart's numbers from its data file at the pinned commit into src/data.json. Usage: chart_data.py <project> <repo-root>

A chart scene names a file and paths into it; this writes the numbers the film draws, so no number is typed by hand.
Run it again whenever the data file or the chart changes; check_video.py fails a src/data.json that no longer matches.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_video import chart_values, judge_charts  # noqa: E402


def main(argv):
    project, repo = argv[1:3]
    s = json.load(open(os.path.join(project, "src", "script.json")))
    ref = (s.get("source") or {}).get("ref", "HEAD")

    def read(path):
        held = subprocess.run(["git", "-C", repo, "show", f"{ref}:{path}"], capture_output=True, text=True)
        return held.stdout if held.returncode == 0 else None

    faults = judge_charts(s, read)
    for f in faults:
        print(f"FAIL {f}")
    if faults:
        return 1
    data = {sc["id"]: chart_values(sc, read) for sc in s.get("scenes", []) if sc.get("kind") == "chart"}
    json.dump(data, open(os.path.join(project, "src", "data.json"), "w"), indent=1)
    for sid, values in data.items():
        print(f"{sid}: {values}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
