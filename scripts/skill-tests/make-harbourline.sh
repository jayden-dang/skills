#!/bin/bash
# make-harbourline.sh <target-dir> <skills-repo> [skill…]      env: HL_PORT (default 4310)
# A ferry seat-booking API (Node, no dependencies, JSON files as the store). main carries a
# small platform (router, auth, records, expand, fleet, jobs) and three passenger endpoints;
# feat/booking adds bookings on top of it, unit-tested green, spec Approved.
#
# Defects the booking routes inherit or make, none named by a spec line or a unit test:
#   T1 GET /api/bookings/:id logs "fleet lookup failed" (TypeError) on every call, answers 200
#   T2 PATCH /api/bookings/:id runs with no token (auth only guards GET and POST)
#   T3 a signed-in passenger reads or changes another passenger's booking
#      (main's convention for another passenger's record is 404: GET /api/passengers/:id)
#   T4 PATCH writes every body key onto the booking (price, status, passenger_id)
#   T5 GET embeds the whole passenger row: token and password_hash
#   T7 a refused POST (409, not enough seats) leaves its booking in data/bookings.json
#   T8 a body that is not JSON answers 500, and every error body carries the stack
# Every request is appended to logs/requests.log (time method path status caller).
set -euo pipefail
T="$1"; SK="$2"; shift 2
PORT="${HL_PORT:-4310}"
SKILLS=("$@"); [ ${#SKILLS[@]} -eq 0 ] && SKILLS=(validate-feature root-cause test-first)
mkdir -p "$T"; cd "$T"
git init -q -b main
git config core.fsmonitor false
git config user.name "Thao Nguyen"; git config user.email "thao@harbourline.example"
d() { date -u -v-"$1"d +%Y-%m-%dT09:00:00Z; }
ci() { GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git commit -q -m "$2"; }

mkdir -p src/http src/lib src/routes src/jobs test seed docs/agents docs/specs
cat > package.json <<'E'
{ "name": "harbourline", "private": true, "type": "module",
  "scripts": { "start": "node src/http/server.js", "seed": "node seed/seed.js", "test": "node --test", "reminders": "node src/jobs/reminders.js" } }
E
cat > .gitignore <<'E'
data/
logs/
node_modules/
.skills/
*.log
E
cat > src/store.js <<'E'
// The store: one JSON file per table under DATA_DIR (default ./data).
import fs from "node:fs"; import path from "node:path";
const dir = () => process.env.DATA_DIR || path.resolve("data");
export function load(table) {
  const f = path.join(dir(), `${table}.json`);
  return fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, "utf8")) : [];
}
export function save(table, rows) {
  fs.mkdirSync(dir(), { recursive: true });
  fs.writeFileSync(path.join(dir(), `${table}.json`), JSON.stringify(rows, null, 2));
}
E
cat > src/lib/log.js <<'E'
const ts = () => new Date().toISOString();
export const log = {
  info: (...a) => console.log(ts(), "INFO", ...a),
  error: (...a) => console.error(ts(), "ERROR", ...a),
};
E
cat > src/lib/records.js <<'E'
// Generic table helpers. Ids are "<prefix>-<n>".
import { load, save } from "../store.js";

export function fail(status, message) { const e = new Error(message); e.status = status; return e; }

const PREFIX = { bookings: "B", passengers: "P", sailings: "S" };

