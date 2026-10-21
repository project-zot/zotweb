#!/usr/bin/env python3
"""Snapshot the current ("latest") docs into a frozen version.

usage: scripts/snapshot-version.py v2.1.x

Copies every page in the latest navigation to <label>/..., rewrites absolute
internal links to the snapshot prefix, and adds the version to docs.json
(`navigation.versions`; the first entry, "latest", is the default). Re-running
for an existing label rebuilds that snapshot from latest.
"""
import copy, json, os, re, shutil, sys

if len(sys.argv) != 2:
    sys.exit(__doc__)
label = sys.argv[1].strip("/")
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
cfg = json.load(open("docs.json"))
nav = cfg["navigation"]

if "versions" in nav:
    latest = next(v for v in nav["versions"] if v["version"] == "latest")
    others = [v for v in nav["versions"] if v["version"] not in ("latest", label)]
else:
    latest, others = {"version": "latest", "tabs": nav.pop("tabs")}, []

def walk(groups):
    for g in groups:
        for p in g.get("pages", []):
            if isinstance(p, str):
                yield p
            else:
                yield from walk([p])

pages = [p for t in latest["tabs"] for p in walk(t.get("groups", []))]
openapi = [g["openapi"] for t in latest["tabs"] for g in t.get("groups", []) if isinstance(g.get("openapi"), str)]
pageset = set(pages)

shutil.rmtree(label, ignore_errors=True)
link = re.compile(r'''(\]\(|href=["']|to=["'])(/[^)"'#?\s]*)''')

def rewrite(m):
    target = m.group(2)
    key = "index" if target == "/" else target.strip("/")
    return m.group(1) + f"/{label}/{key}" if key in pageset else m.group(0)

for p in pages:
    dst = f"{label}/{p}.mdx"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w").write(link.sub(rewrite, open(f"{p}.mdx").read()))
for f in openapi:
    os.makedirs(os.path.dirname(f"{label}/{f}"), exist_ok=True)
    shutil.copy(f, f"{label}/{f}")

def prefix(groups):
    out = []
    for g in groups:
        g = copy.deepcopy(g)
        if "pages" in g:
            g["pages"] = [f"{label}/{p}" if isinstance(p, str) else prefix([p])[0] for p in g["pages"]]
        if isinstance(g.get("openapi"), str):
            src = g["openapi"]
            g["openapi"] = {"source": f"{label}/{src}", "directory": f"{label}/{os.path.dirname(src)}"}
        out.append(g)
    return out

snap_tabs = []
for t in latest["tabs"]:
    t = copy.deepcopy(t)
    t["groups"] = prefix(t.get("groups", []))
    snap_tabs.append(t)

nav["versions"] = [latest] + others + [{"version": label, "tabs": snap_tabs}]
json.dump(cfg, open("docs.json", "w"), indent=2); open("docs.json", "a").write("\n")
print(f"snapshot {label}: {len(pages)} pages, {len(openapi)} openapi file(s)")
