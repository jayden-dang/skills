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

## RED, 2026-11-03: a spec, on 1.2.0

Fixture: `tidegate` plus a committed, unbuilt triad, `docs/specs/2026-11-rebooking`, 14 IDs across 4 stories, a design with
a call path, an `Offer` type, a refusal table and three decisions. Request: "I have not read this spec and nothing of it is
built yet. I want a technical film of it, not a marketing slide film ... 60 seconds." The requester cannot be reached.

| Run | Model | Result |
|---|---|---|
| 1.2.0 installed | Sonnet | No film. "A subject with no code yet is out of scope": it stopped and offered to wait for the build |
| 1.2.0 installed | Haiku | 67.3s against 60. Went around the rule. `source.kind` `feature`, **0 of 14 IDs**, three `points` scenes. Cut for length: "the API contract shape", offer states, masking |
| Nothing in the repo | Sonnet | 53.6s, `source.kind` `feature`, **0 of 14 IDs**, three `points` scenes, no route, no status code, no type. The sheet is bullet slides |

The third run was meant as a no-skill control and is not one: it found the machine's global install of `make-video` and said
so. Read as a second sample of 1.2.0 on the same request.

**Verbatim.** "A film made from the spec text alone would be the unchecked slideshow the skill exists to prevent" (Sonnet).
"The narration does not read out every requirement ID, the 409/404 refusal table, the contract type or the test seams"
(Sonnet, third run). "The film no longer explains phone masking, the offer states, or the API contract shape" (Haiku).

Form: the output had the wrong shape, so the answer is a recipe plus scene kinds the template owns, and a check on what
reached the screen, not a prohibition.

## GREEN, 2026-11-03: a spec, on 2.0.0

Scored from each script and MP4, re-running `check_video.py` as the scorer. All PASS, all 1920x1080, all voiced by ElevenLabs.

| Run | Model | Length | IDs cited | Stories | Scenes |
|---|---|---|---|---|---|
| 14 IDs, English | Sonnet | 55.9s | 11 of 14 | 4 of 4 | the 8 of the recipe, in order |
| 14 IDs, English | Haiku | 57.4s | 13 of 14 | 4 of 4 | the 8 of the recipe, in order |
| 14 IDs, Vietnamese, under `shape` | Sonnet | 56.0s | 10 of 14 | 4 of 4 | 9, two `ears` |
| 14 IDs, Vietnamese, under `shape` | Haiku | 58.5s | 9 of 14 | 4 of 4 | the recipe's |
| PINWIN, a real 108-ID triad | Sonnet | 95.1s | 35 of 108 | 19 of 19 | 10, two `ears`, one `code` |

The route, the `Offer` type and the 409 and 404 are on screen in every film on the small spec. Haiku's film no longer drops
the contract. Vietnamese films keep rules and code in the spec's English, as asked.

**What the sheets found that the check could not, all fixed in the template.** The `planned` label sat over the corner of a
full-height window, so it moved to the bottom. A `sequence` label printed its backticks literally. Neither fix has been through
another subagent run. The final template was rendered end to end from a fresh `new_video.py` and printed PASS, and a still of a
backticked label shows both fixes.

**Meta.** Two runs asked how long a `code` line may be, which the page now says. One asked which rules to keep past three, and
that stays a judgment. One hit this harness's refusal of a JSON literal in a shell command, which is not the skill's.

**Voice.** Unit tests in `scripts/test_voice.py`, watched red first: no key stops before any call, `--engine` is refused, a refused
call leaves no file, `spoken` replaces what is said, and a rerun pays only for the line that changed. A real film on the small
spec billed 674 to 740 characters and PINWIN 1,404.

**Not covered.** Nobody has listened: Vietnamese intelligibility on `eleven_flash_v2_5` stays at the spike's measure, about 11% with
tones. Feature, PR and release films were not re-run on this version; `say` going away is their only behavior change, and
those paths carry the same `voice.py`. A spec with no contract in its design.

**Trigger, now that it is model-invocable.** Ten requests against six neighboring descriptions, Sonnet and Haiku, identical and as
intended: video of a release, of a PR, of a spec and a demo clip route here; "explain the checkout flow", "walk me through this
branch" and "teach me this spec's offer states" go to `understand`; requirements, an HTML report and an end-to-end check go elsewhere.

## RED, 2026-11-03: the walkthrough, judged by its owner

The films of "GREEN, a spec, on 2.0.0" passed every check. Their owner watched one: it summarizes and justifies, and it does not
make them understand the feature. They pointed to Karpathy's note on bespoke 3b1b-style explainers and ASD-STE100.

**Cause, measured from the scripts.** The recipe ordered scenes by the spec's files and the check demanded every story, so the film
recited. Lines giving a reason (so, because, but, if):

| Film | Reasons | Scene changes |
|---|---|---|
| Walkthrough, Sonnet, 14 IDs | 1 of 23, 4% | 8 |
| Walkthrough, Haiku, 14 IDs | 2 of 22, 9% | 8 |
| Walkthrough, Sonnet, Vietnamese | 0 of 20 | 9 |
| Walkthrough, Haiku, Vietnamese | 0 of 21 | 9 |
| Walkthrough, Sonnet, PINWIN | 0 of 30 | 9 |
| Hand-written explainer, 14 IDs | 11 of 17, 64% | 1 |
| Hand-written PINWIN, English | 9 of 21, 42% | 7, with footage |
| Hand-written PINWIN, Vietnamese | 11 of 21, 52% | 7, with footage |

