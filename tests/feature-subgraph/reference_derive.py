"""Test-side reference implementation of load-subgraph passes.md recipes.

Not shipped under skills/. Agents execute passes.md via the skill; unittests
import this module to lock recipe math.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

NEIGHBORS_MAX = 12
P0_SEED_MAX = 12

MANIFEST_LOCK_BASES = frozenset(
    {
        "package.json",
        "Cargo.toml",
        "go.mod",
        "pyproject.toml",
        "Gemfile",
        "composer.json",
        "Package.swift",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "Cargo.lock",
        "poetry.lock",
        "Gemfile.lock",
        "composer.lock",
    }
)

WORKSPACE_ROOT_SEGMENTS = frozenset(
    {
        "src",
        "lib",
        "app",
        "apps",
        "packages",
        "services",
        "crates",
        "cmd",
        "internal",
        "vendor",
        "node_modules",
        "dist",
        "build",
        "target",
        "out",
        "skills",
        "templates",
        "hooks",
        "scripts",
        "docs",
    }
)

LINE_SUFFIX_RE = re.compile(r":[0-9]+([,-][0-9]+)*$")
CODE_RE = re.compile(r"^[A-Z][A-Z0-9]{1,11}$")
ROAD_RE = re.compile(r"\bROAD-\d+\b")
MILE_RE = re.compile(r"\bMILE-\d+\b")
GOAL_RE = re.compile(r"\bGOAL-\d+\b")
ARCH_RE = re.compile(r"\bARCH-\d+\b")
# path-like tokens: has a slash or a file extension
PATH_TOKEN_RE = re.compile(
    r"`?([A-Za-z0-9_./@+-]+(?:\.[A-Za-z0-9]+)?)`?"
)
BULLET_FILE_RE = re.compile(
    r"^\s*[-*]\s*(?:Create|Modify|Move|Test)\s*:\s*(.+?)\s*$",
    re.I | re.M,
)
BACKTICK_TOKEN_RE = re.compile(r"`([^`\n]+)`")
# Unquoted path-like tokens (no spaces); may include dots/slashes
UNQUOTED_TOKEN_RE = re.compile(
    r"(?<![`\w])(\.?[A-Za-z0-9_@+-]+(?:[./][A-Za-z0-9_@.+-]+)*)(?![`\w])"
)
FILES_HEADER_RE = re.compile(
    r"(?im)(?:^\*\*Files:\*\*[ \t]*$|^\s*Files:[ \t]*$)"
)
# Truncated / mid-line Files without newline after header body
FILES_HEADER_ANY_RE = re.compile(r"(?i)\*\*Files:\*\*|^\s*Files:\s*$", re.M)
INDEX_ROW_RE = re.compile(
    r"^\|\s*([A-Z][A-Z0-9]{1,11})\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|",
    re.M,
)

BROAD_EXTENSIONS = frozenset(
    {
        ".md",
        ".py",
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".mjs",
        ".cjs",
        ".sh",
        ".bash",
        ".zsh",
        ".json",
        ".yml",
        ".yaml",
        ".toml",
        ".lock",
        ".txt",
        ".html",
        ".css",
        ".svg",
        ".rs",
        ".go",
        ".java",
        ".kt",
        ".swift",
        ".rb",
        ".php",
        ".cs",
        ".cpp",
        ".h",
        ".hpp",
        ".sql",
        ".proto",
        ".graphql",
        ".vue",
        ".svelte",
        ".r",
        ".jl",
        ".scala",
        ".clj",
        ".ex",
        ".exs",
        ".erl",
        ".hs",
        ".lua",
        ".pl",
        ".pm",
        ".rake",
        ".gradle",
        ".cmake",
        ".mk",
    }
)

WELL_KNOWN_ROOTS = frozenset(
    {
        "Makefile",
        "Dockerfile",
        "LICENSE",
        "COPYING",
        "NOTICE",
        "AUTHORS",
        "CONTRIBUTING",
        "CHANGELOG",
        "HISTORY",
        "Gemfile",
        "Rakefile",
        "Procfile",
        "Vagrantfile",
    }
)

DOTFILE_RE = re.compile(r"^\.[A-Za-z0-9][A-Za-z0-9._-]*$")
PLAUSIBLE_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._-]+$")
ABS_WIN_RE = re.compile(r"^[A-Za-z]:[\\/]")
TRAILING_PUNCT = frozenset(".,;:)]}")
LABEL_WORDS = frozenset({"Create", "Modify", "Move", "Test", "Files", "also", "touch", "for", "legacy", "prose"})

# Section stop lines outside fences (FSUBR-2.2)
STOP_SECTION_RE = re.compile(
    r"(?i)^(?:"
    r"#{2,6}\s|"
    r"\*\*Files:\*\*|"
    r"Files:\s*$|"
    r"\*\*Reuse:\*\*|"
    r"Reuse:|"
    r"\*\*Interfaces:\*\*|"
    r"Interfaces:|"
    r"\*\*Depends-on:\*\*|"
    r"Depends-on:|"
    r"\*\*Steps|"
    r"Steps\s*:|"
    r"[-*]\s*\[\s*[ xX]?\s*\]\s*\*?\*?Step"
    r")"
)


def _strip_line_suffix(token: str) -> str:
    token = token.strip().strip("`").strip()
    # strip trailing line/range glued to path
    return LINE_SUFFIX_RE.sub("", token)


def denoise(paths: set[str]) -> set[str]:
    out: set[str] = set()
    for p in paths:
        p = p.strip().strip("/")
        if not p:
            continue
        base = Path(p).name
        if base in MANIFEST_LOCK_BASES:
            continue
        if "/" not in p and p in WORKSPACE_ROOT_SEGMENTS:
            continue
        out.add(p)
    return out


def overlap_weight(a: set[str], b: set[str]) -> int:
    return len(denoise(a) & denoise(b))


def load_registry(repo_root: Path) -> list[dict[str, str]]:
    index = repo_root / "docs" / "specs" / "INDEX.md"
    if not index.is_file():
        return []
    text = index.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    for m in INDEX_ROW_RE.finditer(text):
        code, name, spec, status, road = (g.strip() for g in m.groups())
        if code in {"Code", "CODE"}:
            continue
        if not CODE_RE.match(code):
            continue
        spec_dir = spec.strip().strip("./")
        if spec_dir.endswith("/"):
            spec_dir = spec_dir[:-1]
        rows.append(
            {
                "code": code,
                "name": name,
                "spec": spec_dir,
                "status": status,
                "road": road if road not in {"—", "-", "–", ""} else "",
            }
        )
    return rows


def _feature_dir(repo_root: Path, row: dict[str, str]) -> Path | None:
    # INDEX paths are relative to docs/specs/
    p = repo_root / "docs" / "specs" / row["spec"]
    if p.is_dir():
        return p
    # sometimes written as ./2020-...
    p2 = repo_root / "docs" / "specs" / Path(row["spec"]).name
    return p2 if p2.is_dir() else None


def _is_fence_line(line: str) -> bool:
    return line.lstrip().startswith("```")


def _is_stop_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    return bool(STOP_SECTION_RE.match(s)) or bool(
        re.match(r"(?i)^\*\*Files:\*\*", s)
    ) or bool(re.match(r"(?i)^Files:\s*$", s))


def _normalize_candidate(raw: str) -> str:
    """Strip wrappers for inspection: backticks, # comments, glued line suffixes."""
    token = raw.strip()
    if token.startswith("`") and token.endswith("`") and len(token) >= 2:
        token = token[1:-1]
    token = token.strip().strip("`").strip()
    token = token.split("#", 1)[0].strip()
    token = LINE_SUFFIX_RE.sub("", token)
    return token


