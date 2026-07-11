# `acceptance-ui`

> Drive the app in a real browser the way a user will: click, type, submit, reload, and assert on what is actually on screen. Component tests mock the network; this proves the wired stack — render, request, response, re-render, persistence.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `docs/agents/project.md` (the `## Run locally (dev)` entry, requirement-tag conventions); a slice of `.skills/<slug>-acceptance.md`; the spec when run directly |
| **Writes** | committed, ID-tagged Playwright specs (the durable artifact); a Playwright/Chromium harness and its run command when absent; the `## Run locally (dev)` entry when missing; results into the ledger |
| **Calls** | [`debug`](debug.md) (the failing spec is the red loop) |
| **Called by** | [`acceptance-check`](acceptance-check.md) |

## When it fires

To validate a frontend against its spec by driving it end-to-end in a real browser the way a user would — automated Playwright specs on Chromium, asserting visible state and persistence across reload — before merging. It covers the happy-path and edge-case flows that component unit tests mock away. It also fires when the repo has no Playwright/Chromium harness, or no documented run command, because it sets those up first.

Usually [`acceptance-check`](acceptance-check.md) invokes it with a slice of the acceptance ledger; it can also run directly against a frontend change. Either way it works through the ledger in order.

The distinction it is built around: a component test mocks the network and proves the component's own logic in isolation. This skill proves the **wired stack** — render, request, response, re-render, persistence — by driving a real browser against the real server. That is the only path that catches a checkbox flipping in memory but never reaching the store, because the component test that mocked the store never asked whether the write landed.

## 1. Get the app running — and persist how

Read `docs/agents/project.md` for `## Run locally (dev)` and start the frontend, and any backend it calls, with the recorded commands. If they are absent, discover them, start the app, confirm it loads in a browser, then **write** them into `project.md` under `## Run locally (dev)`. This is the same contract [`acceptance-api`](acceptance-api.md) follows.

A frontend usually needs both halves running — the app and the API it calls — so the recorded entry captures both commands, not just the dev server. The step is done when the app loads AND the commands are recorded.

## 2. Ensure a Playwright/Chromium harness

Check for one: `@playwright/test` installed and a `playwright.config.*` carrying a Chromium project. If present, use it. If not, set it up — install `@playwright/test`, add a config with a `chromium` project and the dev-server `baseURL`, a test directory, and record the run command (`… playwright test --project=chromium`) in `project.md`.

The config points at the dev-server `baseURL` so specs can navigate with `page.goto('/')` rather than hard-coding a host, and the run command lands in `project.md` next to the dev command so the next run finds both together.

The bar is deliberately low and concrete: the step is done when the Playwright command runs against Chromium **even with zero specs**. Proving the harness boots before writing any flow separates a harness problem from a feature defect.

## 3. Turn each checklist flow into a spec

For each UI item in the ledger, write a Playwright spec that acts as a user. Locate elements by role or label — `getByRole`, `getByLabel` — type and click, and assert on **visible** outcomes:

- text on screen,
- the input cleared,
- list order,
- an error message shown.

Assert what the user sees, not internal state — a locator by role or label is how a user finds a control, and a visible-text assertion is what a user confirms; both keep the spec from coupling to markup the user never sees.

Where the criterion says "persists", call `page.reload()` and assert the state survives the reload — a reload is the browser-side equivalent of the API skill's fresh `GET`, the difference between "it rendered" and "it was actually saved". Tag each spec with its requirement ID per the `project.md` conventions, for example `test('…', { tag: '@CODE-N.M' }, …)`, so [`check-trace`](../resources/scripts.md) can prove the flow is covered.

## 4. Run on Chromium and fix what breaks

Run the specs headless on Chromium. Any failure is a real defect. The **required sub-skill** is [`debug`](debug.md) — the failing spec is your red-capable loop. Fix the root cause, keep the spec as the regression, and re-run. The step is done when every UI flow passes in a fresh Chromium run.

"A real defect" is meant literally: a spec that drove the real app and did not see the expected screen has found something a user would hit. It is never a reason to loosen the assertion — the fix goes into the code, not the expectation.

