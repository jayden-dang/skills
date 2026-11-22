#!/usr/bin/env python3
"""Run: python3 skills/track/shape/scripts/test_skill_receipt.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("skill_receipt.py")


def user(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def tool(name, **tool_input):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "name": name, "input": tool_input}]}}


class Receipt(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.home.cleanup)
        self.cwd = os.path.realpath(self.home.name) + "/repo/.worktrees/feat-x"
        os.makedirs(self.cwd)
        slug = "".join(c if c.isalnum() or c == "-" else "-" for c in self.cwd)
        self.projects = Path(self.home.name) / "cfg" / "projects" / slug
        self.projects.mkdir(parents=True)

    def session(self, filename, name, rows):
        with open(self.projects / filename, "w", encoding="utf-8") as handle:
            for row in [{"type": "custom-title", "customTitle": name}] + rows:
                handle.write(json.dumps(row) + "\n")

    def run_receipt(self, *args):
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(Path(self.home.name) / "cfg"))
        return subprocess.run([sys.executable, "-I", str(SCRIPT), "--cwd", self.cwd, *args], capture_output=True, text=True, env=env)

    def test_a_session_that_skipped_a_required_skill_fails_and_names_it(self):
        self.session("a.jsonl", "work", [user("<command-name>/frame-change</command-name>"), tool("Skill", skill="specify-behavior")])
        result = self.run_receipt("--name", "work", "--require", "frame-change,specify-behavior,clarify-decisions")
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing: clarify-decisions", result.stdout)
        self.assertIn("ran: frame-change, specify-behavior", result.stdout)

    def test_a_session_that_ran_everything_passes(self):
        self.session("a.jsonl", "work", [tool("Skill", skill="plugin:plan-tasks"), tool("Agent", description="scan")])
        result = self.run_receipt("--name", "work", "--require", "plan-tasks", "--min-subagents", "1")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("subagents: 1", result.stdout)
        self.assertIn("missing: none", result.stdout)

    def test_no_subagent_fails_when_one_is_required(self):
        self.session("a.jsonl", "work", [tool("Skill", skill="plan-tasks")])
        result = self.run_receipt("--name", "work", "--require", "plan-tasks", "--min-subagents", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("subagents below 1", result.stdout)

    def test_another_sessions_skills_do_not_count(self):
        self.session("a.jsonl", "work", [tool("Skill", skill="specify-behavior")])
        self.session("b.jsonl", "interpret", [tool("Skill", skill="research")])
        result = self.run_receipt("--name", "work", "--require", "research")
        self.assertEqual(result.returncode, 1)

    def test_a_resumed_session_counts_every_transcript_of_that_name(self):
        self.session("a.jsonl", "work", [tool("Skill", skill="specify-behavior")])
        self.session("b.jsonl", "work", [tool("Skill", skill="plan-tasks")])
        result = self.run_receipt("--name", "work", "--require", "specify-behavior,plan-tasks")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_an_unknown_session_is_reported_rather_than_passed(self):
        self.session("a.jsonl", "work", [])
        result = self.run_receipt("--name", "nobody")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no transcript", result.stdout)


def codex_meta(cwd, agent_path):
    return {"type": "session_meta", "payload": {"id": "t1", "cwd": cwd, "agent_path": agent_path, "thread_source": "subagent"}}


def codex_turn(model, effort):
    return {"type": "turn_context", "payload": {"model": model, "effort": effort}}


def codex_exec(cmd):
    return {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "exec", "input": 'text(await tools.exec_command({cmd:"' + cmd + '"}))'}}


def codex_call(name, arguments):
    return {"type": "response_item", "payload": {"type": "function_call", "name": name, "arguments": json.dumps(arguments)}}


class CodexReceipt(unittest.TestCase):
    """A Codex peer is a spawn_agent child: its rollout names it by agent_path, and it loads a skill by reading SKILL.md."""

    def setUp(self):
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.home.cleanup)
        self.checkout = os.path.realpath(self.home.name) + "/repo"
        self.wt = self.checkout + "/.worktrees/feat-x"
        os.makedirs(self.wt)
        self.sessions = Path(self.home.name) / "codex" / "sessions" / "2026" / "11" / "22"
        self.sessions.mkdir(parents=True)

    def rollout(self, filename, rows):
        with open(self.sessions / filename, "w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")

    def run_receipt(self, *args):
        env = dict(os.environ, CODEX_HOME=str(Path(self.home.name) / "codex"))
        return subprocess.run([sys.executable, "-I", str(SCRIPT), "--harness", "codex", "--cwd", self.wt, *args], capture_output=True, text=True, env=env)

    def test_skills_read_from_skill_files_and_spawned_agents_count(self):
        self.rollout("rollout-a.jsonl", [
            codex_meta(self.checkout, "/root/ledger_work"),
            codex_turn("gpt-6.2-sol", "high"),
            codex_exec("cat /Users/x/.agents/skills/frame-change/SKILL.md"),
            codex_exec("sed -n 1,200p /Users/x/.agents/skills/plan-tasks/SKILL.md"),
            codex_call("spawn_agent", {"task_name": "scan", "model": "gpt-6-luna"}),
        ])
        result = self.run_receipt("--name", "ledger_work", "--require", "frame-change,plan-tasks", "--min-subagents", "1")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("ran: frame-change, plan-tasks", result.stdout)
        self.assertIn("subagents: 1", result.stdout)
        self.assertIn("model: gpt-6.2-sol high", result.stdout)

    def test_a_skill_the_agent_never_read_is_missing(self):
        self.rollout("rollout-a.jsonl", [
            codex_meta(self.checkout, "/root/ledger_work"),
            codex_exec("cat /Users/x/.agents/skills/frame-change/SKILL.md"),
            codex_exec("rg -n clarify-decisions docs/"),
        ])
        result = self.run_receipt("--name", "ledger_work", "--require", "frame-change,clarify-decisions")
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing: clarify-decisions", result.stdout)

    def test_another_agents_rollout_does_not_count(self):
        self.rollout("rollout-a.jsonl", [codex_meta(self.checkout, "/root/ledger_work")])
        self.rollout("rollout-b.jsonl", [codex_meta(self.checkout, "/root/ledger_interpret"), codex_exec("cat /x/skills/research/SKILL.md")])
        result = self.run_receipt("--name", "ledger_work", "--require", "research")
        self.assertEqual(result.returncode, 1)

    def test_an_agent_of_the_same_name_in_another_repo_does_not_count(self):
        self.rollout("rollout-a.jsonl", [codex_meta("/elsewhere/repo", "/root/ledger_work"), codex_exec("cat /x/skills/plan-tasks/SKILL.md")])
        result = self.run_receipt("--name", "ledger_work", "--require", "plan-tasks")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no transcript", result.stdout)


if __name__ == "__main__":
    unittest.main()
