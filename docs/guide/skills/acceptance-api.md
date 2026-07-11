# `acceptance-api`

> Drive the running server the way a real client will. A unit test passes against the code's own assumptions; this proves the wire behavior — status codes, JSON shape, and side effects that survive a reload.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `docs/agents/project.md` (the `## Run locally (dev)` entry, requirement-tag conventions); a slice of `.skills/<slug>-acceptance.md`; the spec when run directly |
| **Writes** | the `## Run locally (dev)` entry in `docs/agents/project.md` when missing; observed results back into the ledger; a committed ID-tagged API test |
| **Calls** | [`debug`](debug.md) (the failing request is the red loop) |
| **Called by** | [`acceptance-check`](acceptance-check.md) |

## When it fires

To validate a backend HTTP/RPC API — REST or RPC endpoints — against its spec, before merging, by driving the running server as a real client. It covers the happy paths and the edge/error criteria that unit tests pass in isolation but miss against a live server. It also fires when the repo does not document how to start the backend, because it has to discover and record that first.

Usually [`acceptance-check`](acceptance-check.md) invokes it with a slice of the acceptance ledger. It can also run directly against an API change, in which case it first derives the checklist itself from the change's acceptance criteria — the spec, or the endpoints touched. Either way, it works through the items in order.

The distinction it is built around: a unit test passes against the code's own assumptions — it calls the handler and checks the value the handler returns. This skill proves the **wire** behavior instead: the status line a real client actually receives, the JSON shape it actually parses, and the side effects that actually survive a reload. Those are precisely the things a handler-level assertion cannot see.

## 1. Get the server running — and persist how

Read `docs/agents/project.md` for a `## Run locally (dev)` entry. If it exists, start the backend with that command. If it does not, discover the command from the repo — Cargo bins, `tauri`, `package.json` scripts, a Makefile — start the server, and confirm it answers, whether via a health route or the first checklist request returning anything at all.

Then **write** the command and its ready-signal into `project.md` under `## Run locally (dev)`. This is the half that is easy to skip and load-bearing not to: the next run, and every sibling skill, reads that entry instead of re-discovering. The step is done when the server answers a request AND the start command is recorded.

Recording the ready-signal — not just the command — matters because an acceptance run needs to know *when* the server is up before it fires the first request; a command with no observable "ready" line leaves the next run guessing.

## 2. Turn each checklist item into a real request

For each API item in the ledger, write the concrete request a client sends — method, path, headers, body — and its expected response. The expectation is specific: the status code, the body fields by name, casing, and id type, and any side effect.

Cover the edge criteria explicitly rather than only the happy path:

- an empty or whitespace field maps to the documented error,
- an unknown id maps to the documented status,
- a malformed body,
- repeated calls.

These are the criteria a unit test tends to assert in isolation and never send over the wire. The expectation is written *before* the request is sent, so the run compares against a criterion drawn from the spec, not against whatever the server happened to return.

## 3. Exercise against the live server

Send each request with `curl`, `http`, or a script, and assert the **full** expectation, not just a 2xx:

- the **status** — the exact code, not merely "some 2xx",
- the **body shape** — field names, casing, and id type as the client will read them,
- where the criterion says "persists", read it back with a fresh `GET`,
- where it says "across restart", restart the server and read again.

A `GET` after the write is what separates "the handler returned success" from "the write actually landed"; a restart-and-read is what separates "it is in memory" from "it is durable". Record actual-versus-expected in the ledger for every item. The step is done when every API item has an observed result.

## 4. Fix what breaks

Any mismatch is a real defect, found before the user found it. The **required sub-skill** is [`debug`](debug.md) — and the point is that the failing request is *already* your red-capable loop: you have a reproduction in hand. Fix the root cause, add the regression test, and re-run the item.

## 5. Promote to a durable test

Turn the exercised requests into a committed test that hits the server, or the handler at its real seam, tagged with the requirement ID per the conventions in `docs/agents/project.md`. It then joins the verify suite and guards the behavior after this run — the ephemeral `curl` becomes a standing regression. The step is done when the durable test is committed, tagged, and green.

## Worked example

The note-taking app's `NOTE` feature exposes `POST /notes`. `project.md` has no `## Run locally (dev)` entry, so step 1 discovers `cargo run --bin api` from the Cargo manifest, starts it, confirms `GET /health` returns `200`, and writes both the command and that ready-signal into `project.md`.

The ledger slice carries `NOTE-1.1` (create and persist) and `NOTE-1.2` (reject empty).

Step 2 turns `NOTE-1.1` into a concrete request and its full expectation:

```bash
# NOTE-1.1 — create returns 201 with an id, and the note reads back
curl -s -X POST localhost:8080/notes \
  -H 'content-type: application/json' \
  -d '{"body":"buy milk"}' -w '\n%{http_code}'
# expect: 201; body { "id": <string uuid>, "body": "buy milk" }

# persistence: read it back with a fresh GET
curl -s localhost:8080/notes
# expect: 200; array contains { "body": "buy milk" }
```

`NOTE-1.2` sends `{"body":""}` and expects `422`, not `201`. Running it against the live server exposes the defect the unit suite hid: the handler returns `201` with a blank body. Step 4 hands the failing request to [`debug`](debug.md), which roots the cause in a missing non-empty validation, fixes it, and re-runs to green.

Step 5 promotes the exercised requests into a committed test that hits the same seam, tagged so it joins the verify suite:

```rust
/// REQ: NOTE-1.2
#[tokio::test]
async fn empty_note_is_rejected() {
    let app = spawn_app().await;
    let res = app.post_notes(r#"{"body":""}"#).await;
    assert_eq!(res.status(), 422);   // not 201
}
```

Now the wire behavior is guarded: `finish-branch` re-runs it, and any future regression to `201` fails the suite instead of reaching a client.

## Why it is written the way it is

The skill asserts the **full** expectation on purpose. The failure it guards against is the "green 2xx" trap — an agent that sends a request, sees a 2-hundred-something, and calls the item passed, while the client that actually reads a specific status and specific field names breaks on the mismatch. Requiring status plus body shape plus a read-back for persistence removes the room for that shortcut.

Persisting the run command in `project.md` and promoting the request to a committed test are what make acceptance cheap the *second* time. Without them each run re-discovers how to boot the server and re-types throwaway `curl`s; with them the surface accumulates a durable, ID-tagged regression suite that the verify gate keeps enforcing.

Routing every failure through [`debug`](debug.md) rather than patching in place is deliberate too. A mismatch found here is a real bug with a real reproduction already in hand — the failing request. Handing it to `debug` means it gets a root cause and a regression test instead of a quick edit that makes the symptom go away, which is the same standard the rest of the set holds any fix to.

## See also

- [`acceptance-check`](acceptance-check.md) — the orchestrator that hands it a ledger slice
- [`acceptance-ui`](acceptance-ui.md) — the same contract for a frontend surface
- [`debug`](debug.md) — the red loop every failing request drops into
- [Traceability](../concepts/traceability.md) — why the promoted test carries a requirement ID
