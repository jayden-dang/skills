"""Static contract assertions over the walk-product guide shell.

These are file-read checks, in the style of the repo's other skill-body contract
tests, and in the spirit ARCH-1 asks of a vertical check: fixed extraction rules,
no judgment. They prove properties of the shipped source — that the offline
branch makes no network call, that no case-supplied value reaches the document
unescaped, that the tick path and both colour schemes survive.

What they do not prove is runtime behavior in a real browser: that a click fires
a POST, that a poll repaints. That half belongs to `validate-ui`, which owns
browser-harness setup; this repo records `Browser E2E: (none)` today. The gap is
deliberate and written down rather than papered over.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHELL = REPO / "skills" / "acceptance" / "walk-product" / "shell" / "guide.html"

NETWORK_PRIMITIVES = ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon")

# Functions allowed to touch the network. Each must be unreachable unless LIVE,
# which `test_live_only_functions_are_guarded` checks separately — the two
# assertions together are what DFSYNC-4.2 actually needs: not "no fetch in the
# file", but "no fetch reachable from a file:// page".
LIVE_ONLY_FUNCTIONS = ("startLive", "postTick")


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

    def test_network_primitives_stay_in_live_only_functions(self):
        """DFSYNC-4.2 — no network primitive sits outside the live-only functions."""
        outside = self.js
        for name in LIVE_ONLY_FUNCTIONS:
            body = function_body(self.js, name)
            if body:
                outside = outside.replace(body, "")
        offenders = [p for p in NETWORK_PRIMITIVES if p in outside]
        self.assertEqual(
            [],
            offenders,
            f"network primitives outside {list(LIVE_ONLY_FUNCTIONS)}: {offenders}",
        )

    def test_live_only_functions_are_guarded(self):
        """DFSYNC-4.2 — every call site of a network-touching function is behind LIVE.

        This is the half that makes the previous test mean something: a function
        can hold all the fetches in the world as long as a file:// page can never
        reach it.
        """
        for name in LIVE_ONLY_FUNCTIONS:
            body = function_body(self.js, name)
            if not body:
                continue
            source_without_definition = self.js.replace(body, "")
            call_sites = [
                m.start()
                for m in re.finditer(re.escape(name) + r"\s*\(", source_without_definition)
                if not source_without_definition[: m.start()].rstrip().endswith("function")
            ]
            self.assertTrue(call_sites, f"{name}() is never called")
            for pos in call_sites:
                # the guard is either the enclosing `if (LIVE)` or an explicit
                # LIVE branch within ~200 chars before the call
                window = source_without_definition[max(0, pos - 200) : pos]
                self.assertIn(
                    "LIVE",
                    window,
                    f"{name}() called without a LIVE guard near offset {pos}",
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
        self.assertIn('walk-product-ticks:', self.js)
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

    def test_every_chip_colour_clears_wcag_aa_in_both_schemes(self):
        """DFSYNC-7.5 — kind and verdict chips hold 4.5:1 on their own background.

        Chips render at 0.75rem, which is normal text, so the bar is 4.5 and not
        the 3.0 large-text allowance. This is pinned because it is invisible to
        review: the original palette looked fine and failed on white for every
        single token, and failed on the dark card for `fail`.
        """
        def channels(hex_colour):
            h = hex_colour.lstrip("#")
            return [int(h[i : i + 2], 16) for i in (0, 2, 4)]

        def luminance(hex_colour):
            out = []
            for raw in channels(hex_colour):
                v = raw / 255
                out.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
            return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]

        def ratio(fg, bg):
            a, b = luminance(fg), luminance(bg)
            hi, lo = max(a, b), min(a, b)
            return (hi + 0.05) / (lo + 0.05)

        def scheme_tokens(block: str) -> dict:
            return dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", block))

        dark_block = self.js.split(":root {", 1)[1].split("}", 1)[0]
        light_block = self.js.split("prefers-color-scheme: light", 1)[1].split("}", 1)[0]
        dark = scheme_tokens(dark_block)
        light = dict(dark, **scheme_tokens(light_block))

        chips = [
            "happy", "edge", "error", "nonbehavior", "persist", "visual", "journey",
            "v-pass", "v-fail", "v-blocked", "v-pending",
        ]
        for scheme, tokens in (("dark", dark), ("light", light)):
            card = tokens["card"]
            for chip in chips:
                with self.subTest(scheme=scheme, chip=chip):
                    self.assertIn(chip, tokens, f"--{chip} undefined in {scheme}")
                    got = ratio(tokens[chip], card)
                    self.assertGreaterEqual(
                        round(got, 2),
                        4.5,
                        f"--{chip} on {card} in {scheme} is {got:.2f}:1, below AA 4.5",
                    )

    def test_ticks_are_keyboard_reachable_with_a_visible_focus_ring(self):
        """DFSYNC-7.5 — every tick is a labelled checkbox and focus is visible."""
        self.assertRegex(self.js, r"<label>")
        self.assertRegex(self.js, r'type="checkbox"')
        self.assertRegex(self.js, r":focus-visible")

    def test_snapshot_banner_exists_for_the_offline_mode(self):
        """DFSYNC-4.3 — the page can say its verdicts are a render-time snapshot."""
        self.assertIn("snapshot", self.js.lower())
        self.assertIn("rendered_at", self.js)


class LiveModeContractTests(unittest.TestCase):
    """The http:// branch. Source-level assertions only — see the module docstring."""

    def setUp(self):
        self.js = shell_text()
        self.live = function_body(self.js, "startLive")

    def test_live_branch_exists_and_is_entered_only_under_live(self):
        """DFSYNC-5.4 — the polling client is reachable only when served over HTTP."""
        self.assertTrue(self.live, "startLive() not found in the shell")
        self.assertRegex(self.js, r"if\s*\(\s*LIVE\s*\)\s*\{?\s*startLive\(\)")

    def test_live_branch_polls_state_on_an_interval(self):
        """DFSYNC-5.4 — the page follows the run without the person reloading."""
        self.assertIn("/state", self.live)
        self.assertRegex(self.live, r"setInterval\(")
        self.assertRegex(self.live, r"\brev\b")

    def test_poll_interval_meets_the_three_second_budget(self):
        """DFSYNC-7.1 — the interval leaves room inside the visibility target."""
        match = re.search(r"setInterval\([^,]+,\s*(\d+)\s*\)", self.live)
        self.assertIsNotNone(match, "no literal poll interval found")
        self.assertLessEqual(int(match.group(1)), 3000)

    def test_live_ticks_post_and_do_not_write_localstorage(self):
        """DFSYNC-5.5 — under HTTP a tick goes to the server, not to browser storage."""
        self.assertIn("/human/", self.js)
        self.assertRegex(self.js, r'method:\s*"POST"')
        save = function_body(self.js, "saveTicks")
        self.assertNotIn("/human/", save, "the offline saver must not post")
        # the change handler has to branch, or one of the two paths is dead
        handler = self.js.split("root.addEventListener", 1)[1][:1200]
        self.assertIn("LIVE", handler)

    def test_live_failure_does_not_take_the_page_down(self):
        """DFSYNC-5.4 — a dropped server leaves the guide readable rather than broken."""
        self.assertRegex(self.live, r"\.catch\(|try\s*\{")


if __name__ == "__main__":
    unittest.main()
