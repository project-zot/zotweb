#!/usr/bin/env python3
"""Apply scripts/redirect-map.json to docs.json (docs-domain redirects) and
landing/ (apex-domain redirect pages + 404 fallback). Safe to re-run."""
import json, os, re, shutil, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
DOCS = "https://docs.zotregistry.dev"
m = json.load(open("scripts/redirect-map.json"))

# 1. docs.json redirects (old unversioned path -> new path on the docs domain)
cfg = json.load(open("docs.json"))
cfg["redirects"] = [{"source": "/" + k, "destination": v} for k, v in m.items()]
json.dump(cfg, open("docs.json", "w"), indent=2); open("docs.json", "a").write("\n")

# 2. landing: static redirect pages for the old default (/latest/...) URLs
stub = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Moved | zot</title>
<link rel="canonical" href="{url}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={url}">
<script>location.replace("{url}" + location.hash);</script>
</head><body>This page moved to <a href="{url}">{url}</a>.</body></html>
"""
shutil.rmtree("landing/latest", ignore_errors=True)
for old, new in m.items():
    d = f"landing/latest/{old}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w").write(stub.format(url=DOCS + (new if new != "/" else "/")))
os.makedirs("landing/latest", exist_ok=True)
open("landing/latest/index.html", "w").write(stub.format(url=DOCS + "/"))

# 3. landing/404.html: maps any other old URL, including /vX.Y.Z/... and /zot/...
page = open("landing/404.html").read()
js = """<script>
(function () {
  var map = %s;
  var p = location.pathname.replace(/^\\/+|\\/+$/g, "").split("/");
  if (/^(latest|zot|v\\d+(\\.\\d+){1,2})$/.test(p[0] || "")) p.shift();
  var key = p.join("/").replace(/\\.html$/, "");
  var dest = map[key];
  var target = "%s" + (dest || "/");
  setTimeout(function () { location.replace(target + (dest ? location.hash : "")); }, 0);
})();
</script>""" % (json.dumps(m, indent=1), DOCS)
page = re.sub(r"<script>.*?</script>", "", page, flags=re.S)
page = page.replace("</head>", js + "\n</head>")
open("landing/404.html", "w").write(page)
print(len(m), "redirects applied")
