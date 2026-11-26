#!/usr/bin/env python3
"""Open and ask a headless interpret session on the other vendor.

`/shape --auto` can run interpret on a different vendor from work. Interpret only
answers, so it runs headless: one resumed turn per message, the reply on stdout.

usage: peer.py open --run RUN --vendor codex|claude --model M --effort E --read WT
                    [--name NAME]        (the filled interpret prompt on stdin)
       peer.py ask  --run RUN [--timeout SECONDS]   (the message on stdin)
       peer.py watch --run RUN                     (the live Codex transcript)

open records RUN/interpret.json; ask resumes it. While an answer is being written,
RUN/interpret.lock holds the caller's pid, and the conductor's watch reads a live
lock as not stalled. A call past --timeout (default 3600 s) is killed. Exit 1 on a
failed or timed-out call (stderr names it), 2 when ask finds no session. The lock is
released on every exit, a SIGTERM included, so a dead call never looks live.

Each call runs from RUN with stdin closed: `codex exec` waits on an open stdin
pipe, and a Codex resume run from elsewhere loses write access to RUN.
Codex writes prompts and progress to RUN/interpret.log as events arrive.
"""
import argparse
import json
import os
import re
import selectors
import signal
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path


def transcript_line(transcript, text):
    # Text from prompts and tools must not be interpreted as terminal controls.
    print(re.sub(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]", "", text), file=transcript, flush=True)


def show_codex_event(transcript, event):
    kind = event.get("type")
    item = event.get("item") or {}
    item_kind = item.get("type")
    if kind == "turn.started":
        transcript_line(transcript, "[Codex] Turn started")
    elif kind in ("turn.failed", "error"):
        transcript_line(transcript, f"[Error] {event.get('error', event.get('message', kind))}")
    elif kind == "item.started" and item_kind == "command_execution":
        transcript_line(transcript, f"[Running] {item.get('command', '')}")
    elif kind == "item.completed" and item_kind == "agent_message":
        transcript_line(transcript, f"\n[Codex]\n{item.get('text', '')}")
    elif kind == "item.completed" and item_kind == "reasoning":
        transcript_line(transcript, f"[Reasoning summary] {item.get('text', '')}")
    elif kind in ("item.started", "item.completed") and item_kind and item_kind not in ("agent_message", "reasoning"):
        status = item.get("status") or kind.split(".")[1]
        transcript_line(transcript, f"[Codex] {item_kind}: {status}")


def codex_events(proc, deadline, transcript):
    pending = b""
    with selectors.DefaultSelector() as selector:
        selector.register(proc.stdout, selectors.EVENT_READ)
        while selector.select(max(0, deadline - time.monotonic())):
            chunk = proc.stdout.read1(65536)
            lines = (pending + chunk).split(b"\n")
            if chunk:
                pending = lines.pop()
            for line in lines:
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if isinstance(event, dict):
                    show_codex_event(transcript, event)
                    yield event
            if not chunk:
                return
            if time.monotonic() >= deadline:
                break
    raise subprocess.TimeoutExpired(proc.args, 0)


def call_codex(record, message, opening, timeout, transcript):
    label = "Opening prompt" if opening else "Question"
    transcript_line(transcript, f"\n[{time.strftime('%H:%M:%S')}] {label} for {record['model']}\n{message}")
    deadline = time.monotonic() + timeout
    thread, reply = None, ""
    with tempfile.TemporaryFile() as stderr:
        try:
            with subprocess.Popen(command(record, message, opening), cwd=record["run"], stdin=subprocess.DEVNULL,
                                  stdout=subprocess.PIPE, stderr=stderr) as proc:
                try:
                    for event in codex_events(proc, deadline, transcript):
                        thread = thread or event.get("thread_id")
                        item = event.get("item") or {}
                        if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                            reply = item.get("text", "")
                    code = proc.wait(timeout=max(0, deadline - time.monotonic()))
                finally:
                    if proc.poll() is None:
                        proc.kill()
        except subprocess.TimeoutExpired:
            failure = f"codex timed out after {timeout} s; the call was killed"
        except OSError as exc:
            failure = f"could not run codex: {exc}"
        else:
            if code == 0 and thread is not None:
                transcript_line(transcript, "[Codex] Turn finished. Waiting for the next question.")
                return thread, reply
            stderr.seek(0)
            detail = stderr.read().decode("utf-8", errors="replace").strip()
            failure = f"codex exited {code}: {detail}" if code else "codex returned no thread ID"
    transcript_line(transcript, f"[Error] {failure}")
    sys.stderr.write(failure + "\n")
    return None, None


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


def call_claude(record, message, opening, timeout):
    try:
        done = subprocess.run(command(record, message, opening), cwd=record["run"], stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        sys.stderr.write(f"{record['vendor']} timed out after {timeout} s; the call was killed\n")
        return None, None
    if done.returncode != 0:
        sys.stderr.write(f"{record['vendor']} exited {done.returncode}: {done.stderr.strip()}\n")
        return None, None
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
    parser.add_argument("action", choices=("open", "ask", "watch"))
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
    transcript = run / "interpret.log"
    if args.action == "watch":
        transcript.touch(mode=0o600, exist_ok=True)
        print("Watch Codex interpret. Send changes in the conversation where you started /shape.", flush=True)
        os.execlp("tail", "tail", "-n", "+1", "-f", str(transcript))

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
        if record["vendor"] == "codex":
            transcript.touch(mode=0o600)
            with transcript.open("a", encoding="utf-8", errors="replace") as stream:
                session, reply = call_codex(record, message, args.action == "open", args.timeout, stream)
        else:
            session, reply = call_claude(record, message, args.action == "open", args.timeout)
        if session is not None and args.action == "open":
            record["id"] = session
            store.write_text(json.dumps(record, indent=2) + "\n")
    finally:
        lock.unlink(missing_ok=True)
    if session is None:
        return 1
    print(reply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