def _reject_unsafe(token: str) -> bool:
    """True if token must be rejected (unsafe/sentinel) before accept."""
    if not token:
        return True
    if token in {".", ".."}:
        return True
    if "://" in token:
        return True
    low = token.lower()
    if low.startswith("http:") or low.startswith("https:") or low.startswith("file:"):
        return True
    if token.startswith("/") or ABS_WIN_RE.match(token):
        return True
    parts = token.replace("\\", "/").split("/")
    if any(seg == ".." for seg in parts):
        return True
    if token[-1] in TRAILING_PUNCT:
        return True
    return False


def _plausible_path_form(token: str) -> bool:
    if "/" in token:
        return all(seg != "" for seg in token.split("/"))
    if token.startswith(".") and len(token) > 1:
        return True
    if PLAUSIBLE_SEGMENT_RE.match(token) and ".." not in token:
        return True
    return False


def _accept_by_provenance(token: str, provenance: str) -> bool:
    if provenance in {"labeled", "backticked"}:
        return _plausible_path_form(token)
    if provenance == "slash_path":
        if "/" not in token:
            return False
        parts = token.split("/")
        return all(seg != "" for seg in parts)
    if provenance == "unquoted_prose":
        if DOTFILE_RE.match(token):
            return True
        base = Path(token).name
        # basename extension check (also works for single-segment files)
        if "." in base:
            ext = "." + base.rsplit(".", 1)[-1].lower()
            # multi-dot identifiers like self.assertEqual: last "ext" is not in set
            if ext in BROAD_EXTENSIONS:
                return True
        if "/" not in token and "." not in token and token in WELL_KNOWN_ROOTS:
            return True
        return False
    return False


