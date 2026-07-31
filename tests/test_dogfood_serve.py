"""`dogfood serve` — the optional loopback layer, and its shutdown contract.

The server is driven through real HTTP against a real bound socket. Nothing here
mocks the transport: the point of most of these assertions is what the socket is
bound to and what the process does when told to stop, and a mock would answer
neither.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLI = REPO / "skills" / "acceptance" / "dogfood" / "scripts" / "dogfood"
FIXTURE = (
    REPO / "tests" / "drive-dogfood" / "fixtures" / "notes-app" / "notes-dogfood.json"
)


def load_dogfood_module():
    spec = importlib.util.spec_from_loader(
        "dogfood_cli", importlib.machinery.SourceFileLoader("dogfood_cli", str(CLI))
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_cases(doc: dict):
    for section in doc["sections"]:
        for case in section["cases"]:
            yield case


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def get(url: str, timeout: float = 5.0):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8")


def post(url: str, payload: dict, timeout: float = 5.0):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


class ServeTestBase(unittest.TestCase):
    def setUp(self):
        self.mod = load_dogfood_module()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)
        self.path = self.dir / "notes-dogfood.json"
        self.path.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")

    def read(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def case(self, case_id: str) -> dict:
        for c in iter_cases(self.read()):
            if c["id"] == case_id:
                return c
        raise KeyError(case_id)

    def start_server(self, token: str = "test-token"):
        server = self.mod.bind_server(self.path, token=token)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(lambda: (server.shutdown(), server.server_close()))
        return server, f"http://127.0.0.1:{server.server_address[1]}"


class ServeTests(ServeTestBase):
    def test_binds_the_loopback_interface_only(self):
        """DFSYNC-5.1, DFSYNC-7.2 — the writable endpoint is not reachable off this machine."""
        server, _ = self.start_server()
        self.assertEqual("127.0.0.1", server.server_address[0])

        # Nothing is listening on this host's routable address.
        routable = socket.gethostbyname(socket.gethostname())
        if routable != "127.0.0.1":
            with socket.socket() as probe:
                probe.settimeout(1.0)
                self.assertNotEqual(
                    0,
                    probe.connect_ex((routable, server.server_address[1])),
                    "server answered on a non-loopback address",
                )

    def test_no_bind_host_is_configurable(self):
        """DFSYNC-5.1 — there is no flag that could expose the endpoint to a network."""
        cp = subprocess.run(
            [sys.executable, str(CLI), "serve", "--help"],
            capture_output=True, text=True, cwd=str(REPO),
        )
        self.assertEqual(0, cp.returncode)
        self.assertNotIn("--host", cp.stdout)
        self.assertNotIn("--bind", cp.stdout)

    def test_default_port_then_the_next_free_one(self):
        """DFSYNC-5.2 — 8787 by default, stepping up when it is taken."""
        self.assertEqual(8787, self.mod.DEFAULT_PORT)
        blocker = socket.socket()
        blocker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        blocker.bind(("127.0.0.1", self.mod.DEFAULT_PORT))
        blocker.listen(1)
        self.addCleanup(blocker.close)
        server, _ = self.start_server()
        self.assertGreater(server.server_address[1], self.mod.DEFAULT_PORT)

    def test_one_process_serves_the_guide_and_the_state(self):
        """DFSYNC-5.3 — the page and the run state come from the same server."""
        _, base = self.start_server()
        status, page = get(base + "/")
        self.assertEqual(200, status)
        self.assertIn("window.__DOGFOOD__", page)

        status, body = get(base + "/state")
        self.assertEqual(200, status)
        state = json.loads(body)
        self.assertIn("rev", state)
        self.assertEqual(
            {c["id"] for c in iter_cases(self.read())}, set(state["cases"])
        )

    def test_a_tick_posted_over_http_reaches_the_run_file(self):
        """DFSYNC-5.5 — a human tick persists into the run file's human field."""
        _, base = self.start_server()
        status, _ = post(base + "/human/CASE-2", {"checked": True, "comment": "looked fine"})
        self.assertEqual(200, status)
        case = self.case("CASE-2")
        self.assertTrue(case["human"]["checked"])
        self.assertEqual("looked fine", case["human"]["comment"])
        self.assertTrue(case["human"]["at"], "a tick records when it happened")

    def test_a_tick_never_moves_a_verdict(self):
        """DFSYNC-2.6 — the tick route cannot reach the verdict field space."""
        _, base = self.start_server()
        post(base + "/human/CASE-2", {"checked": True})
        self.assertEqual("pending", self.case("CASE-2")["run"]["verdict"])

    def test_verdict_bearing_keys_are_refused(self):
        """DFSYNC-2.6 — writing verdict/saw/server/notes over HTTP is a 4xx no-op."""
        _, base = self.start_server()
        before = self.path.read_text(encoding="utf-8")
        for key in ("verdict", "saw", "server", "notes"):
            with self.subTest(key=key):
                status, _ = post(
                    base + "/human/CASE-1", {"checked": True, key: "smuggled"}
                )
                self.assertEqual(400, status)
        self.assertEqual(before, self.path.read_text(encoding="utf-8"))

    def test_unknown_case_is_refused(self):
        """DFSYNC-2.6 — a tick for a case that does not exist changes nothing."""
        _, base = self.start_server()
        before = self.path.read_text(encoding="utf-8")
        status, _ = post(base + "/human/CASE-999", {"checked": True})
        self.assertEqual(404, status)
        self.assertEqual(before, self.path.read_text(encoding="utf-8"))

    def test_a_marked_verdict_appears_in_state_within_the_budget(self):
        """DFSYNC-7.1 — a verdict written by mark is visible to the page within 3 seconds."""
        _, base = self.start_server()
        deadline = time.monotonic() + 3.0
        subprocess.run(
            [sys.executable, str(CLI), "mark", str(self.path), "CASE-1", "pass",
             "--saw", "list shows Alpha", "--server", "GET /api/notes includes Alpha"],
            capture_output=True, text=True, cwd=str(REPO), check=True,
        )
        seen = None
        while time.monotonic() < deadline:
            state = json.loads(get(base + "/state")[1])
            seen = state["cases"]["CASE-1"]["verdict"]
            if seen == "pass":
                break
            time.sleep(0.05)
        self.assertEqual("pass", seen)

    def test_whoami_reports_the_instance_token(self):
        """DFSYNC-5.6 — the server identifies itself, which is what makes shutdown safe."""
        _, base = self.start_server(token="abc123")
        status, body = get(base + "/whoami")
        self.assertEqual(200, status)
        payload = json.loads(body)
        self.assertEqual("abc123", payload["token"])
        self.assertEqual("notes", payload["slug"])
        self.assertIn("pid", payload)


if __name__ == "__main__":
    unittest.main()
