# Capturing a variant's screen

Capture the variant's **own page or window**, never the screen or a region of
it. A region grab taken from window coordinates once captured a different
app's window on the owner's screen instead of the draft, and the image had to
be deleted unread. Stop anything you started by its PID, never by a pattern:
`pkill -f "vite dev"` stops every matching dev server on the machine, the
owner's included.

Save captures outside the repo's tracked tree (or in a path the cleanup
deletes), in a directory of this run's own — `SHOTS=$(mktemp -d /tmp/draft-shots.XXXXXX)` —
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
