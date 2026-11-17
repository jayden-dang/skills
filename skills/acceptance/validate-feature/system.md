# Acceptance — system properties

Run this after the spec checklist, on every endpoint, command or job the branch adds or
changes. The spec does not have to name what is here.

## 1. The probe the spec never names

Send each endpoint that reads a body one that is not JSON (`-d '{bad'`). Expect a 4xx,
nothing written, and no stack trace, file path or SQL in the body. Five of eight baseline runs
never sent one. The endpoint answered `500` with the server's stack and absolute paths.

## 2. A failed probe on a changed surface is this branch's defect

Your drive may show any of these on an endpoint or command the branch adds or changes:

- another account's record can be read or changed
- a route answers without the sign-in its sibling routes need
- a write takes fields the caller should not set, or a read returns secrets
- a refused request still wrote something
- bad input gets a 5xx or a stack trace back

Fix each one in this run: REQUIRED SUB-SKILL: use `root-cause`, then `test-first`. Do this
whether or not the spec names it, and wherever the cause sits, including shared server, router
or helper code the branch calls. When the project already answers the same case somewhere else
(a sibling route's `404` for another account's record), give the same answer.

In eight baseline runs, every one found that any passenger could read and change another's
booking. Three left it open ("I left it unfixed so you can choose", "I didn't add it without a
requirement"), and those branches still served Mai's booking to Tuan when the run ended. Every
run left the `500` on a non-JSON body standing. The runs that saw it in shared server code said
"It is platform code, so I left it."

**The one exception: the fix would change a documented contract.** That is something named in
`docs/`, a test that pins a response shape, or a persisted format. Build the option that keeps
the contract, and put the question in your result under **Needs a decision before merge**.

**A gap that is not on the list above is a question, not a change.** Examples are a price rule,
a business limit, or data the seed does not have. Name it in the result and leave the code as
it is. Baseline runs repriced bookings and invented vessel names that nobody had asked for.

## 3. Report

In the result, list each fix made under this file in a **Beyond the spec** section: the probe
you sent, what came back, and the commit that fixed it.
