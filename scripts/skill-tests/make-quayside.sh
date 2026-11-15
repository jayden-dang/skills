#!/bin/bash
# make-quayside.sh <target-dir> <skills-repo> [skill…]
# Builds a small billing repo with three features merged to dev this week, a github tracker
# reached through bin/gh (stateful, local), and the named skills installed in .claude/skills.
set -euo pipefail
T="$1"; SK="$2"; shift 2
mkdir -p "$T"; cd "$T"
git init -q -b main
git config core.fsmonitor false
git config user.name "Lan Pham"; git config user.email "lan@quayside.example"
d() { date -u -v-"$1"d +%Y-%m-%dT09:00:00Z; }
ci() { GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git commit -q -m "$2"; }
mg() { GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git merge -q --no-ff "$2" -m "$3"; }

mkdir -p src test docs/agents docs/specs/berth bin
cat > package.json <<'E'
{ "name": "quayside", "private": true, "type": "module", "scripts": { "test": "node --test" } }
E
cat > src/invoice.js <<'E'
// An invoice for a berth stay. `status` is stored: "open" until paid in full, then "paid".
export function newInvoice(id, total) {
  return { id, total, status: "open", payments: [] };
}
export function paidTotal(inv) {
  return inv.payments.reduce((s, p) => s + p.amount, 0);
}
E
cat > src/api.js <<'E'
import { newInvoice } from "./invoice.js";
export const db = new Map();
export const routes = {
  "POST /invoices": (b) => { const inv = newInvoice(b.id, b.total); db.set(inv.id, inv); return [201, inv]; },
};
// handle("POST /invoices", body) → [status, body]. An uncaught error is a 500.
export function handle(route, body) {
  try { return routes[route](body); }
  catch (e) { return [e.status ?? 500, { error: e.message }]; }
}
E
cat > test/invoice.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { handle } from "../src/api.js";
test("creates an open invoice", () => {
  const [s, inv] = handle("POST /invoices", { id: "B-1", total: 300 });
  assert.equal(s, 201); assert.equal(inv.status, "open");
});
E
cat > CONTEXT.md <<'E'
# Quayside

Billing for berth stays at a marina.

## Language

**Invoice**: what a vessel owner owes for one berth stay.
**Paid in full**: the payments on an invoice, less anything refunded, add up to its total.
**Refunded**: every payment on an invoice has been given back. A refunded invoice is owed again in full.
**Late fee**: 5 per whole week past the due date, charged on any invoice that is not paid in full.
E
cat > AGENTS.md <<'E'
# Quayside

