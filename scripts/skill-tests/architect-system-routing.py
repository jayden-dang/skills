"""Route first messages against the full skill listing: red uses the descriptions at commit 39c0f86, green the working tree.

python3 scripts/skill-tests/architect-system-routing.py red|green [reps]
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json, subprocess, sys, tempfile, yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".skills/architect-system"
OLD = "39c0f86"
MODELS = ("haiku", "sonnet")
NEW = "architect-system"
QUERIES = [
    (NEW, "Pages are slow and the platform lead wants Redis in front of everything. Work out how caching should work across this codebase."),
    (NEW, "We're three devs on one Postgres and the CTO wants Kafka. Decide how the parts of this system should talk to each other and hand off work."),
    (NEW, "Starting a new project next week: lay out how the code is structured, who owns which data, background jobs and the principles we build by."),
    (NEW, "We keep getting duplicate webhooks and emails in different places. Before patching each one, decide the system-wide approach to retries and idempotency."),
    (NEW, "Should we split this monolith into services or keep a modular monolith? Compare and recommend for the whole codebase."),
    (NEW, "thiết kế lại tầng data cho cả hệ thống: mỗi module một database riêng hay dùng chung một Postgres?"),
    (NEW, "We inherited this API from a contractor. Decide which parts of its architecture we keep (module boundaries, where state lives, how failures recover) before we build on it."),
    (NEW, "Pick how tenant isolation should work across the whole system: a tenant column, a schema per tenant, or a database per tenant."),
    (NEW, "Design how logging, config and secrets should work across all our services so every feature follows the same rules."),
    ("define-project", "We already decided every external call has a timeout. Add it to docs/architecture as ARCH-3."),
    ("define-project", "Update docs/architecture/data.md to match what the code does today."),
    ("define-project", "Check our architecture docs against their templates and report what is missing."),
    ("design-solution", "Requirements for the invoice resend feature are approved. Write its design.md."),
    ("scan-architecture", "Scan the repo and rank where a refactor would pay off most."),
    ("root-cause", "The cache returns a stale balance right after a withdrawal. Find out why."),
    ("draft-ui", "Show me three clickable directions for the settings screen."),
    ("frame-change", "Can we add a CSV export button to the reports page?"),
    ("inspect-invariants", "Does this design.md respect ARCH-2? It cites it in its Respects line."),
    ("research", "How does Redis evict keys under maxmemory-policy allkeys-lru? Write it up with citations."),
]

def listing(phase):
    rows = []
    if phase == "green":
        files = sorted((ROOT / "skills").glob("*/*/SKILL.md"))
        texts = [f.read_text() for f in files]
    else:
        names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", OLD, "skills"], cwd=ROOT, text=True).split()
        texts = [subprocess.check_output(["git", "show", f"{OLD}:{n}"], cwd=ROOT, text=True) for n in names if n.count("/") == 3 and n.endswith("/SKILL.md")]
    for text in texts:
        d = yaml.safe_load(text.split("---", 2)[1])
        if not d.get("disable-model-invocation"):
            rows.append(f"- {d['name']}: {' '.join(str(d['description']).split())}")
    return "\n".join(rows)

def run(i, catalog, model):
    expected, user = QUERIES[i]
    prompt = f"Choose the first skill to load for the message below from this list. Return exactly its name, or NONE. Do not use tools.\n\n{catalog}\n\nMessage: {user}"
    with tempfile.TemporaryDirectory(prefix="work-") as root:
        cmd = ["claude", "-p", "--model", model, "--tools", "", "--setting-sources", "project", "--strict-mcp-config", "--no-session-persistence", "--output-format", "json"]
        r = subprocess.run(cmd, input=prompt, text=True, cwd=root, capture_output=True, timeout=120)
    rows = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    actual = (rows[-1].get("result", "") if rows else "").strip().strip("`").strip()
    return {"query": i + 1, "model": model, "expected": expected, "actual": actual}

def main():
    phase = sys.argv[1]
    reps = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    catalog = listing(phase)
    OUT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda a: run(*a), [(i, catalog, m) for _ in range(reps) for i in range(len(QUERIES)) for m in MODELS]))
    (OUT / f"routing-{phase}-x{reps}.json").write_text(json.dumps(results, indent=1) + "\n")
    expect_old = {"architect-system": "design-project"} if phase == "red" else {}
    ok = [r for r in results if r["actual"] == expect_old.get(r["expected"], r["expected"])]
    for r in results:
        if r not in ok:
            print("miss", r)
    print(f"{phase}: {len(ok)}/{len(results)}")

if __name__ == "__main__":
    main()
