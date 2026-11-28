"""Project-wide UI design-system exercises in disposable checkouts.

cases: tideline-state (a front-end architecture request opened in this skill: it should hand off), pebble-web (a running React app whose screens style themselves), harbor-panels (a Rust GPUI
desktop app), fernway-multi (greenfield: web dispatcher, React Native phone app, marketing site)
red   — no design-system skill; the neighboring skills are installed
green — the new skill installed and opened (pass --skill <name>)
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".skills/ui-system"
MODELS = ("haiku", "sonnet")

CASES = {
    "pebble-web": (
        """Every screen in Pebble styles itself and new ones keep drifting. Set up a design system for the whole app (colors, type, spacing, components, dark mode) so every screen after this follows it. The design lead wants all screens restyled this week, before the partner demo. Write it up in design-system.md.""",
        {
            "README.md": """# Pebble
Online stationery shop. React 19 + Vite + TypeScript, plain CSS modules. Screens: Checkout, Orders, Account.
A partner brand ("Inkwell") will resell through us next quarter with its own colors.
Run `npm test` (Vitest; dependencies not installed in this checkout).""",
            "docs/support.md": """- "I have low vision and can't read the grey prices on checkout."
- "When I tab through checkout I can't see where I am."
- "Please add dark mode, the white page hurts at night." (14 requests this month)""",
            "src/pages/Checkout.module.css": """.price { color: #a0a0a0; font-size: 13px; }
.pay { background: #3d8bfd; color: #fff; padding: 9px 14px; border-radius: 6px; border: 0; outline: none; }
.pay:hover { background: #2f6fd1; }""",
            "src/pages/Checkout.tsx": """import s from './Checkout.module.css'
export function Checkout({ total }: { total: string }) {
  return <section><p className={s.price}>{total}</p><button className={s.pay}>Pay now</button></section>
}""",
            "src/pages/Orders.module.css": """.reorder { background: #1a73e8; color: white; padding: 8px 16px; border-radius: 4px; font-size: 14px; }
.status { color: #888; font-size: 12px; }
.danger { background: #e53935; color: #fff; padding: 6px 12px; border-radius: 20px; }""",
            "src/pages/Orders.tsx": """import s from './Orders.module.css'
export function Orders() {
  return <ul><li><span className={s.status}>Shipped</span> <button className={s.reorder}>Reorder</button> <button className={s.danger}>Cancel</button></li></ul>
}""",
            "src/pages/Account.tsx": """export function Account() {
  return <form><label>Email <input style={{ border: '1px solid #ddd', padding: 7 }} /></label>
    <div onClick={() => {}} style={{ background: '#0b57d0', color: '#fff', padding: '10px 18px', borderRadius: 8, display: 'inline-block' }}>Save</div></form>
}""",
        },
    ),
    "harbor-panels": (
        """Harbor Desk's panels each pick their own colors and sizes, and dark mode is broken in half of them. Create the design system for the app's UI so every panel looks and behaves the same, in light and dark. One dispatcher uses VoiceOver. Write it up in ui-system.md.""",
        {
            "README.md": """# Harbor Desk
Native desktop client in Rust using the GPUI toolkit (macOS now, Windows next year). Panels: Queue, Approvals, Settings.
Build with `cargo build` (toolchain not installed in this checkout). No designer on the team; no Figma.""",
            "src/panels/queue.rs": """// colors are picked per panel
pub const ROW_BG: u32 = 0xffffff;      // stays white in dark mode
pub const ROW_TEXT: u32 = 0x9e9e9e;
pub const ROW_HEIGHT_PX: f32 = 22.0;""",
            "src/panels/approvals.rs": """pub const APPROVE_BG: u32 = 0x2e7d32;
pub const REJECT_BG: u32 = 0xc62828;
pub const BUTTON_SIZE_PX: f32 = 18.0;   // icon-only buttons
// Approve/Reject are icon-only and VoiceOver reads them as "button".""",
            "src/panels/settings.rs": """pub const LABEL_TEXT: u32 = 0x333333;  // unreadable on the dark background
pub const PADDING_PX: f32 = 7.0;""",
            "docs/support.md": """- "In dark mode the Queue rows are a white block."
- "VoiceOver says 'button' for both approval buttons."
- "The approve and reject buttons are tiny on my laptop." """,
        },
    ),
    "fernway-multi": (
        """We are starting Fernway this month: a web dispatcher screen, a phone app for technicians, and a marketing site. Our designer has a brand in Figma (a teal primary, a warm accent, Inter). Set up the design system all three will share, so the first features are built on it. Write it up in design-system.md.""",
        {
            "README.md": """# Fernway
Scheduling for small field-service companies. Planned stack: web dispatcher in React + TypeScript, technician app in React Native (iOS and Android), marketing site in Astro. Two developers, one designer (part-time). Nothing built yet.
Technicians use the phone outdoors in bright sun and in dark basements, often with gloves.""",
            "docs/brand.md": """From the designer's Figma file:
- Primary teal #2bb3a3, accent amber #f2a541, ink #1f2933, paper #ffffff
- Typeface Inter, sizes 12/14/16/20/28
- Corner radius 10""",
        },
    ),
    "tideline-state": (
        """Decide how our React app should handle state, data fetching and errors across every screen, so new screens stop doing their own thing. Write it up in frontend-plan.md.""",
        {
            "README.md": """# Tideline web
Ferry booking web app. React 19 + Vite SPA on a CDN, talking to the bookings API (OpenAPI in `api/openapi.yaml`).""",
            "src/pages/Crossings.tsx": """import { useEffect, useState } from 'react'
export function Crossings() {
  const [rows, setRows] = useState<any[]>([])
  useEffect(() => { fetch('/api/crossings').then(r => r.json()).then(setRows) }, [])
  return <ul>{rows.map(r => <li key={r.id}>{r.time}</li>)}</ul>
}""",
            "src/store.ts": """export const store = { crossings: [] as any[], basket: [] as any[] }""",
        },
    ),
}