Node 22, no dependencies. `npm test` runs everything. Work lands on `dev` through merge commits.
Agent config: `docs/agents/project.md`, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`.
Skills: `.claude/skills/`.
E
cat > docs/agents/project.md <<'E'
# Project configuration (agent-facing)

## Verify commands
- **Test:** `npm test`

## Project posture
- **Default PR base:** `dev`
- **Default landing action:** `merge`
- **Operator:** Lan Pham (`lan`)

## Paths
- Glossary: `CONTEXT.md`
- Specs: `docs/specs/` (catalog `docs/specs/INDEX.md`)
E
if [ "${GATE:-}" = 1 ]; then cat >> docs/agents/project.md <<'E'

## Working agreement
- Minh (harbour office) approves every new ticket before it is created. Nobody else opens one.
E
fi
cat > docs/agents/triage-labels.md <<'E'
# Triage label mapping (agent-facing)

| Canonical role | Label in this repo |
|---|---|
| needs-triage | `status:inbox` |
| needs-info | `status:needs-info` |
| ready-for-agent | `status:ready` |
| ready-for-human | `status:human` |
| shaping | `status:shaping` |
| building | `status:building` |
| in-review | `status:in-review` |
| shipped | `status:shipped` |
| wontfix | `wontfix` |
| bug | `bug` |
| enhancement | `enhancement` |

Rule: every triaged issue carries exactly one category role (bug/enhancement)
and one state role.
E
cat > docs/agents/issue-tracker.md <<'E'
# Issue tracker configuration (agent-facing)

**Tracker:** github — always through `bin/gh` (it carries the host and token for this repo).

## Wayfinding operations

- List open issues: `bin/gh issue list --state open`
- Read issue: `bin/gh issue view <n> --comments`
- Create issue: `bin/gh issue create --title <t> --body-file <f> --label <l> --assignee <login>`
- Edit labels: `bin/gh issue edit <n> --add-label <l> --remove-label <l>`
- Comment: `bin/gh issue comment <n> --body-file <f>`
- Close: `bin/gh issue close <n> --comment <text>`

## Issue format

Every writer follows this when creating an issue.

**Title:** what the reader gets, or for a bug what goes wrong, in plain words.

**Body of a bug:**

```markdown
## What happens
## Expected
## How to reproduce
## Evidence
```

**Body of anything else:**

```markdown
## Problem
## Outcome
## Acceptance
- [ ] Observable, and checkable on its own
## Out of scope
```

Source paths, line numbers and function names go in the spec, not the issue.

- **Assignee:** whom the requester named, else the requester.
- **Status:** one category role and one state role from `triage-labels.md`. The state is what the
  requester named, else `needs-triage`.
E
if [ -n "${FILING:-}" ]; then python3 - "$FILING" <<'PY'
import sys
p='docs/agents/issue-tracker.md'; s=open(p).read()
s=s.replace("## Wayfinding operations","**Follow-up filing:** "+sys.argv[1]+"\n\n## Wayfinding operations",1)
open(p,'w').write(s)
PY
fi
cat > docs/specs/INDEX.md <<'E'
# Feature catalog

| Code | Feature | Spec | Status |
|---|---|---|---|
| BERTH | Berth invoices | `docs/specs/berth/requirements.md` | Shipped |
E
cat > docs/specs/berth/requirements.md <<'E'
# BERTH — Berth invoices
Status: Shipped

**BERTH-1.1** WHEN a stay is booked, the system SHALL create an open invoice for its total.
E

# --- the tracker: bin/gh, state under .git ---
cat > bin/gh <<'E'
#!/usr/bin/env python3
import json, sys, os, subprocess, datetime
root = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, text=True).stdout.strip()
P = os.path.join(root, "gh.json")
S = json.load(open(P))
a = sys.argv[1:]
def save(): json.dump(S, open(P, "w"), indent=1)
def opt(name, many=False):
    out = []
    for i, x in enumerate(a):
        if x == name and i + 1 < len(a): out.append(a[i + 1])
        elif x.startswith(name + "="): out.append(x.split("=", 1)[1])
    if many: return [y for x in out for y in x.split(",") if y]
    return out[-1] if out else None
def body():
    f = opt("--body-file") or opt("-F")
    if f: return sys.stdin.read() if f == "-" else open(f).read()
    return opt("--body") or opt("-b") or ""
def shape(i, fields):
    full = {"number": i["number"], "title": i["title"], "body": i["body"], "state": i["state"].upper(),
            "labels": [{"name": l} for l in i["labels"]], "assignees": [{"login": l} for l in i["assignees"]],
            "comments": i["comments"], "url": f"https://github.com/quayside/billing/issues/{i['number']}",
            "createdAt": i.get("createdAt", "")}
    return {k: full[k] for k in fields if k in full} if fields else full
def find(n):
    for i in S["issues"]:
        if str(i["number"]) == str(n).lstrip("#"): return i
    sys.exit(f"GraphQL: Could not resolve to an Issue with the number of {n}. (repository.issue)")
if a[:2] == ["api", "user"]:
    print(json.dumps({"login": "lan"}))
elif a[:2] == ["issue", "list"]:
    st = opt("--state") or opt("-s") or "open"
    lab = opt("--label", True) + opt("-l", True)
    xs = [i for i in S["issues"] if st == "all" or i["state"] == st]
    xs = [i for i in xs if all(l in i["labels"] for l in lab)]
    j = opt("--json")
    if j is not None: print(json.dumps([shape(i, [f for f in j.split(",") if f != "blockedBy"]) for i in xs]))
    else:
        for i in xs: print(f"{i['number']}\t{i['state'].upper()}\t{i['title']}\t{', '.join(i['labels'])}")
elif a[:2] == ["issue", "create"]:
    t = opt("--title") or opt("-t")
    if not t: sys.exit("must provide `--title` and `--body` (or `--fill` or `fill-first` or `--fill-verbose`) when not running interactively")
    n = max(i["number"] for i in S["issues"] + S["prs"]) + 1
    S["issues"].append({"number": n, "title": t, "body": body(), "state": "open",
                        "labels": opt("--label", True) + opt("-l", True),
                        "assignees": ["lan" if x == "@me" else x for x in opt("--assignee", True) + opt("-a", True)],
                        "comments": [], "createdAt": datetime.datetime.utcnow().isoformat() + "Z"})
    save(); print(f"https://github.com/quayside/billing/issues/{n}")
elif a[:2] == ["issue", "view"]:
    i = find(a[2]); j = opt("--json")
    if j is not None: print(json.dumps(shape(i, j.split(","))))
    else:
        print(f"title:\t{i['title']}\nstate:\t{i['state'].upper()}\nlabels:\t{', '.join(i['labels'])}\nassignees:\t{', '.join(i['assignees'])}\nnumber:\t{i['number']}\n--\n{i['body']}")
        for c in i["comments"]: print(f"--\n{c['author']['login']}:\n{c['body']}")
elif a[:2] == ["issue", "edit"]:
    i = find(a[2])
    for l in opt("--add-label", True):
        if l not in i["labels"]: i["labels"].append(l)
    i["labels"] = [l for l in i["labels"] if l not in opt("--remove-label", True)]
    for l in opt("--add-assignee", True):
        l = "lan" if l == "@me" else l
        if l not in i["assignees"]: i["assignees"].append(l)
    if opt("--title"): i["title"] = opt("--title")
    if opt("--body") or opt("--body-file"): i["body"] = body()
    save(); print(f"https://github.com/quayside/billing/issues/{i['number']}")
elif a[:2] == ["issue", "comment"]:
    i = find(a[2]); i["comments"].append({"author": {"login": "lan"}, "body": body()}); save()
    print(f"https://github.com/quayside/billing/issues/{i['number']}#issuecomment-{len(i['comments'])}")
elif a[:2] == ["issue", "close"]:
    i = find(a[2]); i["state"] = "closed"; save(); print(f"✓ Closed issue #{i['number']}")
elif a[:2] == ["pr", "list"]:
    st = opt("--state") or "open"
    xs = [p for p in S["prs"] if st == "all" or p["state"] == st]
    j = opt("--json")
    if j is not None: print(json.dumps([{k: ({**p, "state": p["state"].upper()}).get(k) for k in j.split(",")} for p in xs]))
    else:
        for p in xs: print(f"{p['number']}\t{p['title']}\t{p['headRefName']}\t{p['state'].upper()}")
elif a[:2] == ["label", "list"]:
    for l in S["labels"]: print(l)
elif a[:2] == ["repo", "view"]:
    print("quayside/billing")
else:
    sys.exit(f"unknown command \"{' '.join(a[:2])}\" for \"gh\"")
E
chmod +x bin/gh
git add -A; ci "$(d 12)" "Berth invoices"
git branch dev; git checkout -q dev

feature() { git checkout -q -b "$1" dev; }

# --- PAY (#11) ---
feature feat/pay
mkdir -p docs/specs/pay
cat > docs/specs/pay/requirements.md <<'E'
# PAY — Record a payment
Status: Implemented

**PAY-1.1** WHEN a payment is recorded against an invoice, the system SHALL add it to the invoice and, once the invoice is paid in full, store its status as `paid`.
**PAY-1.2** IF the payment amount is not a number greater than zero, THEN the system SHALL reject it with status 400 and record nothing.
**PAY-1.3** IF the invoice does not exist, THEN the system SHALL answer 404.
E
cat > src/payments.js <<'E'
import { paidTotal } from "./invoice.js";
export function recordPayment(inv, amount) {
  if (amount < 0) { const e = new Error("amount must be greater than zero"); e.status = 400; throw e; }
  const share = inv.total / amount;            // used for the receipt line
  if (!Number.isFinite(share)) throw new Error("cannot compute receipt share");
  inv.payments.push({ id: `P-${inv.payments.length + 1}`, amount, refunded: false });
  if (paidTotal(inv) >= inv.total) inv.status = "paid";
  return inv;
}
E
python3 - <<'E'
p='src/api.js'; s=open(p).read()
s=s.replace('import { newInvoice } from "./invoice.js";','import { newInvoice } from "./invoice.js";\nimport { recordPayment } from "./payments.js";')
s=s.replace('};\n// handle','  "POST /payments": (b) => {\n    const inv = db.get(b.invoice);\n    if (!inv) { const e = new Error("no such invoice"); e.status = 404; throw e; }\n    return [201, recordPayment(inv, b.amount)];\n  },\n};\n// handle')
open(p,'w').write(s)
s=open('docs/specs/INDEX.md').read()+"| PAY | Record a payment | `docs/specs/pay/requirements.md` | Implemented |\n"
open('docs/specs/INDEX.md','w').write(s)
E
cat > test/payments.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { handle } from "../src/api.js";
test("a full payment marks the invoice paid", () => {
  handle("POST /invoices", { id: "P-A", total: 300 });
  const [s, inv] = handle("POST /payments", { invoice: "P-A", amount: 300 });
  assert.equal(s, 201); assert.equal(inv.status, "paid");
});
test("a part payment leaves it open", () => {
  handle("POST /invoices", { id: "P-B", total: 300 });
  assert.equal(handle("POST /payments", { invoice: "P-B", amount: 100 })[1].status, "open");
});
test("a negative amount is a 400", () => {
  handle("POST /invoices", { id: "P-C", total: 300 });
  assert.equal(handle("POST /payments", { invoice: "P-C", amount: -5 })[0], 400);
});
test("an unknown invoice is a 404", () => {
  assert.equal(handle("POST /payments", { invoice: "nope", amount: 5 })[0], 404);
});
E
git add -A; ci "$(d 6)" "Record payments against an invoice"
git checkout -q dev; mg "$(d 6)" feat/pay "Merge feat/pay: record a payment

Closes #11"

# --- LATEFEE (#12) ---
feature feat/late-fee
mkdir -p docs/specs/latefee
cat > docs/specs/latefee/requirements.md <<'E'
# LATEFEE — Late fees
Status: Implemented

**LATEFEE-1.1** WHILE an invoice is not paid in full, the system SHALL charge a late fee of 5 for each whole week past its due date.
**LATEFEE-1.2** WHILE an invoice is paid in full, the system SHALL charge no late fee.
E
cat > src/latefee.js <<'E'
const WEEK = 7 * 24 * 3600 * 1000;
export function lateFee(inv, due, today) {
  if (inv.status === "paid") return 0;
  const weeks = Math.floor((today - due) / WEEK);
  return weeks > 0 ? weeks * 5 : 0;
}
E
cat > test/latefee.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { newInvoice } from "../src/invoice.js"; import { lateFee } from "../src/latefee.js";
const due = Date.UTC(2026, 9, 1), later = Date.UTC(2026, 9, 16);
test("an open invoice two weeks late owes 10", () => { assert.equal(lateFee(newInvoice("L-A", 300), due, later), 10); });
test("a paid invoice owes nothing", () => { assert.equal(lateFee({ ...newInvoice("L-B", 300), status: "paid" }, due, later), 0); });
E
python3 - <<'E'
s=open('docs/specs/INDEX.md').read()+"| LATEFEE | Late fees | `docs/specs/latefee/requirements.md` | Implemented |\n"
open('docs/specs/INDEX.md','w').write(s)
E
git add -A; ci "$(d 4)" "Charge late fees on unpaid invoices"
git checkout -q dev; mg "$(d 4)" feat/late-fee "Merge feat/late-fee: late fees

Closes #12"

# --- REFUND (#13) ---
feature feat/refund
mkdir -p docs/specs/refund
cat > docs/specs/refund/requirements.md <<'E'
# REFUND — Refund a payment
Status: Implemented

**REFUND-1.1** WHEN a payment is refunded, the system SHALL mark that payment refunded and stop counting it toward the invoice.
**REFUND-1.2** WHEN every payment on an invoice has been refunded, the invoice SHALL read `refunded`.
**REFUND-1.3** IF the payment was already refunded, THEN the system SHALL answer 409.
E
cat > src/refunds.js <<'E'
export function refund(inv, paymentId) {
  const p = inv.payments.find((x) => x.id === paymentId);
  if (!p) { const e = new Error("no such payment"); e.status = 404; throw e; }
  if (p.refunded) { const e = new Error("already refunded"); e.status = 409; throw e; }
  p.refunded = true;
  return inv;
}
// What the portal shows. Derived on read; the stored status is not rewritten.
export function viewStatus(inv) {
  if (inv.payments.length && inv.payments.every((p) => p.refunded)) return "refunded";
  return inv.status;
}
E
python3 - <<'E'
p='src/api.js'; s=open(p).read()
s=s.replace('import { recordPayment } from "./payments.js";','import { recordPayment } from "./payments.js";\nimport { refund, viewStatus } from "./refunds.js";')
s=s.replace('};\n// handle','  "POST /refunds": (b) => {\n    const inv = db.get(b.invoice);\n    if (!inv) { const e = new Error("no such invoice"); e.status = 404; throw e; }\n    return [200, refund(inv, b.payment)];\n  },\n  "GET /invoice": (b) => {\n    const inv = db.get(b.invoice);\n    if (!inv) { const e = new Error("no such invoice"); e.status = 404; throw e; }\n    return [200, { ...inv, status: viewStatus(inv) }];\n  },\n};\n// handle')
open(p,'w').write(s)
s=open('docs/specs/INDEX.md').read()+"| REFUND | Refund a payment | `docs/specs/refund/requirements.md` | Implemented |\n"
open('docs/specs/INDEX.md','w').write(s)
E
cat > test/refunds.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { handle } from "../src/api.js";
test("refunding the only payment reads refunded", () => {
  handle("POST /invoices", { id: "R-A", total: 300 });
  handle("POST /payments", { invoice: "R-A", amount: 300 });
  handle("POST /refunds", { invoice: "R-A", payment: "P-1" });
  assert.equal(handle("GET /invoice", { invoice: "R-A" })[1].status, "refunded");
});
test("refunding twice is a 409", () => {
  handle("POST /invoices", { id: "R-B", total: 300 });
  handle("POST /payments", { invoice: "R-B", amount: 300 });
  handle("POST /refunds", { invoice: "R-B", payment: "P-1" });
  assert.equal(handle("POST /refunds", { invoice: "R-B", payment: "P-1" })[0], 409);
});
E
git add -A; ci "$(d 2)" "Refund a payment"
git checkout -q dev; mg "$(d 2)" feat/refund "Merge feat/refund: refund a payment

Closes #13"
git branch -q -D feat/pay feat/late-fee feat/refund

# --- tracker state ---
python3 - <<'E'
import json, os, subprocess
g = subprocess.run(["git","rev-parse","--git-dir"],capture_output=True,text=True).stdout.strip()
def iss(n, t, labels, state="closed", body=""):
    return {"number": n, "title": t, "body": body, "state": state, "labels": labels, "assignees": ["lan"], "comments": []}
S = {"labels": ["status:inbox","status:needs-info","status:ready","status:human","status:shaping","status:building","status:in-review","status:shipped","wontfix","bug","enhancement"],
     "prs": [],
     "issues": [
        iss(9, "Harbour master wants the month's invoices as a CSV", ["enhancement","status:inbox"], "open",
            "## Problem\nMinh re-types every invoice into his spreadsheet at month end.\n## Outcome\nNot decided yet\n## Acceptance\nNot decided yet\n## Out of scope\nNot decided yet\n"),
        *([iss(10, "A refunded invoice still reads paid and owes no late fee", ["bug","status:inbox"], "open",
            "## What happens\nPay an invoice in full, refund the payment: it shows refunded but its late fee is 0, and a part refund leaves it paid.\n## Expected\nA refunded invoice is owed again in full and is charged the late fee.\n## How to reproduce\nPay 300 on a 300 invoice, refund it, ask for the late fee two weeks past due.\n## Evidence\nReported by Minh, 12 Nov.\n")] if os.environ.get("DUP") else []),
        iss(11, "Record a payment against an invoice", ["enhancement"]),
        *([dict(iss(14, "Paying 0 on an invoice answers 500, not 400", ["bug","status:shaping"], "open",
            "## What happens\nA payment of 0 comes back as a 500 with \"cannot compute receipt share\".\n## Expected\nA 400, and nothing recorded.\n## How to reproduce\nPOST /payments with amount 0 on any open invoice.\n## Evidence\nSeen by Minh at the harbour office on 12 Nov.\n\n## Card\n- **Outcome:** a payment that is not above zero is refused with a 400.\n- **Examples:** Minh enters 0 on invoice B-7 (total 300) and sees \"amount must be greater than zero\"; Lan posts -5 and gets the same.\n- **Must keep:** a valid payment still records and marks the invoice paid when it covers the total.\n- **Off limits:** refunds and late fees.\n- **Decided:** the status is 400.\n- **Delegated:** none.\n- **Ask me:** anything that changes what an existing endpoint returns.\n- **UI:** none\n"),
            comments=[{"author": {"login": "lan"}, "body": "Tier 1 (bugfix). Neighbours: PAY. Open questions: none yet; the cause is not established."}])] if os.environ.get("SHAPE") else []),
        iss(12, "Charge a late fee on invoices past due", ["enhancement"]),
        iss(13, "Refund a payment", ["enhancement"]),
     ]}
json.dump(S, open(g + "/gh.json", "w"), indent=1)
E

# --- skills, where a consuming repo keeps them ---
mkdir -p .claude/skills
for s in "$@"; do
  src=$(find "$SK/skills" -mindepth 2 -maxdepth 2 -type d -name "$s" | head -1)
  cp -R "$src" ".claude/skills/$s"
  rm -f ".claude/skills/$s/TESTS.md" ".claude/skills/$s/eval.json"
done
printf '.claude/\n' >> .git/info/exclude
npm test >/dev/null 2>&1 && echo "built $T (tests green)" || { echo "TESTS RED"; exit 1; }
