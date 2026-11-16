#!/bin/bash
# make-tidewater.sh <target-dir> <skills-repo> [skill…]
# A small ferry-booking repo with a roadmap layer: MILE-1 closed on an accepted assessment,
# MILE-2, MILE-3 and MILE-4 committed with every member shipped in v0.3.0, MILE-5 planned.
# Installs the named skills in .claude/skills and the session's skill listing in .claude/skills/INDEX.md.
set -euo pipefail
T="$1"; SK="$2"; shift 2
mkdir -p "$T"; cd "$T"
git init -q -b main
git config core.fsmonitor false; git config tag.gpgsign false; git config commit.gpgsign false
git config user.name "Mai Tran"; git config user.email "mai@tidewater.example"
d() { date -u -v-"$1"d +%Y-%m-%dT09:00:00Z; }
ci() { git add -A; GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git commit -q -m "$2"; }

mkdir -p src test docs/agents docs/product docs/roadmap/assessments docs/specs
cat > package.json <<'E'
{ "name": "tidewater", "private": true, "type": "module", "scripts": { "test": "node --test" } }
E
cat > docs/agents/project.md <<'E'
# Project

- Verify: `npm test`
- Default PR base: main
- Default landing action: merge
- Team: Mai Tran (owner, approves specs, roadmaps and milestone closes)
E
cat > docs/product/vision.md <<'E'
# Vision: Tidewater

Foot passengers on the Ness Point ferry book and manage their own crossings, and the
operator sees how full each sailing is before it leaves.

## Goals

- **GOAL-1** A passenger books and pays for a crossing without calling the office
- **GOAL-2** A passenger changes or cancels their own booking
- **GOAL-3** The operator sees each sailing's load the day before
E

feature() { # code name road slug body…
  local c=$1 n=$2 r=$3 s=$4; shift 4
  mkdir -p "docs/specs/$s"
  { echo "# Requirements: $n"; echo; echo "Status: Shipped"; echo "Roadmap item: $r"; echo; printf '%s\n' "$@"; } > "docs/specs/$s/requirements.md"
}
cat > docs/specs/INDEX.md <<'E'
# Spec Index

| Code | Feature | Spec | Status | Roadmap item |
|---|---|---|---|---|
E
row() { echo "| $1 | $2 | \`docs/specs/$3/requirements.md\` | Shipped | $4 |" >> docs/specs/INDEX.md; }

# --- MILE-1: book and pay ---
cat > src/booking.js <<'E'
export const sailings = new Map([["NP-0715", { seats: 40, booked: [] }], ["NP-1230", { seats: 40, booked: [] }]]);
export function book(sailing, name, card) {
  const s = sailings.get(sailing);
  if (!s) throw Object.assign(new Error("no such sailing"), { status: 404 });
  if (!card || card.length < 12) throw Object.assign(new Error("card declined"), { status: 402 });
  if (s.booked.length >= s.seats) throw Object.assign(new Error("sailing full"), { status: 409 });
  const ref = `${sailing}-${s.booked.length + 1}`;
  s.booked.push({ ref, name, seat: null, cancelled: false });
  return ref;
}
E
cat > test/booking.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { book } from "../src/booking.js";
test("books a seat and returns a reference", () => { assert.match(book("NP-0715", "Ana", "4111111111111111"), /^NP-0715-/); });
test("refuses a declined card", () => { assert.throws(() => book("NP-0715", "Ana", "1"), /declined/); });
E
feature BOOK "Book a crossing" ROAD-1 book \
  "**BOOK-1.1** WHEN a passenger picks a sailing with a free seat THE SYSTEM SHALL book it and return a reference."
feature PAYCARD "Pay by card" ROAD-2 paycard \
  "**PAYCARD-1.1** WHEN the card is declined THE SYSTEM SHALL refuse the booking with 402."
row BOOK "Book a crossing" book ROAD-1; row PAYCARD "Pay by card" paycard ROAD-2

cat > docs/roadmap/INDEX.md <<'E'
# Roadmap: Tidewater

Status: Approved
Date: DATE0

## Focus

**Now:** MILE-2, MILE-3
**Next:** MILE-4

| ID | Milestone | Depends-on | Commitment |
|---|---|---|---|
| MILE-1 | Book online | none | Closed |
| MILE-2 | Choose your seat | MILE-1 | Planned |
| MILE-3 | Manage my booking | MILE-1 | Planned |
| MILE-4 | Sailing load | MILE-1 | Planned |
| MILE-5 | Season pass | MILE-3 | Planned |

## MILE-1 — Book online