The tag on each spec carries the requirement ID per the `project.md` conventions, which is what lets [`check-trace`](../resources/scripts.md) prove the flow is covered once the spec is committed.

## 5. Commit the specs

The specs are the durable artifact — commit them, tagged, so they join the verify suite and [`finish-branch`](finish-branch.md) re-runs them. Record any new run command in `project.md` and note results in the ledger. The step is done when the specs are committed, tagged, and green.

Unlike [`acceptance-api`](acceptance-api.md), where the durable test is a promotion of the throwaway `curl`, here the spec you wrote to drive the flow **is** the durable test from the start — there is nothing to translate. The same file that acted as the user during acceptance is the regression that guards the flow afterward.

## Worked example

The note-taking app's `NOTE` feature has a create-note form. The ledger slice carries `NOTE-1.1` (a typed note appears and persists) and `NOTE-1.2` (empty submit is rejected, the input keeps its text).

Step 1 starts the Vite dev server and its API and records both. Step 2 finds no harness, installs `@playwright/test`, writes a config with a `chromium` project at `baseURL: http://localhost:5173`, and confirms `playwright test --project=chromium` runs green against zero specs before a single flow is written.

Step 3 then writes each flow as a user would perform it — navigate, fill a labelled field, click a named button, and assert on what shows:

```ts
// e2e/create-note.spec.ts
test('a typed note appears and survives reload', { tag: '@NOTE-1.1' }, async ({ page }) => {
  await page.goto('/')
  await page.getByLabel('New note').fill('buy milk')
  await page.getByRole('button', { name: 'Add' }).click()

  await expect(page.getByRole('listitem').filter({ hasText: 'buy milk' })).toBeVisible()
  await expect(page.getByLabel('New note')).toHaveValue('')   // input cleared

  await page.reload()                                          // persists
  await expect(page.getByRole('listitem').filter({ hasText: 'buy milk' })).toBeVisible()
})

test('an empty note is rejected and keeps the typed text', { tag: '@NOTE-1.2' }, async ({ page }) => {
  await page.goto('/')
  await page.getByLabel('New note').fill('   ')
  await page.getByRole('button', { name: 'Add' }).click()

  await expect(page.getByText('Note cannot be empty')).toBeVisible()
  await expect(page.getByLabel('New note')).toHaveValue('   ') // input NOT cleared
})
```

Run headless on Chromium. Suppose `NOTE-1.2` fails because the form clears on a rejected submit — the exact gap a mocked component test never sees, since the component test asserted the validation function returned an error and never watched the input.

[`debug`](debug.md) roots the cause and fixes it; the spec stays as the regression; step 5 commits both specs, tagged, into the verify suite, where `finish-branch` will re-run them on every future change to the form.

## Why it is written the way it is

The skill insists on assertions against **visible outcomes** and a real `page.reload()` because that is the boundary component tests cannot reach: they mock the network, render in isolation, and prove the component's own logic while the wired stack — request, response, re-render, storage — goes unexercised. Driving a real Chromium session over the real server is the only way to catch a checkbox that flips in memory but never reaches the store.

Setting up the harness to run against zero specs first is a debugging affordance: it forces a green baseline so that the first real failure is unambiguously a feature defect, not a misconfigured runner. And committing the specs is what turns a one-time acceptance pass into a standing, ID-tagged regression that `finish-branch` keeps enforcing.

Chromium specifically, and headless, are chosen to keep the run cheap and repeatable rather than to chase cross-browser coverage — this gate is about proving the feature is wired, and one real engine driven end to end proves that. Routing any failure through [`debug`](debug.md) for a root cause and keeping the spec as the regression holds a UI defect to the same standard as any other fix in the set: understood, not merely un-reproduced.

## See also

- [`acceptance-check`](acceptance-check.md) — the orchestrator that hands it a ledger slice
- [`acceptance-api`](acceptance-api.md) — the same contract for a backend surface
- [`dogfood`](dogfood.md) — the manual sibling, for judgment a Playwright spec cannot make
- [`debug`](debug.md) — the red loop every failing spec drops into
