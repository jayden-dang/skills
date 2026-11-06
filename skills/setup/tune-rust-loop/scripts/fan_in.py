#!/usr/bin/env python3
"""Workspace crates ranked by how many other workspace crates rebuild when they change.

Reads `cargo metadata --format-version 1 --no-deps` (run here, or `--metadata <file>`).
Counts normal and build dependencies only: a dev-dependency edge rebuilds tests, not the crate.
"""
import argparse
import json
import subprocess


def load(path):
    if path:
        return json.load(open(path))
    out = subprocess.run(["cargo", "metadata", "--format-version", "1", "--no-deps"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    pkgs = load(a.metadata)["packages"]
    names = {p["name"] for p in pkgs}
    users = {n: set() for n in names}
    for p in pkgs:
        for d in p["dependencies"]:
            if d["name"] in names and d.get("kind") in (None, "build"):
                users[d["name"]].add(p["name"])

    def closure(n):
        seen, todo = set(), list(users[n])
        while todo:
            x = todo.pop()
            if x not in seen:
                seen.add(x)
                todo.extend(users[x])
        return seen

    rows = sorted(({"crate": p["name"], "direct": len(users[p["name"]]),
                    "transitive": len(closure(p["name"])),
                    "test_targets": sum("test" in t["kind"] for t in p["targets"])}
                   for p in pkgs), key=lambda r: (-r["transitive"], -r["direct"]))
    out = {"workspace_crates": len(names), "crates": rows}
    if a.json:
        print(json.dumps(out, indent=1))
        return
    print(f"workspace crates {len(names)}")
    print("crate                           direct  transitive  test-targets")
    for r in rows[:20]:
        print(f"{r['crate'][:30]:30} {r['direct']:7} {r['transitive']:11} {r['test_targets']:13}")


if __name__ == "__main__":
    main()
