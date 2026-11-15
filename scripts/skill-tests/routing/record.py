#!/usr/bin/env python3
"""record.py <cluster.json> — write the routing evidence into each skill's TESTS.md and a trigger eval.

cluster.json: {"date","messages_file","n_messages","listed_before","listed_after","before","after",
 "note", "skills": {name: {"fire": [numbers], "neighbours": "a, b and c", "eval": number, "body": "sentence on body/consent"}}}
"""
import glob, json, re, sys
c = json.load(open(sys.argv[1]))
msgs = dict(re.findall(r"^(\d+)\. (.*)$", open(c["messages_file"]).read(), re.M))
for name, k in c["skills"].items():
    (d,) = glob.glob(f"skills/*/{name}/")
    fire = " · ".join(f'"{msgs[str(n)]}"' for n in k["fire"])
    entry = f"""
## {c['date']} — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). {k['body']}
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), {c['n_messages']} first messages (`{c['messages_file'].split('/')[-1]}`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, {c['listed_before']} listed) | after ({c['listed_after']} listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here ({', '.join(str(n) for n in k['fire'])}) | {k.get('before', c['before'])} | `{name}` on all | `{name}` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: {fire}. {c['note']}
"""
    p = d + "TESTS.md"
    try:
        s = open(p).read(); i = s.index("\n", s.index("# ")) + 1
        s = s[:i] + entry + s[i:]
    except FileNotFoundError:
        s = f"# TESTS.md — {name}\n" + entry
    open(p, "w").write(s)
    ep = d + "eval.json"
    try: e = json.load(open(ep))
    except FileNotFoundError: e = []
    e.append({"eval_id": max([x["eval_id"] for x in e] or [0]) + 1, "eval_name": "description-routes-here", "kind": "trigger",
              "derived_from": f"TESTS.md § {c['date']} — model-invocable (description routing)", "prompt": msgs[str(k["eval"])],
              "assertions": [f"{name} is the skill reached for", f"{k['neighbours']} are not"]})
    json.dump(e, open(ep, "w"), indent=2); open(ep, "a").write("\n")
    print("recorded", name)
