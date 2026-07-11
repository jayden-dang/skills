#!/usr/bin/env python3
# @skills-linter: check-graph sha256:55008d7c5cf5
"""check-graph — horizontal feature-graph layer.

Harvests, from each feature's existing design.md/tasks.md (NO new authoring):
  - a Surface manifest  (files a feature owns/touches)
  - a Reverse index     (path -> [{code, role}])
  - Summary cards       (code, name, owns, interfaces, out-of-scope)

Modes: --harvest (write <specsDir>/GRAPH.md) | --query (JSON overlaps) | --verify (lint).
Config: docs/agents/trace.json (shared specsDir; optional "graph" key).

This module has no top-level side effects: importing it runs no CLI.
"""
import json
import os
import re
import sys

# Keys stay camelCase: they are read from docs/agents/trace.json, a wire format.
DEFAULTS = {
    "specsDir": "docs/specs",
    "graph": {
        "sourceRoots": ["src", "src-tauri", "tests", "test", "e2e", "crates", "app", "lib", "packages"],
        "sourceExts": ["ts", "tsx", "js", "jsx", "mjs", "cjs", "rs", "css", "scss", "go", "py"],
        "cardCap": 12,
        "queryCap": 8,
    },
}

_QUOTE_PAREN_RE = re.compile(r"[`'\"()]")
_TRAILING_LOCATOR_RE = re.compile(r":\d+(?:[,\d]*)?$", re.ASCII)
_TRAILING_TAIL_RE = re.compile(r"\s*~?\d[\d,\s-]*$", re.ASCII)
_LEADING_DOT_SLASH_RE = re.compile(r"^\./")


def normalize_path(token):
    t = str(token)
    t = _QUOTE_PAREN_RE.sub("", t).strip()
    # Apply both strip regexes repeatedly to a fixpoint: a token can carry a
    # colon-form locator (:208 or :127,172) AND a paren-tail (~208-221) at the
    # same time, in either order, so a single fixed pass can't be trusted to
    # fully reduce it (e.g. "Editor.tsx:208 (~208-221)" needs both applied).
    while True:
        prev = t
        t = _TRAILING_LOCATOR_RE.sub("", t)  # trailing :208 or :127,172 locator
        t = _TRAILING_TAIL_RE.sub("", t)  # trailing "(~208-221)" tail after paren-strip
        t = t.strip()
        if t == prev:
            break
    t = _LEADING_DOT_SLASH_RE.sub("", t)  # leading "./" so "./scripts/x.py" dedups with "scripts/x.py"
    return t


_WHITESPACE_RE = re.compile(r"\s")
_ALNUM_RE = re.compile(r"[A-Za-z0-9]")


def _ext_re(exts):
    return re.compile(r"\.(" + "|".join(exts) + r")$")


def is_source_path(token, cfg):
    t = token
    if not t or _WHITESPACE_RE.search(t):
        return False
    if "*" in t:
        return False  # glob token, not a concrete path (FGRAPH-1.7)
    ext_re = _ext_re(cfg["sourceExts"])
    has_ext = bool(ext_re.search(t))
    seg = t.split("/")
    filename = seg[-1]
    # A "real" filename has a name part before any extension; a token that is
    # just a dot-prefixed suffix (".spec.ts") is a bare-extension pattern, not
    # a concrete path, so it's rejected here regardless of has_ext.
    has_real_filename = (
        len(filename) > 0 and not filename.startswith(".") and bool(_ALNUM_RE.search(filename))
    )
    under_root = any(t == r + "/" or t.startswith(r + "/") for r in cfg["sourceRoots"])
    if has_ext and has_real_filename:
        return True
    if under_root and has_real_filename and ext_re.search(filename):
        return True
    return False


def dedupe_by_fullest(paths):
    uniq = list(dict.fromkeys(paths))  # de-dupe, preserve first-seen order
    kept = []
    for p in uniq:
        is_basename_of_another = any(q != p and q.endswith("/" + p) for q in uniq)
        if not is_basename_of_another:
            kept.append(p)
    return kept


_glob_cache = {}


def _glob_to_re(pattern):
    """Compile an owns-glob to an anchored regex matched against a repo-relative
    folder path. Dialect: a trailing '/**' owns the folder and every descendant;
    a bare '**' owns everything; '*' matches a single path segment; everything
    else is literal.
    """
    cached = _glob_cache.get(pattern)
    if cached is not None:
        return cached
    p = pattern.strip()
    if p.startswith("./"):
        p = p[2:]
    p = p.strip("/")
    if p == "**":
        _glob_cache[pattern] = re.compile("^.*$")
        return _glob_cache[pattern]
    trailing_subtree = p.endswith("/**")
    if trailing_subtree:
        p = p[:-3]
    out = ["^"]
    i, n = 0, len(p)
    while i < n:
        if p[i:i + 2] == "**":
            out.append(".*")
            i += 2
        elif p[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(p[i]))
            i += 1
    if trailing_subtree:
        out.append("(?:/.*)?")
    out.append("$")
    regex = re.compile("".join(out))
    _glob_cache[pattern] = regex
    return regex


