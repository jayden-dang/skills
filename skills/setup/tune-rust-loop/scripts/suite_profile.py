#!/usr/bin/env python3
"""Where a cargo-nextest run spent its time.

Input: a nextest JUnit file (.xml) or the captured stderr of `cargo nextest run` (any other file).
Output: wall time, test-seconds, per-binary share/median, slowest tests. `--json` for machine use.
"""
import argparse
import json
import re
import statistics
import xml.etree.ElementTree as ET

RESULT = re.compile(r"^\s+(PASS|FAIL|FLAKY|LEAK|LEAK-FAIL|TIMEOUT|SIGSEGV|SIGABRT)\s+"
                    r"\[\s*([\d.]+)s\]\s+(?:\(\s*\d+/\d+\)\s+)?(\S+)\s+(\S+)")
SUMMARY = re.compile(r"Summary \[\s*([\d.]+)s\]")


def from_log(path):
    rows, wall = {}, None
    for line in open(path, errors="replace"):
        m = RESULT.match(line)
        if m:  # keyed by test: a retried or SLOW-then-PASS test counts once, last result wins
            rows[(m.group(3), m.group(4))] = float(m.group(2))
        s = SUMMARY.search(line)
        if s:
            wall = float(s.group(1))
    return rows, wall


def from_junit(path):
    root = ET.parse(path).getroot()
    rows = {}
    for case in root.iter("testcase"):
        rows[(case.get("classname"), case.get("name"))] = float(case.get("time") or 0)
    wall = root.get("time")
    return rows, float(wall) if wall else None


def profile(rows, wall):
    total = sum(rows.values()) or 1.0
    per = {}
    for (binary, _), secs in rows.items():
        per.setdefault(binary, []).append(secs)
    binaries = sorted(
        ({"binary": b, "tests": len(v), "test_s": round(sum(v), 1),
          "share": round(sum(v) / total, 3), "median_s": round(statistics.median(v), 3)}
         for b, v in per.items()),
        key=lambda r: -r["test_s"])
    slowest = [{"binary": b, "test": t, "s": s}
               for (b, t), s in sorted(rows.items(), key=lambda kv: -kv[1])[:15]]
    return {"tests": len(rows), "wall_s": wall, "test_s": round(total, 1),
            "binaries": binaries, "slowest": slowest}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rows, wall = (from_junit if a.path.endswith(".xml") else from_log)(a.path)
    p = profile(rows, wall)
    if a.json:
        print(json.dumps(p, indent=1))
        return
    print(f"tests {p['tests']}  wall {p['wall_s']} s  test-seconds {p['test_s']}")
    print("\nbinary                                  share   tests  median_s  test_s")
    for r in p["binaries"][:15]:
        print(f"{r['binary'][:38]:38} {r['share']*100:6.1f}% {r['tests']:6} {r['median_s']:9.2f} {r['test_s']:7.0f}")
    print("\nslowest tests")
    for r in p["slowest"]:
        print(f"{r['s']:8.1f}  {r['binary']}  {r['test']}")


if __name__ == "__main__":
    main()