The owner watched the hand-written films and chose that direction. Those films were written by the author, not an agent, and were
the shape to aim at. Evidence of agents following the text is the next section.

The owner first said 60 seconds, then 120 at most for a large spec. Explaining a 14-ID spec by hand took 86 seconds, so the limit
is 120 for every spec, a recommendation the owner accepted when they approved the direction.

## GREEN, 2026-11-03: the explainer, on 2.0.0

**Limit of this round.** ElevenLabs refused every call: "Your subscription has a failed or incomplete payment." So agents used a stand-in
that estimates line lengths from word counts, and stopped at `preview.mjs`. No agent run reached a render or `check_video.py`'s media
checks. Script rules were run by the scorer against each script. The request named no structure: "Make me a film of it, so I understand the feature."

| Run | Model | Reasons | Script faults | Left out | Length, estimated |
|---|---|---|---|---|---|
| 14 IDs | Sonnet | 12 of 19, 63% | none | 3 | about 110s |
| 14 IDs | Haiku | 12 of 19, 63% | none | 5 | about 105s |
| 14 IDs, Vietnamese | Haiku | 11 of 15, 73% | none | 4 | about 100s |
| PINWIN, 108 IDs | Sonnet | 12 of 24, 50% | none | 91 | about 112s |

All four found a named example without being asked and told it through "but what if". Read from the sheets, three faults remained, all
in this text:

- Four of four opened on "This film explains how...", because step 3 required a `title` scene first.
- Two of four rewound: Lan accepted, then "what if Lan answers late" took her seat back. The recipe had split going right from what goes wrong.
- Three of four first previews cut something off with the camera.

**After those three edits, Haiku, fresh repo.** 11 of 14 lines give a reason, 78%. It opens "Staff cancel Lan's 08:15 ferry, and nobody tells her",
on a `world`. Time only runs forward. About 65 to 70 seconds. No script fault, 6 IDs left out. It still took three previews to fit its camera boxes,
and asked for a larger worked sample. Not added: nothing in the sheets required it.

**Trigger for reasons.** `check_video.py` fails a spec film under a third. The word list is `en` and `vi` only, and an agent could pass it with empty "so"s. It
catches a list of facts, which is what was measured, and does not measure understanding. Only a person watching does.

**Three things the PINWIN capture found, fixed.** A refused voice call printed only "401", which reads as a bad key and hid an unpaid invoice: `voice.py` now prints the vendor's sentence, test first. Vietnamese writes each syllable as a token, so 20 "words" was about 4 seconds and the lines came out clipped: the limit is 30 there. A line can change the world part way through, with `then`, because a long line left one still frame for 7.9 seconds.

**Not covered.** A render of an agent's explainer with real voice. Anyone hearing any film. A built feature through this recipe by an agent: PINWIN's footage film was hand-written, and its server claims were checked by hand on an isolated plane. Footage of today's behavior inside a spec film is left out, since running an app under `--auto` has never been measured.

## 2026-11-04: the voice moves to Vibi

ElevenLabs refused the key over an unpaid invoice, and the owner asked to try Vibi, which fronts ElevenLabs, MiniMax and CapCut. The same 37-word Vietnamese line, spoken once on each voice and transcribed by Vibi's Scribe, with number words read as digits by hand:

| Voice | Wrong words | Credits per character | Wait |
|---|---|---|---|
| MiniMax `speech-2.8-hd`, Professional Narrator | 0 of 37 | 1 | 4.6s |
| MiniMax `speech-2.8-hd`, Articulate Assistant | 0 of 37 | 1 | 4.8s |
| ElevenLabs v4, Sarah | 1 of 37 | 1 | 7.4s |
| ElevenLabs Flash, Sarah | 2 of 37 | 0.5 | 20s |
| CapCut, Trung Caha and Ha Nu | about 3 in 4 | near 0 | 14s |

The owner chose the Professional Narrator. English took Flash by default, which the owner has not ruled on: 0 of 18 like v4, at half the credits. A transcription measures recognition, not how a voice sounds, and the CapCut transcripts read like phonetic spelling, so the transcriber may be part of that result.

Vibi's calls differ from a direct call: a job to poll, then a file to fetch. Unit tests in `scripts/test_voice.py` were watched red first and cover the choice of voice per language, a job that fails, one that never ends, a missing key, the old key, and that the key goes to Vibi alone. Version stays 2.0.0: this branch had not shipped.

English: the owner listened to eight English voices speaking one passage of the film, and chose MiniMax Insightful Speaker. All eight transcribed with no wrong word, so the choice was by ear. Through Vibi, MiniMax waited 5 to 7 seconds and ElevenLabs 22 to 181 while two agents also ran, and the same passage ran 13.5 to 20 seconds by voice.