def resolve_module(path, modules):
    """Return the sorted list of module codes whose 'owns' globs match a
    repo-relative folder path: [] = orphan, [code] = home, [a, b, ...] =
    ambiguous (double-mapped). Neutral by design — callers decide severity.

    Normalize minimally (leading './' and trailing '/'): do NOT use
    normalize_path here — its locator-stripping rules would corrupt a
    digit-suffixed folder segment (e.g. 'src/store2' -> 'src/store').
    """
    folder = _LEADING_DOT_SLASH_RE.sub("", str(path)).strip("/")
    hits = set()
    for m in modules:
        code = m.get("code")
        if not code:
            continue
        for g in m.get("owns", []):
            if _glob_to_re(g).match(folder):
                hits.add(code)
                break
    return sorted(hits)


def _home_feature(owned_paths, touched_paths, override_code, module_codes, modules):
    """Classify a feature's module homing from its owned + touched paths and an
    optional authored `Module:` override. `module_codes` is the set of valid
    module codes, used only to validate the override. Pure — no I/O.

    Returns {home, facets, spanned, unknown_override}:
      home             module code or None
      facets           sorted modules (!= home) each the sole resolution of a
                       touched path; [] when home is None
      spanned          sorted modules the owned paths fall in, ONLY when every
                       owned path resolves to exactly one module, >=2 distinct
                       modules result, and no valid override applies; else []
      unknown_override the override code when one was declared but is not a known
                       module; else None
    """
    derived_home = None
    spanned = []
    if owned_paths:
        codes = []
        clean = True
        for p in owned_paths:
            hits = resolve_module(p, modules)
            if len(hits) != 1:
                clean = False
                break
            codes.append(hits[0])
        if clean:
            uniq = sorted(set(codes))
            if len(uniq) == 1:
                derived_home = uniq[0]
            elif len(uniq) >= 2:
                spanned = uniq
    home = derived_home
    unknown_override = None
    if override_code is not None:
        if override_code in module_codes:
            home = override_code
            spanned = []
        else:
            unknown_override = override_code
    facets = []
    if home is not None:
        fset = set()
        for p in touched_paths:
            hits = resolve_module(p, modules)
            if len(hits) == 1 and hits[0] != home:
                fset.add(hits[0])
        facets = sorted(fset)
    return {"home": home, "facets": facets, "spanned": spanned,
            "unknown_override": unknown_override}


def _home_module(owned_paths, modules):
    """Home a feature by its owned paths alone (no override, no touches): the
    single module code iff every owned path resolves to that one module; else
    None. Thin wrapper over _home_feature preserving the MODGRAPH-1.x contract."""
    return _home_feature(owned_paths, [], None, set(), modules)["home"]


_OWN_HINT_RE = re.compile(r"\b(create|new file|adds? a? ?new file|scaffold)\b", re.ASCII | re.IGNORECASE)
_CREATE_LABEL_RE = re.compile(r"^\s*-?\s*create:", re.IGNORECASE)
_MODIFY_LABEL_RE = re.compile(r"^\s*-?\s*modify:", re.IGNORECASE)


# Best-effort role classification: a `create` block label, or a create/new
# verb in the line itself, means the feature owns the surface; a `modify`
# block label means it only touches it. Everything else defaults to the
# safer "touches" (no false ownership claims from ambiguous prose).
def classify_role(line, block_label):
    if block_label == "create" or _CREATE_LABEL_RE.search(line):
        return "owns"
    if block_label == "modify" or _MODIFY_LABEL_RE.search(line):
        return "touches"
    if _OWN_HINT_RE.search(line):
        return "owns"
    return "touches"


def cap_list(items, cap):
    """Cap a Summary card list at `cap` entries, appending a "…(+N more)" elision marker."""
    if len(items) <= cap:
        return items
    return list(items[:cap]) + [f"…(+{len(items) - cap} more)"]


_SENTENCE_END_RE = re.compile(r"[.!?](?:\s|$)")


def _first_sentence(s):
    """Text up to and including the first sentence terminator, else the whole string."""
    m = _SENTENCE_END_RE.search(s)
    return s[:m.end()].strip() if m else s.strip()


_OUT_OF_SCOPE_RE = re.compile(r"##\s*Out of Scope\s*\n([\s\S]*?)(\n##\s|\n#\s|$)", re.IGNORECASE)
_OOS_BULLET_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$", re.MULTILINE)
_BOLD_RE = re.compile(r"\*\*")


