"""VPF-1.3 VPF-1.4 VPF-8.1 — authored-cases fingerprint and report field contract."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

FIX = Path(__file__).resolve().parent / "vet-product-flow" / "fixtures"
REPO = Path(__file__).resolve().parent.parent
REPORT_SCHEMA = (
    REPO / "skills" / "acceptance" / "vet-product-flow" / "references" / "report-schema.md"
)

# Eight authored case slots only (ASCII sort order for sort_keys=True).
AUTHORED_CASE_KEYS = (
    "backend",
    "expect",
    "id",
    "kind",
    "req",
    "setup",
    "title",
    "try",
)


def cases_fingerprint(doc: dict) -> str:
    """Design recipe: sections → {name, cases[eight slots]}; sort_keys; compact; sha256."""
    sections_out = []
    for section in doc.get("sections") or []:
        cases_out = []
        for case in section.get("cases") or []:
            authored = {key: case[key] for key in AUTHORED_CASE_KEYS}
            cases_out.append(authored)
        sections_out.append({"name": section["name"], "cases": cases_out})
    # Compact JSON; sort_keys orders case slots and section keys (cases, name).
    payload = json.dumps(sections_out, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class TestCasesFingerprint(unittest.TestCase):
    def test_VPF_1_3_fingerprint_stable_when_only_run_human_rev_change(self):
        """VPF-1.3 — fingerprint ignores run/human/rev; authored slots only."""
        a = json.loads((FIX / "minimal-run.json").read_text())
        b = json.loads((FIX / "minimal-run-ticked.json").read_text())
        self.assertEqual(cases_fingerprint(a), cases_fingerprint(b))

    def test_VPF_1_3_fingerprint_changes_when_authored_slot_changes(self):
        """VPF-1.3 — any authored slot edit changes the fingerprint."""
        a = json.loads((FIX / "minimal-run.json").read_text())
        a["sections"][0]["cases"][0]["title"] = "changed"
        base = json.loads((FIX / "minimal-run.json").read_text())
        self.assertNotEqual(cases_fingerprint(a), cases_fingerprint(base))

    def test_VPF_8_1_surface_key_reuses_id_across_two_fixture_reports(self):
        """VPF-8.1 — same surface_key keeps VPF-N on re-check; new key gets next id."""
        r1 = (FIX / "sample-report.md").read_text()
        r2 = (FIX / "sample-report-recheck.md").read_text()
        # Both reports document the same surface_key under the same ### VPF-1
        self.assertIn("surface_key:", r1)
        self.assertIn("### VPF-1", r1)
        self.assertIn("### VPF-1", r2)
        # Extract first surface_key value from each open VPF-1 block — must match
        sk1 = re.search(r"### VPF-1\n.*?surface_key:\s*`([^`]+)`", r1, re.S)
        sk2 = re.search(r"### VPF-1\n.*?surface_key:\s*`([^`]+)`", r2, re.S)
        self.assertIsNotNone(sk1)
        self.assertIsNotNone(sk2)
        self.assertEqual(sk1.group(1), sk2.group(1))
        # Recheck introduces a new finding id not in pass 1 (e.g. VPF-2)
        self.assertRegex(r2, r"### VPF-2\s")

    def test_VPF_1_4_finding_id_integer_namespace_not_criterion_shape(self):
        """VPF-1.4 — finding headers use ### VPF-<int> without .M."""
        text = (FIX / "sample-report.md").read_text()
        self.assertRegex(text, r"### VPF-\d+\s")
        self.assertNotRegex(text, r"### VPF-\d+\.\d+")

    def test_VPF_1_3_report_schema_documents_stamp_fields(self):
        """VPF-1.3 — report-schema.md documents fingerprint + stamp fields."""
        self.assertTrue(REPORT_SCHEMA.is_file(), f"missing {REPORT_SCHEMA}")
        text = REPORT_SCHEMA.read_text()
        for needle in ("cases_fingerprint", "surface_key", "pass_kind", "prior_report"):
            self.assertIn(needle, text, f"report-schema.md must document {needle}")


if __name__ == "__main__":
    unittest.main()
