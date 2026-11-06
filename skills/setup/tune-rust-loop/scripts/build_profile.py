#!/usr/bin/env python3
"""Slowest compile units from a `cargo build --timings` report (target/cargo-timings/cargo-timing.html).

The stable HTML report embeds `const UNIT_DATA = [...]`; `--timings=json` no longer exists.
"""
import argparse
import json


def units(path):
    text = open(path, errors="replace").read()
    marker = "const UNIT_DATA = "
    start = text.index(marker) + len(marker)
    data, _ = json.JSONDecoder().raw_decode(text[start:])
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    u = units(a.path)
    top = sorted(u, key=lambda x: -(x.get("duration") or 0))[:15]
    out = {"units": len(u), "sum_s": round(sum(x.get("duration") or 0 for x in u), 1),
           "top": [{"name": x["name"], "target": x.get("target", "").strip(),
                    "mode": x.get("mode"), "s": x.get("duration")} for x in top]}
    if a.json:
        print(json.dumps(out, indent=1))
        return
    print(f"units {out['units']}  summed unit seconds {out['sum_s']}")
    for r in out["top"]:
        print(f"{r['s']:7.1f}  {r['name']}  {r['target']}  ({r['mode']})")


if __name__ == "__main__":
    main()