def classify_path_token(raw: str, provenance: str) -> str | None:
    """Return accepted path or None after reject-unsafe-first + provenance + denoise."""
    token = _normalize_candidate(raw)
    if not token:
        return None
    if _reject_unsafe(token):
        return None
    if not _accept_by_provenance(token, provenance):
        return None
    denoised = denoise({token})
    if token not in denoised and token.strip("/") not in denoised:
        # denoise may strip trailing slash; accept the denoise result if singleton
        if len(denoised) == 1:
            return next(iter(denoised))
        return None
    # Prefer original token form when denoise kept it (possibly strip-normalized)
    if token in denoised:
        return token
    if token.strip("/") in denoised:
        return token.strip("/")
    return None


def _extract_candidates_from_body(body: str) -> list[tuple[str, str]]:
    """Return (raw_token, provenance) pairs from a Files body."""
    candidates: list[tuple[str, str]] = []
    labeled_spans: list[tuple[int, int]] = []

    for m in BULLET_FILE_RE.finditer(body):
        raw = m.group(1).strip()
        # prefer backtick-wrapped path on the bullet if present
        bt = BACKTICK_TOKEN_RE.search(raw)
        if bt:
            token = bt.group(1)
            candidates.append((token, "labeled"))
        else:
            # first path-like chunk before trailing prose
            token = raw.split("#", 1)[0].strip()
            # drop leading leftover labels
            if token.lower().startswith("also "):
                continue
            candidates.append((token, "labeled"))
        labeled_spans.append((m.start(), m.end()))

    def _in_labeled(pos: int) -> bool:
        return any(a <= pos < b for a, b in labeled_spans)

    # Backticked tokens not already taken as labeled
    for m in BACKTICK_TOKEN_RE.finditer(body):
        if _in_labeled(m.start()):
            continue
        candidates.append((m.group(1), "backticked"))

    # Mask backticks so unquoted scan does not re-hit them
    masked = list(body)
    for m in BACKTICK_TOKEN_RE.finditer(body):
        for i in range(m.start(), m.end()):
            masked[i] = " "
    masked_body = "".join(masked)

    for m in UNQUOTED_TOKEN_RE.finditer(masked_body):
        if _in_labeled(m.start()):
            continue
        raw = m.group(1)
        if raw in LABEL_WORDS:
            continue
        if raw.lower() in {w.lower() for w in LABEL_WORDS}:
            continue
        if "/" in raw:
            candidates.append((raw, "slash_path"))
        else:
            candidates.append((raw, "unquoted_prose"))

    return candidates


def _iter_files_blocks(text: str) -> list[tuple[int, int, str | None]]:
    """Find Files headers; return list of (header_start, body_start, skip_reason).

    skip_reason is set when header is malformed (not followed by newline content start).
    """
    blocks: list[tuple[int, int, str | None]] = []
    for m in re.finditer(r"(?i)\*\*Files:\*\*|^(?:[ \t]*)Files:[ \t]*$", text, re.M):
        header = m.group(0)
        end = m.end()
        # Header must be followed by newline (block content on subsequent lines)
        # Allow optional spaces then newline; if EOF or non-newline junk without newline → malformed
        rest = text[end:]
        if rest.startswith("\n") or rest.startswith("\r\n"):
            body_start = end + (2 if rest.startswith("\r\n") else 1)
            blocks.append((m.start(), body_start, None))
        elif rest == "" or rest.lstrip(" \t") == "":
            # empty after header at EOF — empty body, not malformed
            blocks.append((m.start(), end, None))
        elif rest.lstrip(" \t")[:1] in {"\n", "\r"}:
            # spaces then newline
            nl = rest.find("\n")
            body_start = end + nl + 1
            blocks.append((m.start(), body_start, None))
        else:
            # truncated header: **Files:**foo without newline
            if "**Files:**" in header or header.strip().lower().startswith("files:"):
                # mid-line content immediately after **Files:** without newline is structural fail
                if not header.strip().endswith(":") and "\n" not in header:
                    blocks.append((m.start(), end, "truncated_header"))
                else:
                    # **Files:** immediately followed by non-space non-newline
                    blocks.append((m.start(), end, "truncated_header"))
            else:
                blocks.append((m.start(), end, "truncated_header"))
    return blocks