**First full films by agents, real voice, render, PASS re-run by the scorer.** Haiku in Vietnamese: 92.0s, 13 of 19 lines give a reason, 3 IDs left out. Sonnet in English on Flash Sarah, before the choice above: 78.4s, 12 of 18, 3 left out.

**The camera, a check and not a rule.** The recipe's camera rule was already in the text, and the Sonnet film still framed "10:00 C" and "held fo". So `judge_world` replays each scene and fails anything on screen cut by the frame, the background it sits inside excepted. Unit tests watched red first. Against every film so far, before any tuning: 22 faults on the Sonnet film the sheet had caught, and 0 on the Haiku recheck, the Haiku Vietnamese film and both hand-made PINWIN films.

`check_video.py --script` runs every script rule before a voice exists. Agents had been paying for a voice, then finding a fault after a render.

**Final text, Haiku, English, the chosen voice, render.** 80.1s, PASS re-run by the scorer, 10 of 16 lines give a reason, 3 IDs left out, no camera fault, and its sheet shows nothing cut. It hit two faults on the way and fixed both: a label too long for its pill, stopped by the render, and a still of 6.2 seconds, which it answered with `then`. It asked for a guide to label widths, because fit errors only appear at preview. Not added: the check names the label.

**Not covered.** A real `/shape --auto --video` through live peers, so the script review by `interpret` and the thin page with `out/uncited.json` have never run. Nobody but the owner has heard a film. Feature, PR and release films were not re-run on Vibi: they share `voice.py`, and their footage path did not change.

## 3.0.0: one look, and things change on the word (2026-11-04)

The owner found the films monotonous, and pointed at a site's look and at a film whose motion they wanted. They saw a throwaway re-staging of one passage, moved its parts about, and chose it. Then they reversed the rule that a project's film follows its design system: one look on every film, and the project's only when asked.

**RED, 2.0.0, on the repo with an Approved design-tokens file.** Same request, one run each, scored from the files. Sonnet and Haiku both filled the tokens from `web/tokens.css` and dropped the fonts because "the standard requires" the system stack. Both made about one change a line (1.00 and 1.08), and 13 of 13 and 8 of 12 world lines ran past 9 words on one state, longest 18 and 16.

**The measure of a hold, three tries.** `freezedetect` passes anything that drifts, and the new template never stops drifting. A mean over the frame came next, calibrated on the films to hand, and it failed in use: a label changing did not count, so one Haiku run added seats sliding and notes shifting to pass it, and it passed two films that held for nearly 7 seconds. What ships counts pixels that changed between the two bands, at 640 wide. Thresholds of 40 to 160 pixels move the answer by under a second on every film:

| Film | Longest hold at 80 pixels |
|---|---|
| The owner's reference film | 2.7s |
| The approved look | 2.2s |
| The sample through the template | 3.1s |
| The old rebooking film, an agent's on 2.0.0 | 5.3s |
| PINWIN, by hand on 2.0.0 | 8.1s |

The limit on a spec film is 4.5 seconds, and the closing line may rest, since it is the one place a film stops to let its last words land. The word limit came second: 12 words passed the script and then failed the render, since 8 words after a last change held 3.7 seconds, so it is 9 (14 in Vietnamese, about 3.5 tokens a second on this voice).

**GREEN, 3.0.0, Haiku, three full films.** The agents stopped before the voice, because their sandbox has no `VIBI_API`. The scorer spoke the lines, and the same agents went on through preview, render and check. The scorer re-ran each check.

| Run | Look | Changes a line | Lines past the limit | Length | Longest hold | Check |
|---|---|---|---|---|---|---|
| English | template, untouched | 2.77 | 0 of 13 | 68.2s | 4.2s | PASS |
| Vietnamese | template, untouched | 3.08 | 0 of 12 | 73.8s | 4.3s | PASS |
| `--project-style` | `web/tokens.css`, `cut` 0, `spectrum` [] | 2.57 | 0 of 14 | 76.5s | 4.2s | PASS |

Sonnet on the same request before the word limit tightened: template untouched, 1.77 changes a line. It was not re-run at 9 words.

Faults the agents hit and fixed themselves: a label too long, which the render stopped by name; a row overlapping two code objects, seen on the sheet; a hold of 5.1 seconds answered with more changes. The Vietnamese run met the pixel measure at a hold of 4.6 seconds and fixed it with state changes on the words, with nothing sliding. Diacritics draw correctly in both fonts, in the frames and on the sheet.

`shape` 1.6.0: a shape check, Haiku reading `auto.md` for three commands, got film, language, look and spec language right on all three, citing the new sentences.

**Not covered.** `--project-style` through a real `/shape --auto --video`, which has still never run through live peers. The project film kept the moves its agent added against the old measure, so it shows more sliding than the text now needs. Nobody but the owner can hear the sound layer: the bed and the hits are synthesized, and only their levels are measured. Gauges, bar charts and photographs, which the reference film has, were not built, and neither was a way for an agent to write its own scene. Feature, PR and release films were not re-run: they share the look and the check, and `clip` keeps its 6-second limit. A Haiku story still let Lan come "back in time" after her hold expired, against the recipe's rule, and no check sees that.
