#!/usr/bin/env python3
"""Report which skills and subagents one Claude Code session actually ran.

The evidence is the session's own transcript, not what the session says it did.

usage: skill_receipt.py --cwd <session working dir> --name <session name>
                        [--require a,b,c] [--min-subagents N]

Prints ran / subagents / missing lines. Exits 1 when a requirement is unmet,
2 when no transcript for that session exists.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


def transcript_dir(cwd):
    slug = re.sub(r"[^A-Za-z0-9-]", "-", os.path.realpath(cwd))
    root = os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude"
    return Path(os.path.expanduser(root)) / "projects" / slug


def read_session(path):
    name, skills, subagents = None, [], 0
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except ValueError:
                continue
            name = row.get("customTitle") or row.get("agentName") or name
            message = row.get("message")
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if row.get("type") == "user" and isinstance(content, str):
                skills += re.findall(r"<command-name>/?([^<\s]+)</command-name>", content)
            if isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    if block.get("name") == "Skill":
                        skills.append(str(block.get("input", {}).get("skill", "")))
                    elif block.get("name") in ("Agent", "Task"):
                        subagents += 1
    return name, [skill.split(":")[-1] for skill in skills if skill], subagents


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--require", default="")
    parser.add_argument("--min-subagents", type=int, default=0)
    args = parser.parse_args()

    ran, subagents, found = [], 0, False
    for path in sorted(transcript_dir(args.cwd).glob("*.jsonl")):
        name, skills, count = read_session(path)
        if name == args.name:
            found = True
            ran += skills
            subagents += count
    if not found:
        print(f"no transcript for session {args.name} under {transcript_dir(args.cwd)}")
        return 2

    required = [skill for skill in args.require.split(",") if skill]
    missing = [skill for skill in required if skill not in ran]
    short = subagents < args.min_subagents
    print("ran: " + (", ".join(dict.fromkeys(ran)) or "none"))
    print(f"subagents: {subagents}")
    print("missing: " + (", ".join(missing) or "none") + (f"; subagents below {args.min_subagents}" if short else ""))
    return 1 if missing or short else 0


if __name__ == "__main__":
    sys.exit(main())