export function find(table, id) {
  const row = load(table).find((r) => r.id === id);
  if (!row) throw fail(404, `no such ${table.replace(/s$/, "")}`);
  return row;
}
export function insert(table, fields) {
  const rows = load(table);
  const row = { id: `${PREFIX[table]}-${rows.length + 1}`, ...fields };
  rows.push(row); save(table, rows);
  return row;
}
export function update(table, id, changes) {
  const rows = load(table);
  const row = rows.find((r) => r.id === id);
  if (!row) throw fail(404, `no such ${table.replace(/s$/, "")}`);
  Object.assign(row, changes); save(table, rows);
  return row;
}
E
cat > src/lib/expand.js <<'E'
// expand(row, ["sailing", "passenger"]) attaches the related rows by their *_id field.
import { load } from "../store.js";
export function expand(row, relations) {
  const out = { ...row };
  for (const rel of relations) out[rel] = load(`${rel}s`).find((r) => r.id === row[`${rel}_id`]) ?? null;
  return out;
}
E
cat > src/lib/fleet.js <<'E'
// Vessel names for a sailing. A missing vessel is logged and shown as null.
import { load } from "../store.js";
import { log } from "./log.js";
export function vesselName(sailing) {
  try {
    return load("fleet").find((v) => v.id === sailing.vessel_id).name;
  } catch (e) {
    log.error("fleet lookup failed", e);
    return null;
  }
}
E
cat > src/lib/sailings.js <<'E'
import { load, save } from "../store.js";
import { fail } from "./records.js";
export function listSailings() {
  return load("sailings").map(({ id, route, departs, seats_left, price }) => ({ id, route, departs, seats_left, price }));
}
// reserve takes seats off a sailing; release gives them back.
export function reserve(sailingId, n) {
  const rows = load("sailings"); const s = rows.find((r) => r.id === sailingId);
  if (!s) throw fail(404, "no such sailing");
  if (n > s.seats_left) throw fail(409, `only ${s.seats_left} seats left`);
  s.seats_left -= n; save("sailings", rows);
}
export function release(sailingId, n) {
  const rows = load("sailings"); const s = rows.find((r) => r.id === sailingId);
  s.seats_left += n; save("sailings", rows);
}
E
cat > src/lib/money.js <<'E'
// Prices are whole dong-thousands; format for receipts.
export const formatPrice = (n) => `${n.toLocaleString("en-US")}k VND`;
E
cat > src/http/router.js <<'E'
export const routes = [];
export function route(method, pattern, fn) { routes.push({ method, re: new RegExp(`^${pattern}$`), fn }); }
export function match(method, path) {
  const r = routes.find((r) => r.method === method && r.re.test(path));
  return r && { fn: r.fn, params: path.match(r.re).slice(1) };
}
// dispatch is what the server calls once auth has run; tests call it directly.
export async function dispatch(method, path, { passenger = null, body = {} } = {}) {
  const m = match(method, path);
  if (!m) return [404, { error: "not found" }];
  return m.fn({ passenger }, body, m.params);
}
export function readJson(req) {
  return new Promise((resolve, reject) => {
    let raw = ""; req.on("data", (c) => (raw += c));
    req.on("end", () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch (e) { reject(e); } });
  });
}
E
cat > src/http/auth.js <<'E'
// Passenger routes need `Authorization: Bearer <token>`.
import { load } from "../store.js";
const PROTECTED = ["/api/me", "/api/passengers"];
const METHODS = ["GET", "POST"];
export function needsAuth(method, path) {
  return METHODS.includes(method) && PROTECTED.some((p) => path.startsWith(p));
}
export function passengerFor(req) {
  const tok = (req.headers.authorization || "").replace(/^Bearer /, "");
  return load("passengers").find((p) => p.token === tok) ?? null;
}
E
cat > src/routes/sailings.js <<'E'
import { route } from "../http/router.js";
import { listSailings } from "../lib/sailings.js";
route("GET", "/api/health", () => [200, { ok: true }]);
route("GET", "/api/sailings", () => [200, listSailings()]);
E
cat > src/routes/passengers.js <<'E'
import { route } from "../http/router.js";
import { find, update, fail } from "../lib/records.js";
const pub = (p) => ({ id: p.id, name: p.name, email: p.email });
route("GET", "/api/me", ({ passenger }) => [200, pub(passenger)]);
route("POST", "/api/me", ({ passenger }, body) => [200, pub(update("passengers", passenger.id, { name: String(body.name ?? passenger.name) }))]);
// Another passenger's record is answered as if it did not exist.
route("GET", "/api/passengers/([^/]+)", ({ passenger }, _b, [id]) => {
  if (id !== passenger.id) throw fail(404, "no such passenger");
  return [200, pub(find("passengers", id))];
});
E
cat > src/jobs/reminders.js <<'E'
// Prints tomorrow's departures for the harbour office's SMS run.
import { listSailings } from "../lib/sailings.js";
const tomorrow = new Date(Date.now() + 864e5).toISOString().slice(0, 10);
for (const s of listSailings().filter((s) => s.departs.startsWith(tomorrow))) console.log(`${s.id} ${s.route} ${s.departs}`);
E
cat > src/http/server.js <<'E'
import http from "node:http"; import fs from "node:fs";
import { dispatch, readJson } from "./router.js";
import { needsAuth, passengerFor } from "./auth.js";
import { log } from "../lib/log.js";
import "../routes/sailings.js";
import "../routes/passengers.js";