def _body_until_stop(text: str, body_start: int) -> tuple[str, int, bool]:
    """Walk from body_start with fence awareness; return (body, stop_index, unclosed_fence)."""
    pos = body_start
    fence_depth = 0
    lines_out: list[str] = []
    n = len(text)

    while pos < n:
        nl = text.find("\n", pos)
        if nl == -1:
            line = text[pos:]
            next_pos = n
        else:
            line = text[pos:nl]
            next_pos = nl + 1

        if _is_fence_line(line):
            # toggle fence; fence line itself is included in body
            fence_depth = 0 if fence_depth else 1
            lines_out.append(line)
            pos = next_pos
            continue

        if fence_depth == 0 and _is_stop_line(line):
            # stop before this line; do not consume it
            return "\n".join(lines_out), pos, False

        lines_out.append(line)
        pos = next_pos

    unclosed = fence_depth != 0
    return "\n".join(lines_out), pos, unclosed


def extract_owns_from_tasks_text(text: str) -> dict[str, Any]:
    """P1 OWNS extract: multi-block, fence-aware, reject-unsafe-first classifier.

    Returns ``{"paths": set[str], "notes": list[dict]}``.
    """
    paths: set[str] = set()
    notes: list[dict[str, Any]] = []
    seen_notes: set[tuple[str, str, str]] = set()

    def _add_note(kind: str, detail: str = "", code: str = "") -> None:
        key = (kind, code, detail)
        if key in seen_notes:
            return
        seen_notes.add(key)
        note: dict[str, Any] = {"kind": kind}
        if code:
            note["code"] = code
        if detail:
            note["detail"] = detail
        notes.append(note)

    blocks = _iter_files_blocks(text)
    if not blocks:
        # No Files headers: legacy whole-text scan is NOT used under FSUBR —
        # OWNS empty when no Files block (first-block-only era scanned whole file
        # only as fallback when split found no header; keep empty for no headers).
        return {"paths": paths, "notes": notes}

    for _header_start, body_start, skip_reason in blocks:
        if skip_reason:
            _add_note("p1_block_skipped", skip_reason)
            continue
        body, _stop, unclosed = _body_until_stop(text, body_start)
        if unclosed:
            _add_note("p1_block_skipped", "unclosed_fence")
            continue
        for raw, provenance in _extract_candidates_from_body(body):
            accepted = classify_path_token(raw, provenance)
            if accepted:
                paths.add(accepted)

    return {"paths": paths, "notes": notes}


def owns_result_for_code(repo_root: Path, code: str) -> dict[str, Any]:
    """OWNS for one CODE: ``{paths, notes}`` including unreadable notes."""
    empty: dict[str, Any] = {"paths": set(), "notes": []}
    for row in load_registry(repo_root):
        if row["code"] != code:
            continue
        fdir = _feature_dir(repo_root, row)
        if not fdir:
            return empty
        tasks = fdir / "tasks.md"
        if not tasks.is_file():
            # Missing tasks.md: empty OWNS, no unreadable note (FSUBR-10.4 baseline)
            return empty
        try:
            raw = tasks.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            return {
                "paths": set(),
                "notes": [
                    {
                        "kind": "p1_file_unreadable",
                        "code": code,
                        "detail": type(exc).__name__,
                    }
                ],
            }
        result = extract_owns_from_tasks_text(text)
        # stamp feature code on block notes when absent
        stamped = []
        for n in result["notes"]:
            nn = dict(n)
            nn.setdefault("code", code)
            stamped.append(nn)
        return {"paths": result["paths"], "notes": stamped}
    return empty


