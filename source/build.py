"""Rebuild the self-contained mockup from home.html + assets.json.

Run:  python build.py
Writes ../mockups/flexfusionx-home-latest.html (every image embedded, opens in any browser).
"""
import base64
import io
import json
import os
import re

from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
assets = json.load(open(os.path.join(here, "assets.json")))
page = open(os.path.join(here, "home.html"), encoding="utf8").read()

keys = set(re.findall(r"\{\{(\w+)\}\}", page))
missing = keys - set(assets)
if missing:
    raise SystemExit("missing assets: %s" % ", ".join(sorted(missing)))
for k in keys:
    page = page.replace("{{" + k + "}}", assets[k])

# the FX mark's aspect ratio drives the red FX bullets and placeholders
mark = Image.open(io.BytesIO(base64.b64decode(assets["mark"].split(",")[1])))
page = page.replace("--note-ink:#1A1400;", "--note-ink:#1A1400;\n  --fxratio:%d / %d;" % mark.size, 1)

out = os.path.normpath(os.path.join(here, "..", "mockups", "flexfusionx-home-latest.html"))
open(out, "w", encoding="utf8").write(page)
print("wrote", out, len(page) // 1024, "KB")

# artifact variant: claude.ai blocks third-party iframes, so the live Cliniko embed
# becomes a card with a real link to the booking page
import re as _re
fallback = (
    '<div class="ckfall"><span class="eyebrow" style="color:#53575C">Online bookings · Powered by Cliniko</span>'
    '<h3>Live Cliniko booking appears here on the website</h3>'
    "<p>This preview can't show embedded booking widgets. Open the real booking page to see available times.</p>"
    '<a class="btn btn-k" style="background:#0A0A0B;color:#fff;border-color:#0A0A0B" href="https://flexfusionx.au5.cliniko.com/bookings" target="_blank" rel="noopener">Open the booking page ↗</a></div>'
)
art = _re.sub(r"<!--CLINIKO-->.*?<!--/CLINIKO-->", fallback, page, flags=_re.S)
art_out = os.path.normpath(os.path.join(here, "..", "mockups", "flexfusionx-home-artifact.html"))
open(art_out, "w", encoding="utf8").write(art)
print("wrote", art_out)

# policy pages sit beside the homepage
import pages
for p in pages.build(os.path.dirname(out), assets):
    print("wrote", p)
