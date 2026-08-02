"""Structural validator for codebase/map — pack-only helper for SDOC tests."""

from __future__ import annotations

import re
from typing import List, Tuple

REQUIRED_HEADINGS = [
    "## Purpose and boundary",
    "## Top-level layout",
    "## Placement rules",
    "## Not spine / not feature registry",
]

PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|lorem)\b|\.\.\.", re.I)
NONE_LINE_RE = re.compile(r"^None\s*[—\-]\s*\S+", re.M)
STATUS_APPROVED_RE = re.compile(r"^Status:\s*Approved\s*$", re.M)
BLOCKER_RE = re.compile(r"^(?:\*\*)?Blocker:\s*(.+?)\s*(?:\*\*)?$", re.M | re.I)
RESOLVED_RE = re.compile(r"^(?:\*\*)?Resolved:\s*(.+?)\s*(?:\*\*)?$", re.M | re.I)
STRIKE_BLOCKER_RE = re.compile(r"~~.*Blocker:.*~~", re.I)


def _section_body(text: str, heading: str) -> str:
    parts = text.split("\n")
    try:
        i = next(n for n, line in enumerate(parts) if line.strip() == heading)
    except StopIteration:
        return ""
    body: List[str] = []
    for line in parts[i + 1 :]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body).strip()


def _has_table_with_data(body: str) -> bool:
    rows = [ln for ln in body.splitlines() if ln.strip().startswith("|")]
    # header + separator + ≥1 data, or header + data without separator
    data_rows = [
        r
        for r in rows
        if not re.match(r"^\|\s*---", r)
        and not re.match(r"^\|\s*Path\s*\|", r, re.I)
        and not re.match(r"^\|\s*-+\s*\|", r)
    ]
    # count non-separator rows; need ≥2 (header + data) or header-like + data
    non_sep = [r for r in rows if not re.match(r"^\|[\s\-:|]+\|$", r.replace(" ", ""))]
    non_sep = [r for r in rows if not re.match(r"^\|\s*:?-{3,}", r)]
    return len(non_sep) >= 2


def validate_codebase_map(text: str) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    for h in REQUIRED_HEADINGS:
        if h not in text:
            reasons.append(f"missing heading: {h}")

    purpose = _section_body(text, "## Purpose and boundary")
    if "## Purpose and boundary" in text:
        if not purpose or (
            not NONE_LINE_RE.search(purpose) and len(purpose) < 1
        ):
            reasons.append("purpose incomplete")
        elif not purpose:
            reasons.append("purpose empty")

    layout = _section_body(text, "## Top-level layout")
    if "## Top-level layout" in text:
        if not (NONE_LINE_RE.search(layout) or _has_table_with_data(layout)):
            reasons.append("layout incomplete (need table with data row or None — reason)")

    placement = _section_body(text, "## Placement rules")
    if "## Placement rules" in text:
        if not placement:
            reasons.append("placement empty")
        elif not NONE_LINE_RE.search(placement):
            # need at least one bullet or non-empty paragraph
            bullets = [ln for ln in placement.splitlines() if ln.strip().startswith(("-", "*"))]
            if not bullets and len(placement.strip()) < 3:
                reasons.append("placement incomplete")

    disclaimer = _section_body(text, "## Not spine / not feature registry")
    if "## Not spine / not feature registry" in text and not disclaimer:
        reasons.append("disclaimer empty")

    # placeholders in required bodies
    for h in REQUIRED_HEADINGS:
        body = _section_body(text, h)
        if body and PLACEHOLDER_RE.search(body):
            reasons.append(f"forbidden placeholder in {h}")

    # blockers
    blockers = [m.group(1).strip() for m in BLOCKER_RE.finditer(text)]
    resolved = {m.group(1).strip() for m in RESOLVED_RE.finditer(text)}
    for b in blockers:
        # skip if struck in same file roughly
        if STRIKE_BLOCKER_RE.search(text):
            continue
        if b not in resolved:
            reasons.append(f"unresolved blocker: {b}")

    if not STATUS_APPROVED_RE.search(text):
        reasons.append("missing Status: Approved")

    return (len(reasons) == 0, reasons)