def owns_for_code(repo_root: Path, code: str) -> set[str]:
    return owns_result_for_code(repo_root, code)["paths"]


def all_owns(repo_root: Path) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for row in load_registry(repo_root):
        out[row["code"]] = owns_for_code(repo_root, row["code"])
    return out


def p0_seeds(repo_root: Path, terms: list[str] | None) -> dict[str, Any]:
    terms = [t.strip() for t in (terms or []) if t and len(t.strip()) >= 3]
    if not terms:
        return {"codes": [], "matched": 0, "truncated": False, "returned": 0}

    scored: list[tuple[int, str]] = []
    for row in load_registry(repo_root):
        fdir = _feature_dir(repo_root, row)
        if not fdir:
            continue
        blobs: list[str] = []
        for name in ("requirements.md", "design.md", "tasks.md"):
            p = fdir / name
            if p.is_file():
                try:
                    blobs.append(p.read_text(encoding="utf-8"))
                except OSError:
                    pass
        text = "\n".join(blobs)
        text_l = text.lower()
        distinct = 0
        hits = 0
        for t in terms:
            tl = t.lower()
            c = text_l.count(tl)
            if c:
                distinct += 1
                hits += c
        if distinct:
            score = distinct * 1000 + hits
            scored.append((score, row["code"]))

    scored.sort(key=lambda x: (-x[0], x[1]))
    matched = len(scored)
    top = scored[:P0_SEED_MAX]
    codes = [c for _, c in top]
    return {
        "codes": codes,
        "matched": matched,
        "truncated": matched > P0_SEED_MAX,
        "returned": len(codes),
    }


def _via_rank(via: str) -> int:
    return {"both": 2, "path": 1, "term": 0}.get(via, 0)


def neighbors(
    repo_root: Path, code: str, terms: list[str] | None = None
) -> dict[str, Any]:
    owns_map = all_owns(repo_root)
    focus = owns_map.get(code, set())
    path_w: dict[str, int] = {}
    for other, oset in owns_map.items():
        if other == code:
            continue
        w = overlap_weight(focus, oset)
        if w > 0:
            path_w[other] = w

    term_set: set[str] = set()
    p0_meta = p0_seeds(repo_root, terms) if terms else {
        "codes": [],
        "matched": 0,
        "truncated": False,
        "returned": 0,
    }
    if terms:
        term_set = set(p0_meta["codes"]) - {code}

    candidates = set(path_w) | term_set
    rows: list[dict[str, Any]] = []
    for c in candidates:
        pw = path_w.get(c, 0)
        is_term = c in term_set
        if pw > 0 and is_term:
            via = "both"
        elif pw > 0:
            via = "path"
        else:
            via = "term"
        rows.append({"code": c, "shared_paths": pw, "via": via})

    rows.sort(key=lambda r: (-r["shared_paths"], -_via_rank(r["via"]), r["code"]))
    truncated = rows[:NEIGHBORS_MAX]
    return {
        "neighbors": truncated,
        "p0": p0_meta,
        "owns_coverage": owns_coverage(repo_root, owns_map),
        "advisory": True,
    }


def owns_coverage(
    repo_root: Path, owns_map: dict[str, set[str]] | None = None
) -> dict[str, Any]:
    owns_map = owns_map or all_owns(repo_root)
    registered = len(owns_map)
    with_owns = sum(1 for s in owns_map.values() if s)
    ratio = (with_owns / registered) if registered else 0.0
    return {"with_owns": with_owns, "registered": registered, "ratio": ratio}


