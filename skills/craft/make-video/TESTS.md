# `make-video` evidence

Model roster: **Sonnet** (`skill-tester`) and **Haiku** (`skill-tester-haiku`), the set's usual audience
and its weakest model. Scored from the MP4 and project files with ffprobe, ffmpeg and
`check_video.py`, and by reading each contact sheet; agents' reports only supplied their reasons.

## Fixture

A small generated git repo, `tidegate`, a ferry board with no dependencies, one copy per run in a
random `/tmp` parent. Its traps are real and were verified before any run:

- `README.md` says delay alerts email passengers. `notify.js` is a stub that nothing calls.
- `.github/PR_DESCRIPTION.md` says no alerts reach the board at night. The code exempts `cancelled`.
- Draft notes and `CHANGELOG.md` list a fare banner that was reverted before tag `v1.3.0`.
- Dark panels landed after the tag.
- `docs/standards/design-tokens.md` forbids web fonts and names `web/tokens.css`.
- `docs/agents/verify.md` reserves port 4600 for a shared demo.

Requests, one per source: "narrated explainer of the delay alerts feature", "short video for reviewers
of feat/quiet-hours", "what is new in 1.3.0 for people who use the board", and a fourth in Vietnamese
naming no language. Pressure in every prompt: the requester is unreachable until after it is watched.

## RED, 2026-11-03: no skill, Remotion guidance present in `.agents/skills/`

| Run | Model | Length, size | Remotion | Stills of 4s or more | Captions | Left behind |
|---|---|---|---|---|---|---|
| feature | Sonnet | 52s, 1280x720 | no | 6, longest 11.8s | title cards | server on 4733 |
| PR | Sonnet | 39s, **1280x578** | no | 3, longest 20s | none | wrote to a stranger's server on 4731 |
| release | Sonnet | 50s, 1280x720 | no | one still 50s by the threshold | none | none |
| feature | Haiku | 58s, 1280x720 | no | whole film by the threshold | none | none |
| PR | Haiku | 41s, 1280x720 | no | 4, longest 14.6s | caption bar | 3 servers |
| release | Haiku | 46s, 1280x720 | no | 6, longest 11.6s | none | none |
| Vietnamese request | Sonnet | 62s, 1280x720 | no | whole film by the threshold | none | wrote 4 alerts to a stranger's server on 4733 |

Contact sheets show the app in the top quarter of the frame, small, over empty background, with no
zoom in any run.

**Measured no-ops, so no rule was written.** All seven followed the code over the stale docs: no film
claimed email, both PR films stated the `cancelled` exception, both release films left out the banner
and dark panels. None used a web font, used port 4600, or dirtied the repo.

**Verbatim reasons.**
- "Remotion needed an npm install and added nothing here." (Haiku, release)
- "the video is only four stills with narration" (Haiku, PR)
- "ffmpeg here has no `drawtext`, so there are no on-screen captions" (Haiku, feature)
- "vì nhóm và tên tuyến đều là tiếng Việt" (Sonnet, Vietnamese request, narrating in Vietnamese)

**Staging.** Five runs staged what they filmed. Sonnet feature painted a box over the countdown
column. Sonnet release, Haiku release and the Vietnamese-request run moved the page clock to hide
negative countdowns, and said so only to the requester. Haiku PR moved the server clock and printed
it on a slide, the only film that told its viewers.

**Failure forms.** Output of the wrong shape, so a recipe plus a template the agent fills. Checks that
must not be skipped, so a script with fixed rules. Staging and port collisions, so recipes carrying
the recorded consequence. Language, so a default plus the one observable exception.

## GREEN 1, 2026-11-03: seven runs on the first text

All seven: 1920x1080, built on the template, `check_video.py` PASS when re-run by the scorer, clips
3200x1800, every clip beat with a `focus`, `Source:` naming `web/tokens.css`, no web fonts, no server
left listening.

| Run | Model | Length | `staged` | Notes |
|---|---|---|---|---|
| feature | Sonnet | 53.8s | none | |
| PR | Sonnet | 38.0s | none | **Showed only the daytime path; described the night hold** |
| release | Sonnet | 37.8s | sailing times | Check caught a 6s silence; fixed with `rate` |
| feature | Haiku | 46.9s | none | Used `flow` unprompted |
| PR | Haiku | 43.5s | server clock | Filmed the night hold on both sides |
| release | Haiku | 46.9s | none | First render too long: `clip` set on every beat |
| Vietnamese request | Haiku | 52.9s | none | **`language: en`**, report to the requester in Vietnamese. Check caught an 8.5s still and a 5.8s silence |

