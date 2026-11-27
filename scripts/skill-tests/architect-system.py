"""Run the system-design exercises for architect-system in disposable checkouts.

cases: ledgerline, kettle-orders, fernway, cairn-register (the 1.0.0 takeover case), settle-data
red   — the skill set before the change: design-project 1.0.0 (design cases) or define-project 1.4.0 (settle-data) opened
green — architect-system opened (design cases) or the edited define-project opened beside it (settle-data)
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".skills/architect-system"
MODELS = ("haiku", "sonnet")
OLD = "39c0f86"  # last commit carrying design-project 1.0.0 and define-project 1.4.0

ARCH_INDEX = """# Architecture invariants

Status: Approved

**ARCH-1** Every change to an account balance goes through `ledger/post.py`.
**ARCH-2** A module imports only from its own package and `shared/`.
"""

CASES = {
    "ledgerline": (
        "design",
        """Pages in Ledgerline are slow and the platform lead already provisioned Redis last sprint; their plan is a 5-minute TTL in front of every read, and they want it settled at the 3pm review today. Work out how caching should work across this codebase and write it up in cache-plan.md with a diagram. This is what the team will follow from now on, so put anything else wherever it belongs.""",
        {
            "README.md": """# Ledgerline
Small savings app. Python 3, one Postgres (simulated here with SQLite). Modules: `accounts/` (balances, withdrawals), `catalog/` (savings products and their rates), `ledger/` (posting), `shared/`.
Run `python3 -m accounts.views` or `python3 -m catalog.views` to print a page.""",
            "docs/architecture/INDEX.md": ARCH_INDEX,
            "docs/ops-notes.md": """## Incidents
- INC-14 (March): a member withdrew twice because the withdrawal screen showed a balance read before their first withdrawal posted. Refund issued by hand.
## Latency
- Product rates come from the partner bank's rates API: about 800 ms per call, rate-limited to 10 calls/second. Rates change at most once a day at 06:00.
- Account pages read balances from our own database in under 20 ms.""",
            "shared/__init__.py": "",
            "shared/db.py": """import sqlite3
from pathlib import Path
DB = Path(__file__).resolve().parents[1] / 'ledgerline.db'
def conn():
    c = sqlite3.connect(DB)
    c.execute('create table if not exists balance(account text primary key, cents integer)')
    return c""",
            "accounts/__init__.py": "",
            "accounts/views.py": """from shared.db import conn
def balance_page(account):
    row = conn().execute('select cents from balance where account=?', (account,)).fetchone()
    return f'Balance: {(row or (0,))[0] / 100:.2f}'
def withdrawal_page(account):
    return balance_page(account) + '  [Withdraw]'
if __name__ == '__main__':
    print(withdrawal_page('A-1'))""",
            "catalog/__init__.py": "",
            "catalog/rates.py": """import time
def fetch_rates():
    time.sleep(0.8)  # partner bank rates API
    return {'easy-saver': 3.1, 'fixed-1y': 4.4}""",
            "catalog/views.py": """from catalog.rates import fetch_rates
def products_page():
    return '\\n'.join(f'{k}: {v}%' for k, v in fetch_rates().items())
if __name__ == '__main__':
    print(products_page())""",
            "ledger/__init__.py": "",
            "ledger/post.py": """from shared.db import conn
def post(account, delta_cents):
    c = conn()
    c.execute('insert into balance values (?, ?) on conflict(account) do update set cents = cents + excluded.cents', (account, delta_cents))
    c.commit()""",
        },
    ),
    "kettle-orders": (
        "design",
        """Kettle is three developers and one Postgres database. Support keeps reporting duplicate confirmation emails, and the CTO wants us on Kafka now because we are going to scale. Decide how the parts of this system should talk to each other and hand off work, and write it to messaging.md with a diagram the team can review tomorrow morning. It should be the approach every new feature uses.""",
        {
            "README.md": """# Kettle
