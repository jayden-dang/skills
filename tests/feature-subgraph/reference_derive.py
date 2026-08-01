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
    r"^\s*[-*]\s*(?:Create|Modify|Move|Test)\s*:\s*`?([^`\n]+?)`?\s*$",
    re.I | re.M,
)
INDEX_ROW_RE = re.compile(
    r"^\|\s*([A-Z][A-Z0-9]{1,11})\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|",
    re.M,
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


def extract_owns_from_tasks_text(text: str) -> set[str]:
    owns: set[str] = set()
    # Prefer content under **Files:** block if present
    files_blocks = re.split(r"(?i)\*\*Files:\*\*|^\s*Files:\s*$", text, maxsplit=1)
    body = files_blocks[1] if len(files_blocks) > 1 else text
    # stop at next ### heading if any
    body = re.split(r"\n### ", body, maxsplit=1)[0]

    for m in BULLET_FILE_RE.finditer(body):
        raw = m.group(1).strip()
        # drop trailing comments
        raw = raw.split("#", 1)[0].strip()
        path = _strip_line_suffix(raw)
        if path and not path.lower().startswith("also "):
            owns.add(path)

    # prose / leftover path-like tokens
    for m in PATH_TOKEN_RE.finditer(body):
        raw = m.group(1)
        if raw in {"Create", "Modify", "Move", "Test", "Files"}:
            continue
        if ":" in raw and not raw.startswith("http"):
            # may be path:lines — strip
            path = _strip_line_suffix(raw)
        else:
            path = raw
        path = path.strip("`")
        if not path or path.startswith("http"):
            continue
        # require slash or known extension-ish
        if "/" not in path and "." not in path:
            continue
        if path.endswith(":"):
            continue
        owns.add(path)

    # cleanup: drop pure labels
    cleaned = set()
    for p in owns:
        p = _strip_line_suffix(p.strip())
        if p and not p.startswith("-"):
            cleaned.add(p)
    return cleaned


def owns_for_code(repo_root: Path, code: str) -> set[str]:
    for row in load_registry(repo_root):
        if row["code"] != code:
            continue
        fdir = _feature_dir(repo_root, row)
        if not fdir:
            return set()
        tasks = fdir / "tasks.md"
        if not tasks.is_file():
            return set()
        try:
            return extract_owns_from_tasks_text(tasks.read_text(encoding="utf-8"))
        except OSError:
            return set()
    return set()


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