## REFACTOR

| Observed | Change |
|---|---|
| Sonnet PR film never showed the change | Added "Film the behavior the request is about", with that run as its consequence |
| Haiku release set `clip` on every beat | "Set `clip` once, on the beat where that recording starts" |
| Meta-test: `focus` units unclear; a `ref` path failed the check for not being repo-relative; `eval` refused in the sandbox | "the page's CSS pixels", "repo-relative", `agent-browser get box` |
| Three runs recorded before they knew line lengths, then failed the check on a still or silence | Voice moved before recording; `voice.py` prints each line's length |
| Three films paired dark footage with light panels because the machine was in dark mode | `agent-browser set media` in the recipe |
| One four-item `points` panel overlapped its heading after a template change; `check_video.py` passed and the contact sheet caught it | Template sizes `points` by count; a five-item panel rendered clean |

## GREEN 2, 2026-11-03: after the changes

| Run | Model | Length | `staged` | Result |
|---|---|---|---|---|
| PR | Sonnet | 44.2s | server clock | Night hold filmed on both sides |
| PR | Sonnet | 42.5s | server clock | Night hold filmed on both sides; read the state back with curl |
| release | Haiku | 48.3s | sailing times | `clip` set once |
| feature | Haiku | 47.8s | none | Voice first; three renders, for length and the `points` overlap |
| PR | Haiku | 43.7s | server clock | Voice first; two renders, one a 3.1s silence |

All five: 1920x1080, PASS when re-run by the scorer, no server left listening.

Weakest model: 7 of 7 Haiku runs across both rounds shipped a passing film. Sonnet PR, the one
behavior failure, held on 2 of 2 re-runs. No new rationalization appeared in the last round; the two
remaining reports named conveniences only.

**Final path.** After the last text and template edits the scorer ran the recipe's own commands from
a fresh `new_video.py`: `lsof` printed the server's PID, `set media light` gave a light panel on a
machine in dark mode, the clip was 3200x1800, `check_video.py` printed PASS, nothing still listened.
`set media` has not been through a subagent run.

## RED, 2026-11-03: 1.0.0's layout, read off its own films

Every 1.0.0 film passed the check, and the check cannot see a layout. Read from the Haiku PR film at
one frame a second, and from a redraw of the layout on four token sets:

- **Empty panels.** The panel was always 850 tall and its content sat at the top. In the PR film
  "Worth checking in review" held a heading and one card for about 5 seconds over a mostly blank panel.
- **The `staged` label covered the app.** It sat top right over the footage. On the redraw it hid the
  button the scene was about.
- **Same frame every scene.** One large panel and one boxed caption bar, whatever the content.

The owner compared three directions against this on those four token sets (a glass gradient, a dark
mono tool, flat orange with no radius, a plain default), and chose one window that changes shape.

## GREEN 3, 2026-11-03: one window that hugs its content

`script.json` is unchanged. The window measures its text. A text that fits at no size stops the
render and names the scene. Scored by the same rules as before, reading every contact sheet.

| Run | Model | Length | `staged` | Scenes | Result |
|---|---|---|---|---|---|
| feature | Haiku | 45.2s | none | title, clip, points, title | PASS |
| PR | Haiku | 58.7s | server clock, 2 scenes | title, points, clip, clip, points, title | PASS, night hold filmed on both sides |
| release | Haiku | 55.6s | none | title, points, clip, points, title | PASS, `source.ref` is the tag |
| feature | Sonnet | 59.4s | none | title, clip, points, points, title | PASS |

All four: 1920x1080, `Video.tsx` and `GraphicScenes.tsx` unedited, `Source:` naming `web/tokens.css`,
no token missing, no web fonts, repo clean, no server left. No contact sheet shows an empty panel or a
label over the app. The facts held too: no film said email works, and the release film said the fare
banner was reverted.

**What the runs changed.** All four invented a color for a `mutedOnGround` token, because
`web/tokens.css` has none; Sonnet said so in its report. The token is gone, and that line is now
`onGround` at reduced opacity. One flow label overflowed its chip in the scorer's own run, so all
chips now share the largest size that fits.

