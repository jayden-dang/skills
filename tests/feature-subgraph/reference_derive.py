"""Test-side reference implementation of load-subgraph passes.md recipes.

Not shipped under skills/. Agents execute passes.md via the skill; unittests
import this module to lock recipe math.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

NEIGHBORS_MAX = 12
P0_SEED_MAX = 12
CLUSTER_K = 1
CLUSTER_MEMBERS_MAX = 8
PATH_EVIDENCE_MAX = 5
TERM_EVIDENCE_MAX = 5
OOS_ITEM_MAX = 6
OOS_TEXT_CEILING = 1200
SCHEMA_VERSION = "1.1"
RECIPE_ID = "fsubr-1.1"

OPTIONAL_LAYER_PATHS = (
    "docs/roadmap/INDEX.md",
    "docs/architecture/INDEX.md",
)

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


def parse_registry(text: str) -> list[dict[str, str]]:
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


def load_registry(repo_root: Path) -> list[dict[str, str]]:
    index = repo_root / "docs" / "specs" / "INDEX.md"
    if not index.is_file():
        return []
    text = index.read_text(encoding="utf-8")
    return parse_registry(text)


class _FsSession:
    """Read-once filesystem session: each path appears at most once in the ledger."""

    def __init__(self, repo_root: Path, allow_io: bool = True) -> None:
        self.repo_root = Path(repo_root)
        self.allow_io = allow_io
        self.read_ledger: list[dict[str, str]] = []
        self._seen: set[str] = set()
        self.source_bytes: dict[str, bytes] = {}
        self.source_texts: dict[str, str] = {}
        self.fingerprints: dict[str, dict[str, Any]] = {}
        # rel → error class name when path exists but read/decode failed
        self.read_errors: dict[str, str] = {}

    def _ensure_io(self, rel: str) -> None:
        if not self.allow_io:
            raise OSError(f"IO disabled: {rel}")

    def _record(self, rel: str, op: str) -> None:
        if rel in self._seen:
            return
        self._seen.add(rel)
        self.read_ledger.append({"path": rel, "op": op})

    def consider(self, rel: str) -> str | None:
        """Open/stat path once. Return UTF-8 text, or None if absent/unreadable."""
        if rel in self.source_texts:
            return self.source_texts[rel]
        if rel in self._seen:
            return None
        self._ensure_io(rel)
        path = self.repo_root / rel
        if not path.is_file():
            self._record(rel, "stat_absent")
            self.fingerprints[rel] = {"sha256": None, "present": False}
            return None
        try:
            raw = path.read_bytes()
        except OSError as exc:
            self._record(rel, "read")
            self.fingerprints[rel] = {"sha256": None, "present": True}
            self.read_errors[rel] = type(exc).__name__
            return None
        self._record(rel, "read")
        self.source_bytes[rel] = raw
        self.fingerprints[rel] = {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "present": True,
        }
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            self.read_errors[rel] = type(exc).__name__
            return None
        self.source_texts[rel] = text
        return text


def _feature_rel(row: dict[str, str], name: str) -> str:
    spec = row["spec"].strip().strip("./")
    if spec.endswith("/"):
        spec = spec[:-1]
    return f"docs/specs/{spec}/{name}"


def _note_key(note: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(note.get("kind") or ""),
        str(note.get("code") or ""),
        str(note.get("detail") or ""),
    )


def _add_note(notes: list[dict[str, Any]], seen: set[tuple[str, str, str]], note: dict[str, Any]) -> None:
    key = _note_key(note)
    if key in seen:
        return
    seen.add(key)
    notes.append(note)


def _cluster_returned_members(owns_map: dict[str, set[str]], focus: str) -> list[str]:
    """Stage B membership from Stage A OWNS only (focus first, weight≥K, cap)."""
    if focus not in owns_map:
        return []
    focus_paths = owns_map[focus]
    scored: list[tuple[int, str]] = []
    for code, paths in owns_map.items():
        if code == focus:
            continue
        w = overlap_weight(focus_paths, paths)
        if w >= CLUSTER_K:
            scored.append((w, code))
    scored.sort(key=lambda x: (-x[0], x[1]))
    members = [focus]
    for _, code in scored:
        if len(members) >= CLUSTER_MEMBERS_MAX:
            break
        members.append(code)
    return members


def build_snapshot(
    repo_root: Path | str,
    query: dict[str, Any],
    *,
    allow_io: bool = True,
    fs: Any = None,
) -> dict[str, Any]:
    """Two-stage DerivationSnapshot (design §0). Queries must not open files after this."""
    if fs is not None and not allow_io:
        raise OSError("IO disabled")
    repo_root = Path(repo_root)
    session = _FsSession(repo_root, allow_io=allow_io)
    kind = query.get("kind", "neighbors")
    terms_raw = query.get("terms")
    if terms_raw is None and kind == "subgraph":
        terms_raw = (query.get("seeds") or {}).get("terms")
    terms = [t.strip() for t in (terms_raw or []) if t and len(str(t).strip()) >= 3]
    need_triad = bool(terms) or kind in {"subgraph", "cluster"}

    notes: list[dict[str, Any]] = []
    seen_notes: set[tuple[str, str, str]] = set()

    # --- Stage A: core ---
    index_rel = "docs/specs/INDEX.md"
    index_text = session.consider(index_rel)
    registry = parse_registry(index_text) if index_text else []

    owns: dict[str, set[str]] = {}
    for row in registry:
        code = row["code"]
        owns[code] = set()
        tasks_rel = _feature_rel(row, "tasks.md")
        text = session.consider(tasks_rel)
        if text is None:
            if tasks_rel in session.read_errors:
                _add_note(
                    notes,
                    seen_notes,
                    {
                        "kind": "p1_file_unreadable",
                        "code": code,
                        "detail": session.read_errors[tasks_rel],
                    },
                )
            # missing tasks.md: empty OWNS, no unreadable note
        else:
            result = extract_owns_from_tasks_text(text)
            owns[code] = set(result["paths"])
            for n in result["notes"]:
                nn = dict(n)
                nn.setdefault("code", code)
                _add_note(notes, seen_notes, nn)

    # Term / subgraph / cluster triad texts (each path still ≤1 via session)
    if need_triad:
        for row in registry:
            for name in ("requirements.md", "design.md"):
                session.consider(_feature_rel(row, name))

    # Optional layers — presence sentinels always
    for opt in OPTIONAL_LAYER_PATHS:
        session.consider(opt)

    # --- Stage B: cluster OOS (after members from Stage A OWNS only) ---
    if kind == "cluster":
        focus = query.get("focus") or query.get("code") or ""
        members = _cluster_returned_members(owns, focus)
        code_to_row = {r["code"]: r for r in registry}
        for mcode in members:
            row = code_to_row.get(mcode)
            if not row:
                continue
            # requirements for OOS if not already buffered
            session.consider(_feature_rel(row, "requirements.md"))

    cov = owns_coverage_from_map(owns)

    return {
        "registry": registry,
        "source_texts": dict(session.source_texts),
        "source_bytes": dict(session.source_bytes),
        "owns": owns,
        "owns_coverage": cov,
        "p3_p4_p5": {},
        "notes": notes,
        "fingerprints": dict(session.fingerprints),
        "read_ledger": list(session.read_ledger),
        "schema_version": SCHEMA_VERSION,
        "recipe_id": RECIPE_ID,
        "query": dict(query),
        "_repo_root": str(repo_root),
    }


def owns_coverage_from_map(owns_map: dict[str, set[str]]) -> dict[str, Any]:
    registered = len(owns_map)
    with_owns = sum(1 for s in owns_map.values() if s)
    ratio = (with_owns / registered) if registered else 0.0
    return {"with_owns": with_owns, "registered": registered, "ratio": ratio}


def p0_seeds_from_snapshot(
    snapshot: dict[str, Any], terms: list[str] | None
) -> dict[str, Any]:
    terms = [t.strip() for t in (terms or []) if t and len(t.strip()) >= 3]
    if not terms:
        return {"codes": [], "matched": 0, "truncated": False, "returned": 0}

    scored: list[tuple[int, str]] = []
    texts = snapshot.get("source_texts") or {}
    for row in snapshot.get("registry") or []:
        blobs: list[str] = []
        for name in ("requirements.md", "design.md", "tasks.md"):
            rel = _feature_rel(row, name)
            if rel in texts:
                blobs.append(texts[rel])
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


def neighbors_from_snapshot(
    snapshot: dict[str, Any],
    code: str,
    terms: list[str] | None = None,
    fs: Any = None,
) -> dict[str, Any]:
    """Pure neighbors query — zero file IO (fs must not be used for reads)."""
    if fs is not None:
        # Touch only to force adapters that raise on any attribute use when misused
        # Queries intentionally ignore fs; presence documents purity contract for tests.
        pass
    owns_map: dict[str, set[str]] = snapshot["owns"]
    focus = owns_map.get(code, set())
    path_w: dict[str, int] = {}
    for other, oset in owns_map.items():
        if other == code:
            continue
        w = overlap_weight(focus, oset)
        if w > 0:
            path_w[other] = w

    term_set: set[str] = set()
    p0_meta = (
        p0_seeds_from_snapshot(snapshot, terms)
        if terms
        else {"codes": [], "matched": 0, "truncated": False, "returned": 0}
    )
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
        "owns_coverage": snapshot.get("owns_coverage")
        or owns_coverage_from_map(owns_map),
        "advisory": True,
        "notes": list(snapshot.get("notes") or []),
        "schema_version": snapshot.get("schema_version", SCHEMA_VERSION),
        "recipe_id": snapshot.get("recipe_id", RECIPE_ID),
    }


def cluster_from_snapshot(
    snapshot: dict[str, Any],
    focus: str,
    fs: Any = None,
) -> dict[str, Any]:
    """Minimal pure cluster shell for Stage B purity (full payload is later task)."""
    if fs is not None:
        pass
    owns_map: dict[str, set[str]] = snapshot["owns"]
    members = _cluster_returned_members(owns_map, focus)
    notes = list(snapshot.get("notes") or [])
    if focus not in owns_map:
        key_notes = {_note_key(n) for n in notes}
        inv = {
            "kind": "cluster_focus_invalid",
            "code": focus,
            "detail": "not_registered",
        }
        if _note_key(inv) not in key_notes:
            notes.append(inv)
    return {
        "focus": focus,
        "members": members,
        "notes": notes,
        "owns_coverage": snapshot.get("owns_coverage")
        or owns_coverage_from_map(owns_map),
        "advisory": True,
        "schema_version": snapshot.get("schema_version", SCHEMA_VERSION),
        "recipe_id": snapshot.get("recipe_id", RECIPE_ID),
    }


def _parse_roadmap_text(text: str) -> dict[str, Any]:
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


def implements_map_from_registry(registry: list[dict[str, str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in registry:
        road = row.get("road") or ""
        m = ROAD_RE.search(road)
        if m:
            out[row["code"]] = m.group(0)
    return out


def ancestors_from_snapshot(snapshot: dict[str, Any], code: str) -> list[str]:
    chain = [code]
    impl = implements_map_from_registry(snapshot.get("registry") or [])
    road = impl.get(code)
    if not road:
        return chain
    chain.append(road)
    rm_text = (snapshot.get("source_texts") or {}).get("docs/roadmap/INDEX.md")
    if not rm_text:
        return chain
    rm = _parse_roadmap_text(rm_text)
    for mile, roads in rm["miles"].items():
        if road in roads:
            chain.append(mile)
            for g in rm["goals"].get(mile, []):
                chain.append(g)
            break
    return chain


def descendants_from_snapshot(snapshot: dict[str, Any], mile: str) -> list[str]:
    rm_text = (snapshot.get("source_texts") or {}).get("docs/roadmap/INDEX.md")
    if not rm_text:
        return []
    rm = _parse_roadmap_text(rm_text)
    roads = rm["miles"].get(mile, [])
    out = list(roads)
    impl = implements_map_from_registry(snapshot.get("registry") or [])
    for code, road in impl.items():
        if road in roads:
            out.append(code)
    return out


def respects_edges_from_snapshot(snapshot: dict[str, Any]) -> list[dict[str, str]]:
    arch_fp = (snapshot.get("fingerprints") or {}).get("docs/architecture/INDEX.md")
    # ARCH-2 / design freeze: architecture INDEX sentinel absent → no-op
    if not arch_fp or not arch_fp.get("present"):
        return []
    edges: list[dict[str, str]] = []
    for rel, text in (snapshot.get("source_texts") or {}).items():
        norm = rel.replace("\\", "/")
        if not norm.endswith("design.md"):
            continue
        if "/specs/" not in norm:
            continue
        for line in text.splitlines():
            if "Respects:" in line:
                for arch_id in ARCH_RE.findall(line):
                    edges.append({"from": rel, "to": arch_id})
    return edges


def blast_radius_from_snapshot(snapshot: dict[str, Any], path: str) -> list[str]:
    path = _strip_line_suffix(path)
    owns_map: dict[str, set[str]] = snapshot["owns"]
    hit: set[str] = set()
    for code, oset in owns_map.items():
        if path in oset:
            hit.add(code)
            continue
        for tok in oset:
            is_dir = tok.endswith("/") or ("." not in Path(tok).name)
            if is_dir and (
                path == tok.rstrip("/") or path.startswith(tok.rstrip("/") + "/")
            ):
                hit.add(code)
    return sorted(hit)


def subgraph_from_snapshot(
    snapshot: dict[str, Any], seeds: dict[str, Any] | None
) -> dict[str, Any]:
    seeds = seeds or {}
    owns_map: dict[str, set[str]] = snapshot["owns"]
    nodes: set[str] = set(seeds.get("codes") or [])
    terms = seeds.get("terms") or []
    p0 = (
        p0_seeds_from_snapshot(snapshot, terms)
        if terms
        else {"codes": [], "matched": 0, "truncated": False, "returned": 0}
    )
    nodes |= set(p0["codes"])
    for path in seeds.get("paths") or []:
        for code, oset in owns_map.items():
            if path in oset or path in denoise(oset):
                nodes.add(code)
    expanded = set(nodes)
    for c in list(nodes):
        n = neighbors_from_snapshot(snapshot, c, None)
        for row in n["neighbors"][:NEIGHBORS_MAX]:
            expanded.add(row["code"])
    ordered = sorted(expanded)
    seed_list = list(nodes)
    rest = [c for c in ordered if c not in nodes]
    final = (seed_list + rest)[: NEIGHBORS_MAX * 3]
    return {
        "nodes": final,
        "seeds": list(nodes),
        "p0": p0,
        "respects": respects_edges_from_snapshot(snapshot),
    }


def run_on_snapshot(
    snapshot: dict[str, Any],
    query: dict[str, Any],
    fs: Any = None,
) -> dict[str, Any]:
    """Pure query on a prebuilt snapshot — zero file IO."""
    if fs is not None:
        pass
    kind = query.get("kind", "neighbors")
    owns_map: dict[str, set[str]] = snapshot["owns"]
    cov = snapshot.get("owns_coverage") or owns_coverage_from_map(owns_map)
    base: dict[str, Any] = {
        "advisory": True,
        "owns_coverage": cov,
        "notes": list(snapshot.get("notes") or []),
    }

    if kind == "neighbors":
        terms = query.get("terms") or []
        code = query["code"]
        n = neighbors_from_snapshot(
            snapshot, code, terms if terms else None, fs=fs
        )
        base.update(n)
        return base

    if kind == "cluster":
        focus = query.get("focus") or query.get("code") or ""
        c = cluster_from_snapshot(snapshot, focus, fs=fs)
        base.update(c)
        return base

    if kind == "ancestors":
        base["ancestors"] = ancestors_from_snapshot(snapshot, query["code"])
        base["p0"] = {"codes": [], "matched": 0, "truncated": False, "returned": 0}
        return base

    if kind == "descendants":
        base["descendants"] = descendants_from_snapshot(snapshot, query["mile"])
        base["p0"] = {"codes": [], "matched": 0, "truncated": False, "returned": 0}
        return base

    if kind == "subgraph":
        sub = subgraph_from_snapshot(snapshot, query.get("seeds") or {})
        base.update(sub)
        return base

    if kind == "blast_radius":
        base["codes"] = blast_radius_from_snapshot(snapshot, query.get("path", ""))
        base["p0"] = {"codes": [], "matched": 0, "truncated": False, "returned": 0}
        return base

    base["notes"].append(f"unknown kind {kind}")
    return base


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
    q: dict[str, Any] = {
        "kind": "neighbors",
        "code": code,
        "terms": list(terms) if terms else [],
    }
    snap = build_snapshot(repo_root, q)
    return neighbors_from_snapshot(snap, code, terms)


def owns_coverage(
    repo_root: Path, owns_map: dict[str, set[str]] | None = None
) -> dict[str, Any]:
    owns_map = owns_map or all_owns(repo_root)
    return owns_coverage_from_map(owns_map)


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
    """Build Stage A/B snapshot once, then run a pure query (zero further file IO)."""
    repo_root = Path(repo_root)
    snap = build_snapshot(repo_root, query)
    return run_on_snapshot(snap, query)
