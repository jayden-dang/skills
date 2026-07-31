# HTML packet constraints

WHEN filling or validating `shell/packet.html`, read this file and follow it
exactly.

- One continuous page; TOC → Background, Intuition, Code, Quiz.
- **Offline:** no required CDN fonts, scripts, or images.
- Code blocks: `<pre><code>` with CSS `white-space: pre` or `pre-wrap`.
- Primary Intuition figures: HTML/CSS (or inline SVG) — **not** ASCII as primary.
- Quiz: interactive click feedback; visible `:focus-visible`; correctness not by color alone (include text label Correct/Incorrect).
- Escape all repo-derived text for HTML/JS contexts before inject.
- Fill `shell/packet.html`; replace `/* __PACKET_DATA__ */` / set `window.__PACKET__` with JSON-safe content — do not rewrite the quiz JS shell each run.
