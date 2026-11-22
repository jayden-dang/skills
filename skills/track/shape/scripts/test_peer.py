#!/usr/bin/env python3
"""Run: python3 skills/track/shape/scripts/test_peer.py

peer.py opens a headless interpret session on the other vendor and asks it one
message at a time. The vendor CLIs are the system boundary, so fakes stand in
for `codex` and `claude` on PATH and record how they were called.
"""
import json
import os
import stat
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("peer.py")

FAKE = textwrap.dedent('''\
    #!{python}
    import json, os, stat, sys
    log = os.environ["FAKE_LOG"]
    run = os.environ["FAKE_RUN"]
    row = {{"argv": sys.argv[1:], "cwd": os.getcwd(),
            "stdin_devnull": stat.S_ISCHR(os.fstat(0).st_mode),
            "lock_held": os.path.exists(os.path.join(run, "interpret.lock"))}}
    with open(log, "a") as f:
        f.write(json.dumps(row) + "\\n")
    if os.environ.get("FAKE_SLEEP"):
        import time; time.sleep(float(os.environ["FAKE_SLEEP"]))
    if os.environ.get("FAKE_FAIL"):
        sys.stderr.write("boom\\n"); sys.exit(3)
    if os.path.basename(sys.argv[0]) == "codex":
        print(json.dumps({{"type": "thread.started", "thread_id": "th-1"}}))
        print(json.dumps({{"type": "item.completed", "item": {{"type": "agent_message", "text": "first"}}}}))
        print(json.dumps({{"type": "item.completed", "item": {{"type": "agent_message", "text": "codex says hi"}}}}))
    else:
        print(json.dumps({{"type": "result", "result": "claude says hi", "session_id": "ignored"}}))
''')


