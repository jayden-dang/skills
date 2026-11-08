#!/usr/bin/env python3
"""Run a command and record what it printed, for a terminal scene. Usage:
  record_terminal.py <project> <name> [--cwd DIR] [--env KEY=VALUE ...] [--show "what to type"] -- <command> [args...]

The output is real: the film plays it back, typed and printed in time with the line. --show is the command as a viewer
should read it, such as `tidegate sailings` for `node bin/tidegate.js sailings`; it defaults to the command itself.
"""
import json
import os
import re
import shlex
import subprocess
import sys
import time

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
MAX_LINES = 40


def main(argv):
    if "--" not in argv:
        print(__doc__)
        return 2
    cut = argv.index("--")
    head, command = argv[1:cut], argv[cut + 1 :]
    project, name = head[0], head[1]
    opts = head[2:]
    cwd = opts[opts.index("--cwd") + 1] if "--cwd" in opts else os.getcwd()
    shown = opts[opts.index("--show") + 1] if "--show" in opts else shlex.join(command)
    env = dict(os.environ)
    for i, o in enumerate(opts):
        if o == "--env":
            k, v = opts[i + 1].split("=", 1)
            env[k] = v
    start = time.monotonic()
    proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    lines = []
    for raw in proc.stdout:
        lines.append({"t": round(time.monotonic() - start, 3), "text": ANSI.sub("", raw.rstrip("\n")).expandtabs(4)})
    code = proc.wait()
    cut_off = len(lines) > MAX_LINES
    path = os.path.join(project, "src", "terminals.json")
    data = json.load(open(path)) if os.path.exists(path) else {}
    data[name] = {"command": shown, "lines": lines[:MAX_LINES], "more": len(lines) - MAX_LINES if cut_off else 0, "exit": code}
    json.dump(data, open(path, "w"), indent=1)
    print(f"recorded {name}: {len(lines)} lines, exit {code}" + (f", showing the first {MAX_LINES}" if cut_off else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