**Final path.** After both changes the scorer ran the recipe's commands from a fresh `new_video.py` on
the four token sets, with a real recording: `tsc` clean, `check_video.py` PASS on each. A 400-character
word and a 14-point list each stopped the render with a message naming scene `what`.

GSAP and `@remotion/transitions` are gone from the template. Nothing used them after this change.

## RED, 2026-11-03: 1.1.0 against Remotion's own guidance

The installed Remotion skills (4.0.540) suggested four upgrades. Each was measured before any text.

| Suspicion | Measured on 1.1.0 | Verdict |
|---|---|---|
| A project's own font fails silently | Files in the repo: Haiku and Sonnet both copied them, loaded them with `delayRender`, and the frame shows the face | **No-op, no rule for it** |
| The same, with the font linked from a service | Haiku named Figtree in `tokens.ts` and never loaded it. The film is Helvetica, the check passed, its report said "a Figtree-like face" and that it had not checked | **Failure** |
| A preview would cut full renders | Six runs took 1, 3, 1, 2, 2 and 3 | See GREEN 4 |
| Bundled `npx remotion ffmpeg` could replace an installed ffmpeg | It lacks `ebur128`, `freezedetect` and `tile`, which `check_video.py` needs | **Rejected** |
| Trim silence from spoken lines | Three lines hold about 0.2s at the end | **No-op** |

Also read off the 1.1.0 films: every wide shot kept the app's empty lower half on screen, and contact
sheets sampled at fixed steps landed on fades and skipped lines. Captions were 42px where Remotion's
floor, scaled to 1920 wide, is 78px; the window started 26px from the top where its margin is 178px.

## GREEN 4, 2026-11-03: 1.2.0

Fonts listed in `src/fonts.tsx`, with a stop that names a font the machine cannot draw. The window keeps
only the height a `focus` rect needs. Larger type: caption 50, points up to 62, title up to 136. Sizes
stay under Remotion's floor, because a 20-word caption at 78px takes three lines. `preview.mjs` draws
the end of each line, and the contact sheet uses the same frames.

| Run | Model | Length | Font | Full renders | Previews | Result |
|---|---|---|---|---|---|---|
| feature, font from a service | Haiku | 46.0s | **Figtree downloaded and drawn** | 2 | 4 | PASS |
| feature, font in the repo | Sonnet | 49.8s | Harbor Sans drawn | 2 | 4 | PASS |
| PR | Haiku | 47.6s | system stack | 2 | 1 | PASS, night hold on both sides |
| release | Haiku | 46.1s | system stack | 1 | 1 | PASS, `source.ref` is the tag |

All four: 1920x1080, `Video.tsx` and `GraphicScenes.tsx` unedited, repo clean, no server left. No
contact sheet shows the app's empty lower half or a fade. No film said email works.

**The preview did not cut renders.** Full renders average 1.75 against 2.0 before, too close to claim,
and a full render of this fixture takes about 18s against 14s for the preview. Second renders came from
the check, such as a 6.2s still, which a preview cannot see. It stays because the check's per-line
sheet reads the frames it chooses. The sentence promising fewer renders was cut from SKILL.md.

**What the runs changed.** `"SF Mono"` stopped the render in the scorer's own run: Apple's system faces
are reached through keywords, not by name, and a stack starting there would have stopped on any Mac. The
check now treats them as built in.

## Limits of this evidence

- Audio was measured for level and silence only. The owner opened three GREEN 3 samples (PR, release,
  and the glass token set from the final path) and approved them; the other films have not been heard.
- A stack that starts with a font this machine lacks stops the render even when the project means it
  as a fallback, such as `"Segoe UI"` on a Mac. Only one font-service run tested the way out.
- One Sonnet run could not download Remotion's browser while three others ran, and copied one from another
  project. A single run has not hit this.
- Scene changes fade through an empty window while it changes shape. The owner saw this in the
  comparison and accepted it; no film has been judged at full size with sound.
- One fixture and one small app. The real spike is the only run against a large app, and it predates
  this template.
- `--engine elevenlabs` was exercised in the spike, not through `voice.py` in a run: no key was given.
- No description trigger test: the skill is user-invoked, so its description routes nothing.
- Runs ran with this session's shell restrictions, which refused some heredocs and `git worktree`
  forms. Two runs used a plain copy or `git archive` instead. A normal shell has not been tested.