class Peer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(os.path.realpath(self.tmp.name))
        self.run_dir = root / "run"
        self.wt = root / "wt"
        self.bin = root / "bin"
        for d in (self.run_dir, self.wt, self.bin):
            d.mkdir()
        self.log = root / "calls.jsonl"
        for name in ("codex", "claude"):
            path = self.bin / name
            path.write_text(FAKE.format(python=sys.executable))
            path.chmod(path.stat().st_mode | stat.S_IEXEC)

    def peer(self, *args, message="hello", fail=False, sleep=None):
        env = dict(os.environ, PATH=f"{self.bin}{os.pathsep}{os.environ['PATH']}",
                   FAKE_LOG=str(self.log), FAKE_RUN=str(self.run_dir))
        if fail:
            env["FAKE_FAIL"] = "1"
        if sleep:
            env["FAKE_SLEEP"] = str(sleep)
        return subprocess.run([sys.executable, "-I", str(SCRIPT), *args, "--run", str(self.run_dir)],
                              input=message, capture_output=True, text=True, env=env, timeout=30)

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def open(self, vendor, model, effort):
        return self.peer("open", "--vendor", vendor, "--model", model, "--effort", effort,
                         "--read", str(self.wt), "--name", "ledger-interpret", message="the filled prompt")

    def test_codex_open_runs_the_model_and_effort_writable_only_in_run_and_records_the_thread(self):
        result = self.open("codex", "gpt-6.2-sol", "high")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "codex says hi")
        call = self.calls()[0]
        argv = call["argv"]
        self.assertEqual(argv[:2], ["exec", "--json"])
        self.assertIn("--skip-git-repo-check", argv)
        self.assertEqual(argv[argv.index("-m") + 1], "gpt-6.2-sol")
        self.assertIn("model_reasoning_effort=high", argv)
        self.assertEqual(argv[argv.index("-s") + 1], "workspace-write")
        self.assertEqual(argv[argv.index("-C") + 1], str(self.run_dir))
        self.assertEqual(argv[-2:], ["--", "the filled prompt"])
        self.assertEqual(call["cwd"], str(self.run_dir))
        self.assertTrue(call["stdin_devnull"], "codex exec waits on an open stdin pipe")
        record = json.loads((self.run_dir / "interpret.json").read_text())
        self.assertEqual(record["vendor"], "codex")
        self.assertEqual(record["id"], "th-1")
        self.assertEqual((record["model"], record["effort"]), ("gpt-6.2-sol", "high"))

    def test_codex_ask_resumes_from_run_with_write_access_and_the_same_model(self):
        self.open("codex", "gpt-6.2-sol", "high")
        result = self.peer("ask", message="fork: which table owns tenant_id?")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "codex says hi")
        call = self.calls()[1]
        argv = call["argv"]
        self.assertEqual(argv[:3], ["exec", "resume", "--json"])
        self.assertIn("th-1", argv)
        self.assertIn("--skip-git-repo-check", argv)
        self.assertEqual(argv[argv.index("-m") + 1], "gpt-6.2-sol")
        self.assertIn("model_reasoning_effort=high", argv)
        self.assertIn('sandbox_mode="workspace-write"', argv)
        self.assertEqual(argv[-2:], ["--", "fork: which table owns tenant_id?"])
        self.assertEqual(call["cwd"], str(self.run_dir), "a resume from WT loses write access to RUN")
        self.assertTrue(call["stdin_devnull"])

    def test_claude_open_and_ask_keep_one_session_and_read_the_worktree(self):
        opened = self.open("claude", "opus", "high")
        self.assertEqual(opened.returncode, 0, opened.stderr)
        self.assertEqual(opened.stdout.strip(), "claude says hi")
        asked = self.peer("ask", message="review design.md")
        self.assertEqual(asked.stdout.strip(), "claude says hi")
        first, second = (call["argv"] for call in self.calls())
        session = first[first.index("--session-id") + 1]
        self.assertEqual(second[second.index("--resume") + 1], session)
        for argv in (first, second):
            self.assertEqual(argv[0], "-p")
            self.assertEqual(argv[argv.index("--model") + 1], "opus")
            self.assertEqual(argv[argv.index("--effort") + 1], "high")
            self.assertEqual(argv[argv.index("--permission-mode") + 1], "auto")
            self.assertEqual(argv[argv.index("--add-dir") + 1], str(self.wt))
            self.assertEqual(argv[argv.index("--output-format") + 1], "json")
            self.assertEqual(argv[-2], "--", "without it --add-dir swallows the prompt")
        self.assertEqual(first[first.index("--name") + 1], "ledger-interpret")
        self.assertTrue(all(call["cwd"] == str(self.run_dir) for call in self.calls()))

    def test_ask_holds_the_lock_while_the_peer_answers_and_releases_it(self):
        self.open("codex", "gpt-6.2-sol", "high")
        self.peer("ask")
        self.assertTrue(self.calls()[1]["lock_held"], "the watch reads a live lock as not stalled")
        self.assertFalse((self.run_dir / "interpret.lock").exists())

    def test_a_failed_answer_exits_non_zero_names_the_error_and_releases_the_lock(self):
        self.open("codex", "gpt-6.2-sol", "high")
        result = self.peer("ask", fail=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("boom", result.stderr)
        self.assertFalse((self.run_dir / "interpret.lock").exists())

    def test_a_hung_answer_times_out_exits_non_zero_and_releases_the_lock(self):
        self.open("codex", "gpt-6.2-sol", "high")
        result = self.peer("ask", "--timeout", "1", sleep=20)
        self.assertEqual(result.returncode, 1)
        self.assertIn("timed out", result.stderr)
        self.assertFalse((self.run_dir / "interpret.lock").exists(), "a hung call must not hide a stall")

    def test_a_terminated_ask_releases_the_lock(self):
        self.open("codex", "gpt-6.2-sol", "high")
        env = dict(os.environ, PATH=f"{self.bin}{os.pathsep}{os.environ['PATH']}", FAKE_LOG=str(self.log),
                   FAKE_RUN=str(self.run_dir), FAKE_SLEEP="20")
        proc = subprocess.Popen([sys.executable, "-I", str(SCRIPT), "ask", "--run", str(self.run_dir)],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True)
        proc.stdin.write("hello")
        proc.stdin.close()
        lock = self.run_dir / "interpret.lock"
        for _ in range(100):
            if lock.exists():
                break
            time.sleep(0.05)
        self.assertTrue(lock.exists())
        proc.terminate()
        proc.wait(timeout=10)
        self.assertFalse(lock.exists(), "a killed ask must not leave a live-looking lock")

    def test_ask_before_open_is_refused(self):
        result = self.peer("ask")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no interpret session", result.stderr)


if __name__ == "__main__":
    unittest.main()