Online tea shop. Python 3 monolith, one Postgres (SQLite here). `orders/place.py` handles checkout. `jobs/` holds the cron scripts.
About 300 orders a day, peak 40 an hour before holidays.""",
            "docs/architecture/INDEX.md": """# Architecture invariants

Status: Approved

**ARCH-1** All persistent state lives in the one Postgres database.
**ARCH-2** Checkout responds within 2 seconds at the 95th percentile.
""",
            "docs/support.md": """- Ticket 2211: customer got three identical order confirmation emails for order K-5521.
- Ticket 2240: checkout spun for 20 seconds then failed, but the order was placed and charged.""",
            "docs/vendor-notes.md": """Payments provider: delivers the payment.succeeded webhook at least once; retries for 72 hours until it gets a 2xx. The same event id can arrive more than once.
Email provider: the send call takes 1-15 seconds and times out often; a timed-out call may still have sent the email.""",
            "orders/__init__.py": "",
            "orders/place.py": """import time
from orders import inventory, mailer

def place(order_id, items, email):
    inventory.reserve(order_id, items)          # in-process call, writes to the DB
    for attempt in range(3):                    # added after ticket 2240
        try:
            mailer.send_confirmation(email, order_id)
            break
        except TimeoutError:
            time.sleep(1)
    return 'ok'""",
            "orders/inventory.py": """def reserve(order_id, items):
    pass  # updates stock rows in the same database""",
            "orders/mailer.py": """def send_confirmation(email, order_id):
    raise TimeoutError('email provider timed out (the email may still have been sent)')""",
            "orders/webhooks.py": """def payment_succeeded(event):
    from orders.place import place
    return place(event['order_id'], event['items'], event['email'])""",
            "jobs/nightly_restock.py": """# cron 02:00: polls the orders table and emails suppliers
def run():
    pass""",
        },
    ),
    "fernway": (
        "design",
        """We are starting Fernway this month with two developers. Lay out the foundation of the system: how the code is structured, the data, how the pieces communicate, caching, background work and the principles we build by, so every feature after this follows it. Write it to foundation.md.""",
        {
            "README.md": """# Fernway
Scheduling for small field-service companies (plumbers, electricians). A dispatcher assigns jobs on a web screen; technicians see and update their jobs on a phone app, often in basements with no signal. First customers: three companies from the founder's network. Stack picked: TypeScript, Node, Postgres. Nothing built yet.""",
            "docs/brief.md": """Must-haves for the first customers: create a job, assign it to a technician, technician marks it started/finished and adds photos and notes, dispatcher sees status. Later: invoicing, customer SMS reminders, a public booking page.""",
        },
    ),
    "cairn-register": (
        "design",
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
    "settle-data": (
        "record",
        """Update our architecture docs: we still have to settle whether each module keeps its own SQLite file or we move everything to one shared Postgres, and then add it as an invariant so the design docs follow it.""",
        {
            "README.md": """# Brightpost
Newsletter platform. Modules `subscribers/`, `campaigns/`, `billing/`, each with its own SQLite file today. Billing reports join subscribers and campaigns by copying the files nightly. Two developers. Hosting on one VM.""",
            "docs/architecture/INDEX.md": """# Architecture invariants

Status: Approved

**ARCH-1** A module owns its tables; no other module writes them.
**ARCH-2** Every external call has a timeout.
""",
            "docs/architecture/data.md": """# Data architecture

Status: Approved

Each module stores its data in its own SQLite file under `data/<module>.db`.
""",
            "subscribers/__init__.py": "",
            "campaigns/__init__.py": "",
            "billing/report.py": """# nightly: copies data/subscribers.db and data/campaigns.db, then joins them
def run():
    pass""",
        },
    ),
}

NEIGHBORS = ("spec/design-solution", "track/scan-architecture", "craft/draft-ui", "discovery/run-spike",
             "discovery/clarify-decisions", "discovery/define-domain")