def extract_out_of_scope(req_text):
    """Extract the `## Out of Scope` bullet list from a requirements.md body (best-effort)."""
    m = _OUT_OF_SCOPE_RE.search(req_text)
    if not m:
        return []
    return [_BOLD_RE.sub("", x).strip() for x in _OOS_BULLET_RE.findall(m.group(1))]


_INTERFACE_LABEL_ONLY_RE = re.compile(r"^(?:produces|consumes|provides|exposes):?$", re.IGNORECASE)
_INTERFACE_LABEL_PREFIX_RE = re.compile(r"^(?:produces|consumes|provides|exposes):\s*", re.IGNORECASE)
_INTERFACES_HEADING_RE = re.compile(r"^\s*\*?\*?interfaces:?\*?\*?\s*$", re.IGNORECASE | re.MULTILINE)
_BULLET_LINE_RE = re.compile(r"^\s*[-*]\s+")
_LEADING_WS_RE = re.compile(r"^\s*")
_BACKTICK_RE = re.compile(r"`")


def _is_bare_interface_label(text):
    """A bullet whose text is just a bare section-lead label (`Produces:` etc), with no substance of its own."""
    return bool(_INTERFACE_LABEL_ONLY_RE.match(text.strip()))


def _clean_interface_entry(text):
    """Reduce a kept bullet's text to a short single-line entry: strip a leading
    label prefix, truncate at the first ` — ` em-dash (drop trailing prose),
    strip backticks, trim."""
    s = _INTERFACE_LABEL_PREFIX_RE.sub("", text)
    dash_idx = s.find(" — ")
    if dash_idx != -1:
        s = s[:dash_idx]
    return _BACKTICK_RE.sub("", s).strip()


def extract_interfaces(bodies):
    """Extract bullet items under any `Interfaces:` heading across design.md/tasks.md bodies (best-effort).
    Each entry is a short single-line signature: only the top-level bullets
    under the heading are considered (a bare section-lead label like
    `Produces:` has no substance of its own, so its direct children are
    promoted instead); nested sub-bullets under a substantive top-level entry
    are prose/detail and are skipped to avoid duplicating the entry."""
    out = []
    for body in bodies:
        if not body:
            continue
        lines = body.split("\n")
        for i in range(len(lines)):
            if not _INTERFACES_HEADING_RE.match(lines[i]):
                continue
            group = []
            j = i + 1
            while j < len(lines) and _BULLET_LINE_RE.match(lines[j]):
                group.append(
                    {
                        "indent": len(_LEADING_WS_RE.match(lines[j]).group(0)),
                        "text": _BULLET_LINE_RE.sub("", lines[j], count=1),
                    }
                )
                j += 1
            if len(group) == 0:
                continue
            min_indent = min(g["indent"] for g in group)
            for k in range(len(group)):
                if group[k]["indent"] != min_indent:
                    continue  # only top-level bullets
                text = group[k]["text"]
                if _is_bare_interface_label(text):
                    # Pass-through: this bullet contributes no signal of its own —
                    # promote its direct children (the next indent level down) instead.
                    children = []
                    m = k + 1
                    while m < len(group) and group[m]["indent"] > min_indent:
                        children.append(group[m])
                        m += 1
                    if len(children) == 0:
                        continue
                    child_min = min(c["indent"] for c in children)
                    for c in children:
                        if c["indent"] != child_min or _is_bare_interface_label(c["text"]):
                            continue
                        cleaned = _clean_interface_entry(c["text"])
                        if cleaned:
                            out.append(cleaned)
                    continue
                cleaned = _clean_interface_entry(text)
                if cleaned:
                    out.append(cleaned)
    return out


_SKIP_DIRS = {"node_modules", ".git", "dist", "build", "target", "coverage", ".next", ".skills", "vendor"}
_SURFACE_BACKTICK_RE = re.compile(r"`([^`]+)`")
_WORD_RE = re.compile(r"[A-Za-z0-9_./-]+")

# A command-invocation line names a tool being run, not a surface being
# owned/touched — a path that appears ONLY on such lines is not surface.
# The command word must sit at a genuine command-START position — line
# start (optionally after a `- `/`* `/`> ` list prefix), right after a
# backtick, or right after a `$ ` shell prompt — NOT anywhere mid-line
# (FGRAPH-1.9): plain prose like "the git log" or "this node in the tree"
# uses these words as ordinary English and must not be treated as a command.
_CMD_LINE_RE = re.compile(r"(?:^\s*(?:[-*>]\s+)?|`|\$\s*)(?:node|npm|pnpm|npx|yarn|git|bash|sh|deno|bun)\s")
_RUN_LINE_RE = re.compile(r"^\s*(?:[-*>]\s+)?run\b", re.ASCII | re.IGNORECASE)
_DOLLAR_LINE_RE = re.compile(r"^\s*\$ ")


