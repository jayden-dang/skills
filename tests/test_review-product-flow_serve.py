"""`review-product-flow serve` — the optional loopback layer, and its shutdown contract.

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
CLI = REPO / "skills" / "acceptance" / "review-product-flow" / "scripts" / "review-product-flow"
FIXTURE = (
    REPO / "tests" / "run-product-walkthrough" / "fixtures" / "notes-app" / "notes-review-product-flow.json"
)


def load_walk_product_module():
    spec = importlib.util.spec_from_loader(
        "walk_product_cli", importlib.machinery.SourceFileLoader("walk_product_cli", str(CLI))
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
        self.mod = load_walk_product_module()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)
        self.path = self.dir / "notes-review-product-flow.json"
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
        self.assertIn("window.__WALK PRODUCT__", page)

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

    def test_a_malformed_content_length_is_refused_not_crashed_on(self):
        """DFSYNC-2.6 — a bad or oversized body length is a 4xx, never an unbounded read."""
        _, base = self.start_server()
        before = self.path.read_text(encoding="utf-8")
        host, port = base.rsplit(":", 1)[0].split("//")[1], int(base.rsplit(":", 1)[1])

        for header, expected in (("not-a-number", 400), (str(10 * 1024 * 1024), 413)):
            with self.subTest(content_length=header):
                conn = socket.create_connection((host, port), timeout=5)
                conn.sendall(
                    (
                        "POST /human/CASE-1 HTTP/1.1\r\n"
                        f"Host: {host}\r\n"
                        "Content-Type: application/json\r\n"
                        f"Content-Length: {header}\r\n\r\n"
                    ).encode("ascii")
                )
                status = int(conn.recv(64).decode("latin-1").split()[1])
                conn.close()
                self.assertEqual(expected, status)
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


class ShutdownTests(ServeTestBase):
    """The stop contract.

    A pidfile records a PID the operating system may since have handed to an
    unrelated process, and `kill -0` cannot tell the difference because it answers
    "does this PID exist" — which stays true after a recycle. So the load-bearing
    test here is the recycled-PID one: it fails loudly against any implementation
    that trusts the pidfile. See docs/adr/0007.
    """

    def pidfile(self) -> Path:
        return self.mod.pidfile_path(self.path)

    def write_pidfile(self, pid: int, port: int, token: str) -> Path:
        target = self.pidfile()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps({"pid": pid, "port": port, "token": token, "slug": "notes"}),
            encoding="utf-8",
        )
        return target

    def serve_in_background(self):
        proc = subprocess.Popen(
            [sys.executable, str(CLI), "serve", str(self.path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=str(REPO),
        )
        self.addCleanup(lambda: (proc.kill(), proc.wait()))
        # Ready means *this* process has written the pidfile — not merely that a
        # pidfile exists, which a stale one already satisfies.
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if self.pidfile().is_file():
                try:
                    info = json.loads(self.pidfile().read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    info = None
                if info and info.get("pid") == proc.pid:
                    return proc, info
            if proc.poll() is not None:
                self.fail(f"serve exited early: {proc.communicate()}")
            time.sleep(0.05)
        self.fail("serve never wrote its own pidfile")

    def stop(self, check: bool = False):
        return subprocess.run(
            [sys.executable, str(CLI), "serve", str(self.path), "--stop"],
            capture_output=True, text=True, cwd=str(REPO), check=check,
        )

    def test_the_url_is_visible_while_the_server_is_still_running(self):
        """DFSYNC-5.2 — the bound URL reaches a redirected stdout before the process ends.

        The documented usage is an agent launching this in the background with
        output redirected, and Python buffers stdout when it is not a tty. Since
        serve_forever() never returns, an unflushed URL is a URL nobody ever sees
        — the requirement is to print it, and printing it into a buffer that
        outlives the reader's need for it does not count.
        """
        out = self.dir / "serve.out"
        with out.open("w") as sink:
            proc = subprocess.Popen(
                [sys.executable, str(CLI), "serve", str(self.path)],
                stdout=sink, stderr=subprocess.DEVNULL, text=True, cwd=str(REPO),
            )
        self.addCleanup(lambda: (proc.kill(), proc.wait()))

        deadline = time.monotonic() + 10
        seen = ""
        while time.monotonic() < deadline:
            seen = out.read_text(encoding="utf-8")
            if "127.0.0.1" in seen:
                break
            if proc.poll() is not None:
                self.fail(f"serve exited early: {seen}")
            time.sleep(0.1)

        self.assertIn("127.0.0.1", seen, "the URL never reached stdout while running")
        self.assertIsNone(proc.poll(), "it must still be serving when the URL appears")

    def test_pidfile_records_pid_port_and_instance_token(self):
        """DFSYNC-5.6 — the pidfile carries everything a safe stop needs."""
        proc, info = self.serve_in_background()
        self.assertEqual(proc.pid, info["pid"])
        self.assertIsInstance(info["port"], int)
        self.assertTrue(info["token"])
        self.assertEqual(
            self.pidfile().name, "notes-review-product-flow-serve.pid", "pidfile is named per slug"
        )
        status, body = get(f"http://127.0.0.1:{info['port']}/whoami")
        self.assertEqual(info["token"], json.loads(body)["token"])

    def test_background_launch_returns_control_to_the_caller(self):
        """DFSYNC-5.7 — the server keeps running while the caller carries on."""
        proc, info = self.serve_in_background()
        self.assertIsNone(proc.poll(), "serve must still be running")
        self.assertEqual(200, get(f"http://127.0.0.1:{info['port']}/state")[0])

    def test_stop_terminates_only_on_a_token_match(self):
        """DFSYNC-6.1 — --stop verifies /whoami before it signals anything."""
        proc, info = self.serve_in_background()
        cp = self.stop()
        self.assertEqual(0, cp.returncode, cp.stderr)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and proc.poll() is None:
            time.sleep(0.05)
        self.assertIsNotNone(proc.poll(), "server should have stopped")
        self.assertFalse(self.pidfile().exists())

    def test_stop_never_kills_a_recycled_pid(self):
        """DFSYNC-6.2 — a pidfile pointing at an unrelated live process kills nothing."""
        victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
        self.addCleanup(lambda: (victim.kill(), victim.wait()))
        self.write_pidfile(pid=victim.pid, port=free_port(), token="stale-token")

        cp = self.stop()
        self.assertEqual(0, cp.returncode, cp.stderr)
        self.assertIsNone(victim.poll(), "an unrelated process was killed")
        self.assertFalse(self.pidfile().exists(), "the stale pidfile should be cleaned")
        self.assertIn("gone", (cp.stdout + cp.stderr).lower())

    def test_stop_refuses_when_the_token_disagrees(self):
        """DFSYNC-6.2 — a live server answering with a different token is not ours to kill."""
        proc, info = self.serve_in_background()
        self.write_pidfile(pid=info["pid"], port=info["port"], token="not-the-token")
        cp = self.stop()
        self.assertEqual(0, cp.returncode, cp.stderr)
        self.assertIsNone(proc.poll(), "a server we cannot identify must be left alone")

    def test_serve_cleans_a_stale_pidfile_without_signalling(self):
        """DFSYNC-6.3 — startup applies the same verification to an existing pidfile."""
        victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
        self.addCleanup(lambda: (victim.kill(), victim.wait()))
        self.write_pidfile(pid=victim.pid, port=free_port(), token="stale-token")

        proc, info = self.serve_in_background()
        self.assertIsNone(victim.poll(), "startup must not signal the recorded pid")
        self.assertNotEqual("stale-token", info["token"])
        self.assertEqual(proc.pid, info["pid"])

    def test_termination_has_no_path_other_than_explicit_stop(self):
        """DFSYNC-6.5 — the CLI signals a process only from the --stop branch."""
        source = CLI.read_text(encoding="utf-8")
        kills = [ln.strip() for ln in source.splitlines() if "os.kill" in ln]
        self.assertEqual(1, len(kills), f"expected exactly one kill site, got {kills}")
        stop_fn = source.split("def cmd_serve_stop", 1)
        self.assertEqual(2, len(stop_fn), "the kill must live in the stop branch")
        self.assertIn("os.kill", stop_fn[1].split("\ndef ", 1)[0])

    def test_mark_result_is_identical_with_and_without_a_server(self):
        """DFSYNC-3.6 — mark behaves the same whether or not serve is running."""
        def mark():
            return subprocess.run(
                [sys.executable, str(CLI), "mark", str(self.path), "CASE-1", "pass",
                 "--saw", "list shows Alpha", "--server", "GET /api/notes includes Alpha"],
                capture_output=True, text=True, cwd=str(REPO),
            )

        pristine = self.path.read_text(encoding="utf-8")
        offline = mark()
        without_server = self.read()

        self.path.write_text(pristine, encoding="utf-8")
        self.serve_in_background()
        online = mark()
        with_server = self.read()

        self.assertEqual(offline.returncode, online.returncode)
        self.assertEqual(offline.stdout, online.stdout)
        self.assertEqual(without_server, with_server)


if __name__ == "__main__":
    unittest.main()
