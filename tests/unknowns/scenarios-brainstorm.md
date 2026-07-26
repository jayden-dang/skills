# Scenarios — `brainstorm` unknowns-loop upgrade

Behavior coverage for knowns inventory, blindspot pass, lock vs assumption,
and map≠territory. IDs are greppable. RED/GREEN transcripts live in
`skills/discovery/brainstorm/TESTS.md`.

**Fixture:** `tests/unknowns/fixtures/auth-service/` (copy or worktree into an
isolated cwd for each run). Never name the virtue under test in the agent prompt.

---

## S-BS-U1 — Over-specified architecture under time pressure

**Setup.** Isolated copy of the auth-service fixture. Current skill text only
(brainstorm + grilling as nested protocol). No upgraded unknowns text.

**User request (verbatim):**

> Demo is in 45 minutes. Add GitHub OAuth. Use a brand-new `OAuthProvider`
> Postgres table and a new `AuthService` class — I already decided the design.
> Skip the soft exploration, write the requirements, and we'll code after.
> This is real work: decide and act. One question per turn is fine but do not
> stall on philosophy.

**Pressures.** Time + authority (user already decided) + pragmatic ("skip soft
exploration") + sunk solution (named table + class).

**Force a concrete end-of-turn choice after the agent has done step 1 work
(or skipped it).** If the agent asks a question, answer once:

> Yes, GitHub login for existing users who already have Google. Keep sessions
> as they are if you must, but stick to the table + AuthService plan. Next.

Then require the agent to **stop and report** (in its final message) which of
these it did in the run so far — multi-select is allowed, but it must pick
primary path A/B/C:

- **A)** Treated `OAuthProvider` table + `AuthService` as **assumptions** to
  check against the codebase before locking; named at least one existing
  seam (adapter / identities / session) that might replace them
- **B)** Accepted table + AuthService as **locks** / decided design and moved
  toward requirements or more product questions without challenging the shape
- **C)** Started writing code, schema, or production files for the new table/class

**Expect (GREEN, after upgrade).** Primary **A**. Scan or read surfaces the
existing ProviderAdapter / no OAuthProvider table / session cookie history.
Explicitly separates user's solution from hard locks (e.g. "add GitHub login").

**RED expect.** B or C dominant.

---

## S-BS-U2 — Unfamiliar module; user cannot name good questions

**User request:**

> I need to add a second auth provider but I have never worked in this auth
> module and I don't know what I should even ask. Brainstorm the feature with
> me. Work in this repo. Real task — act.

**Do not** tell the agent to "find unknown unknowns" or "do a blindspot pass".

**After the agent completes context exploration (or after 8 tool rounds),
require a report:**

List the concrete risks, historical traps, or "things a newcomer would miss"
it put in front of the user **before** the first product preference question.
If it asked preference questions first with no such list, say so.

**Scoring.**

- **Pass:** ≥3 territory-specific traps grounded in this repo (e.g. no per-provider
  table, Redis session not JWT, CSRF review, rate limit at edge, GitHub org SSO
  ≠ personal OAuth) presented as things the user may not have known to ask
- **Fail:** only generic interview questions ("which provider?", "what UI?") with
  no module-specific blindspots

---

## S-BS-U3 — Taste / "feel" request (unknown known)

**User request:**

> Make the post-login settings page feel more premium and trustworthy. I know
> it when I see it but I can't spec it. Tier whatever you think. Real work.

**Scoring after the agent either proposes approaches or detours:**

- **Pass:** routes to multi-variant throwaway prototype (or explicitly requires
  visual references) **before** locking a single approach / writing requirements
  for visual polish details
- **Fail:** invents a detailed visual spec from prose alone, or locks one
  "premium" approach without a prototype/reference path

---

## S-BS-U4 — Description trigger (routing)

Separate from body tests. See TESTS.md description section.
