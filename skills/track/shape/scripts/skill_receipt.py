#!/usr/bin/env python3
"""Report which skills and subagents one session actually ran.

The evidence is the session's own transcript, not what the session says it did.
Claude Code: a session named with --name, under ~/.claude/projects.
Codex: a spawn_agent child named by its task_name, under $CODEX_HOME/sessions;
it loads a skill by reading that skill's SKILL.md.

usage: skill_receipt.py [--harness claude|codex] --cwd <session working dir>
                        --name <session name> [--require a,b,c] [--min-subagents N]

Prints ran / subagents / model / missing lines. Exits 1 when a requirement is
unmet, 2 when no transcript for that session exists.
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


SKILL_FILE = re.compile(r"skills/([A-Za-z0-9_-]+)/SKILL\.md")


def codex_sessions(cwd, name):
    """Yield (skills, subagents, model) for each Codex rollout of agent `name` in this repo."""
    root = Path(os.path.expanduser(os.environ.get("CODEX_HOME") or "~/.codex")) / "sessions"
    here = os.path.realpath(cwd)
    for path in sorted(root.rglob("*.jsonl")):
        skills, subagents, model, mine = [], 0, None, False
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                payload = row.get("payload") or {}
                if row.get("type") == "session_meta":
                    agent = str(payload.get("agent_path") or "")
                    base = os.path.realpath(str(payload.get("cwd") or "/nonexistent"))
                    in_repo = here == base or here.startswith(base + os.sep) or base.startswith(here + os.sep)
                    mine = agent.rsplit("/", 1)[-1] == name and in_repo
                    if not mine:
                        break
                elif row.get("type") == "turn_context" and model is None:
                    model = " ".join(str(v) for v in (payload.get("model"), payload.get("effort")) if v)
                elif row.get("type") == "response_item":
                    kind = payload.get("type")
                    if kind == "function_call" and payload.get("name") == "spawn_agent":
                        subagents += 1
                    elif kind in ("custom_tool_call", "function_call"):
                        call = str(payload.get("input") or "") + str(payload.get("arguments") or "")
                        skills += SKILL_FILE.findall(call)
        if mine:
            yield skills, subagents, model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness", choices=("claude", "codex"), default="claude")
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--require", default="")
    parser.add_argument("--min-subagents", type=int, default=0)
    args = parser.parse_args()

    ran, subagents, found, models = [], 0, False, []
    if args.harness == "codex":
        for skills, count, model in codex_sessions(args.cwd, args.name):
            found = True
            ran += skills
            subagents += count
            models += [model] if model else []
        where = "$CODEX_HOME/sessions"
    else:
        for path in sorted(transcript_dir(args.cwd).glob("*.jsonl")):
            name, skills, count = read_session(path)
            if name == args.name:
                found = True
                ran += skills
                subagents += count
        where = transcript_dir(args.cwd)
    if not found:
        print(f"no transcript for session {args.name} under {where}")
        return 2

    required = [skill for skill in args.require.split(",") if skill]
    missing = [skill for skill in required if skill not in ran]
    short = subagents < args.min_subagents
    print("ran: " + (", ".join(dict.fromkeys(ran)) or "none"))
    print(f"subagents: {subagents}")
    if models:
        print("model: " + ", ".join(dict.fromkeys(models)))
    print("missing: " + (", ".join(missing) or "none") + (f"; subagents below {args.min_subagents}" if short else ""))
    return 1 if missing or short else 0


if __name__ == "__main__":
    sys.exit(main())
