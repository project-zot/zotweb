#!/usr/bin/env python3
"""Generate the architecture and overview diagrams as theme-specific SVGs.

usage: build-diagrams.py --outfit Outfit.ttf --mono JetBrainsMono-Regular.ttf [--out images]

Text is converted to outlines (fontTools) so the diagrams render identically on
every platform. Requires fontTools. Fonts: Outfit (variable, SIL OFL) and a
monospace font such as JetBrains Mono (SIL OFL). Writes, for each diagram, a
`-light.svg` and a `-dark.svg` file; the docs show one or the other with
`dark:hidden` / `hidden dark:block`. Edit the content in the two `*_diagram`
functions below, then re-run.
"""
import argparse, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ap = argparse.ArgumentParser()
ap.add_argument("--outfit", required=True)
ap.add_argument("--mono", required=True)
ap.add_argument("--out", default="images")
ap.add_argument("--logo-dir", default="logo")
args = ap.parse_args()

_fonts = {}
def font(kind, wght=None):
    key = (kind, wght)
    if key not in _fonts:
        if kind == "sans":
            f = instantiateVariableFont(TTFont(args.outfit), {"wght": wght})
        else:
            f = TTFont(args.mono)
        _fonts[key] = (f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _fonts[key]

def text_width(s, size, kind="sans", wght=500):
    f, gs, cmap, upm = font(kind, wght)
    return sum(gs[cmap.get(ord(c), cmap[ord("?")])].width for c in s) * size / upm

def text(x, y, s, size, fill, kind="sans", wght=500, anchor="start"):
    """Outlined text with baseline at y."""
    f, gs, cmap, upm = font(kind, wght)
    w = text_width(s, size, kind, wght)
    if anchor == "middle": x -= w / 2
    elif anchor == "end": x -= w
    k = size / upm; pen = SVGPathPen(gs); cx = 0
    for c in s:
        g = gs[cmap.get(ord(c), cmap[ord("?")])]
        g.draw(TransformPen(pen, (k, 0, 0, -k, x + cx * k, y))); cx += g.width
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>'

THEMES = {
    "light": dict(text="#0F172A", muted="#475569", accent="#4F46E5", accent2="#7C3AED",
                  core_fill="#EEF2FF", core_stroke="#C7D2FE", ext_fill="#F5F3FF", ext_stroke="#DDD6FE",
                  chip_fill="#FFFFFF", frame_stroke="#CBD5E1", frame_fill="#F8FAFC", code_fill="#0F172A", code_text="#E2E8F0",
                  arrow="#6366F1", logo="light.svg"),
    "dark": dict(text="#F1F5F9", muted="#A3AEC2", accent="#A5B4FC", accent2="#C4B5FD",
                 core_fill="#1B2144", core_stroke="#363F78", ext_fill="#241D4A", ext_stroke="#453A85",
                 chip_fill="#0F1428", frame_stroke="#2B3550", frame_fill="#0E1322", code_fill="#060912", code_text="#E2E8F0",
                 arrow="#818CF8", logo="dark.svg"),
}

def rect(x, y, w, h, fill, stroke, r=10, sw=1.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def arrow(x1, y1, x2, y2, c, both=True):
    """Straight vertical/horizontal arrow with optional second head."""
    import math
    ang = math.atan2(y2 - y1, x2 - x1); L = 7
    def head(x, y, a):
        p1 = (x - L * math.cos(a - 0.45), y - L * math.sin(a - 0.45)); p2 = (x - L * math.cos(a + 0.45), y - L * math.sin(a + 0.45))
        return f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x} {y} L{p2[0]:.1f} {p2[1]:.1f}" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    s = f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c}" stroke-width="2" stroke-linecap="round"/>' + head(x2, y2, ang)
    return s + (head(x1, y1, ang + 3.14159) if both else "")

def logo(th, x, y, h):
    src = open(os.path.join(args.logo_dir, th["logo"])).read()
    inner = src[src.index(">") + 1: src.rindex("</svg>")]
    vb = [float(v) for v in src.split('viewBox="')[1].split('"')[0].split()]
    return f'<svg x="{x}" y="{y}" height="{h}" width="{h * vb[2] / vb[3]:.1f}" viewBox="0 0 {vb[2]:g} {vb[3]:g}" fill="none">{inner}</svg>'

def wrap(w, h, body, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{title}</title><desc id="d">{desc}</desc>{body}</svg>\n')

# ---------------------------------------------------------------- architecture
def architecture_diagram(th):
    T, M = th["text"], th["muted"]; b = []
    W, H = 720, 574
    # clients
    b.append(rect(8, 2, 704, 44, th["chip_fill"], th["frame_stroke"], r=12))
    b.append(text(24, 29, "Clients", 15, T, wght=600))
    b.append(text(98, 29, "docker · podman · skopeo · containerd · Kubernetes · helm · oras · zli · web UI", 12.5, M, wght=400))
    b.append(arrow(360, 50, 360, 80, th["arrow"]))
    b.append(text(376, 70, "HTTP / HTTPS", 12, M, wght=500))
    # zot frame
    b.append(rect(8, 84, 704, 442, th["frame_fill"], th["frame_stroke"], r=16))
    b.append(logo(th, 24, 92, 22))
    # HTTP API row
    y = 124
    b.append(rect(24, y, 348, 64, th["core_fill"], th["core_stroke"]))
    b.append(text(40, y + 26, "OCI Distribution Specification API", 15, T, wght=600))
    b.append(text(40, y + 48, "push, pull, tags, catalog, referrers, delete", 12.5, M, wght=400))
    b.append(rect(388, y, 308, 64, th["ext_fill"], th["ext_stroke"]))
    b.append(text(404, y + 26, "Extension APIs", 15, T, wght=600))
    b.append(text(404, y + 48, "search (GraphQL) · mgmt · userprefs · trust", 12.5, M, wght=400))
    # security bar
    y = 200
    b.append(rect(24, y, 672, 44, th["core_fill"], th["core_stroke"]))
    b.append(text(40, y + 27, "TLS · Authentication · Authorization · Rate limiting", 15, T, wght=600))
    b.append(text(680, y + 27, "checked before storage", 12.5, M, wght=400, anchor="end"))
    # core row
    y = 256; h = 100
    cols = [(24, 244, "Image storage", ["OCI image layout", "Local · S3 · GCS · Azure", "Inline GC and dedupe"]),
            (280, 208, "MetaDB", ["BoltDB · Redis · DynamoDB", "Created when a feature", "needs it"]),
            (500, 196, "Task scheduler", ["Garbage collection", "Retention · sync · scrub"])]
    for x, w, head, lines in cols:
        b.append(rect(x, y, w, h, th["core_fill"], th["core_stroke"]))
        b.append(text(x + 16, y + 26, head, 15, T, wght=600))
        for i, ln in enumerate(lines):
            b.append(text(x + 16, y + 50 + i * 18, ln, 12.5, M, wght=400))
    # extensions panel
    y = 368; h = 124
    b.append(rect(24, y, 672, h, th["ext_fill"], th["ext_stroke"]))
    b.append(text(40, y + 28, "Extensions", 15, T, wght=600))
    b.append(text(680, y + 28, "full build only", 12.5, th["accent2"], wght=500, anchor="end"))
    chips = ["Search + CVE scan", "Web UI", "Sync", "Scrub", "Lint", "Metrics", "Image trust", "Events"]
    for i, c in enumerate(chips):
        cx = 40 + (i % 4) * 164; cy = y + 44 + (i // 4) * 38
        b.append(rect(cx, cy, 148, 30, th["chip_fill"], th["ext_stroke"], r=8, sw=1.2))
        b.append(text(cx + 74, cy + 20, c, 13, T, wght=500, anchor="middle"))
    # config bar
    y = 502
    b.append(text(360, y + 14, "One configuration file (JSON or YAML) controls all of it", 13, M, wght=500, anchor="middle"))
    # legend
    ly = 556
    b.append(rect(8, ly - 11, 14, 14, th["core_fill"], th["accent"], r=4, sw=1.2))
    b.append(text(30, ly, "Core: in every build, including minimal", 12.5, M, wght=400))
    b.append(rect(300, ly - 11, 14, 14, th["ext_fill"], th["accent2"], r=4, sw=1.2))
    b.append(text(322, ly, "Extension: full build, enabled in the configuration", 12.5, M, wght=400))
    return wrap(W, H, "".join(b), "zot architecture",
                "Clients reach zot over HTTP or HTTPS. The OCI Distribution Specification API and extension APIs sit behind TLS, authentication, authorization and rate limiting. "
                "Below are core components, which are image storage, MetaDB and a task scheduler, and optional extensions: search and CVE scan, web UI, sync, scrub, lint, metrics, image trust and events. "
                "The minimal build contains only the core; the full build adds the extensions.")

# -------------------------------------------------------------------- overview
def overview_diagram(th):
    T, M, A = th["text"], th["muted"], th["accent"]; b = []
    W, H = 720, 400
    # clients column
    b.append(rect(2, 60, 168, 270, th["chip_fill"], th["frame_stroke"], r=14))
    b.append(text(86, 92, "Registry clients", 15, T, wght=600, anchor="middle"))
    for i, c in enumerate(["docker", "podman", "skopeo", "containerd", "helm", "oras"]):
        cy = 108 + i * 34
        b.append(rect(22, cy, 128, 26, th["core_fill"], th["core_stroke"], r=8, sw=1.2))
        b.append(text(86, cy + 18, c, 12.5, T, kind="mono", wght=400, anchor="middle"))
    b.append(arrow(176, 195, 214, 195, th["arrow"]))
    # zot frame
    b.append(rect(220, 2, 498, 396, th["frame_fill"], th["frame_stroke"], r=16))
    b.append(logo(th, 238, 12, 24))
    # distribution spec panel
    b.append(rect(238, 52, 462, 104, th["core_fill"], th["core_stroke"]))
    b.append(text(256, 80, "OCI Distribution Specification", 16, T, wght=600))
    b.append(text(256, 100, "The registry HTTP API: what clients speak", 12.5, M, wght=400))
    b.append(rect(256, 112, 426, 32, th["code_fill"], th["code_fill"], r=8, sw=0))
    b.append(text(272, 133, "GET /v2/alpine/manifests/edge", 13, th["code_text"], kind="mono", wght=400))
    # connector
    b.append(arrow(469, 160, 469, 190, th["arrow"]))
    # image layout panel
    b.append(rect(238, 194, 462, 190, th["core_fill"], th["core_stroke"]))
    b.append(text(256, 222, "OCI image layout", 16, T, wght=600))
    b.append(text(256, 242, "The on-disk format: any OCI layout can be served", 12.5, M, wght=400))
    b.append(rect(256, 254, 426, 118, th["code_fill"], th["code_fill"], r=8, sw=0))
    tree = [("alpine/", 0), ("├─ oci-layout", 0), ("├─ index.json", 0), ("└─ blobs/sha256/", 0), ("   ├─ 41dcc5…", 0), ("   └─ deb7de…", 0)]
    for i, (ln, _) in enumerate(tree):
        b.append(text(272, 276 + i * 17, ln, 13, th["code_text"], kind="mono", wght=400))
    b.append(text(666, 276 + 2 * 17, "tags and manifests", 12, th["accent"] if th["logo"] == "dark.svg" else "#A5B4FC", wght=500, anchor="end"))
    b.append(text(666, 276 + 4 * 17, "image data (blobs)", 12, th["accent"] if th["logo"] == "dark.svg" else "#A5B4FC", wght=500, anchor="end"))
    return wrap(W, H, "".join(b), "How zot serves images",
                "Registry clients such as docker, podman, skopeo, containerd, helm and oras talk to zot over the OCI Distribution Specification HTTP API, "
                "for example GET /v2/alpine/manifests/edge. zot stores the data on disk as an OCI image layout, with an oci-layout file, an index.json and a blobs/sha256 directory per repository.")

os.makedirs(args.out, exist_ok=True)
for name, fn in (("zot-architecture", architecture_diagram), ("zot-overview", overview_diagram)):
    for tname, th in THEMES.items():
        path = os.path.join(args.out, f"{name}-{tname}.svg")
        open(path, "w").write(fn(th))
        print("wrote", path)
