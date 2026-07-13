#!/usr/bin/env python3
"""Build index.html from template.html + assets/screens/*.jpg + assets/icons/*.png (embedded as data URIs)."""
import base64, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

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