**Outcome:** A passenger books and pays for a crossing on the website without calling the office.
**Goals:** GOAL-1
**Members:**
- **ROAD-1** book-crossing — After: none — Surfaces: `src/booking.js`
- **ROAD-2** pay-by-card — After: ROAD-1 — Surfaces: `src/booking.js`
**Depends-on:** none
**Commitment:** Closed DATE0
**Closed:** CLOSED1
**Deferred:** None
**Blockers:** None

## MILE-2 — Choose your seat

**Outcome:** A passenger picks their own seat when booking and gets an email confirming it.
**Goals:** GOAL-1
**Members:**
- **ROAD-3** seat-map — After: MILE-1 — Surfaces: `src/seats.js`
- **ROAD-4** booking-email — After: ROAD-3 — Surfaces: `src/mail.js`
**Depends-on:** MILE-1
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## MILE-3 — Manage my booking

**Outcome:** A passenger cancels or moves their own booking to another sailing from the confirmation link.
**Goals:** GOAL-2
**Members:**
- **ROAD-5** cancel-booking — After: MILE-1 — Surfaces: `src/manage.js`
- **ROAD-6** change-sailing — After: ROAD-5 — Surfaces: `src/manage.js`
**Depends-on:** MILE-1
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## MILE-4 — Sailing load

**Outcome:** The operator opens one page the day before and sees how many seats each sailing has booked.
**Goals:** GOAL-3
**Members:**
- **ROAD-7** load-report — After: MILE-1 — Surfaces: `src/load.js`
**Depends-on:** MILE-1
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## MILE-5 — Season pass

**Outcome:** A regular passenger buys a season pass once and books any crossing with it.
**Goals:** GOAL-1
**Members:**
- **ROAD-8** season-pass — After: MILE-3 — Surfaces: None — the pass model is not designed yet
**Depends-on:** MILE-3
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## Goal dispositions

| Goal | Disposition | Date | Reason |
|---|---|---|---|
E
sed -i '' "s/DATE0/$(date -u -v-60d +%Y-%m-%d)/g; s/CLOSED1/None/" docs/roadmap/INDEX.md
ci "$(d 60)" "feat: book and pay for a crossing (BOOK, PAYCARD)"
git tag -m "v0.1.0" v0.1.0
sed -i '' "s/^\*\*Closed:\*\* None$/**Closed:** $(git rev-parse HEAD)/" docs/roadmap/INDEX.md  # first Closed line is MILE-1's
python3 - <<'Q'
p = "docs/roadmap/INDEX.md"; s = open(p).read(); i = s.index("## MILE-2 ")
open(p, "w").write(s[:i] + s[i:].replace(s[:i].split("**Closed:** ")[1].split("\n")[0], "None"))
Q
ci "$(d 59)" "docs(roadmap): close MILE-1 at v0.1.0"

# Commit MILE-2, 3, 4 — one commit each, so each Committed line has its own pickaxe commit.
for m in 2 3 4; do
  python3 - "$m" "$(date -u -v-$((50 - m))d +%Y-%m-%d)" <<'P'
import sys, re
m, day = sys.argv[1], sys.argv[2]
p = "docs/roadmap/INDEX.md"; s = open(p).read()
s = re.sub(rf"(\| MILE-{m} \|[^\n]*\| )Planned \|", r"\1Committed |", s)
blk = s.index(f"## MILE-{m} ")
nxt = s.index("**Commitment:** Planned", blk)
s = s[:nxt] + f"**Commitment:** Committed {day}" + s[nxt + len("**Commitment:** Planned"):]
open(p, "w").write(s)
P
  ci "$(d $((50 - m)))" "docs(roadmap): commit MILE-$m"
done

# --- MILE-2: seats + email ---
cat > src/seats.js <<'E'
import { sailings } from "./booking.js";
export function chooseSeat(ref, seat) {
  const [sailing] = ref.split(/-(?=\d+$)/);
  const s = sailings.get(sailing); const b = s?.booked.find((x) => x.ref === ref);
  if (!b) throw Object.assign(new Error("no such booking"), { status: 404 });
  if (seat < 1 || seat > s.seats) throw Object.assign(new Error("no such seat"), { status: 400 });
  if (s.booked.some((x) => x.seat === seat && !x.cancelled)) throw Object.assign(new Error("seat taken"), { status: 409 });
  b.seat = seat; return b;
}
E
cat > src/mail.js <<'E'
export const outbox = [];
export function confirm(b, to) { outbox.push({ to, subject: `Booking ${b.ref}`, body: `Seat ${b.seat}. Manage: https://tidewater.example/b/${b.ref}` }); }
E
cat > test/seats.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { book } from "../src/booking.js"; import { chooseSeat } from "../src/seats.js"; import { confirm, outbox } from "../src/mail.js";
test("a passenger picks a free seat and is emailed", () => {
  const b = chooseSeat(book("NP-1230", "Ben", "4111111111111111"), 7); confirm(b, "ben@example.com");
  assert.equal(b.seat, 7); assert.match(outbox.at(-1).body, /Seat 7/);
});
test("a taken seat is refused", () => {
  const r = book("NP-1230", "Cy", "4111111111111111"); assert.throws(() => chooseSeat(r, 7), /taken/);
});
E
feature SEAT "Choose a seat" ROAD-3 seat "**SEAT-1.1** WHEN a passenger picks a free seat THE SYSTEM SHALL assign it to the booking."
feature MAIL "Booking email" ROAD-4 mail "**MAIL-1.1** WHEN a seat is assigned THE SYSTEM SHALL email the booking reference, the seat and a manage link."
row SEAT "Choose a seat" seat ROAD-3; row MAIL "Booking email" mail ROAD-4
ci "$(d 30)" "feat: seat map and booking email (SEAT, MAIL)"