def install(catalog, phase):
    """Copy the skills a consuming project would hold."""
    def put(path, src_root):
        shutil.copytree(src_root / path, catalog / path.split("/")[-1],
                        ignore=shutil.ignore_patterns("TESTS.md", "eval.json"))
    for path in NEIGHBORS:
        put(path, ROOT / "skills")
    if phase == "red":
        old = Path(tempfile.mkdtemp())
        archive = subprocess.check_output(["git", "archive", OLD, "skills/project/define-project", "skills/project/design-project"], cwd=ROOT)
        subprocess.run(["tar", "-x", "-C", str(old)], input=archive, check=True)
        put("project/define-project", old / "skills")
        put("project/design-project", old / "skills")
    else:
        put("project/define-project", ROOT / "skills")
        put("project/architect-system", ROOT / "skills")


def seed(case, phase):
    root = Path(tempfile.mkdtemp()) / case
    root.mkdir()
    kind, prompt, files = CASES[case]
    for name, content in files.items():
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content.rstrip() + "\n")
    if case == "cairn-register":  # the 1.0.0 takeover case, from commit fa64751
        import sqlite3
        with sqlite3.connect(root / "app/receipts.db") as db:
            db.executescript("create table receipt(id text primary key, amount integer); insert into receipt values ('CR-17', 125);")
    install(root / ".claude/skills", phase)
    if kind == "record":
        skill = "define-project"
    else:
        skill = "design-project" if phase == "red" else "architect-system"
    prompt = f"Open .claude/skills/{skill}/SKILL.md for this work. " + prompt
    prompt += " Keep writes inside this checkout. Do not commit or send messages."
    return root, prompt


def run(case, phase, model, output):
    root, prompt = seed(case, phase)
    dest = output / model / case
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "fixture.txt").write_text(str(root) + "\n")
    (dest / "prompt.txt").write_text(prompt + "\n")
    for args in (["init", "-q"], ["config", "core.fsmonitor", "false"], ["add", "."],
                 ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "seed"]):
        subprocess.run(["git", *args], cwd=root, check=True)
    cmd = ["claude", "-p", "--model", model, "--setting-sources", "project", "--strict-mcp-config",
           "--permission-mode", "acceptEdits",
           "--allowedTools", "Read,Glob,Grep,Write,Edit,Bash(python3:*),Bash(git diff:*),Bash(git status:*),Bash(ls:*)",
           "--disallowedTools", "Agent,WebFetch,WebSearch",
           "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--max-turns", "40"]
    try:
        with (dest / "transcript.jsonl").open("w") as out, (dest / "stderr.txt").open("w") as err:
            result = subprocess.run(cmd, cwd=root, input=prompt, text=True, stdout=out, stderr=err,
                                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=480)
        code = result.returncode
    except subprocess.TimeoutExpired:
        code = 124
    status = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, text=True)
    status = "\n".join(l for l in status.splitlines() if ".claude/" not in l)
    (dest / "status.txt").write_text(status + "\n")
    (dest / "diff.txt").write_text(subprocess.check_output(["git", "diff"], cwd=root, text=True))
    for line in status.splitlines():
        rel = line[3:]
        src = root / rel
        if src.is_file():
            target = dest / "files" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, target)
    tracked = subprocess.check_output(["git", "diff", "--name-only"], cwd=root, text=True).split()
    print(phase, model, case, "exit", code, "| changed:", " ".join(l[3:] for l in status.splitlines()) or "-",
          "| seeded files edited:", " ".join(tracked) or "none", flush=True)
    return code == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("red", "green"))
    parser.add_argument("cases", nargs="*", metavar="case", help=", ".join(CASES))
    parser.add_argument("--models", nargs="+", choices=MODELS, default=MODELS)
    args = parser.parse_args()
    for case in args.cases:
        if case not in CASES:
            parser.error(f"unknown case: {case}")
    OUT.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix=f"{args.phase}-", dir=OUT))
    print(f"Reports: {output}", flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        jobs = [pool.submit(run, c, args.phase, m, output) for c in (args.cases or CASES) for m in args.models]
        results = [j.result() for j in jobs]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
