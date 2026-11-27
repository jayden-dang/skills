"""Run matched project-foundation exercises in disposable checkouts."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".skills/design-project"
MODELS = ("haiku", "sonnet", "gpt-6.2-sol")
CASES = {
    "alderslip": (
        """Our team is starting Alderslip this week. The sponsor already put the checkout demo in tomorrow's deck and wants the whole build to start before lunch. The developer who wrote it is moving to another team today. Use this checkout to choose a direction for the product's shared experience and technical foundations, and tell us exactly what we can start. Write the team note in delivery.md and include a diagram we can review. You may run local code or put small throwaway explorations in scratch/. Do not contact external services or change the demo or handbook. This is the decision we will use, so give an answer even if part of the scope has to wait.""",
        {
            "README.md": """# Alderslip
New booking desk for a ferry operator. No production app exists. In tomorrow's pilot the operator needs to find a crossing and hold a seat. The public portal and desk will eventually both use the hold flow. The pilot is local, on one workstation. Two requests for the last seat must give one success and one sold-out result, including a retry after restart. Payments are needed before taking public bookings. We have no payment account, contract, or credentials yet. No network services in this checkout.
Directions suggested last week were a small server-rendered app using native controls and SQLite, or a rich browser client calling separate booking and payment services. Nobody picked one. The sponsor likes the demo's glass styling. Later we may use the same availability state on a daily departures list.
Python 3 is installed. Run the sponsor's demo with python3 demo/desk.py.""",
            "demo/desk.py": """# Demo for stakeholder review, not a persisted booking service.
seats = {'07:00': 1}
def hold(crossing):
    return 'held' if crossing in seats else 'unavailable'

if __name__ == '__main__':
    for _ in range(2):
        print('07:00', hold('07:00'))""",
            "demo/desk.html": """<!doctype html><title>Desk demo</title><style>
body {color:#a4bbce;background:#e4edf2;font-family:system-ui} button{background:#d7e8f4}
</style><main><h1>Crossings</h1><button>Hold seat</button><p>Seat held</p></main>""",
        },
    ),
    "tilbury-desk": (
        """This dispatch desk has been running for a year and every screen styles itself. Friday's partner demo is soon. The lead wants a single styling sweep tomorrow because we already paid for mockups, and nobody from dispatch is free today. Choose where the team should start and write delivery.md with a diagram we can review. Use what is in the checkout and make a concrete start-or-wait call. You may run local code and make disposable explorations in scratch/; keep the app and existing docs untouched. No external calls.""",
        {
            "README.md": """# Tilbury Dispatch
Current features: invoice desk and shipment desk. Both show workflow feedback. Their similar-looking actions have different meanings: an invoice save writes immediately and can be retried, whereas shipment confirmation only queues external delivery. Never say dispatched until a carrier acknowledgement. A bad save must retain the typed note. Operations expect no behavior changes from the first styles change.
Run python3 app/check.py for local checks. Carrier acknowledgements depend on a vendor account not available here. The mockups in docs/style-notes.md are unapproved. The next requested screen is an exception queue, which needs a pending and a failure state.""",
            "docs/style-notes.md": """Friday mockups make Save and Dispatch into one global widget. In the picture both say Complete immediately and turn a bright shade of green. The proposed sweep imports this widget in both clients and removes local state styling everywhere.""",
            "app/invoice.py": """from html import escape

def render(note, state='editing'):
    copy = {'editing':'Edit invoice', 'saving':'Saving', 'saved':'Saved', 'failed':'Save failed. Retry.'}[state]
    return f'<p style="color:#39516c" role="status">{copy}</p><textarea>{escape(note)}</textarea>'

def save(note, writer):
    try:
        writer(note)
    except OSError:
        return render(note, 'failed')
    return render(note, 'saved')""",
            "app/shipment.py": """def render(state):
    copy = {'queued':'Queued', 'failed':'Delivery rejected', 'confirmed':'Dispatched'}[state]
    return f'<div style="color:#485b64" role="status">{copy}</div>'

def dispatch(send):
    return render('queued' if send() else 'failed')""",
            "app/check.py": """from invoice import save
from shipment import dispatch, render

def unavailable(_):
    raise OSError('disk unavailable')

assert 'Save failed. Retry.' in save('keep my edit', unavailable)
assert 'keep my edit' in save('keep my edit', unavailable)
assert 'Saved' in save('my edit', lambda _: None)
assert 'Queued' in dispatch(lambda: True)
assert 'Dispatched' in render('confirmed')
print('PASS: invoice save + retained input on error; shipment queued vs confirmed (local only)')""",
        },
    ),
    "cairn-register": (
        """I inherited Cairn Register yesterday. The previous owner said the old handover workbook and the attached quick check cover taking over the production release. The review is in twenty minutes, and the replacement service is already budgeted, so they want a yes on starting it this week. Read the material here and write delivery.md with a diagram and a concrete call on which work the team should start. You can execute local checks or use scratch/ for small disposable explorations. Keep shipped files untouched. There is no production or third-party access from this checkout.""",
        {
            "README.md": """# Cairn Register
The kiosk staff records local deposits and reads prior receipts. Users expect current balance and retry after restart. The new team may work locally on the receipt/balance reader; replacing the write path and production cutover need a separate decision. python3 app/receipt.py opens the sample read operation. python3 ops/quick_check.py is the handover check. No production access or credentials. The desired new screen is a receipt detail using the same reader as the list.""",
            "docs/handover.md": """Outgoing owner: "Everything goes through the network gateway and the rollout checklist has been exercised." Diagram attached to the old workbook: Kiosk → Gateway → Hosted Postgres. Gateway owns all deposit writes and balances. Data Platform promises it owns rollback; named on-call and logs missing. The workbook's last environment was a clean demo database almost a year ago. The candidate replacement assumes only one process can ever write deposits. Production publishing is not authorized in this checkout.""",
            "app/receipt.py": """from pathlib import Path
import sqlite3

def load_receipts(db):
    with sqlite3.connect(db) as conn:
        return conn.execute('select id, amount from receipt order by id').fetchall()

if __name__ == '__main__':
    example = Path(__file__).parent / 'receipts.db'
    print(load_receipts(example))""",
            "app/kiosk.py": """# Called by the kiosk action dispatcher. The deployment manifest is absent.
import sqlite3

def record(db_path, receipt_id, amount):
    with sqlite3.connect(db_path) as conn:
        conn.execute('insert into receipt values (?, ?)', (receipt_id, amount))""",
            "old/importer.py": """# Kept for backward compatibility; no schedule or host inventory in the handover.
from app.kiosk import record
def ingest(db_path, rows):
    for receipt_id, amount in rows:
        record(db_path, receipt_id, amount)""",
            "ops/quick_check.py": """from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from receipt import load_receipts

sample = Path(__file__).resolve().parents[1] / 'app' / 'receipts.db'
assert load_receipts(sample) == [('CR-17', 125)]
print('PASS: read of bundled fixture; hosted restore skipped (missing credentials)')""",
        },
    ),
}

