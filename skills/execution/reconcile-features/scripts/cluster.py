"""Path clustering for new-capability OBS candidates."""

from __future__ import annotations

from collections import defaultdict

PATH_STOPWORDS = {
    "apps",
    "app",
    "src",
    "lib",
    "internal",
    "routes",
    "features",
    "crates",
    "packages",
    "backend",
    "frontend",
    # "web" kept meaningful — monorepo package name (apps/web/…)
    "server",
    "client",
    "test",
    "tests",
    "__tests__",
    "node_modules",
    "target",
    "dist",
    "build",
    "vendor",
    "generated",
    "gen",
}


def meaningful_segments(path: str) -> list[str]:
    return [s for s in path.split("/") if s and s not in PATH_STOPWORDS]


def _directory_segments(path: str) -> list[str]:
    """Path segments with a trailing filename (has '.') removed."""
    parts = [s for s in path.split("/") if s]
    if parts and "." in parts[-1]:
        parts = parts[:-1]
    return parts


def cluster_key(path: str) -> str:
    """Two-segment directory key: meaningful pair, or one meaningful + next raw."""
    dirs = _directory_segments(path)
    if not dirs:
        return path.split("/")[0] if path else "platform"
    meaningful_idx = [i for i, s in enumerate(dirs) if s not in PATH_STOPWORDS]
    if len(meaningful_idx) >= 2:
        i, j = meaningful_idx[0], meaningful_idx[1]
        return f"{dirs[i]}/{dirs[j]}"
    if len(meaningful_idx) == 1:
        i = meaningful_idx[0]
        if i + 1 < len(dirs):
            return f"{dirs[i]}/{dirs[i + 1]}"
        if i > 0:
            return f"{dirs[i - 1]}/{dirs[i]}"
        return dirs[i]
    # all stopwords — keep last two raw directory segments
    if len(dirs) >= 2:
        return f"{dirs[-2]}/{dirs[-1]}"
    return dirs[0]


def longest_common_prefix(paths: list[str]) -> list[str]:
    if not paths:
        return []
    split = [p.split("/") for p in paths]
    prefix: list[str] = []
    for parts in zip(*split):
        if len(set(parts)) != 1:
            break
        prefix.append(parts[0])
    return prefix


def domain_slug(paths: list[str]) -> str:
    """Domain from longest common meaningful prefix — majority roots win."""
    if not paths:
        return "platform"
    # Prefer LCP of all paths, then strip stopwords from the right
    lcp = longest_common_prefix(paths)
    segs = [s for s in lcp if s and s not in PATH_STOPWORDS]
    if segs:
        slug = segs[-1].lower().replace("_", "-")[:32]
        return slug or "platform"
    # Fall back: majority first meaningful segment
    votes: dict[str, int] = defaultdict(int)
    for p in paths:
        ms = meaningful_segments(p)
        if ms:
            votes[ms[0].lower().replace("_", "-")[:32]] += 1
    if not votes:
        return "platform"
    return sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def surface_roots(paths: list[str], max_roots: int = 3) -> list[str]:
    """Stable roots = LCP + one segment, or per-path meaningful prefixes."""
    lcp = longest_common_prefix(paths)
    roots: list[str] = []
    if len(lcp) >= 2:
        root = "/".join(lcp) + "/"
        roots.append(root)
        return roots[:max_roots]
    for p in sorted(paths):
        parts = p.split("/")
        keep: list[str] = []
        for part in parts:
            keep.append(part)
            if part not in PATH_STOPWORDS and len(keep) >= 2:
                break
        if not keep:
            continue
        root = "/".join(keep)
        if not root.endswith("/") and "." not in keep[-1]:
            root += "/"
        if root not in roots:
            roots.append(root)
        if len(roots) >= max_roots:
            break
    return roots


def cluster_unowned_paths(paths: list[str]) -> dict[str, list[str]]:
    """Group unowned behavior paths by directory cluster keys (not filenames)."""
    groups: dict[str, list[str]] = defaultdict(list)
    for p in paths:
        groups[cluster_key(p)].append(p)
    return dict(groups)
