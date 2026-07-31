"""Static contract assertions over the dogfood guide shell.

These are file-read checks, in the style of the repo's other skill-body contract
tests, and in the spirit ARCH-1 asks of a vertical check: fixed extraction rules,
no judgment. They prove properties of the shipped source — that the offline
branch makes no network call, that no case-supplied value reaches the document
unescaped, that the tick path and both colour schemes survive.

What they do not prove is runtime behavior in a real browser: that a click fires
a POST, that a poll repaints. That half belongs to `acceptance-ui`, which owns
browser-harness setup; this repo records `Browser E2E: (none)` today. The gap is
deliberate and written down rather than papered over.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHELL = REPO / "skills" / "acceptance" / "dogfood" / "shell" / "guide.html"

NETWORK_PRIMITIVES = ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon")


def shell_text() -> str:
    return SHELL.read_text(encoding="utf-8")


def function_body(js: str, name: str) -> str:
    """Source of `function <name>( … ) { … }`, brace-matched. '' when absent."""
    match = re.search(r"function\s+" + re.escape(name) + r"\s*\([^)]*\)\s*\{", js)
    if not match:
        return ""
    depth = 0
    start = match.end() - 1
    for i in range(start, len(js)):
        if js[i] == "{":
            depth += 1
        elif js[i] == "}":
            depth -= 1
            if depth == 0:
                return js[start : i + 1]
    return js[start:]


class GuideContractTests(unittest.TestCase):
    def setUp(self):
        self.js = shell_text()

    def test_offline_branch_makes_no_network_call(self):
        """DFSYNC-4.2 — nothing outside the live branch can touch the network.

        A guide opened from file:// must be correct with nothing running, so every
        network primitive has to sit inside the one function the live mode calls.
        """
        live = function_body(self.js, "startLive")
        outside = self.js.replace(live, "") if live else self.js
        offenders = [p for p in NETWORK_PRIMITIVES if p in outside]
        self.assertEqual(
            [],
            offenders,
            f"network primitives reachable outside startLive(): {offenders}",
        )

    def test_live_mode_is_chosen_by_protocol(self):
        """DFSYNC-4.2 — the mode is decided by the URL the page was loaded from."""
        self.assertRegex(self.js, r"location\.protocol")
        self.assertRegex(self.js, r"var\s+LIVE\s*=")

    def test_no_case_value_reaches_the_document_unescaped(self):
        """DFSYNC-4.4 — every case-supplied string is wrapped in an escaper."""
        body = function_body(self.js, "renderCase")
        self.assertTrue(body, "renderCase() not found in the shell")
        raw = re.findall(r"\+\s*(c\.[A-Za-z_$][\w$]*)", body)
        self.assertEqual(
            [], raw, f"case fields concatenated without an escaper: {sorted(set(raw))}"
        )
        self.assertIn("escapeHtml(", body)
        self.assertIn("escapeAttr(", body)

    def test_escapers_cover_the_dangerous_characters(self):
        """DFSYNC-4.4 — the escaper replaces every character that could break out."""
        body = function_body(self.js, "escapeHtml")
        for token in ("&amp;", "&lt;", "&gt;", "&quot;"):
            self.assertIn(token, body)
        self.assertIn("&#39;", function_body(self.js, "escapeAttr"))

    def test_machine_readable_attributes_survive(self):
        """DFSYNC-4.5 — each case element still carries its five data-* attributes."""
        body = function_body(self.js, "renderCase")
        for attr in ("data-case", "data-req", "data-kind", "data-backend", "data-setup"):
            self.assertIn(attr, body)

    def test_offline_ticks_still_use_localstorage_and_can_be_reset(self):
        """DFSYNC-4.6 — the file:// tick path persists locally and keeps its reset control."""
        self.assertIn("localStorage.getItem", self.js)
        self.assertIn("localStorage.setItem", self.js)
        self.assertIn('dogfood-ticks:', self.js)
        self.assertRegex(self.js, r'id="reset"')
        self.assertRegex(self.js, r'getElementById\("reset"\)')

    def test_kind_chip_and_both_colour_schemes_survive(self):
        """DFSYNC-4.9 — the kind chip renders and the page follows the viewer's scheme."""
        self.assertIn("chip", function_body(self.js, "renderCase"))
        self.assertIn("prefers-color-scheme", self.js)
        for kind in ("happy", "edge", "error", "nonbehavior", "persist", "visual", "journey"):
            self.assertIn(f"--{kind}:", self.js, f"no colour token for kind {kind}")

    def test_verdict_badge_is_never_colour_alone(self):
        """DFSYNC-7.5 — the verdict is carried by text, not only by a colour."""
        body = function_body(self.js, "renderCase")
        self.assertRegex(body, r"verdict")
        # the badge prints the verdict word itself, so colour is reinforcement
        self.assertRegex(body, r"escapeHtml\(\s*verdict|escapeHtml\(\s*run\.verdict")

    def test_ticks_are_keyboard_reachable_with_a_visible_focus_ring(self):
        """DFSYNC-7.5 — every tick is a labelled checkbox and focus is visible."""
        self.assertRegex(self.js, r"<label>")
        self.assertRegex(self.js, r'type="checkbox"')
        self.assertRegex(self.js, r":focus-visible")

    def test_snapshot_banner_exists_for_the_offline_mode(self):
        """DFSYNC-4.3 — the page can say its verdicts are a render-time snapshot."""
        self.assertIn("snapshot", self.js.lower())
        self.assertIn("rendered_at", self.js)


if __name__ == "__main__":
    unittest.main()
