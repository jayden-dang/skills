# Keep the winner

The winner is the surface's first real code. After the lock, `design.md` and
`tasks.md` finish it: they polish it, wire the real calls, and take the fake out
of the production path. They do not rewrite it.

## 1. Migrate the winner into the real screen

Delete the losing variants and the switcher. Move the winner out of the draft
folder into the route, view or window the surface will ship at, under the names
the codebase would give it, and delete the draft folder and its dev-only mount.
The winner keeps importing the same kit, shell and client it was drafted on, so
the move changes paths and names, not markup.
No draft folder, no `v3`, and no variant key may remain in a path or symbol.
Undo whatever a variant added to a shared file for the switcher.

*Done when: `git grep` for the switcher's param or env var (`?variant=`,
`*_VARIANT`, the draft flag) and for the draft folder's name finds nothing.*

## 2. The fake stays, behind one switch

The fake from SKILL.md §2 stays: out of the draft folder, it moves behind the
app's client, and the app selects it in exactly one place.
How you check it depends on whether the app had a fake mode before the draft:

- **The app had a fake mode before the draft** (`--fake`, `*_FAKE=1`, a fixture
  server): the fake stays a part of that mode, and that mode decides when it
  runs.
- **The app had no fake mode:** run the production build, then grep its output
  for the fake's module name and for one fixture value. Any hit fails the lock.

Write the contract into the brief under `## Contract`: one line for each call
the fake answers, giving the request, the response, and each error the screen
handles. `design-solution` lifts this section as the Interface the real
endpoints implement.

*Done when: the production check finds no fake, and every call the screen makes
has a `## Contract` line.*

## 3. Lock tests

Each thing the user decided is now held by a test, so later polish and
integration cannot drift away from it. Write one test per decided thing, at the
seam the screen already has (a view-model, or a component rendered on the fake):

- the finding sentence for today's data;
- each state the brief names;
- each moment of the interaction: what changes on the press, on success, and on
  failure.

Assert the decided structure, copy and state. Never assert pixels, spacing or
colour values: those change during polish.

The code was written before these tests, so you must watch each test fail. Break
the thing it guards, for example by removing the branch or changing the copy.
Run the test red, then restore the code. A test that never failed does not
lock anything.

*Done when: the whole suite is green, and every lock test has been seen red
once.*

## 4. Brief and commit

Write `ui-brief.md` as SKILL.md §5 says, with two extra lines:

- `Code:` the kept files and the fake's switch;
- `Lock tests:` the test files.

Keep the screenshot. Commit the winner, the fake, the lock tests and the brief
together on the feature branch, with a message that cites the brief path.

This commit is what the build starts from. Never label it "throwaway" or "not
for merge".

*Done when: `git status` is clean, and the commit holds the winner, the fake,
the lock tests and the brief, with no losing variant.*

## 5. The user tries the real screen

Run the app on the fake and hand the user the real screen's URL (or, for a
native app, its launch command), with one line on what to try: the moments the
lock tests hold. Leave it running. This is the first time the winner runs as the
product will, and the user's word on it is a change or a go, as in SKILL.md §3.
When your caller says where the try goes and runs the next step itself (a
charter), write the URL there and go on: the caller collects that word later.

Record no video here unless the user asks for one, or your caller passed
`--video`. Then record one walk of this screen, per `capture.md` § Recording a
walk, and hand over its path with the URL.

*Done when: the user has the URL, and a video exists exactly when it was asked
for.*

## What the build does next

`design-solution` lifts `## UI design` and `## Contract` from the brief.
`plan-tasks` writes the finishing tasks:

- polish the kept surface;
- the real interaction timings;
- the real endpoints, built to the contract;
- the fake taken out of the production path.

Each of these tasks is test-first, and the lock tests stay green throughout.