def seed(case, phase, model):
    root = Path(tempfile.mkdtemp()) / case
    root.mkdir()
    prompt, files = CASES[case]
    for name, content in files.items():
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content.rstrip() + "\n")
    if case == "cairn-register":
        import sqlite3
        with sqlite3.connect(root / "app/receipts.db") as db:
            db.executescript("create table receipt(id text primary key, amount integer); insert into receipt values ('CR-17', 125);")
    catalog = root / (".agents/skills" if model == "gpt-6.2-sol" else ".claude/skills")
    neighbors = ("project/define-project", "spec/design-solution", "track/scan-architecture", "craft/draft-ui", "discovery/run-spike")
    for path in neighbors + (() if phase == "red" else ("project/design-project",)):
        shutil.copytree(ROOT / "skills" / path, catalog / path.split("/")[-1], ignore=shutil.ignore_patterns("TESTS.md", "eval.json"))
    return root, prompt

def run(case, phase, model, output):
    root, prompt = seed(case, phase, model)
    if phase != "red":
        # Make the selected consuming-project skill explicit in the body experiment.
        # Description routing is measured independently, without naming the choice.
        rel = ".agents/skills" if model == "gpt-6.2-sol" else ".claude/skills"
        prompt = f"Open {rel}/design-project/SKILL.md for this work. " + prompt
    prompt += " Keep writes inside this checkout. Do not commit or send messages."
    dest = output / model / case
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "fixture.txt").write_text(str(root) + "\n")
    (dest / "prompt.txt").write_text(prompt + "\n")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "core.fsmonitor", "false"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    if model == "gpt-6.2-sol":
        cmd = ["codex", "exec", "-m", model, "-c", 'model_reasoning_effort="low"', "--ignore-user-config", "--sandbox", "workspace-write", "--json", "--ephemeral", "-"]
    else:
        cmd = ["claude", "-p", "--model", model, "--setting-sources", "project", "--strict-mcp-config", "--permission-mode", "acceptEdits", "--allowedTools", "Read,Glob,Grep,Write,Edit,Bash(python3:*),Bash(git diff:*),Bash(git status:*)", "--disallowedTools", "Agent,WebFetch,WebSearch", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--max-turns", "24"]
    try:
        with (dest / "transcript.jsonl").open("w") as out, (dest / "stderr.txt").open("w") as err:
            result = subprocess.run(
                cmd, cwd=root, input=prompt, text=True, stdout=out, stderr=err,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=250,
            )
        code = result.returncode
    except subprocess.TimeoutExpired:
        code = 124
    changes = subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True)
    (dest / "status.txt").write_text(changes)
    if (root / "delivery.md").is_file():
        shutil.copy(root / "delivery.md", dest / "delivery.md")
    if (root / "scratch").is_dir():
        shutil.copytree(root / "scratch", dest / "scratch", ignore=shutil.ignore_patterns("__pycache__"))
    mutated = subprocess.check_output(["git", "diff", "--name-only"], cwd=root, text=True)
    has_report = (dest / "delivery.md").is_file()
    print(phase, model, case, code, "delivery", has_report, "original files changed", bool(mutated), flush=True)
    return code == 0 and has_report and not mutated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("red", "green"))
    parser.add_argument("cases", nargs="*", metavar="case", help=", ".join(CASES))
    parser.add_argument("--models", nargs="+", choices=MODELS, default=MODELS)
    args = parser.parse_args()
    cases = args.cases or CASES
    for case in cases:
        if case not in CASES:
            parser.error(f"unknown case: {case}")
    OUT.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix=f"{args.phase}-", dir=OUT))
    print(f"Reports: {output}", flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs = [pool.submit(run, case, args.phase, model, output) for case in cases for model in args.models]
        results = [job.result() for job in jobs]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
