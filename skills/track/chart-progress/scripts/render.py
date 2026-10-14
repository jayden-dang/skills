"""Render a progress snapshot (from extract.py) into one self-contained HTML page.

Deterministic: the same snapshot and notes give the same bytes. The only prose not
derived from the snapshot is the optional notes file the agent writes.

    python3 render.py snapshot.json [--notes notes.json] --out dashboard.html

notes.json: {"summary": "...", "recommendations": ["...", ...]}
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import zlib
from pathlib import Path

STATE_LABEL = {
    "done": "done", "building": "building", "specced": "specced",
    "framing": "framing", "unspecced": "unspecced", "deferred": "deferred", "retired": "retired",
}

CSS = """
:root{--paper:#F5F7F4;--panel:#FFFFFF;--ink:#18211E;--muted:#5B6A64;--rule:#D9DFDB;
--accent:#1F5FBF;--accent-soft:#E3ECFA;--done:#2E7D4F;--done-soft:#E1F1E7;--build:#B7791F;
--build-soft:#FBF0DC;--alert:#C2412D;--alert-soft:#F9E3DE;--idle:#8A9792;--idle-soft:#ECEFED;
--display:Charter,"Iowan Old Style","Palatino Linotype",Georgia,serif;
--body:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
@media (prefers-color-scheme: dark){:root{--paper:#111715;--panel:#18201D;--ink:#E3EAE6;--muted:#95A49E;
--rule:#2A3531;--accent:#7FA8F0;--accent-soft:#1B2A44;--done:#5CC48A;--done-soft:#163225;--build:#E0A84A;
--build-soft:#3A2C12;--alert:#F07B63;--alert-soft:#3F1D16;--idle:#7D8B86;--idle-soft:#212A27}}
:root[data-theme="dark"]{--paper:#111715;--panel:#18201D;--ink:#E3EAE6;--muted:#95A49E;
--rule:#2A3531;--accent:#7FA8F0;--accent-soft:#1B2A44;--done:#5CC48A;--done-soft:#163225;--build:#E0A84A;
--build-soft:#3A2C12;--alert:#F07B63;--alert-soft:#3F1D16;--idle:#7D8B86;--idle-soft:#212A27}
:root[data-theme="light"]{--paper:#F5F7F4;--panel:#FFFFFF;--ink:#18211E;--muted:#5B6A64;--rule:#D9DFDB;
--accent:#1F5FBF;--accent-soft:#E3ECFA;--done:#2E7D4F;--done-soft:#E1F1E7;--build:#B7791F;
--build-soft:#FBF0DC;--alert:#C2412D;--alert-soft:#F9E3DE;--idle:#8A9792;--idle-soft:#ECEFED}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 var(--body)}
header.top{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:baseline;justify-content:space-between;
padding:20px 32px;border-bottom:1px solid var(--rule)}
header.top h1{font:600 26px/1.2 var(--display);margin:0;text-wrap:balance}
.meta{font:13px var(--mono);color:var(--muted)}
nav.jump{display:flex;flex-wrap:wrap;gap:6px 14px;padding:10px 32px;position:sticky;top:0;z-index:2;
background:var(--paper);border-bottom:1px solid var(--rule);font-size:13px}
nav.jump a{color:var(--muted);text-decoration:none}
nav.jump a:hover,nav.jump a:focus-visible{color:var(--accent)}
button.theme{margin-left:auto;font:12px var(--body);color:var(--muted);background:none;border:1px solid var(--rule);
border-radius:4px;padding:2px 8px;cursor:pointer}
main{display:grid;grid-template-columns:minmax(0,1fr);gap:28px;padding:24px 32px 64px;max-width:1500px}
main>*,.cols>*,.grid-domains>*{min-width:0}
li,p{overflow-wrap:anywhere}
section>h2{font:600 20px/1.25 var(--display);margin:0 0 12px;text-wrap:balance}
h3{font:600 12px/1.3 var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 8px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.tile{background:var(--panel);border:1px solid var(--rule);border-radius:6px;padding:12px 14px}
.tile b{display:block;font:600 28px/1.1 var(--mono);font-variant-numeric:tabular-nums}
.tile span{font-size:13px;color:var(--muted)}
.tile.warn{border-left:4px solid var(--alert)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:20px}
.card{background:var(--panel);border:1px solid var(--rule);border-radius:6px;padding:16px 18px;min-width:0}
.notes{border-left:4px solid var(--accent)}
.notes p{margin:0 0 8px;max-width:75ch}
.notes ol{margin:0;padding-left:20px}
.src{font-size:12px;color:var(--muted)}
table{border-collapse:collapse;width:100%;font-size:14px}
th{font:600 12px var(--body);letter-spacing:.04em;text-transform:uppercase;color:var(--muted);text-align:left;
padding:6px 8px;border-bottom:1px solid var(--rule)}
td{padding:6px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;font-family:var(--mono)}
.scroll{overflow-x:auto}
code,.id{font-family:var(--mono);font-size:13px}
.pill{display:inline-block;font:600 11px/1.6 var(--body);letter-spacing:.03em;padding:0 7px;border-radius:9px;
white-space:nowrap;background:var(--idle-soft);color:var(--idle)}
.pill.done{background:var(--done-soft);color:var(--done)}
.pill.building{background:var(--build-soft);color:var(--build)}
.pill.ready,.pill.specced,.pill.framing{background:var(--accent-soft);color:var(--accent)}
.pill.alert{background:var(--alert-soft);color:var(--alert)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font:12px var(--mono);border:1px solid var(--rule);border-radius:4px;padding:1px 6px;background:var(--paper)}
.bar{height:6px;border-radius:3px;background:var(--idle-soft);overflow:hidden;min-width:80px}
.bar i{display:block;height:100%;background:var(--done)}
.path{display:flex;flex-wrap:wrap;gap:4px;align-items:center;font:13px var(--mono)}
.path span+span::before{content:"→";color:var(--muted);margin-right:4px}
details{border-top:1px solid var(--rule);padding:8px 0}
details>summary{cursor:pointer;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
details>summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.grid-domains{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.stack{display:flex;height:10px;border-radius:5px;overflow:hidden;background:var(--idle-soft);margin:6px 0 8px}
.stack i{display:block;height:100%}
figure{margin:0}
figcaption{font-size:13px;color:var(--muted);margin-top:6px;max-width:75ch}
svg text{font-family:var(--mono)}
.empty{color:var(--muted);font-style:italic}
a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-reduced-motion: reduce){*{scroll-behavior:auto}}
html{scroll-behavior:smooth}
"""

THEME_JS = """
document.querySelector('button.theme').addEventListener('click',function(){
 var r=document.documentElement,c=r.getAttribute('data-theme');
 var dark=c?c==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;
 r.setAttribute('data-theme',dark?'light':'dark');});
"""


def e(s: object) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def num(i: str) -> int:
    return int(i.split("-")[1])


def pill(state: str, label: str | None = None) -> str:
    return f'<span class="pill {e(state)}">{e(label or STATE_LABEL.get(state, state))}</span>'


# ---------------------------------------------------------------- svg layout


def layered(nodes: list[str], edges: list[tuple[str, str]], order: dict[str, int]) -> dict[str, tuple[int, int]]:
    """Column = longest path from a root; row = barycenter of predecessors, then input order."""
    preds: dict[str, list[str]] = {n: [] for n in nodes}
    for a, b in edges:
        if a in preds and b in preds:
            preds[b].append(a)
    col: dict[str, int] = {}

    def depth(n: str, guard: frozenset = frozenset()) -> int:
        if n in col:
            return col[n]
        d = 0
        for p in preds[n]:
            if p not in guard:
                d = max(d, depth(p, guard | {n}) + 1)
        col[n] = d
        return d

    for n in nodes:
        depth(n)
    pos: dict[str, tuple[int, int]] = {}
    for c in range(max(col.values(), default=-1) + 1):
        layer = [n for n in nodes if col[n] == c]

        def key(n: str) -> tuple[float, int]:
            rows = [pos[p][1] for p in preds[n] if p in pos]
            return (sum(rows) / len(rows) if rows else -1.0, order[n])

        for r, n in enumerate(sorted(layer, key=key)):
            pos[n] = (c, r)
    return pos


def svg_graph(title: str, desc: str, nodes: list[dict], edges: list[tuple[str, str]],
              w: int = 210, h: int = 66, gx: int = 64, gy: int = 18) -> str:
    """nodes: {id, label, sub, kind, frac?, ghost?}. kind picks the stroke/fill tokens."""
    if not nodes:
        return ""
    order = {n["id"]: i for i, n in enumerate(nodes)}
    pos = layered([n["id"] for n in nodes], edges, order)
    pad = 24
    cols = max(c for c, _ in pos.values()) + 1
    rows = max(r for _, r in pos.values()) + 1
    width = pad * 2 + cols * w + (cols - 1) * gx
    height = pad * 2 + rows * h + (rows - 1) * gy

    def xy(nid: str) -> tuple[int, int]:
        c, r = pos[nid]
        return pad + c * (w + gx), pad + r * (h + gy)

    fill = {"done": "var(--done-soft)", "building": "var(--build-soft)", "ready": "var(--accent-soft)",
            "committed": "var(--accent-soft)", "closed": "var(--done-soft)"}
    stroke = {"done": "var(--done)", "building": "var(--build)", "ready": "var(--accent)",
              "committed": "var(--accent)", "closed": "var(--done)", "alert": "var(--alert)"}
    tid = f"t-{zlib.crc32(title.encode()):08x}"
    out = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" '
           f'aria-labelledby="{tid}">',
           f'<title id="{tid}">{e(title)}</title><desc>{e(desc)}</desc>',
           '<defs><marker id="arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" '
           'orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="var(--muted)"/></marker></defs>']
    for a, b in edges:
        if a not in pos or b not in pos:
            continue
        x1, y1 = xy(a)
        x2, y2 = xy(b)
        x1, y1 = x1 + w, y1 + h // 2
        y2 = y2 + h // 2
        mx = (x1 + x2) / 2
        out.append(f'<path d="M{x1},{y1} C{mx:.0f},{y1} {mx:.0f},{y2} {x2 - 2},{y2}" fill="none" '
                   f'stroke="var(--muted)" stroke-opacity=".55" stroke-width="1.2" marker-end="url(#arr)"/>')
    for n in nodes:
        x, y = xy(n["id"])
        k = n.get("kind", "")
        dash = ' stroke-dasharray="4 3"' if n.get("ghost") else ""
        out.append(f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="var(--panel)"/>'
                   f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill.get(k, "var(--panel)")}" '
                   f'stroke="{stroke.get(k, "var(--idle)")}" stroke-width="{1.6 if k in stroke else 1}"{dash}/>')
        head = n.get("head", "")
        label = n["label"] if len(n["label"]) <= 27 else n["label"][:26] + "…"
        sub = n.get("sub", "")
        sub = sub if len(sub) <= 30 else sub[:29] + "…"
        out.append(f'<text x="{x + 10}" y="{y + 17}" font-size="11" fill="var(--muted)">{e(head)}</text>'
                   f'<text x="{x + 10}" y="{y + 34}" font-size="12.5" font-weight="600" fill="var(--ink)" '
                   f'style="font-family:var(--body)">{e(label)}</text>'
                   f'<text x="{x + 10}" y="{y + 50}" font-size="11" fill="var(--muted)">{e(sub)}</text>')
        if n.get("frac") is not None:
            bw = int((w - 20) * n["frac"])
            out.append(f'<rect x="{x + 10}" y="{y + h - 9}" width="{w - 20}" height="3" rx="1.5" fill="var(--idle-soft)"/>'
                       f'<rect x="{x + 10}" y="{y + h - 9}" width="{bw}" height="3" rx="1.5" fill="var(--done)"/>')
        out.append(f'<title>{e(n.get("tip", n["label"]))}</title></g>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- sections


def tiles(s: dict) -> str:
    g, w, m = s["graph"], s["windows"]["week"], s["windows"]["month"]
    building = [f for f in s["features"] if f["status"] == "In-progress"]
    cov = s["coverage"]
    t = [(len(w["finished"]), "finished this week", ""), (len(m["finished"]), "finished in 30 days", ""),
         (len(building), "building now", ""), (len(g["ready"]), "ready to start", ""),
         (len(s["findings"]), "structural findings", "warn" if s["findings"] else ""),
         (f'{cov["with_after"]}/{cov["live_items"]}', "items with After:",
          "warn" if s["has_roadmap"] and cov["with_after"] < cov["live_items"] else "")]
    return '<div class="tiles">' + "".join(
        f'<div class="tile {c}"><b>{e(v)}</b><span>{e(lbl)}</span></div>' for v, lbl, c in t) + "</div>"


def notes_card(notes: dict | None) -> str:
    if not notes:
        return ""
    recs = "".join(f"<li>{e(r)}</li>" for r in notes.get("recommendations", []))
    return (f'<div class="card notes"><h3>Notes for next week</h3><p>{e(notes.get("summary", ""))}</p>'
            f'{"<ol>" + recs + "</ol>" if recs else ""}'
            '<p class="src">Written by the agent from this snapshot; every number below is derived, not written.</p></div>')


def plan_section(s: dict) -> str:
    items = {i["id"]: i for i in s["items"]}
    g = s["graph"]
    ms = {m["id"]: m for m in s["milestones"]}
    rank = sorted(g["ready"], key=lambda r: (
        0 if ms[items[r]["milestone"]]["commitment"] == "Committed" else 1,
        ms[items[r]["milestone"]]["order"], -g["unlocks"].get(r, 0), num(r)))
    rows = "".join(
        f'<tr><td class="id">{e(r)}</td><td>{e(items[r]["slug"])}</td><td>{pill(items[r]["state"])}'
        f'{" " + e(items[r]["feature"]) if items[r]["feature"] else ""}</td>'
        f'<td class="id">{e(items[r]["milestone"])} <span class="src">{e(ms[items[r]["milestone"]]["commitment"])}</span></td>'
        f'<td class="n">{g["unlocks"].get(r, 0)}</td></tr>' for r in rank)
    ready = (f'<div class="scroll"><table><thead><tr><th>Item</th><th>Slug</th><th>State</th><th>Milestone</th>'
             f'<th class="n">Unlocks</th></tr></thead><tbody>{rows}</tbody></table></div>'
             if rank else '<p class="empty">Nothing is ready: every open item waits on unfinished work.</p>')
    building = "".join(
        f'<tr><td class="id">{e(i["id"])}</td><td>{e(i["feature"])}</td><td>{e(i["slug"])}</td>'
        f'<td>{progress(s, i["feature"])}</td></tr>' for i in s["items"] if i["state"] == "building")
    by_path: dict[str, set] = {}
    for c in g["conflicts"]:
        for p in c["paths"]:
            by_path.setdefault(p, set()).update(c["items"])
    conflicts = "".join(
        f'<li><code>{e(p)}</code> — {", ".join(sorted(ids, key=num))}</li>'
        for p, ids in sorted(by_path.items(), key=lambda kv: (-len(kv[1]), kv[0])))
    crit = "".join(f'<span title="{e(items[r]["slug"])}">{e(r)}</span>' for r in g["critical_path"])
    closable = g.get("closable", [])
    close_html = ("<div class='chips'>" + "".join(
        f'<span class="chip" title="{e(ms[m]["outcome"])}">{e(m)} {e(ms[m]["name"])}</span>' for m in closable) + "</div>"
        + '<p class="src">Every live member is done but the milestone is not Closed. Run /assess-milestone on each before closing it.</p>'
        ) if closable else '<p class="empty">None.</p>'
    return f"""<section id="plan"><h2>Plan next week</h2><div class="cols">
<div class="card"><h3>Ready to start ({len(rank)})</h3>{ready}
<p class="src">Ready = not done, not building, and everything in its After: is done. Ranked: committed milestones first, then milestone order, then how many items it unlocks.</p></div>
<div class="card"><h3>Building now</h3>{"<div class='scroll'><table><thead><tr><th>Item</th><th>Feature</th><th>Slug</th><th>Tasks</th></tr></thead><tbody>" + building + "</tbody></table></div>" if building else '<p class="empty">Nothing in progress.</p>'}
<h3 style="margin-top:16px">Critical path ({len(g["critical_path"])} items)</h3>{"<div class='path'>" + crit + "</div>" if crit else '<p class="empty">No open chain.</p>'}
<p class="src">The longest chain of unfinished items; its length bounds how soon the last of them can land.</p>
<h3 style="margin-top:16px">Milestones ready to close ({len(closable)})</h3>{close_html}
<h3 style="margin-top:16px">Shared paths among ready and building items ({len(by_path)})</h3>
<p class="src">Items listed on one path touch it together; run them in sequence or agree the split first.</p>
{"<ul>" + conflicts + "</ul>" if conflicts else '<p class="empty">No two of them touch the same path.</p>'}
</div></div></section>"""


def progress(s: dict, code: str | None) -> str:
    f = next((x for x in s["features"] if x["code"] == code), None)
    if not f or not f.get("tasks_total"):
        return '<span class="src">no tasks.md</span>'
    if f.get("tasks_done") is None:
        return f'<span class="src">{f["tasks_total"]} tasks, no ledger</span>'
    done = f["tasks_done"]
    frac = min(1.0, done / f["tasks_total"])
    return (f'<div style="display:flex;gap:8px;align-items:center"><div class="bar"><i style="width:{frac * 100:.0f}%"></i></div>'
            f'<span class="id">{done}/{f["tasks_total"]}</span></div>')


def window_card(title: str, w: dict, feats: dict) -> str:
    def codes(lst: list[str]) -> str:
        return ('<div class="chips">' + "".join(
            f'<span class="chip" title="{e(feats.get(c, {}).get("name", ""))}">{e(c)}</span>' for c in lst) + "</div>"
                if lst else '<p class="empty">None.</p>')
    def brief(ids: list[str]) -> str:
        return ", ".join(ids) if len(ids) <= 12 else ", ".join(ids[:12]) + f" … +{len(ids) - 12} more"
    road = []
    if w["roadmap_new"]:
        road.append(f'new ({len(w["roadmap_new"])}): {brief(w["roadmap_new"])}')
    if w["roadmap_revived"]:
        road.append(f'back from deferred: {brief(w["roadmap_revived"])}')
    if w["roadmap_dropped"]:
        road.append(f'left the plan: {brief(w["roadmap_dropped"])}')
    scopes = "".join(f'<tr><td><code>{e(k)}</code></td><td class="n">{v}</td></tr>' for k, v in w["scopes"][:8])
    batches = "".join(
        f'<p class="src">{pill("alert", "batch")} <span class="id">{e(b["sha"])}</span> on {e(b["date"])} moved '
        f'{len(b["codes"])} features to done at once ({e(", ".join(b["codes"]))}): that date is when the record caught up, '
        'not necessarily when the work finished.</p>' for b in w.get("batches", []))
    return f"""<div class="card"><h3>{e(title)} — since {e(w["since"])}</h3>
<p><b>Finished ({len(w["finished"])})</b></p>{codes(w["finished"])}{batches}
<p><b>Started ({len(w["started"])})</b></p>{codes(w["started"])}
<p><b>New specs ({len(w["specced"])})</b></p>{codes(w["specced"])}
<p><b>Roadmap</b></p>{"<p class='id'>" + e("; ".join(road)) + "</p>" if road else '<p class="empty">No item entered or left the plan.</p>'}
<p><b>Decisions ({len(w["adrs"])})</b></p>{codes(w["adrs"])}
<p><b>Commits</b> <span class="id">{w["commits"]}</span> · merges <span class="id">{w["merges"]}</span></p>
<div class="scroll"><table><tbody>{scopes}</tbody></table></div></div>"""


def happened_section(s: dict) -> str:
    feats = {f["code"]: f for f in s["features"]}
    return (f'<section id="happened"><h2>What happened</h2><div class="cols">'
            f'{window_card("Last 7 days", s["windows"]["week"], feats)}'
            f'{window_card("Last 30 days", s["windows"]["month"], feats)}</div>'
            '<p class="src">Finished and started come from status changes in the catalog\'s git history, not from commit messages.</p></section>')


def roadmap_section(s: dict) -> str:
    if not s["has_roadmap"] or not s["milestones"]:
        return '<section id="roadmap"><h2>Roadmap</h2><p class="empty">No roadmap in this repo (docs/roadmap/INDEX.md).</p></section>'
    items = {i["id"]: i for i in s["items"]}
    ready = set(s["graph"]["ready"])
    live_ms = [m for m in s["milestones"] if not m["retired"]]
    nodes = []
    for m in live_ms:
        c = m["counts"]
        total = sum(c.values())
        kind = {"Closed": "closed", "Committed": "committed"}.get(m["commitment"], "")
        if total and c["done"] == total:
            kind = "done"
        nodes.append({"id": m["id"], "head": f'{m["id"]} · {m["commitment"]}', "label": m["name"], "sub": f'{c["done"]}/{total} done',
                      "kind": kind, "frac": (c["done"] / total) if total else None, "tip": m["outcome"]})
    medges = [(d, m["id"]) for m in live_ms for d in m["depends_on"]]
    overview = svg_graph("Which milestones wait on which", "Milestone dependency graph; arrows point from the milestone that must finish first.",
                         nodes, medges)
    blocks = []
    for m in live_ms:
        mine = [items[r] for r in m["members"] if items[r]["state"] not in ("retired",)]
        if not mine:
            continue
        ids = {i["id"] for i in mine}
        gnodes, gedges, ghosts = [], [], {}
        for i in mine:
            state = "ready" if i["id"] in ready else i["state"]
            gnodes.append({"id": i["id"], "head": f'{i["id"]} · {state}', "label": i["slug"],
                           "sub": (i["feature"] or "no spec") + ("" if i["after_source"] == "field" else " · implied order"),
                           "kind": state, "tip": f'After: {", ".join(i["after"]) or "none"}'})
        for a, b in s["graph"]["edges"]:
            if b in ids:
                if a not in ids and a not in ghosts and a in items:
                    ghosts[a] = {"id": a, "head": f'{a} · {items[a]["state"]}', "label": items[a]["slug"], "sub": items[a]["milestone"],
                                 "kind": items[a]["state"], "ghost": True}
                gedges.append((a, b))
        fig = svg_graph(f'Build order inside {m["id"]}', f'Items of {m["id"]} and the outside items they wait on (dashed).',
                        list(ghosts.values()) + gnodes, gedges)
        c = m["counts"]
        summary = (f'<span class="id">{e(m["id"])}</span> <b>{e(m["name"])}</b> {pill("done" if m["commitment"] == "Closed" else ("ready" if m["commitment"] == "Committed" else "idle"), m["commitment"])}'
                   f' <span class="src">{c["done"]} done · {c["building"]} building · {c["specced"] + c["framing"]} specced/framing · {c["unspecced"]} unspecced</span>')
        blocks.append(f'<details><summary>{summary}</summary><p style="max-width:75ch">{e(m["outcome"])}</p>'
                      f'<figure class="scroll">{fig}<figcaption>Dashed boxes sit in another milestone. "implied" marks an item with no After: field, ordered by list position.</figcaption></figure></details>')
    return f"""<section id="roadmap"><h2>Roadmap</h2>
<figure class="card scroll">{overview}<figcaption>Columns are dependency depth: everything in a column can proceed once the columns to its left are done. Bars show members done.</figcaption></figure>
<div class="card">{"".join(blocks)}</div></section>"""


def catalog_section(s: dict) -> str:
    colors = {"Shipped": "var(--done)", "Implemented": "var(--done)", "In-progress": "var(--build)",
              "Approved": "var(--accent)", "Draft": "var(--idle)", "Recognized": "var(--idle)", "Retired": "var(--rule)"}
    feats = {f["code"]: f for f in s["features"]}
    recent = {}
    for ev in s["windows"]["month"]["events"]:
        recent[ev["code"]] = ev
    cards = []
    for d in s["domains"]:
        total = sum(d["counts"].values())
        stack = "".join(f'<i style="width:{v / total * 100:.2f}%;background:{colors.get(k, "var(--idle)")}" title="{e(k)} {v}"></i>'
                        for k, v in sorted(d["counts"].items(), key=lambda kv: list(colors).index(kv[0]) if kv[0] in colors else 99))
        counts = " · ".join(f"{e(k)} {v}" for k, v in sorted(d["counts"].items()))
        active = [c for c in d["features"] if feats[c]["status"] in ("In-progress", "Approved", "Draft")]
        latest = sorted((recent[c] for c in d["features"] if c in recent and recent[c]["to"] in ("Implemented", "Shipped")),
                        key=lambda ev: ev["date"], reverse=True)[:5]
        cards.append(f"""<div class="card"><h3>{e(d["domain"])}</h3><div class="stack">{stack}</div>
<p class="src">{counts}</p>
<p><b>Open</b></p>{"<div class='chips'>" + "".join(f'<span class="chip" title="{e(feats[c]["name"])}">{e(c)} · {e(feats[c]["status"])}</span>' for c in active) + "</div>" if active else '<p class="empty">None.</p>'}
<p><b>Latest finished</b></p>{"<div class='chips'>" + "".join(f'<span class="chip" title="{e(feats[ev["code"]]["name"])}">{e(ev["code"])} · {e(ev["date"])}</span>' for ev in latest) + "</div>" if latest else '<p class="empty">None in 30 days.</p>'}
</div>""")
    return f'<section id="catalog"><h2>Catalog by domain</h2><div class="grid-domains">{"".join(cards)}</div></section>'


def architecture_section(s: dict) -> str:
    arch = s["architecture"]
    rows = "".join(f'<tr><td class="id">{e(a["id"])}</td><td>{e(a["title"])}</td><td class="n">{len(a["respected_by"])}</td></tr>'
                   for a in arch if not a["retired"])
    adrs = sorted((a for a in s["adrs"] if a["date"]), key=lambda a: (a["date"], a["id"]), reverse=True)[:15]
    arows = "".join(f'<tr><td class="id">{e(a["date"])}</td><td class="id">{e(a["id"])}</td><td>{e(a["title"])}</td>'
                    f'<td>{e((a["status"] or "").split(" ")[0])}</td></tr>' for a in adrs)
    return f"""<section id="architecture"><h2>Architecture</h2><div class="cols">
<div class="card"><h3>Invariants</h3>{"<div class='scroll'><table><thead><tr><th>ID</th><th>Invariant</th><th class='n'>Designs citing</th></tr></thead><tbody>" + rows + "</tbody></table></div>" if rows else '<p class="empty">No docs/architecture/INDEX.md.</p>'}
<p class="src">Designs citing = feature design.md files whose Respects: line names the invariant.</p></div>
<div class="card"><h3>Latest decisions</h3>{"<div class='scroll'><table><thead><tr><th>Date</th><th>ADR</th><th>Decision</th><th>Status</th></tr></thead><tbody>" + arows + "</tbody></table></div>" if arows else '<p class="empty">No ADRs.</p>'}</div>
</div></section>"""


def health_section(s: dict) -> str:
    cov = s["coverage"]
    f = "".join(f'<li>{pill("alert", x["rule"])} <span class="id">{e(x["item"])}</span> {e(x["detail"])}</li>' for x in s["findings"])
    gap = cov["live_items"] - cov["with_after"]
    cov_line = (f'<p><b>{cov["with_after"]} of {cov["live_items"]}</b> live items carry an After: field. '
                + (f'The other {gap} are ordered by list position, so the ready set and critical path treat them as one chain per milestone and understate what can run in parallel. Backfill them through plan-milestones.'
                   if gap else "Every item states its own order.") + "</p>") if s["has_roadmap"] else ""
    return f"""<section id="health"><h2>Health</h2><div class="card">{cov_line}
<h3>Structural findings</h3>{"<ul>" + f + "</ul>" if f else '<p class="empty">None: every After: target resolves and no chain loops.</p>'}</div></section>"""


def render(s: dict, notes: dict | None = None) -> str:
    title = f'{s["repo"]} — week of {s["today"]}'
    body = "".join([
        notes_card(notes), tiles(s), plan_section(s), happened_section(s), roadmap_section(s),
        catalog_section(s), architecture_section(s), health_section(s),
    ])
    nav = "".join(f'<a href="#{i}">{lbl}</a>' for i, lbl in [
        ("plan", "Plan next week"), ("happened", "What happened"), ("roadmap", "Roadmap"),
        ("catalog", "Catalog"), ("architecture", "Architecture"), ("health", "Health")])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><style>{CSS}</style></head><body>
<header class="top"><h1>{e(s["repo"])} — progress</h1>
<span class="meta">{e(s["today"])} · {e(s["branch"])} @ {e(s["head"])}</span></header>
<nav class="jump" aria-label="Sections">{nav}<button class="theme" type="button">Theme</button></nav>
<main>{body}</main><script>{THEME_JS}</script></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("snapshot")
    ap.add_argument("--notes")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    snap = json.loads(Path(a.snapshot).read_text())
    notes = json.loads(Path(a.notes).read_text()) if a.notes else None
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(render(snap, notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
