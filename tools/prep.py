import base64, io, json, os
from PIL import Image, ImageOps

sp = os.path.dirname(os.path.abspath(__file__))
media = os.path.join(sp, "word", "media")
out = {}

def b64(img, fmt="JPEG", q=72):
    buf = io.BytesIO()
    if fmt == "JPEG":
        img.convert("RGB").save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        mime = "image/jpeg"
    else:
        img.save(buf, "PNG", optimize=True)
        mime = "image/png"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()

def photo(name, key, maxside=1400, q=70):
    im = Image.open(os.path.join(media, name))
    im.thumbnail((maxside, maxside))
    out[key] = b64(im, q=q)
    print(key, im.size, len(out[key]) // 1024, "KB")

photo("image6.jpg", "sled")
photo("image7.jpg", "ring")
photo("image17.jpg", "soccer")
photo("image18.jpg", "mtb")
photo("image14.jpg", "boxgym")
photo("image5.jpg", "smile")
for n, k in [("image11.jpg", "ref_lifter"), ("image9.jpg", "ref_wheel"), ("image12.jpg", "ref_knee"),
             ("image3.jpg", "ref_track"), ("image10.jpg", "ref_run"), ("image15.jpg", "ref_spine")]:
    photo(n, k, maxside=600, q=80)

# Logo: luminance -> alpha, black ink on transparent
logo = Image.open(os.path.join(media, "image8.png")).convert("L")
ink = ImageOps.invert(logo).point(lambda v: 0 if v < 40 else min(255, int((v - 40) * 1.3)))
w, h = logo.size
rows = [any(ink.getpixel((x, y)) > 128 for x in range(0, w, 4)) for y in range(h)]
bands, start = [], None
for y, r in enumerate(rows):
    if r and start is None:
        start = y
    if not r and start is not None:
        bands.append((start, y)); start = None
print("bands", bands)

def ink_png(box):
    a = ink.crop(box)
    a = a.crop(a.getbbox())
    rgba = Image.new("RGBA", a.size, (0, 0, 0, 0))
    rgba.putalpha(a)
    black = Image.new("RGBA", a.size, (0, 0, 0, 255)); black.putalpha(a)
    black.thumbnail((900, 900))
    return b64(black, fmt="PNG")

mark_band = bands[0]
word_band = bands[1]
out["mark"] = ink_png((0, mark_band[0], w, mark_band[1]))
out["word"] = ink_png((0, word_band[0], w, word_band[1]))
out["lockup"] = ink_png((0, 0, w, h))
json.dump(out, open(os.path.join(sp, "assets.json"), "w"))
print("total KB", sum(len(v) for v in out.values()) // 1024)
