#!/usr/bin/env python3
"""Build the gallery:
   - index.html  (single file, screenshots + icons embedded as data URIs)
   - a/<id>/index.html  (per-app share pages with their own OG preview image,
     so a texted link unfurls with THAT app's screenshot, then forwards a real
     visitor into the gallery's deep link)

   Set the deployed site URL so social previews use absolute image URLs:
     GALLERY_BASE_URL=https://your-site.netlify.app python3 build.py
"""
import base64, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Where the site will live. Update after deploying (or pass GALLERY_BASE_URL).
BASE_URL = os.environ.get("GALLERY_BASE_URL", "https://webappgallery.com").rstrip("/")

def embed(dirname, ext, mime):
    d = os.path.join(HERE, "assets", dirname)
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(ext):
            with open(os.path.join(d, f), "rb") as fh:
                out[f[:-len(ext)]] = f"data:{mime};base64," + base64.b64encode(fh.read()).decode()
    return out

screens = embed("screens", ".jpg", "image/jpeg")
icons = embed("icons", ".png", "image/png")

tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
for ph in ("__SCREENS_JSON__", "__ICONS_JSON__"):
    if ph not in tpl:
        sys.exit(f"template.html is missing the {ph} placeholder")
out = tpl.replace("__SCREENS_JSON__", json.dumps(screens)).replace("__ICONS_JSON__", json.dumps(icons))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print(f"built index.html — {len(screens)} screenshots + {len(icons)} icons embedded, "
      f"{os.path.getsize(os.path.join(HERE, 'index.html'))//1024} KB")

# ---- per-app share pages ----
apps = re.findall(
    r'\{id:"([^"]+)",\s*name:"([^"]+)",\s*cat:"([^"]+)",[^\n]*\n\s*tag:"([^"]+)"', tpl)

SHARE_TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — The Gallery</title>
<meta name="description" content="{tag}">
<meta property="og:type" content="website">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{tag}">
<meta property="og:image" content="{img}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name}">
<meta name="twitter:description" content="{tag}">
<meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url=../../index.html#/app/{id}">
<script>location.replace("../../index.html#/app/{id}");</script>
<style>body{{font-family:Charter,Georgia,serif;background:#EDE3D3;color:#3D3428;
  display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0;text-align:center}}
a{{color:#A88448}}</style>
</head>
<body>
<p>Opening <b>{name}</b> in The Gallery… <a href="../../index.html#/app/{id}">tap here if it doesn't.</a></p>
</body>
</html>
"""

n = 0
for aid, name, cat, tag in apps:
    d = os.path.join(HERE, "a", aid)
    os.makedirs(d, exist_ok=True)
    img_file = f"{aid}-main.jpg"
    img = f"{BASE_URL}/assets/screens/{img_file}" if BASE_URL else f"../../assets/screens/{img_file}"
    page = SHARE_TPL.format(
        id=aid,
        name=html.escape(name),
        tag=html.escape(tag),
        img=img,
        url=f"{BASE_URL}/a/{aid}/" if BASE_URL else f"a/{aid}/",
    )
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
    n += 1
print(f"built {n} per-app share pages under a/  (BASE_URL={BASE_URL or '(relative)'})")