def _parse_roadmap(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "docs" / "roadmap" / "INDEX.md"
    if not path.is_file():
        return {"miles": {}, "goals": {}}
    text = path.read_text(encoding="utf-8")
    miles: dict[str, list[str]] = {}
    goals: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        hm = re.match(r"^##\s+(MILE-\d+)", line)
        if hm:
            current = hm.group(1)
            miles.setdefault(current, [])
            continue
        if current and "Goals:" in line:
            goals[current] = GOAL_RE.findall(line)
        if current:
            for r in ROAD_RE.findall(line):
                if r not in miles[current]:
                    miles[current].append(r)
    return {"miles": miles, "goals": goals}


def implements_map(repo_root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in load_registry(repo_root):
        road = row.get("road") or ""
        m = ROAD_RE.search(road)
        if m:
            out[row["code"]] = m.group(0)
    return out


def ancestors(repo_root: Path, code: str) -> list[str]:
    chain = [code]
    impl = implements_map(repo_root)
    road = impl.get(code)
    if not road:
        return chain
    chain.append(road)
    rm = _parse_roadmap(repo_root)
    for mile, roads in rm["miles"].items():
        if road in roads:
            chain.append(mile)
            for g in rm["goals"].get(mile, []):
                chain.append(g)
            break
    return chain


def descendants(repo_root: Path, mile: str) -> list[str]:
    rm = _parse_roadmap(repo_root)
    roads = rm["miles"].get(mile, [])
    out = list(roads)
    impl = implements_map(repo_root)
    for code, road in impl.items():
        if road in roads:
            out.append(code)
    return out


def respects_edges(repo_root: Path) -> list[dict[str, str]]:
    arch = repo_root / "docs" / "architecture"
    if not arch.is_dir():
        return []
    edges: list[dict[str, str]] = []
    for design in (repo_root / "docs" / "specs").rglob("design.md"):
        try:
            text = design.read_text(encoding="utf-8")
        except OSError:
            continue
        for arch_id in ARCH_RE.findall(text):
            if "Respects:" in text or "Respects" in text:
                # only if line has Respects
                pass
        for line in text.splitlines():
            if "Respects:" in line:
                for arch_id in ARCH_RE.findall(line):
                    edges.append({"from": str(design), "to": arch_id})
    return edges


def run(repo_root: Path, query: dict[str, Any]) -> dict[str, Any]:
    repo_root = Path(repo_root)
    kind = query.get("kind", "neighbors")
    owns_map = all_owns(repo_root)
    cov = owns_coverage(repo_root, owns_map)
    base: dict[str, Any] = {
        "advisory": True,
        "owns_coverage": cov,
        "notes": [],
    }

    if kind == "neighbors":
        terms = query.get("terms") or []
        code = query["code"]
        n = neighbors(repo_root, code, terms if terms else None)
        base.update(n)
        return base

    if kind == "ancestors":
        base["ancestors"] = ancestors(repo_root, query["code"])
        base["p0"] = {"codes": [], "matched": 0, "truncated": False, "returned": 0}
        return base

    if kind == "descendants":
        base["descendants"] = descendants(repo_root, query["mile"])
        base["p0"] = {"codes": [], "matched": 0, "truncated": False, "returned": 0}
        return base

    if kind == "subgraph":
        seeds = query.get("seeds") or {}
        nodes: set[str] = set(seeds.get("codes") or [])
        terms = seeds.get("terms") or []
        p0 = p0_seeds(repo_root, terms) if terms else {
            "codes": [],
            "matched": 0,
            "truncated": False,
            "returned": 0,
        }
        nodes |= set(p0["codes"])
        for path in seeds.get("paths") or []:
            for code, oset in owns_map.items():
                if path in oset or path in denoise(oset):
                    nodes.add(code)
        # expand 1 hop overlaps
        expanded = set(nodes)
        for c in list(nodes):
            n = neighbors(repo_root, c, None)
            for row in n["neighbors"][:NEIGHBORS_MAX]:
                expanded.add(row["code"])
        # bound
        ordered = sorted(expanded)
        # prefer seeds first then alpha — keep max 36
        seed_list = list(nodes)
        rest = [c for c in ordered if c not in nodes]
        final = (seed_list + rest)[: NEIGHBORS_MAX * 3]
        base["nodes"] = final
        base["seeds"] = list(nodes)
        base["p0"] = p0
        base["respects"] = respects_edges(repo_root)
        return base

    if kind == "blast_radius":
        path = query.get("path", "")
        path = _strip_line_suffix(path)
        hit: set[str] = set()
        for code, oset in owns_map.items():
            if path in oset:
                hit.add(code)
                continue
            for tok in oset:
                # directory ownership only when token looks like dir (ends / or no extension)
                is_dir = tok.endswith("/") or ("." not in Path(tok).name)
                if is_dir and (path == tok.rstrip("/") or path.startswith(tok.rstrip("/") + "/")):
                    hit.add(code)
        base["codes"] = sorted(hit)
        base["p0"] = {"codes": [], "matched": 0, "truncated": False, "returned": 0}
        return base

    base["notes"].append(f"unknown kind {kind}")
    return base