NEIGHBORS = ("craft/draft-ui", "review/inspect-ui", "craft/craft-page", "project/architect-system",
             "project/define-project",  "discovery/run-spike", "discovery/clarify-decisions", "spec/design-solution")


def run(case, phase, model, output, skill):
    prompt, files = CASES[case]
    root = Path(tempfile.mkdtemp()) / case
    root.mkdir()
    for name, content in files.items():
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content.rstrip() + "\n")
    catalog = root / ".claude/skills"
    paths = NEIGHBORS + ((f"craft/{skill}",) if phase == "green" else ())
    for path in paths:
        shutil.copytree(ROOT / "skills" / path, catalog / path.split("/")[-1],
                        ignore=shutil.ignore_patterns("TESTS.md", "eval.json"))
    if phase == "green":
        prompt = f"Open .claude/skills/{skill}/SKILL.md for this work. " + prompt
    prompt += " Keep writes inside this checkout. Do not commit or send messages."
    dest = output / model / case
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "prompt.txt").write_text(prompt + "\n")
    for args in (["init", "-q"], ["config", "core.fsmonitor", "false"], ["add", "."],
                 ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "seed"]):
        subprocess.run(["git", *args], cwd=root, check=True)
    cmd = ["claude", "-p", "--model", model, "--setting-sources", "project", "--strict-mcp-config",
           "--permission-mode", "acceptEdits",
           "--allowedTools", "Read,Glob,Grep,Write,Edit,Skill,Bash(python3:*),Bash(node:*),Bash(git diff:*),Bash(git status:*),Bash(ls:*)",
           "--disallowedTools", "Agent,WebFetch,WebSearch",
           "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--max-turns", "45"]
    try:
        with (dest / "transcript.jsonl").open("w") as out, (dest / "stderr.txt").open("w") as err:
            code = subprocess.run(cmd, cwd=root, input=prompt, text=True, stdout=out, stderr=err,
                                  env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=540).returncode
    except subprocess.TimeoutExpired:
        code = 124
    status = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, text=True)
    status = "\n".join(l for l in status.splitlines() if ".claude/" not in l)
    (dest / "status.txt").write_text(status + "\n")
    (dest / "diff.txt").write_text(subprocess.check_output(["git", "diff"], cwd=root, text=True))
    for line in status.splitlines():
        src = root / line[3:]
        if src.is_file():
            target = dest / "files" / line[3:]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, target)
    tracked = subprocess.check_output(["git", "diff", "--name-only"], cwd=root, text=True).split()
    print(phase, model, case, "exit", code, "| changed:", " ".join(l[3:] for l in status.splitlines()) or "-",
          "| seeded files edited:", " ".join(tracked) or "none", flush=True)
    return code == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("red", "green"))
    parser.add_argument("cases", nargs="*")
    parser.add_argument("--models", nargs="+", choices=MODELS, default=MODELS)
    parser.add_argument("--skill", default="")
    args = parser.parse_args()
    if args.phase == "green" and not args.skill:
        parser.error("green needs --skill")
    OUT.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix=f"{args.phase}-", dir=OUT))
    print(f"Reports: {output}", flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        jobs = [pool.submit(run, c, args.phase, m, output, args.skill) for c in (args.cases or CASES) for m in args.models]
        results = [j.result() for j in jobs]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
