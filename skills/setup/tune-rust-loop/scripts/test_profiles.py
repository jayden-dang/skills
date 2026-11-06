"""Tests for the three measurement scripts. Run: python3 -m unittest discover -s <this dir>."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))

NEXTEST_LOG = """\
    Starting 6 tests across 2 binaries
        PASS [   0.010s] (1/6) fast it::a
        PASS [   6.900s] (2/6) web::it trash::one
        PASS [   7.100s] (3/6) web::it trash::two
        PASS [   7.000s] (4/6) web::it trash::three
        SLOW [> 60.000s] (5/6) jobs::lease reclaim_waits
        PASS [  84.500s] (5/6) jobs::lease reclaim_waits
        FAIL [ 169.000s] (6/6) jobs::lease reclaim_twice
     Summary [ 180.000s] 6 tests run: 5 passed, 1 failed, 0 skipped
"""

JUNIT = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="nextest-run" tests="3" time="20.0">
  <testsuite name="web::it" tests="2">
    <testcase name="trash::one" classname="web::it" time="6.9"/>
    <testcase name="trash::two" classname="web::it" time="7.1"/>
  </testsuite>
  <testsuite name="fast" tests="1">
    <testcase name="a" classname="fast" time="0.01"/>
  </testsuite>
</testsuites>
"""


def run(script, *args):
    out = subprocess.run([sys.executable, os.path.join(HERE, script), *args],
                         capture_output=True, text=True, check=True)
    return out.stdout


def write(text, suffix):
    f = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False)
    f.write(text)
    f.close()
    return f.name


class SuiteProfile(unittest.TestCase):
    def test_log_totals_and_binary_shares(self):
        data = json.loads(run("suite_profile.py", write(NEXTEST_LOG, ".log"), "--json"))
        self.assertEqual(data["tests"], 6)
        self.assertEqual(data["wall_s"], 180.0)
        bins = {b["binary"]: b for b in data["binaries"]}
        # the SLOW progress line is not a second result for the same test
        self.assertEqual(bins["jobs::lease"]["tests"], 2)
        self.assertAlmostEqual(bins["web::it"]["median_s"], 7.0)
        self.assertEqual(data["binaries"][0]["binary"], "jobs::lease")  # largest share first

    def test_junit_matches_log_shape(self):
        data = json.loads(run("suite_profile.py", write(JUNIT, ".xml"), "--json"))
        self.assertEqual(data["tests"], 3)
        self.assertEqual(data["wall_s"], 20.0)
        self.assertEqual(data["binaries"][0]["binary"], "web::it")

    def test_slowest_tests_listed(self):
        data = json.loads(run("suite_profile.py", write(NEXTEST_LOG, ".log"), "--json"))
        self.assertEqual(data["slowest"][0]["test"], "reclaim_twice")


class BuildProfile(unittest.TestCase):
    def test_units_ranked_from_timing_html(self):
        units = [
            {"name": "gateways", "target": " gateways", "mode": "build", "duration": 70.0},
            {"name": "aws-lc-sys", "target": " build script (run)", "mode": "run-custom-build", "duration": 42.0},
            {"name": "x", "target": " x \"lib\" (doc test)", "mode": "todo", "duration": 0.0},
        ]
        html = "<html><script>\nconst UNIT_DATA = " + json.dumps(units) + ";\nconst X = 1;</script>"
        data = json.loads(run("build_profile.py", write(html, ".html"), "--json"))
        self.assertEqual(data["units"], 3)
        self.assertEqual(data["top"][0]["name"], "gateways")
        self.assertAlmostEqual(data["sum_s"], 112.0)


class FanIn(unittest.TestCase):
    def test_direct_and_transitive_dependents(self):
        meta = {"packages": [
            {"name": "base", "dependencies": [], "targets": [{"kind": ["lib"]}]},
            {"name": "domain", "dependencies": [{"name": "base", "kind": None}], "targets": [{"kind": ["lib"]}]},
            {"name": "web", "dependencies": [{"name": "domain", "kind": None},
                                             {"name": "tempfile", "kind": "dev"}],
             "targets": [{"kind": ["lib"]}, {"kind": ["test"]}, {"kind": ["test"]}]},
        ]}
        data = json.loads(run("fan_in.py", "--metadata", write(json.dumps(meta), ".json"), "--json"))
        rows = {r["crate"]: r for r in data["crates"]}
        self.assertEqual(rows["base"]["direct"], 1)
        self.assertEqual(rows["base"]["transitive"], 2)
        self.assertEqual(rows["web"]["test_targets"], 2)
        self.assertEqual(data["workspace_crates"], 3)


if __name__ == "__main__":
    unittest.main()