def _is_command_line(line):
    return bool(_CMD_LINE_RE.search(line)) or bool(_RUN_LINE_RE.search(line)) or bool(_DOLLAR_LINE_RE.match(line))


def _walk(dir_, predicate):
    """Recursively collect files under dir_ for which predicate(fullPath) is true."""
    out = []

    def _recurse(d):
        try:
            entries = list(os.scandir(d))
        except OSError:
            return
        for e in entries:
            if e.name.startswith(".") and e.name != ".":
                continue
            full = os.path.join(d, e.name)
            if e.is_dir(follow_symlinks=False):
                if e.name not in _SKIP_DIRS:
                    _recurse(full)
            elif predicate(full):
                out.append(full)

    _recurse(dir_)
    return out


def enumerate_folders(root, cfg):
    """Walk each existing sourceRoot under `root`; return (repo_folders,
    source_folders) as sorted repo-relative directory paths. source_folders
    directly contain a file whose extension is in graph.sourceExts. Uses the
    same dotfile/_SKIP_DIRS exclusions as _walk. Never called at import time.
    """
    graph = cfg["graph"]
    exts = tuple("." + e for e in graph["sourceExts"])
    repo_folders = set()
    source_folders = set()

    def walk(abs_dir, rel_dir):
        try:
            entries = list(os.scandir(abs_dir))
        except OSError:
            return
        has_source = False
        for e in entries:
            if e.name.startswith("."):
                continue
            if e.is_dir(follow_symlinks=False):
                if e.name in _SKIP_DIRS:
                    continue
                child_rel = e.name if not rel_dir else rel_dir + "/" + e.name
                repo_folders.add(child_rel)
                walk(e.path, child_rel)
            elif e.is_file(follow_symlinks=False) and e.name.endswith(exts):
                has_source = True
        if rel_dir and has_source:
            source_folders.add(rel_dir)

    for r in graph["sourceRoots"]:
        abs_r = os.path.join(root, r)
        if os.path.isdir(abs_r):
            repo_folders.add(r)
            walk(abs_r, r)
    return sorted(repo_folders), sorted(source_folders)


