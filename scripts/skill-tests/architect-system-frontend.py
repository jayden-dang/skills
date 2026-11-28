"""Front-end architecture exercises for architect-system, in disposable checkouts.

cases: tideline-web (a web SPA), harbor-desk (a native desktop client of a local daemon)
red   — architect-system as of commit 6f8f36c (2.0.0) opened
green — the working tree's architect-system opened
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".skills/architect-system-frontend"
MODELS = ("haiku", "sonnet")
BASE = "6f8f36c"

CASES = {
    "tideline-web": (
        """Tideline's web app grew screen by screen and each one does its own thing. The lead wants everything moved into one Redux Toolkit store by Friday, and the API team ships a breaking change to the bookings response next month. Decide how this web front end should work across all screens (rendering, state, data fetching, auth, errors, performance and anything else it needs) so every new screen follows it. Write it to frontend-plan.md with a diagram.""",
        {
            "README.md": """# Tideline web
Ferry booking web app. React 19 + Vite SPA, served from a CDN. Talks to the bookings API (`/api/*`, owned by another team, OpenAPI file in `api/openapi.yaml`).
Users: mostly phones, many low-end Android devices on slow mobile networks in coastal towns. Marketing pages and the booking flow live in the same app.
Run `npm test` for the unit tests (not installed in this checkout).""",
            "docs/incidents.md": """- INC-7: after an API deploy, users whose tab had been open for days hit "Cannot read properties of undefined (reading 'seats')" until they reloaded. The CDN served the old bundle for 2 days.
- INC-9: a support agent pasted a customer message containing HTML into the notes field; the notes page rendered it as HTML.""",
            "docs/architecture/INDEX.md": """# Architecture invariants

Status: Approved

**ARCH-1** The bookings API is the only authority for seats and bookings.
**ARCH-2** Every external call has a timeout.
""",
            "api/openapi.yaml": """openapi: 3.1.0
info: {title: bookings, version: 4.2.0}
paths:
  /api/crossings: {get: {responses: {'200': {description: list}}}}
  /api/bookings: {post: {responses: {'201': {description: created}}}}""",
            "src/auth.ts": """export function saveLogin(token: string) {
  localStorage.setItem('access_token', token)   // read by every fetch
}
export const authHeader = () => ({ Authorization: `Bearer ${localStorage.getItem('access_token')}` })""",
            "src/pages/Crossings.tsx": """import { useEffect, useState } from 'react'
import { authHeader } from '../auth'
export function Crossings() {
  const [rows, setRows] = useState<any[]>([])
  useEffect(() => { fetch('/api/crossings', { headers: authHeader() }).then(r => r.json()).then(setRows) }, [])
  return <ul>{rows.map(r => <li key={r.id}>{r.time} - {r.seats.left} seats</li>)}</ul>
}""",
            "src/pages/Notes.tsx": """export function Notes({ html }: { html: string }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />
}""",
            "src/store.ts": """// global store added for the booking flow; crossings are also copied here
export const store = { crossings: [] as any[], basket: [] as any[] }""",
        },
    ),
    "harbor-desk": (
        """Harbor Desk is our desktop app for dispatchers. Users report the window freezing during sync, and one of our dispatchers is blind and uses VoiceOver. We ship a new build every two weeks but some offices never update. Lay out the front-end architecture for this desktop client (state, how it talks to the daemon, errors, accessibility, updates and anything else it needs) so every new panel follows it. Write it to client-architecture.md with a diagram.""",
        {
            "README.md": """# Harbor Desk
Native desktop client written in Rust with the GPUI toolkit (macOS first, Windows next year). It talks to `harbord`, a local daemon, over a Unix socket using JSON-RPC. The daemon syncs with the cloud and may restart at any time.
Panels: Queue, Approvals, Settings. Build with `cargo build` (toolchain not installed in this checkout).""",
            "docs/support.md": """- "The whole window freezes for 10-20 seconds when the morning sync runs."
- "After the daemon restarted, the Approvals panel still showed requests that were already decided."
- "VoiceOver reads the approval buttons as 'button' with no name."
- Offices on build 1.8 (four months old) still connect to the current daemon.""",
            "src/rpc.rs": """use std::os::unix::net::UnixStream;
use std::io::{Read, Write};
// called from panel render code
pub fn call(method: &str, params: &str) -> String {
    let mut s = UnixStream::connect("/tmp/harbord.sock").unwrap();
    s.write_all(format!("{{\\"method\\":\\"{method}\\",\\"params\\":{params}}}").as_bytes()).unwrap();
    let mut out = String::new();
    s.read_to_string(&mut out).unwrap();
    out
}""",
            "src/panels/approvals.rs": """// Approvals panel: on render, calls rpc::call("approvals.list", "{}") and keeps the result in a field.
// Approve/Reject buttons are icon-only.""",
            "src/main.rs": """mod rpc;
fn main() { /* opens the window and the three panels */ }""",
        },
    ),
}

NEIGHBORS = ("spec/design-solution", "track/scan-architecture", "craft/draft-ui", "discovery/run-spike",
             "discovery/clarify-decisions", "discovery/define-domain", "review/inspect-ui")


def install(catalog, phase):
    def put(path, src_root):
        shutil.copytree(src_root / path, catalog / path.split("/")[-1],
                        ignore=shutil.ignore_patterns("TESTS.md", "eval.json"))
    for path in NEIGHBORS:
        put(path, ROOT / "skills")
    if phase == "red":
        old = Path(tempfile.mkdtemp())
        archive = subprocess.check_output(["git", "archive", BASE, "skills/project/define-project", "skills/project/architect-system"], cwd=ROOT)
        subprocess.run(["tar", "-x", "-C", str(old)], input=archive, check=True)
        src = old / "skills"
    else:
        src = ROOT / "skills"
    put("project/define-project", src)
    put("project/architect-system", src)


def run(case, phase, model, output):
    prompt, files = CASES[case]
    root = Path(tempfile.mkdtemp()) / case
    root.mkdir()
    for name, content in files.items():
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content.rstrip() + "\n")
    install(root / ".claude/skills", phase)
    prompt = "Open .claude/skills/architect-system/SKILL.md for this work. " + prompt + " Keep writes inside this checkout. Do not commit or send messages."
    dest = output / model / case
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "prompt.txt").write_text(prompt + "\n")
    for args in (["init", "-q"], ["config", "core.fsmonitor", "false"], ["add", "."],
                 ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "seed"]):
        subprocess.run(["git", *args], cwd=root, check=True)
    cmd = ["claude", "-p", "--model", model, "--setting-sources", "project", "--strict-mcp-config",
           "--permission-mode", "acceptEdits",
           "--allowedTools", "Read,Glob,Grep,Write,Edit,Bash(python3:*),Bash(node:*),Bash(git diff:*),Bash(git status:*),Bash(ls:*)",
           "--disallowedTools", "Agent,WebFetch,WebSearch",
           "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--max-turns", "40"]
    try:
        with (dest / "transcript.jsonl").open("w") as out, (dest / "stderr.txt").open("w") as err:
            code = subprocess.run(cmd, cwd=root, input=prompt, text=True, stdout=out, stderr=err,
                                  env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=480).returncode
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
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix=f"{args.phase}-", dir=OUT))
    print(f"Reports: {output}", flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        jobs = [pool.submit(run, c, args.phase, m, output) for c in (args.cases or CASES) for m in args.models]
        results = [j.result() for j in jobs]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