# --- MILE-3: cancel + move ---
cat > src/manage.js <<'E'
import { sailings } from "./booking.js";
function find(ref) { for (const s of sailings.values()) { const b = s.booked.find((x) => x.ref === ref); if (b) return b; } }
export function cancel(ref) { const b = find(ref); if (!b) throw Object.assign(new Error("no such booking"), { status: 404 }); b.cancelled = true; b.seat = null; return b; }
export function move(ref, to) {
  const b = find(ref); const t = sailings.get(to);
  if (!b || !t) throw Object.assign(new Error("not found"), { status: 404 });
  if (t.booked.filter((x) => !x.cancelled).length >= t.seats) throw Object.assign(new Error("sailing full"), { status: 409 });
  b.cancelled = true; const nb = { ...b, ref: `${to}-${t.booked.length + 1}`, seat: null, cancelled: false }; t.booked.push(nb); return nb;
}
E
cat > test/manage.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { book } from "../src/booking.js"; import { cancel, move } from "../src/manage.js";
test("a passenger cancels their booking", () => { assert.equal(cancel(book("NP-0715", "Di", "4111111111111111")).cancelled, true); });
test("a passenger moves to another sailing", () => { assert.match(move(book("NP-0715", "Ed", "4111111111111111"), "NP-1230").ref, /^NP-1230-/); });
E
feature CANCEL "Cancel a booking" ROAD-5 cancel "**CANCEL-1.1** WHEN a passenger cancels from the manage link THE SYSTEM SHALL cancel the booking and free its seat."
feature MOVE "Change sailing" ROAD-6 move "**MOVE-1.1** WHEN a passenger moves to a sailing with room THE SYSTEM SHALL rebook them on it and cancel the old booking."
row CANCEL "Cancel a booking" cancel ROAD-5; row MOVE "Change sailing" move ROAD-6
ci "$(d 20)" "feat: cancel and change sailing (CANCEL, MOVE)"

# --- MILE-4: load report ---
cat > src/load.js <<'E'
import { sailings } from "./booking.js";
export function load() { return [...sailings].map(([id, s]) => ({ id, booked: s.booked.filter((b) => !b.cancelled).length, seats: s.seats })); }
E
cat > test/load.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { load } from "../src/load.js";
test("lists every sailing with its booked count", () => { const l = load(); assert.equal(l.length, 2); assert.ok(l.every((x) => x.seats === 40)); });
E
feature LOAD "Sailing load" ROAD-7 load "**LOAD-1.1** WHEN the operator opens the load page THE SYSTEM SHALL list every sailing with its booked and total seats."
row LOAD "Sailing load" load ROAD-7
ci "$(d 12)" "feat: sailing load page (LOAD)"
GIT_AUTHOR_DATE="$(d 10)" GIT_COMMITTER_DATE="$(d 10)" git commit -q --allow-empty -m "chore: release v0.3.0"
git tag -m "v0.3.0" v0.3.0

# --- skills, where a consuming repo keeps them ---
mkdir -p .claude/skills
for s in "$@"; do
  src=$(find "$SK/skills" -mindepth 2 -maxdepth 2 -type d -name "$s" | head -1)
  cp -R "$src" ".claude/skills/$s"
  rm -f ".claude/skills/$s/TESTS.md" ".claude/skills/$s/eval.json"
done
(cd "$SK" && python3 scripts/skill-tests/routing/listing.py --out "$T/.claude/skills/INDEX.md" 2>/dev/null)
printf '.claude/\n' >> .git/info/exclude
npm test >/dev/null 2>&1 && echo "built $T (tests green)" || { echo "TESTS RED"; exit 1; }
