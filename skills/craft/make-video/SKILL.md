---
name: make-video
version: 1.0.0
description: Makes a narrated 1080p video of a built feature, a pull request, or a release, from the real code and the running app. Run it with /make-video <feature, branch, or tag>.
disable-model-invocation: true
---

# Make Video

One narrated film, about a minute, built on the Remotion project in `template/`. You write
two files, `src/script.json` and `src/tokens.ts`. The scripts here do the rest. `$SKILL` below
means the folder holding this file.

Seven runs without this skill got the facts right and made slideshows: none was 1080p, none
used Remotion, and most of each film was one still frame with the app small on screen.
The template and `scripts/check_video.py` are the point of this skill.

## The Iron Law

```
NO FILM SHIPS UNTIL check_video.py PRINTS PASS AND YOU HAVE READ ITS CONTACT SHEET
```

| Thought | Reality |
|---|---|
| "Remotion needed an npm install and added nothing here" | Said in a run whose film held one frame for 11.6 seconds. `new_video.py` does the install in about 10 seconds |
| "the video is only four stills with narration" | Four stills is the failure. A `clip` scene moves the camera on every line |
| "ffmpeg here has no drawtext, so there are no on-screen captions" | The template draws captions. Five of the seven films had none |

## 1. Pin what the film shows

The film shows one commit. Bind it to `$REF` and write it to `source.ref`.

| Request names | `source.kind` | `$REF` | Run the app from |
|---|---|---|---|
| A feature | `feature` | current `HEAD` | a temporary worktree at `$REF` |
| A branch or range | `pr` | the branch head; film the base too when the change is a before and after | one temporary worktree for each |
| A version | `release` | the tag | a temporary worktree at the tag |

```bash
git worktree add --detach "$(mktemp -d)/app" "$REF"
```

One release run filmed `main`, which showed a change made after the tag. Another deleted a CSS
line by hand to imitate the tag. The worktree needs neither.

A subject with no code yet is out of scope: stop and say so.

*Done when: `$REF` resolves with `git rev-parse` and each worktree exists.*

## 2. Start the project and match the project's look

```bash
python3 "$SKILL/scripts/new_video.py" . <slug>
```

It prints the project path, under `.skills/video/`. Fill every value in `src/tokens.ts` from the
repo's design tokens and name that file in its `Source:` comment. Find them through
`docs/standards/`, `docs/agents/`, then any theme or tokens file. A repo with none keeps the
template's values, and your report says so.

*Done when: `Source:` names a file, or your report will say there is none.*

## 3. Write the script

Narration and captions are in English, and `language` stays `en`. Use another language only when
the request names one. A request written in Vietnamese with no language named still gets English:
the one run given that request narrated in Vietnamese because "the team and route names are
Vietnamese".

Every beat is one spoken line, 20 words at most, with a `ref`: a repo-relative `file:line` you
opened at `$REF`, or the run output that showed it.

| `kind` | Use it for | Slots |
|---|---|---|
| `title` | The opening and the closing line | `title`, optional `subtitle` |
| `clip` | Anything the app shows | each beat may set `clip`, `rate`, `focus`, `ring` |
| `flow` | Several things meeting in one result | `title`, `sources`, `target`, optional `note` |
| `points` | What changed, or what it does not do | `title`, `points` |

A `flow` or `points` item appears when its matching beat starts.

*Done when: `src/script.json` opens with a `title` scene and ends on one.*

## 4. Speak it

```bash
python3 "$SKILL/scripts/voice.py" <project>
```

It prints each line's length. Those lengths time your recording. Three of ten runs recorded first,
then failed the check on a still of up to 8.5 seconds or a silence of up to 6, and had to redo it.

`voice.py` uses the machine's `say`, so no text leaves the machine. Add `--engine elevenlabs` only
when the request asks for it and a key is in the environment. It sends the script to that vendor,
and your report says so. Run it again whenever you change a line.

