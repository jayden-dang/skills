#!/usr/bin/env python3
"""Open and ask a headless interpret session on the other vendor.

`/shape --auto` can run interpret on a different vendor from work. Interpret only
answers, so it runs headless: one resumed turn per message, the reply on stdout.

usage: peer.py open --run RUN --vendor codex|claude --model M --effort E --read WT
                    [--name NAME]        (the filled interpret prompt on stdin)
       peer.py ask  --run RUN [--timeout SECONDS]   (the message on stdin)

open records RUN/interpret.json; ask resumes it. While an answer is being written,
RUN/interpret.lock holds the caller's pid, and the conductor's watch reads a live
lock as not stalled. A call past --timeout (default 3600 s) is killed. Exit 1 on a
failed or timed-out call (stderr names it), 2 when ask finds no session. The lock is
released on every exit, a SIGTERM included, so a dead call never looks live.

Each call runs from RUN with stdin closed: `codex exec` waits on an open stdin
pipe, and a Codex resume run from elsewhere loses write access to RUN.
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path


def codex_reply(stdout):
    thread, reply = None, ""
    for line in stdout.splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        thread = thread or row.get("thread_id")
        item = row.get("item") or {}
        if row.get("type") == "item.completed" and item.get("type") == "agent_message":
            reply = item.get("text", "")
    return thread, reply


def claude_reply(stdout):
    try:
        return json.loads(stdout).get("result", "")
    except ValueError:
        return stdout


def command(record, message, opening):
    model, effort = record["model"], record["effort"]
    if record["vendor"] == "codex":
        if opening:
            head = ["codex", "exec", "--json", "--skip-git-repo-check", "-s", "workspace-write", "-C", record["run"]]
        else:
            head = ["codex", "exec", "resume", "--json", "--skip-git-repo-check", record["id"],
                    "-c", 'sandbox_mode="workspace-write"']
        return head + ["-m", model, "-c", f"model_reasoning_effort={effort}", "--", message]
    session = ["--session-id", record["id"]] + (["--name", record["name"]] if record.get("name") else []) if opening \
        else ["--resume", record["id"]]
    return ["claude", "-p", *session, "--model", model, "--effort", effort, "--permission-mode", "auto",
            "--add-dir", record["read"], "--output-format", "json", "--", message]


def call(record, message, opening, timeout):
    try:
        done = subprocess.run(command(record, message, opening), cwd=record["run"], stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        sys.stderr.write(f"{record['vendor']} timed out after {timeout} s; the call was killed\n")
        return None, None
    if done.returncode != 0:
        sys.stderr.write(f"{record['vendor']} exited {done.returncode}: {done.stderr.strip()}\n")
        return None, None
    if record["vendor"] == "codex":
        return codex_reply(done.stdout)
    return record["id"], claude_reply(done.stdout)


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def take_lock(lock):
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return
        except FileExistsError:
            try:
                holder = int(lock.read_text().strip() or 0)
            except (OSError, ValueError):
                holder = 0
            if not alive(holder):
                lock.unlink(missing_ok=True)
                continue
            time.sleep(2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("open", "ask"))
    parser.add_argument("--run", required=True)
    parser.add_argument("--vendor", choices=("codex", "claude"))
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--read")
    parser.add_argument("--name")
    parser.add_argument("--timeout", type=float, default=3600)
    args = parser.parse_args()
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))

    run = Path(os.path.realpath(args.run))
    store, lock = run / "interpret.json", run / "interpret.lock"
    message = sys.stdin.read()

    if args.action == "open":
        missing = [flag for flag in ("vendor", "model", "effort", "read") if not getattr(args, flag)]
        if missing:
            parser.error("open needs --" + ", --".join(missing))
        record = {"vendor": args.vendor, "model": args.model, "effort": args.effort, "run": str(run),
                  "read": os.path.realpath(args.read), "name": args.name,
                  "id": str(uuid.uuid4()) if args.vendor == "claude" else None}
    else:
        if not store.exists():
            sys.stderr.write(f"no interpret session recorded at {store}; run peer.py open first\n")
            return 2
        record = json.loads(store.read_text())

    take_lock(lock)
    try:
        session, reply = call(record, message, args.action == "open", args.timeout)
    finally:
        lock.unlink(missing_ok=True)
    if session is None:
        return 1
    if args.action == "open":
        record["id"] = session
        store.write_text(json.dumps(record, indent=2) + "\n")
    print(reply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
