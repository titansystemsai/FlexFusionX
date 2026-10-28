"""Build the production site for flexfusionx.com.au into deploy/site/.

Differences from the mockup build (source/build.py):
  - images are separate files in img/ (cacheable) instead of data URIs
  - mockup controls (replay, theme toggle, viewport chip) are removed
  - real <head>: title, description, canonical, Open Graph, favicon
  - live Cliniko embed (no artifact fallback)
  - robots.txt, sitemap.xml and cache headers for Cloudflare Pages

Run:  python deploy/build_prod.py
Deploy: npx wrangler pages deploy deploy/site --project-name flexfusionx --branch main
"""
import base64, io, json, os, re, shutil, sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "source")
SITE = os.path.join(HERE, "site")
DOMAIN = "https://flexfusionx.com.au"

sys.path.insert(0, SRC)
import pages  # noqa: E402

assets = json.load(open(os.path.join(SRC, "assets.json")))
page = open(os.path.join(SRC, "home.html"), encoding="utf8").read()

shutil.rmtree(SITE, ignore_errors=True)
os.makedirs(os.path.join(SITE, "img"))

# --- images out to files
used = sorted(set(re.findall(r"\{\{(\w+)\}\}", page)))
paths = {}
for k in used:
    head, b64 = assets[k].split(",", 1)
    ext = "png" if "png" in head else "jpg"
    rel = f"img/{k}.{ext}"
    open(os.path.join(SITE, rel), "wb").write(base64.b64decode(b64))
    paths[k] = "/" + rel
for k in used:
    page = page.replace("{{" + k + "}}", paths[k])

mark = Image.open(io.BytesIO(base64.b64decode(assets["mark"].split(",")[1])))
page = page.replace("--note-ink:#1A1400;", "--note-ink:#1A1400;\n  --fxratio:%d / %d;" % mark.size, 1)

# --- strip mockup controls and the script that drives them
page, n = re.subn(r'<div class="ctrl" aria-label="Mockup controls">.*?</div>\n', "", page, flags=re.S)
assert n == 1, "mockup controls not found"
for pat in [r"\n  var vpc=document\.getElementById\('vpchip'\);[^\n]*",
            r"\n  var tt=document\.getElementById\('themeToggle'\);[^\n]*",
            r"\n  function setTheme\(light\)[^\n]*",
            r"\n  try\{if\(localStorage\.getItem\('ffx6-theme'\)[^\n]*",
            r"\n  tt\.addEventListener\('click'[^\n]*",
            r"\n  document\.getElementById\('replay'\)\.addEventListener\('click',play\);"]:
    page, n = re.subn(pat, "", page)
    assert n == 1, pat
page = page.replace("<!--BOOKING-->\n", "").replace("<!--/BOOKING-->\n", "")

# --- real head
title = "FlexFusionX | Performance & NDIS Physiotherapy in Adelaide"
desc = ("Rehab that works around your training. Performance, sports injury and NDIS physiotherapy "
        "in Evandale, at home across Adelaide, or by telehealth. Book online.")
page = re.sub(r"<title>.*?</title>\n<meta name=\"description\"[^>]*>", "", page, count=1)
head = f"""<!doctype html>
<html lang="en-AU">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}/">
<meta name="theme-color" content="#0A0A0B">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FlexFusionX">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/">
<meta property="og:image" content="{DOMAIN}/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="image" href="{paths['sled_hd']}">
"""
page = head + page
open(os.path.join(SITE, "index.html"), "w", encoding="utf8").write(page)

# --- icons and share image
def icon(size, name, pad=0.18):
    m = mark.convert("RGBA")
    canvas = Image.new("RGBA", (size, size), (10, 10, 11, 255))
    inner = int(size * (1 - 2 * pad))
    m.thumbnail((inner, inner), Image.LANCZOS)
    white = Image.new("RGBA", m.size, (255, 255, 255, 255))
    white.putalpha(m.getchannel("A") if m.mode == "RGBA" else m.convert("L"))
    canvas.alpha_composite(white, ((size - m.size[0]) // 2, (size - m.size[1]) // 2))
    canvas.convert("RGB").save(os.path.join(SITE, name))
icon(64, "favicon.png")
icon(180, "apple-touch-icon.png")

hero = Image.open(os.path.join(SITE, paths["sled_hd"].lstrip("/"))).convert("RGB")
w, h = 1200, 630
r = max(w / hero.width, h / hero.height)
hero = hero.resize((int(hero.width * r), int(hero.height * r)), Image.LANCZOS)
x, y = (hero.width - w) // 2, (hero.height - h) // 2
og = hero.crop((x, y, x + w, y + h))
shade = Image.new("RGB", (w, h), (10, 10, 11))
og = Image.blend(og, shade, 0.35)
word = Image.open(io.BytesIO(base64.b64decode(assets["lockup"].split(",")[1]))).convert("RGBA")
word.thumbnail((520, 200), Image.LANCZOS)
white = Image.new("RGBA", word.size, (255, 255, 255, 255))
white.putalpha(word.getchannel("A"))
og = og.convert("RGBA"); og.alpha_composite(white, (64, h - word.size[1] - 64))
og.convert("RGB").save(os.path.join(SITE, "og.jpg"), quality=86)

# --- policy pages
for p in pages.build(SITE, assets):
    pass
for name in ("privacy.html", "terms.html"):
    fp = os.path.join(SITE, name)
    t = open(fp, encoding="utf8").read()
    if "<link rel=\"icon\"" not in t:
        t = t.replace("<head>", '<head>\n<link rel="icon" type="image/png" href="/favicon.png">', 1)
    open(fp, "w", encoding="utf8").write(t)

# --- crawl + cache
open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
open(os.path.join(SITE, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{DOMAIN}/{u}</loc></url>\n" for u in ("", "privacy", "terms"))
    + "</urlset>\n")
open(os.path.join(SITE, "_headers"), "w").write(
    "/img/*\n  Cache-Control: public, max-age=31536000, immutable\n"
    "/*\n  Strict-Transport-Security: max-age=31536000\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")

total = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(SITE) for f in fs)
print("built", SITE, "index.html", os.path.getsize(os.path.join(SITE, "index.html")) // 1024, "KB,",
      len(os.listdir(os.path.join(SITE, "img"))), "images, total", total // 1024, "KB")