*Done when: it printed a length for every beat.*

## 5. Record the app

Run this when the repo has a way to run the app, usually `docs/agents/verify.md`. With no way to
run it, use graphic scenes only and say so in your report.

```bash
PORT=$(python3 -c 'import socket;s=socket.socket();s.bind(("",0));print(s.getsockname()[1]);s.close()')
<launch command from the run recipe, with this port> & SERVER=$!
lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t      # must print $SERVER or its child before you click anything
agent-browser open "http://localhost:$PORT/"
agent-browser set viewport 1600 900 2       # after open, or it is ignored; 2 keeps zoomed text sharp
agent-browser set media light               # or dark: the scheme src/tokens.ts describes
agent-browser reload
agent-browser get box "<selector>"          # the x, y, width, height for focus and ring
agent-browser record start /tmp/<name>.mp4 --cursor
# drive the flow, waiting between actions for the length voice.py printed for each line
agent-browser record stop
python3 "$SKILL/scripts/add_clip.py" <project> <name> /tmp/<name>.mp4
```

Two runs hit a port someone else's server held. Their own server failed to start, so they clicked
through a stranger's app and wrote alerts into its data, four in one run. The `lsof` line stops that.

**Film the app as it is.** Five runs staged what they filmed: four moved a clock, three of them to
hide a negative countdown, and one painted a box over that column. Only one told its viewers.
Film the behavior the request is about, even when the app only shows it in a state you must set up.
One review film of a night-only change showed the daytime path and only described the change. When
a state must be staged, set `staged` on that scene to a short sentence, such as `Server clock set to
22:55 for this demo`. The film prints it on screen. Prefer real data you created through the app.

Now fill in the `clip` scenes. Every beat sets `focus` to the rect it is talking about, in the page's
CSS pixels, so the camera moves on every line and the thing named fills the frame. Set `ring` on a
control the line tells people to press. Set `clip` once, on the beat where that recording starts,
because a beat with `clip` waits for the clip before it. The beats after it keep playing the same
recording. Use `rate` up to 2 when a recording runs longer than its lines.

```json
{"id": "report", "kind": "clip", "title": "Report a delay", "beats": [
  {"text": "Each sailing has a report delay button.", "ref": "web/app.js:3", "clip": "board",
   "focus": {"x": 28, "y": 62, "w": 1017, "h": 219}, "ring": {"x": 788, "y": 121, "w": 116, "h": 30}},
  {"text": "Press it, and the alert appears on the right.", "ref": "alerts.js:3",
   "focus": {"x": 1063, "y": 62, "w": 509, "h": 219}}
]}
```

*Done when: `add_clip.py` printed `added` for each clip, and each `clip` beat has a `focus`.*

## 6. Render and check

```bash
(cd <project> && npx tsc --noEmit && npx remotion render Film out/film.mp4)
python3 "$SKILL/scripts/check_video.py" <project> . <project>/out/film.mp4 --sheet /tmp/<slug>-sheet.png
```

Read the contact sheet as an image. Fix text cut off by its box, a frame with the subject off
screen, and any `FAIL` line, then render and check again.

*Done when: the check prints `PASS` and the sheet shows no fault.*

## 7. Stop what you started, and report

```bash
kill "$SERVER"
agent-browser close
git worktree remove --force <each temporary worktree>
```

Stop your server by the PID you recorded. Two runs tried a blanket `pkill`, were refused, and left
servers running. Check that nothing still listens on `$PORT`.

Copy the film to the path the request named. Report that path, its length, what it says, the
check result, every `staged` line, and that you have not heard the audio.

## Red Flags

- A film under 1920x1080, or assembled with ffmpeg alone
- A `clip` beat with no `focus`
- A narration language the request did not name
- Clicking before `lsof` showed your own server
- A changed clock, hidden column, or painted box with no `staged` line
- A server still listening after your report