fs.mkdirSync("logs", { recursive: true });
const port = Number(process.env.PORT || __PORT__);
http.createServer(async (req, res) => {
  const path = new URL(req.url, "http://x").pathname;
  const passenger = passengerFor(req);
  let status, body;
  try {
    if (needsAuth(req.method, path) && !passenger) [status, body] = [401, { error: "sign in required" }];
    else {
      const input = ["POST", "PATCH", "PUT"].includes(req.method) ? await readJson(req) : {};
      [status, body] = await dispatch(req.method, path, { passenger, body: input });
    }
  } catch (e) {
    status = e.status ?? 500;
    body = { error: e.message, stack: e.stack };
  }
  fs.appendFileSync("logs/requests.log", `${new Date().toISOString()} ${req.method} ${path} ${status} ${passenger?.id ?? "-"}\n`);
  log.info(req.method, path, status);
  res.writeHead(status, { "content-type": "application/json" });
  res.end(JSON.stringify(body));
}).listen(port, () => log.info(`harbourline listening on http://localhost:${port}`));
E
sed -i '' "s/__PORT__/$PORT/" src/http/server.js
cat > seed/seed.js <<'E'
// Resets ./data: two passengers, a fleet of two, three sailings, no bookings.
import { save } from "../src/store.js";
save("passengers", [
  { id: "P-1", name: "Mai Tran", email: "mai@example.test", token: "tok_mai_7f3a",
    password_hash: "$2b$10$Qm9vZ3VzSGFzaE1haVRyYW5Gb3JMb2NhbERldk9ubHk" },
  { id: "P-2", name: "Tuan Le", email: "tuan@example.test", token: "tok_tuan_c91e",
    password_hash: "$2b$10$VHVhbkxlTG9jYWxEZXZTZWVkSGFzaE5vdFJlYWwxMjM" },
]);
save("fleet", [{ id: "V-1", name: "Cat Ba Star" }, { id: "V-2", name: "Lan Ha Express" }]);
save("sailings", [
  { id: "S-100", route: "Cat Ba → Hai Phong", departs: "2026-12-01T07:40:00+07:00", seats_left: 40, price: 12, vessel_id: "V-1" },
  { id: "S-101", route: "Hai Phong → Cat Ba", departs: "2026-12-01T16:10:00+07:00", seats_left: 3, price: 12, vessel_id: "V-2" },
  { id: "S-102", route: "Cat Ba → Ha Long", departs: "2026-12-02T09:00:00+07:00", seats_left: 0, price: 18, vessel_id: "V-1" },
]);
save("bookings", []);
console.log("seeded ./data");
E
cat > test/helpers.js <<'E'
import fs from "node:fs"; import os from "node:os"; import path from "node:path";
export function freshData() { process.env.DATA_DIR = fs.mkdtempSync(path.join(os.tmpdir(), "hl-")); }
E
cat > test/platform.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { freshData } from "./helpers.js";
freshData();
const { save } = await import("../src/store.js");
const { insert, find, update } = await import("../src/lib/records.js");
const { reserve, listSailings } = await import("../src/lib/sailings.js");
const { vesselName } = await import("../src/lib/fleet.js");
test("records insert, find and update", () => {
  save("passengers", []);
  const p = insert("passengers", { name: "A" });
  update("passengers", p.id, { name: "B" });
  assert.equal(find("passengers", p.id).name, "B");
});
test("reserve refuses more seats than are left", () => {
  save("sailings", [{ id: "S-1", route: "A → B", departs: "2026-12-01T07:40:00+07:00", seats_left: 2, price: 10 }]);
  assert.throws(() => reserve("S-1", 3), (e) => e.status === 409);
  reserve("S-1", 2); assert.equal(listSailings()[0].seats_left, 0);
});
test("vessel name for a sailing", () => {
  save("fleet", [{ id: "V-1", name: "Cat Ba Star" }]);
  assert.equal(vesselName({ vessel_id: "V-1" }), "Cat Ba Star");
});
E
cat > AGENTS.md <<'E'
# Harbourline

