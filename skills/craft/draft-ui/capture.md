# Capturing a variant's screen

Capture the variant's **own page or window**, never the screen or a region of
it. A region grab taken from window coordinates once captured a different
app's window on the owner's screen instead of the draft, and the image had to
be deleted unread. Stop anything you started by its PID, never by a pattern:
`pkill -f "vite dev"` stops every matching dev server on the machine, the
owner's included.

Save captures outside the repo's tracked tree (or in a path the cleanup
deletes), in a directory of this run's own — the one your caller names for
captures when it names one, else `SHOTS=$(mktemp -d /tmp/draft-shots.XXXXXX)` —
one per variant, named `<key>-<name>.png`. Three drafts run at once in one fixed
`/tmp/draft-shots` each saw the others' captures beside their own. Then open each image with
your file-reading tool. A capture you did not open is not a look.

## Browser

Serve the draft, then per variant:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --window-size=1280,860 --virtual-time-budget=4000 \
  --screenshot=$SHOTS/a-wide-plan.png "http://127.0.0.1:5180/?variant=a"
```

On Linux the binary is `google-chrome` or `chromium`. A width under 500 crops a
wider layout instead of reflowing it; for a narrow screen, emulate the
viewport through `agent-browser` (`set viewport`) or the DevTools protocol.

## Recording a walk

Only when the user asked for a video, or the caller passed `--video`: one walk
of the winner on the real screen after the lock (`keep.md` §5), never one per
variant. Write the walk once, before recording: one line per moment, in order
(`reserve M for Jonas → Jonas fitted, M 2→1`). Record it in an `agent-browser`
session of its own, named from the full path of this run's capture directory. A fixed `draft-a` was already in use by a draft running
next to it: one walk clicked into the other run's recording and stopped it.

```sh
S=draft-$(printf %s "$SHOTS" | shasum | cut -c1-8)-walk   # unique to this run
agent-browser --session $S open "http://127.0.0.1:5341/gear"   # the real screen, after the lock
# sign in now, if the app asks, so the video starts on the screen itself
agent-browser --session $S set viewport 1440 900
agent-browser --session $S record start $SHOTS/walk.mp4 --cursor --contact-sheet \
  --contact-sheet-threshold 0.01            # a badge or toast changes ~1% of the frame
agent-browser --session $S snapshot -i      # fresh refs before every action
agent-browser --session $S click @e12       # one moment's action, as the user would
agent-browser --session $S wait 1500        # long enough for a viewer to see the result
# …next moment: snapshot, act, wait…
agent-browser --session $S record stop      # writes walk.mp4 and walk.contact-sheet.png
agent-browser --session $S close            # your own sessions, by name; never `close --all`
```

`close --all` once closed a session belonging to a draft running beside it.

Use a fresh snapshot before each action: after the screen changes, an old ref can
point at an element that is now covered.

A step that fails still leaves a saved video. In one trial walk a click landed
on a covering element, the command printed `✗`, and the mp4 saved anyway.
Read every command's output, then open the contact sheet: each moment's result
must appear on it. At the default threshold (0.05) one sheet skipped a reserve and a
cancel whose only change was a row label. If a result is missing, fix the cause and record the walk
again; if you cannot, name that moment unrecorded.

## macOS native app

Launch the variant in the background, keep its PID, wait for the first frame,
find that PID's window, capture the window by ID:

```sh
TIDEBOOK_VARIANT=b .build/debug/Tidebook >$SHOTS/b.log 2>&1 &
PID=$!; sleep 4
cat > $SHOTS/winid.swift <<'EOF'
import CoreGraphics
let pid = Int32(CommandLine.arguments[1])!
let all = CGWindowListCopyWindowInfo([.optionAll], kCGNullWindowID) as! [[String: Any]]
for w in all where (w[kCGWindowOwnerPID as String] as? Int32) == pid
    && (w[kCGWindowLayer as String] as? Int) == 0 { print(w[kCGWindowNumber as String]!) }
EOF
WIN=$(swift $SHOTS/winid.swift $PID | head -1)
screencapture -x -o -l "$WIN" $SHOTS/b-dense-list.png
kill $PID
```

Run the built binary, not `swift run` / `cargo run`, so `$!` is the app's PID.
The same holds for a Rust GUI app (`target/debug/<app>`).

## Linux native app (X11)

```sh
WIN=$(xdotool search --pid "$PID" | head -1)
import -window "$WIN" $SHOTS/b-dense-list.png
```

## No window to capture

No window server (a sandbox, CI, SSH), the launch exits, or no window appears
for the PID → the variant is **unseen**. Say so at hand-over with the error or
the log line, and give the owner the launch command; never describe a screen
you did not see.
