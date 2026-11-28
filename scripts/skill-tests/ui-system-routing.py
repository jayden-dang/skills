"""Route first messages for the UI design-system skill against the whole listing.

python3 scripts/skill-tests/ui-system-routing.py <expected-name-or-NONE> [reps] [--as NAME]
The listing is the working tree's. --as renames the skill in the listing only, to compare names.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json, subprocess, sys, tempfile, yaml

ROOT = Path(__file__).resolve().parents[2]
MODELS = ("haiku", "sonnet")
NEW = "@new"
QUERIES = [
    (NEW, "Every screen styles itself. Set up a design system for the whole app: tokens, type, spacing, components and dark mode."),
    (NEW, "We need design tokens shared by our web app and React Native app, synced with our Figma variables."),
    (NEW, "Create the UI design system for our Rust GPUI desktop app so every panel looks the same in light and dark."),
    (NEW, "Define our component library before we build more screens: which primitives, their states and the accessibility rules."),
    (NEW, "A partner brand arrives next quarter. Set up theming so we can swap brand colors without touching every screen."),
    (NEW, "Our UI has 14 shades of blue. Consolidate them into a token system and plan how existing screens migrate."),
    (NEW, "Set up the docs and governance for our design system: Storybook, who approves new components, versioning."),
    ("draft-ui", "Show me three design directions for the checkout screen."),
    ("inspect-ui", "Review this branch's UI in the running app for contrast and focus."),
    ("craft-page", "Make a polished standalone HTML report of our Q3 numbers."),
    ("architect-system", "Decide how our front end handles state management and data fetching across all screens."),
    ("define-project", "Our design tokens are approved. Write the docs/standards/design-tokens.md entry for them."),
]

def listing(rename):
    rows = []
    for f in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        d = yaml.safe_load(f.read_text().split("---", 2)[1])
        name = d["name"]
        if rename and name == rename[0]:
            name = rename[1]
        rows.append(f"- {name}: {' '.join(str(d['description']).split())}")
    return "\n".join(rows)

def run(i, catalog, model):
    expected, user = QUERIES[i]
    prompt = f"Choose the first skill to load for the message below from this list. Return exactly its name, or NONE. Do not use tools.\n\n{catalog}\n\nMessage: {user}"
    with tempfile.TemporaryDirectory(prefix="work-") as root:
        r = subprocess.run(["claude", "-p", "--model", model, "--tools", "", "--setting-sources", "project", "--strict-mcp-config", "--no-session-persistence", "--output-format", "json"],
                           input=prompt, text=True, cwd=root, capture_output=True, timeout=120)
    rows = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    return {"query": i + 1, "model": model, "expected": expected, "actual": (rows[-1].get("result", "") if rows else "").strip().strip("`*").strip()}

def main():
    new = sys.argv[1]
    reps = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 1
    rename = None
    if "--as" in sys.argv:
        rename = (new, sys.argv[sys.argv.index("--as") + 1]); new = rename[1]
    catalog = listing(rename)
    with ThreadPoolExecutor(max_workers=10) as pool:
        res = list(pool.map(lambda a: run(*a), [(i, catalog, m) for _ in range(reps) for i in range(len(QUERIES)) for m in MODELS]))
    for x in res:
        if x["expected"] == NEW: x["expected"] = new
    out = ROOT / ".skills/ui-system"; out.mkdir(parents=True, exist_ok=True)
    (out / f"routing-{new}-x{reps}.json").write_text(json.dumps(res, indent=1) + "\n")
    for m in MODELS:
        sel = [x for x in res if x["model"] == m]
        bad = [(x["query"], x["actual"][:28]) for x in sel if x["actual"] != x["expected"]]
        print(new, m, f"{len(sel) - len(bad)}/{len(sel)}", bad)

if __name__ == "__main__":
    main()