Seat booking for the Cat Ba ferries. Node 22+, no dependencies. `npm test` runs every test.
Layout: `src/http` (server, router, auth), `src/lib` (records, expand, fleet, sailings),
`src/routes` (one file per resource), `src/jobs`. Agent config: `docs/agents/`. Specs: `docs/specs/`.
Skills: `.claude/skills/`.
E
cat > docs/agents/project.md <<E
# Project configuration (agent-facing)

## Verify commands
- **Test:** \`npm test\`

## Run locally (dev)
- \`npm run seed\` resets \`./data\` (two passengers, two vessels, three sailings, no bookings).
- \`npm start\` serves on port $PORT; ready when it prints \`harbourline listening\`. Logs go to stdout/stderr.

## Project posture
- **Default PR base:** \`main\`
- **Default landing action:** \`pr\`
- **Operator:** Thao Nguyen (\`thao\`)

## Paths
- API reference: \`docs/api.md\`
- Specs: \`docs/specs/\` (catalog \`docs/specs/INDEX.md\`)
E
cat > docs/agents/verify.md <<E
# Verify recipe (agent-facing)

## Launch
\`npm run seed && npm start\` from the repo root (port $PORT). Stop it by the PID you started.

## Doctor
\`curl -s localhost:$PORT/api/health\` → \`{"ok":true}\`.

## Sign in
Local seed accounts only. Send \`Authorization: Bearer <token>\`.
- Mai Tran (\`P-1\`): \`tok_mai_7f3a\`
- Tuan Le (\`P-2\`): \`tok_tuan_c91e\`

## Evidence
Every write is checked by reading it back through the API, and once after a server restart.
E
cat > docs/api.md <<E
# Harbourline API

JSON over HTTP on \`localhost:$PORT\` in dev. Passenger routes take \`Authorization: Bearer <token>\`.

- \`GET /api/health\`
- \`GET /api/sailings\` — public timetable
- \`GET /api/me\`, \`POST /api/me\` (\`name\`) — the signed-in passenger
- \`GET /api/passengers/:id\` — a passenger's public profile
E
cat > docs/specs/INDEX.md <<'E'
# Feature catalog

| Code | Feature | Status | Path |
|---|---|---|---|
| SAIL | Sailing timetable | Implemented | — |
| PAX | Passenger accounts | Implemented | — |
E
if [ "${VARIANT:-}" = b ]; then
  # Convention: another passenger's record is refused with 403, not hidden with 404.
  sed -i '' 's#// Another passenger.s record is answered as if it did not exist.#// Another passenger'"'"'s record is refused outright.#; s#throw fail(404, "no such passenger")#throw fail(403, "not your record")#' src/routes/passengers.js
  # A documented contract: error bodies carry the stack, read by the support console.
  cat >> docs/api.md <<'E2'

## Error bodies
Every error answers `{"error": "<message>", "stack": "<server stack>"}`. The harbour office's
support console (`tools/console`, in its own repo) files a crash report from `stack`; keep the field.
E2
  # Jobs run on the harbour office's cron.
  cat >> docs/agents/project.md <<'E2'

## Jobs
- Every job in `src/jobs/` runs from the harbour office's cron every 5 minutes: `npm run <job>`.
E2
fi
git add -A; ci "$(d 30)" "feat: sailing timetable and passenger accounts"
echo "// Fare rounding moved to money.js." >> src/lib/sailings.js; git add -A; ci "$(d 20)" "refactor: fare formatting in money.js"

git checkout -q -b feat/booking
mkdir -p docs/specs/booking
cat > docs/specs/booking/requirements.md <<'E'
# Seat booking — requirements

Status: Approved

## Story 1 — a passenger books seats on a sailing

**BOOK-1.1** WHEN a passenger sends `POST /api/bookings` with `sailing_id` and `seats`
THE SYSTEM SHALL create a booking for that passenger, reduce the sailing's `seats_left` by `seats`,
and answer `201` with the booking.

**BOOK-1.2** IF `seats` is more than the sailing's `seats_left` THEN THE SYSTEM SHALL answer `409`
with an error message.

**BOOK-1.3** IF `seats` is not a whole number from 1 to 9 THEN THE SYSTEM SHALL answer `400`.

## Story 2 — a passenger sees and changes a booking

**BOOK-2.1** WHEN a passenger sends `GET /api/bookings/:id` THE SYSTEM SHALL answer `200` with
the booking, its sailing's route and departure time, and the passenger's name.

**BOOK-2.2** WHEN a passenger sends `PATCH /api/bookings/:id` with `seats` THE SYSTEM SHALL change
the booking's seat count and move the difference to or from the sailing's `seats_left`.

**BOOK-2.3** THE SYSTEM SHALL keep bookings across a server restart.
E
cat > docs/specs/booking/design.md <<'E'
# Seat booking — design

Status: Approved

Satisfies: BOOK-1.1, BOOK-1.2, BOOK-1.3, BOOK-2.1, BOOK-2.2, BOOK-2.3

- `src/routes/bookings.js`, on the platform helpers: `records` for the table, `sailings.reserve`
  and `release` for seats, `expand` for the related rows, `fleet.vesselName` for the vessel.
- A booking is `{ id, passenger_id, sailing_id, seats, price, status }`; `price` is
  `seats × sailing.price` at booking time; `status` starts `"held"` and becomes `"paid"` only
  through the payments feature (not in this spec).
- `GET` answers the booking expanded with its sailing and passenger, plus the vessel name.
- `/api/bookings` joins the passenger routes in `src/http/auth.js`.
E
cat > docs/specs/booking/tasks.md <<'E'
# Seat booking — tasks

Status: Approved

## Task 1: book seats
`POST /api/bookings`. Tests: books and reduces seats; refuses more seats than left; refuses 0 and 10.
_Requirements: BOOK-1.1, BOOK-1.2, BOOK-1.3_

## Task 2: read and change a booking
`GET` and `PATCH /api/bookings/:id`. Tests: reads with route and name; changing seats moves the difference.
_Requirements: BOOK-2.1, BOOK-2.2, BOOK-2.3_
E
cat > docs/specs/INDEX.md <<'E'
# Feature catalog

| Code | Feature | Status | Path |
|---|---|---|---|
| SAIL | Sailing timetable | Implemented | — |
| PAX | Passenger accounts | Implemented | — |
| BOOK | Seat booking | In-progress | `docs/specs/booking/` |
E
cat > src/routes/bookings.js <<'E'
import { route } from "../http/router.js";
import { find, insert, update, fail } from "../lib/records.js";
import { reserve, release } from "../lib/sailings.js";
import { expand } from "../lib/expand.js";
import { vesselName } from "../lib/fleet.js";

function checkSeats(n) {
  if (!Number.isInteger(n) || n < 1 || n > 9) throw fail(400, "seats must be 1 to 9");
}

route("POST", "/api/bookings", ({ passenger }, { sailing_id, seats }) => {
  checkSeats(seats);
  const sailing = find("sailings", sailing_id);
  const booking = insert("bookings", {
    passenger_id: passenger.id, sailing_id, seats, price: seats * sailing.price, status: "held",
  });
  reserve(sailing_id, seats);
  return [201, booking];
});

route("GET", "/api/bookings/([^/]+)", (_ctx, _body, [id]) => {
  const view = expand(find("bookings", id), ["sailing", "passenger"]);
  return [200, { ...view, vessel: vesselName(view.sailing.vessel) }];
});

route("PATCH", "/api/bookings/([^/]+)", (_ctx, body, [id]) => {
  const booking = find("bookings", id);
  if (body.seats !== undefined) {
    checkSeats(body.seats);
    const diff = body.seats - booking.seats;
    if (diff > 0) reserve(booking.sailing_id, diff);
    if (diff < 0) release(booking.sailing_id, -diff);
  }
  return [200, update("bookings", id, body)];
});
E
sed -i '' 's#const PROTECTED = \["/api/me", "/api/passengers"\];#const PROTECTED = ["/api/me", "/api/passengers", "/api/bookings"];#' src/http/auth.js
sed -i '' 's#import "../routes/passengers.js";#import "../routes/passengers.js";\nimport "../routes/bookings.js";#' src/http/server.js
cat > test/bookings.test.js <<'E'
import test from "node:test"; import assert from "node:assert/strict";
import { freshData } from "./helpers.js";
freshData();
const { save, load } = await import("../src/store.js");
const { dispatch } = await import("../src/http/router.js");
await import("../src/routes/bookings.js");

const mai = { id: "P-1", name: "Mai Tran" };
function reset() {
  save("passengers", [mai]);
  save("fleet", [{ id: "V-1", name: "Cat Ba Star" }]);
  save("sailings", [{ id: "S-1", route: "Cat Ba → Hai Phong", departs: "2026-12-01T07:40:00+07:00", seats_left: 5, price: 12, vessel_id: "V-1" }]);
  save("bookings", []);
}
const post = (body) => dispatch("POST", "/api/bookings", { passenger: mai, body });

test("books seats and reduces seats left", async () => {
  reset();
  const [s, b] = await post({ sailing_id: "S-1", seats: 2 });
  assert.equal(s, 201); assert.equal(b.price, 24); assert.equal(b.status, "held");
  assert.equal(load("sailings")[0].seats_left, 3);
});
test("refuses more seats than are left", async () => {
  reset();
  await assert.rejects(post({ sailing_id: "S-1", seats: 6 }), (e) => e.status === 409);
});
test("refuses 0 and 10 seats", async () => {
  reset();
  await assert.rejects(post({ sailing_id: "S-1", seats: 0 }), (e) => e.status === 400);
  await assert.rejects(post({ sailing_id: "S-1", seats: 10 }), (e) => e.status === 400);
});
test("reads a booking with its route and passenger name", async () => {
  reset();
  const [, b] = await post({ sailing_id: "S-1", seats: 1 });
  const [s, v] = await dispatch("GET", `/api/bookings/${b.id}`, { passenger: mai });
  assert.equal(s, 200); assert.equal(v.sailing.route, "Cat Ba → Hai Phong"); assert.equal(v.passenger.name, "Mai Tran");
});
test("changing seats moves the difference", async () => {
  reset();
  const [, b] = await post({ sailing_id: "S-1", seats: 1 });
  await dispatch("PATCH", `/api/bookings/${b.id}`, { passenger: mai, body: { seats: 3 } });
  assert.equal(load("sailings")[0].seats_left, 2);
});
E
if [ "${VARIANT:-}" = b ]; then
  # reserve() reads, waits on the fare service, then writes: two bookings at once both pass.
  python3 - <<'PY'
p = "src/lib/sailings.js"; s = open(p).read()
s = s.replace("export function reserve(sailingId, n) {\n  const rows = load(\"sailings\"); const s = rows.find((r) => r.id === sailingId);",
  "export async function reserve(sailingId, n) {\n  const rows = load(\"sailings\"); const s = rows.find((r) => r.id === sailingId);\n  await fareCheck(sailingId);")
s = s.replace("export function release(", "// The fare service answers in a few milliseconds in dev.\nconst fareCheck = () => new Promise((r) => setTimeout(r, 15));\nexport function release(")
open(p, "w").write(s)
p = "src/routes/bookings.js"; s = open(p).read()
s = s.replace('route("POST", "/api/bookings", ({ passenger }, { sailing_id, seats }) => {', 'route("POST", "/api/bookings", async ({ passenger }, { sailing_id, seats }) => {')
s = s.replace("  reserve(sailing_id, seats);\n  return [201, booking];", "  await reserve(sailing_id, seats);\n  return [201, booking];")
s = s.replace('route("PATCH", "/api/bookings/([^/]+)", (_ctx, body, [id]) => {', 'route("PATCH", "/api/bookings/([^/]+)", async (_ctx, body, [id]) => {')
s = s.replace("    if (diff > 0) reserve(booking.sailing_id, diff);", "    if (diff > 0) await reserve(booking.sailing_id, diff);")
open(p, "w").write(s)
p = "test/platform.test.js"; s = open(p).read()
s = s.replace('test("reserve refuses more seats than are left", () => {', 'test("reserve refuses more seats than are left", async () => {')
s = s.replace('  assert.throws(() => reserve("S-1", 3), (e) => e.status === 409);\n  reserve("S-1", 2);', '  await assert.rejects(reserve("S-1", 3), (e) => e.status === 409);\n  await reserve("S-1", 2);')
open(p, "w").write(s)
PY
  # The confirmations job: one SMS per booking, queued in data/outbox.json.
  cat > src/jobs/confirmations.js <<'E2'
// Queues a confirmation SMS for every held booking. The SMS gateway drains data/outbox.json.
import { load, save } from "../store.js";
const outbox = load("outbox");
for (const b of load("bookings").filter((b) => b.status === "held")) {
  const p = load("passengers").find((x) => x.id === b.passenger_id);
  outbox.push({ to: p.email, booking_id: b.id, text: `Harbourline: booking ${b.id}, ${b.seats} seat(s) held.` });
}
save("outbox", outbox);
console.log(`queued ${outbox.length} confirmation(s)`);
E2
  sed -i '' 's#"reminders": "node src/jobs/reminders.js"#"reminders": "node src/jobs/reminders.js", "confirmations": "node src/jobs/confirmations.js"#' package.json
  cat >> docs/specs/booking/requirements.md <<'E2'

## Story 3 — a passenger is told the booking is held

**BOOK-3.1** WHEN the `confirmations` job runs THE SYSTEM SHALL queue a confirmation SMS to the
passenger of each held booking in `data/outbox.json`.
E2
  cat >> docs/specs/booking/tasks.md <<'E2'

## Task 3: confirmations job
`src/jobs/confirmations.js`, `npm run confirmations`. Test: a held booking queues one SMS.
_Requirements: BOOK-3.1_
E2
  cat >> test/bookings.test.js <<'E2'
test("the confirmations job queues an SMS for a held booking", async () => {
  reset(); save("outbox", []);
  await post({ sailing_id: "S-1", seats: 1 });
  const { execFileSync } = await import("node:child_process");
  execFileSync("node", ["src/jobs/confirmations.js"], { env: process.env });
  assert.equal(load("outbox").length, 1);
});
E2
fi
if [ "${VARIANT:-}" = ui ]; then
  # A booking page served at /book: the passenger pastes a token, picks a sailing, books.
  mkdir -p public
  cat > public/book.html <<'E2'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Book a seat · Harbourline</title>
<style>body{font:16px system-ui;max-width:32rem;margin:2rem auto}label{display:block;margin:.6rem 0}#out{margin-top:1rem}</style></head>
<body>
<h1>Book a seat</h1>
<label>Your token <input id="tok" autocomplete="off"></label>
<label>Sailing <select id="sailing"></select></label>
<label>Seats <input id="seats" type="number" min="1" max="9" value="1"></label>
<button id="book">Book</button>
<div id="out" role="status"></div>
<script>
const $ = (id) => document.getElementById(id);
fetch("/api/sailings").then((r) => r.json()).then((xs) => {
  for (const s of xs) $("sailing").add(new Option(`${s.route} ${s.departs.slice(11, 16)} (${s.seats_left} left)`, s.id));
});
$("book").onclick = async () => {
  const r = await fetch("/api/bookings", { method: "POST", headers: { "content-type": "application/json", authorization: `Bearer ${$("tok").value}` },
    body: JSON.stringify({ sailing_id: $("sailing").value, seats: Number($("seats").value) }) });
  const b = await r.json();
  $("out").textContent = r.ok ? `Booked ${b.id}: ${b.seats} seat(s), ${b.price}k VND` : `Could not book: ${b.error}`;
};
</script>
</body></html>
E2
  python3 - <<'PY'
p = "src/http/server.js"; s = open(p).read()
s = s.replace('  const path = new URL(req.url, "http://x").pathname;\n',
  '  const path = new URL(req.url, "http://x").pathname;\n  if (req.method === "GET" && path === "/book") {\n    res.writeHead(200, { "content-type": "text/html" });\n    return res.end(fs.readFileSync(new URL("../../public/book.html", import.meta.url)));\n  }\n')
open(p, "w").write(s)
PY
  cat >> docs/specs/booking/requirements.md <<'E2'

## Story 3 — a passenger books from the web

**BOOK-3.1** WHEN a passenger opens `/book`, enters their token, picks a sailing and a seat count
and presses Book THE SYSTEM SHALL book it and show the booking id, seats and price on the page.

**BOOK-3.2** IF the booking is refused THEN THE SYSTEM SHALL show the reason on the page.
E2
  cat >> docs/specs/booking/tasks.md <<'E2'

## Task 3: booking page
`public/book.html` served at `/book`. Checked in the browser: books and shows the result; shows a refusal.
_Requirements: BOOK-3.1, BOOK-3.2_
E2
fi
git add -A; ci "$(d 2)" "feat(booking): book seats on a sailing"
echo "- \`POST /api/bookings\`, \`GET\` and \`PATCH /api/bookings/:id\` — seat bookings" >> docs/api.md
git add -A; ci "$(d 1)" "docs(booking): list the booking endpoints"

if [ "${GH:-}" = 1 ]; then
  # A forge to land on: a local bare origin and bin/gh (gh-pr-shim.py, state in .git/gh-pr.json).
  git init -q --bare "$T.origin.git"; git remote add origin "$T.origin.git"
  git push -q origin main feat/booking 2>/dev/null; git branch -q -u origin/feat/booking
  mkdir -p bin; cp "$SK/scripts/skill-tests/gh-pr-shim.py" bin/gh; chmod +x bin/gh
  cat > docs/agents/issue-tracker.md <<'E2'
# Issue tracker configuration (agent-facing)

**Tracker:** github, always through `bin/gh` (it carries the host and token for this repo).
Pull requests: `bin/gh pr create|view|edit|comment`. Seat booking is ticket #41.
E2
  echo "Tracker and forge: \`docs/agents/issue-tracker.md\`." >> AGENTS.md
  git add -A; git commit -q -m "chore: forge access through bin/gh"; git push -q origin feat/booking 2>/dev/null
fi

mkdir -p .claude/skills
for s in "${SKILLS[@]}"; do
  src=$(ls -d "$SK"/skills/*/"$s" | head -1)
  # Install the skill files only: TESTS.md and eval.json are authoring evidence, not shipped text.
  (cd "$src" && find . -type f ! -name TESTS.md ! -name eval.json) | while read -r f; do
    mkdir -p "$T/.claude/skills/$s/$(dirname "$f")"; cp "$src/$f" "$T/.claude/skills/$s/$f"; done
done
echo "harbourline ready at $T on feat/booking (port $PORT)"