def _read_maybe(p):
    try:
        with open(p, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_BLANK_LINE_RE = re.compile(r"^\s*$")
_HEADING_HASH_RE = re.compile(r"^\s*#{1,6}\s")
_BLOCK_RESET_LABEL_RE = re.compile(r"^\s*\*?\*?(files|interfaces|steps)\b", re.ASCII | re.IGNORECASE)


def _scan_surface(text, cfg):
    """Extract normalized source paths (with roles) from one design.md/tasks.md body.

    path -> role: `keep` (tracked internally) records whether the path had at
    least one NON-command-line occurrence (FGRAPH-1.8) — a path seen ONLY on
    command-invocation lines (e.g. `Run \\`bash scripts/build.sh\\``) is not
    surface, but a path that also appears in a Create/Modify bullet or prose
    line must still be kept even if it's ALSO named on a command line.
    """
    raw = {}  # path -> {"role", "keep"}; dict preserves insertion order
    block_label = None
    in_fence = False
    for line in text.split("\n"):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            block_label = None
            continue
        if in_fence:
            continue
        if _CREATE_LABEL_RE.search(line):
            block_label = "create"
        elif _MODIFY_LABEL_RE.search(line):
            block_label = "modify"
        elif _BLANK_LINE_RE.match(line) or _HEADING_HASH_RE.match(line) or _BLOCK_RESET_LABEL_RE.match(line):
            block_label = None
        is_cmd = _is_command_line(line)
        cands = []
        seen = set()
        for m in _SURFACE_BACKTICK_RE.finditer(line):
            c = m.group(1)
            if c not in seen:
                seen.add(c)
                cands.append(c)
        for m in _WORD_RE.finditer(line):
            c = m.group(0)
            if c not in seen:
                seen.add(c)
                cands.append(c)
        for c in cands:
            p = normalize_path(c)
            if not is_source_path(p, cfg["graph"]):
                continue
            role = classify_role(line, block_label)
            prev = raw.get(p)
            keep = bool(prev and prev["keep"]) or not is_cmd
            final_role = role if (role == "owns" or not prev) else prev["role"]
            raw[p] = {"role": final_role, "keep": keep}
    return {p: v["role"] for p, v in raw.items() if v["keep"]}


_FEATURE_CODE_RE = re.compile(r"^Feature code:\s*([A-Z][A-Z0-9]{1,11})", re.MULTILINE)
_REQUIREMENTS_TITLE_RE = re.compile(r"^#\s*Requirements:\s*(.+)$", re.MULTILINE)


def harvest(specs_dir, cfg=DEFAULTS):
    """Harvest the Surface manifest, Reverse index, and Shared surface from <specsDir>."""
    features = []
    if not os.path.exists(specs_dir):
        return {"features": features, "reverse": {}, "shared": []}
    _manifest_modules, _manifest_errs = load_manifest(cfg)
    if _manifest_errs:
        _manifest_modules = []
    req_files = _walk(specs_dir, lambda p: p.endswith("requirements.md"))
    for req in sorted(req_files):
        text = _read_maybe(req)
        code_m = _FEATURE_CODE_RE.search(text)
        code = code_m.group(1) if code_m else None
        if not code:
            continue
        name_m = _REQUIREMENTS_TITLE_RE.search(text)
        name = name_m.group(1).strip() if name_m else code
        dir_ = os.path.dirname(req)
        design_body = _read_maybe(os.path.join(dir_, "design.md"))
        tasks_body = _read_maybe(os.path.join(dir_, "tasks.md"))
        surface = {}
        for body in (design_body, tasks_body):
            if not body:
                continue
            for p, role in _scan_surface(body, cfg).items():
                if role == "owns" or p not in surface:
                    surface[p] = role
        # basename/full dedup within this feature, keeping the winning role: a
        # path is `owns` if EITHER the surviving fullest form, OR any basename
        # form of it that got collapsed away, was itself recorded as `owns`.
        surface_keys = list(surface.keys())
        fullest = set(dedupe_by_fullest(surface_keys))
        owns, touches = [], []
        for p in fullest:
            is_owned = any((k == p or p.endswith("/" + k)) and surface[k] == "owns" for k in surface_keys)
            (owns if is_owned else touches).append(p)
        # owns/touches stay UNCAPPED here: the reverse index and shared surface
        # below are built from these raw lists, so a 13th shared file is never
        # silently dropped from FGRAPH-2.x just because the Summary card elides
        # it. The cap is applied in a separate pass, after reverse/shared exist.
        features.append(
            {
                "code": code,
                "name": name,
                "owns": sorted(owns),
                "touches": sorted(touches),
                "interfaces": extract_interfaces([design_body, tasks_body]),
                "oos": extract_out_of_scope(text),
                "home": _home_module(sorted(owns), _manifest_modules),
            }
        )
    features.sort(key=lambda f: f["code"])

    # FGRAPH-2.4: canonicalize each path to the FULLEST form of that file seen
    # across ALL features before indexing, so a bare basename in one feature
    # (`mathInputExtension.ts`) and the full path to the same file in another
    # feature (`src/components/mathInputExtension.ts`) merge into a single
    # reverse-index / shared-surface key instead of two separate ones.
    all_surface_paths = [p for f in features for p in (f["owns"] + f["touches"])]
    uniq_all = list(dict.fromkeys(all_surface_paths))
    canon = {}  # path -> fullest path seen for that file
    for p in uniq_all:
        longest = p
        for q in uniq_all:
            if q != p and q.endswith("/" + p) and len(q) > len(longest):
                longest = q
        canon[p] = longest

    reverse = {}
    for f in features:
        refs = [(p, "owns") for p in f["owns"]] + [(p, "touches") for p in f["touches"]]
        for p, role in refs:
            key = canon.get(p, p)
            reverse.setdefault(key, []).append({"code": f["code"], "role": role})
    for p in reverse:
        reverse[p].sort(key=lambda r: r["code"])
    shared_keys = sorted(p for p in reverse if len(reverse[p]) >= 2)
    shared = [{"path": p, "refs": reverse[p]} for p in shared_keys]

    # Summary cards: cap each list AFTER reverse/shared have been derived from
    # the uncapped owns/touches above, so the capped card fields never feed
    # back into the index.
    cap = cfg["graph"]["cardCap"]
    for f in features:
        f["owns"] = cap_list(f["owns"], cap)
        f["touches"] = cap_list(f["touches"], cap)
        f["interfaces"] = cap_list(f["interfaces"], cap)
        f["oos"] = cap_list(f["oos"], cap)
    return {"features": features, "reverse": reverse, "shared": shared}


def render_graph_md(graph):
    """Render the Graph into a deterministic markdown document: a generated
    banner, one Summary card per feature (## Cards, sorted by code per
    harvest()'s ordering), and a Shared surface table (sorted by path per
    harvest()'s ordering). Pure: takes a Graph, returns a string, touches no
    file — the CLI is responsible for writing GRAPH.md.
    """
    lines = []
    lines.append("# Feature Graph")
    lines.append("")
    lines.append(_GRAPH_BANNER)
    lines.append("")
    lines.append("## Cards")
    lines.append("")
    for f in graph["features"]:
        lines.append(f"### {f['code']} — {f['name']}")
        lines.append(f"- owns: {', '.join(f['owns']) or '—'}")
        lines.append(f"- touches: {', '.join(f['touches']) or '—'}")
        lines.append(f"- interfaces: {', '.join(f['interfaces']) or '—'}")
        lines.append(f"- out-of-scope: {' | '.join(f['oos']) or '—'}")
        lines.append("")
    lines.append("## Shared surface")
    lines.append("")
    lines.append("| Path | Features |")
    lines.append("|---|---|")
    for s in graph["shared"]:
        refs_str = ", ".join(f"{r['code']}:{r['role']}" for r in s["refs"])
        lines.append(f"| {s['path']} | {refs_str} |")
    lines.append("")
    return "\n".join(lines)


_GRAPH_BANNER = "<!-- GENERATED by `check-graph --harvest`. Do not edit by hand; regenerated by sync-spec. -->"


def render_all(graph, cfg):
    """Render the graph to {specsDir-relative path: content}. Flat mode (no valid
    manifest) returns {"GRAPH.md": render_graph_md(graph)} unchanged. Manifest
    mode returns the module index at GRAPH.md plus one compact shard per module
    (and _unassigned) under modules/."""
    modules, errs = load_manifest(cfg)
    if errs or not modules:
        return {"GRAPH.md": render_graph_md(graph)}
    names = {m["code"]: m["name"] for m in modules}
    by_module = {}
    for f in graph["features"]:
        by_module.setdefault(f.get("home"), []).append(f)
    home_of = {f["code"]: f.get("home") for f in graph["features"]}

    idx = ["# Feature Graph", "", _GRAPH_BANNER, "", "## Modules", ""]
    for code in sorted(names):
        n = len(by_module.get(code, []))
        link = f" → modules/{code}.md" if n else ""
        idx.append(f"- {code} — {names[code]} ({n} features){link}")
    if by_module.get(None):
        idx.append(f"- (unassigned) — {len(by_module[None])} features → modules/_unassigned.md")
    idx += ["", "## Cross-module shared surface", "", "| Path | Modules |", "|---|---|"]
    for path in sorted(graph["reverse"]):
        homes = sorted({home_of.get(r["code"]) for r in graph["reverse"][path]
                        if home_of.get(r["code"]) is not None})
        if len(homes) >= 2:
            idx.append(f"| {path} | {', '.join(homes)} |")
    idx.append("")

    files = {"GRAPH.md": "\n".join(idx)}

    def shard(title, feats):
        rows = [f"# Module {title}", "", _GRAPH_BANNER, "", "| Feature | Name | Owns |", "|---|---|---|"]
        for f in sorted(feats, key=lambda x: x["code"]):
            rows.append(f"| {f['code']} | {f['name']} | {', '.join(f['owns']) or '—'} |")
        rows.append("")
        return "\n".join(rows)

    for code in sorted(k for k in by_module if k is not None):
        files[f"modules/{code}.md"] = shard(f"{code} — {names.get(code, code)}", by_module[code])
    if by_module.get(None):
        files["modules/_unassigned.md"] = shard("(unassigned)", by_module[None])
    return files


def _stale_shards(specs_dir, files):
    """Sorted names of stale GENERATED shards on disk: specsDir/modules/*.md files
    that carry the GENERATED banner but whose relpath is not in `files`.
    Hand-authored .md files (no banner) are never stale — the tool owns modules/
    only for files it wrote itself (MODGRAPH-2.6 'previously generated shard
    file'; MODGRAPH-4.2 flat-mode preservation)."""
    modules_dir = os.path.join(specs_dir, "modules")
    stale = []
    if os.path.isdir(modules_dir):
        for name in sorted(os.listdir(modules_dir)):
            path = os.path.join(modules_dir, name)
            if not name.endswith(".md") or not os.path.isfile(path):
                continue
            if f"modules/{name}" in files:
                continue
            with open(path, "r", encoding="utf-8") as fh:
                if _GRAPH_BANNER in fh.read():
                    stale.append(name)
    return stale


def query(graph, paths=None, keywords=None):
    """Query the Graph for features overlapping a set of paths (via the Reverse
    index) or matching a keyword against name/out-of-scope (case-insensitive
    substring). Results are ranked by IDF score descending — each overlapping
    path contributes 1/df, where df is the number of features referencing that
    path in the Reverse index — tied broken by code for determinism. Each
    result carries the feature's full Summary card and its score.
    """
    path_set = set(paths or [])
    # Filter out falsy tokens before lowercasing, so a trailing valueless
    # --keyword (no argument after it) degrades to "no keyword" instead of
    # crashing on a None.
    kws = [k.lower() for k in (keywords or []) if k]
    scored = {}  # code -> {"feature", "overlapPaths": set()}

    def bump(code):
        if code not in scored:
            feature = next((f for f in graph["features"] if f["code"] == code), None)
            scored[code] = {"feature": feature, "overlapPaths": set()}
        return scored[code]

    for p in path_set:
        for ref in graph["reverse"].get(p, []):
            bump(ref["code"])["overlapPaths"].add(p)
    for f in graph["features"]:
        hay = (f["name"] + " " + " ".join(f["oos"])).lower()
        if any(k in hay for k in kws):
            bump(f["code"])
    results = []
    for entry in scored.values():
        feature = entry["feature"]
        score = sum(1.0 / len(graph["reverse"][p]) for p in sorted(entry["overlapPaths"])
                    if graph["reverse"].get(p))
        results.append(
            {
                "code": feature["code"],
                "name": feature["name"],
                "card": feature,
                "overlapPaths": sorted(entry["overlapPaths"]),
                "score": score,
            }
        )
    results.sort(key=lambda r: (-r["score"], r["code"]))
    return results


class ConfigError(Exception):
    """Raised by load_config on an unparseable trace.json.

    load_config itself never calls sys.exit — the CLI (Task 4) is responsible
    for catching this and translating it into an exit code + stderr message.
    """


def load_config(root):
    """Load docs/agents/trace.json (optional), deep-merging the nested
    "graph" key over DEFAULTS["graph"]. Raises ConfigError, never exits, on
    unparseable JSON.
    """
    p = os.path.join(root, "docs/agents/trace.json")
    if not os.path.exists(p):
        return DEFAULTS
    try:
        with open(p, "r", encoding="utf-8") as fh:
            user = json.load(fh)
    except (OSError, ValueError) as exc:
        raise ConfigError(f"could not parse {p}: invalid JSON") from exc
    merged = {**DEFAULTS, **user}
    merged["graph"] = {**DEFAULTS["graph"], **(user.get("graph") or {})}
    return merged


_MODULE_CODE_RE = re.compile(r"^[A-Z][A-Z0-9]{1,11}$")


def load_manifest(cfg):
    """Parse and validate the module manifest from cfg['modules'].

    Returns (modules, validity_errors). Absent/empty 'modules' -> ([], []). A
    module is {"code", "name", "owns":[str], "layer":str|None, "owner":str|None}.
    Validity errors are collected, never raised.
    """
    raw = cfg.get("modules")
    if not raw:
        return [], []
    if not isinstance(raw, list):
        return [], ["E: 'modules' must be a list of module entries"]
    modules = []
    errors = []
    seen = set()
    for i, entry in enumerate(raw):
        if not isinstance(entry, dict):
            errors.append(f"E: module entry #{i + 1} is not an object")
            continue
        code = entry.get("code")
        name = entry.get("name")
        owns = entry.get("owns")
        label = code if isinstance(code, str) and code else f"#{i + 1}"
        if not (isinstance(code, str) and code):
            errors.append(f"E: module entry {label} is missing 'code'")
        if not (isinstance(name, str) and name):
            errors.append(f"E: module {label} is missing 'name'")
        if not (isinstance(owns, list) and owns
                and all(isinstance(g, str) and g for g in owns)):
            errors.append(f"E: module {label} is missing a non-empty 'owns' list")
        if isinstance(code, str) and code:
            if not _MODULE_CODE_RE.match(code):
                errors.append(
                    f"E: module code {code} is malformed "
                    f"(need 2-12 chars, A-Z0-9, starting with a letter)")
            if code in seen:
                errors.append(f"E: duplicate module code {code}")
            seen.add(code)
        modules.append({
            "code": code,
            "name": name,
            "owns": owns if isinstance(owns, list) else [],
            "layer": entry.get("layer"),
            "owner": entry.get("owner"),
        })
    return modules, errors


def _collect_flag(args, name):
    """Collect every value that follows a repeatable flag, e.g. --path a --path b -> ['a', 'b']."""
    out = []
    for i in range(len(args)):
        if args[i] == name:
            out.append(args[i + 1] if i + 1 < len(args) else None)
    return out


def _verify_boundaries(root, cfg, modules):
    """Check module coverage of the source tree. Returns (errors, warnings).

    Orphan and double-mapped SOURCE folders are errors; a module 'owns' pattern
    matching no REPO folder is a warning (aligns with 'no folder in the repo').
    """
    errors = []
    warnings = []
    repo_folders, source_folders = enumerate_folders(root, cfg)
    for folder in source_folders:
        hits = resolve_module(folder, modules)
        if not hits:
            errors.append(f"E: source folder {folder} maps to no module (orphan)")
        elif len(hits) > 1:
            errors.append(
                f"E: source folder {folder} is double-mapped to modules "
                f"{', '.join(hits)}")
    for m in modules:
        code = m.get("code")
        for g in m.get("owns", []):
            rx = _glob_to_re(g)
            if not any(rx.match(f) for f in repo_folders):
                warnings.append(
                    f"W: module {code} owns '{g}' which matches no folder under a configured source root")
    return errors, warnings


def _run_verify(root, cfg, specs_dir, as_json):
    """--verify lint: (1) freshness — every file in render_all(harvest(...), cfg)
    must be byte-identical to its committed copy, with no stale modules/*.md
    shards left behind, and (2) registration — every harvested feature code must
    appear in <specsDir>/INDEX.md. Returns 1 and reports on either failure;
    returns 0 when both hold.
    """
    errors = []
    warnings = []
    graph = harvest(specs_dir, cfg)
    files = render_all(graph, cfg)
    for relpath, content in files.items():
        p = os.path.join(specs_dir, relpath)
        committed = None
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as fh:
                committed = fh.read()
        if committed != content:
            errors.append(f"{relpath} is stale — run `check-graph --harvest` and commit the result.")
    for name in _stale_shards(specs_dir, files):
        errors.append(f"E: stale shard modules/{name} — run `check-graph --harvest`.")

    index_md_path = os.path.join(specs_dir, "INDEX.md")
    index_text = ""
    if os.path.exists(index_md_path):
        with open(index_md_path, "r", encoding="utf-8") as fh:
            index_text = fh.read()
    for f in graph["features"]:
        registered = re.search(r"\b" + re.escape(f["code"]) + r"\b", index_text, re.ASCII) is not None
        if not registered:
            errors.append(f"E: feature code {f['code']} is not registered in INDEX.md")

    # boundary verification (MODMAP): only when a valid manifest is present.
    modules, validity_errors = load_manifest(cfg)
    if validity_errors:
        errors.extend(validity_errors)
    elif modules:
        berrors, bwarnings = _verify_boundaries(root, cfg, modules)
        errors.extend(berrors)
        warnings.extend(bwarnings)

    if as_json:
        print(json.dumps({"errors": errors, "warnings": warnings}, indent=2, ensure_ascii=False))
    else:
        print(f"check-graph --verify: {'FAIL' if errors else 'OK'}")
        for e in errors:
            print(f"  {e}")
        for w in warnings:
            print(f"  {w}")
    return 1 if errors else 0


def main(argv):
    """CLI entry point. Never calls sys.exit — returns the exit code.

    Flags: --root R, --json, --query --path P --keyword K, --verify.
    --harvest is NOT parsed: it is the fall-through default mode. Unknown
    flags are ignored silently (no argparse — that exits 2 on an unknown flag).
    """
    root_idx = argv.index("--root") if "--root" in argv else -1
    root = os.path.abspath(argv[root_idx + 1]) if root_idx != -1 else os.getcwd()
    as_json = "--json" in argv

    try:
        cfg = load_config(root)
    except ConfigError as exc:
        print(f"check-graph: {exc}", file=sys.stderr)
        return 1

    specs_dir = os.path.join(root, cfg["specsDir"])

    if "--query" in argv:
        graph = harvest(specs_dir, cfg)
        res = query(graph, paths=_collect_flag(argv, "--path"), keywords=_collect_flag(argv, "--keyword"))
        cap = cfg["graph"]["queryCap"]
        kept, omitted = res[:cap], max(0, len(res) - cap)
        for r in kept:
            r["card"] = dict(r["card"], oos=[_first_sentence(x) for x in r["card"]["oos"]])
        if as_json:
            print(json.dumps({"results": kept, "omitted": omitted}, indent=2, ensure_ascii=False))
        else:
            print("\n".join(f"{r['code']} ({len(r['overlapPaths'])})" for r in kept))
            if omitted:
                print(f"(+{omitted} more omitted)")
        return 0

    if "--verify" in argv:
        return _run_verify(root, cfg, specs_dir, as_json)

    # default: --harvest
    graph = harvest(specs_dir, cfg)
    if not os.path.exists(specs_dir):
        print(f"check-graph: no specs dir at {cfg['specsDir']}", file=sys.stderr)
        return 0
    files = render_all(graph, cfg)
    for relpath, content in files.items():
        dest = os.path.join(specs_dir, relpath)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(content)
    for name in _stale_shards(specs_dir, files):
        os.remove(os.path.join(specs_dir, "modules", name))
    print(f"check-graph: wrote GRAPH.md — {len(graph['features'])} features, {len(graph['shared'])} shared paths.")
    return 0


# Deliberately duplicated across the vendored linters (not shared) — this file ships standalone with zero cross-imports.
# Run main() only when this file IS the entry point. Comparing realpath on
# both sides is what makes a copy under /tmp (a symlink to /private/tmp on
# macOS) actually run its CLI instead of silently no-op'ing.
def _invoked_as_script():
    argv0 = sys.argv[0] if sys.argv else None
    if not argv0:
        return False
    try:
        return os.path.realpath(argv0) == os.path.realpath(__file__)
    except OSError:
        return False


if _invoked_as_script():
    sys.exit(main(sys.argv[1:]))
