import base64, io, json, os
from PIL import Image

sp = os.path.dirname(os.path.abspath(__file__))
media = os.path.join(sp, "word", "media")
ig = os.path.join(sp, "ig")
a = json.load(open(os.path.join(sp, "assets.json")))

def enc(path, maxside, q=68, crop=None):
    im = Image.open(path).convert("RGB")
    if crop:
        w, h = im.size
        im = im.crop((int(w * crop[0]), int(h * crop[1]), int(w * crop[2]), int(h * crop[3])))
    im.thumbnail((maxside, maxside))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    s = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    print(os.path.basename(path), im.size, len(s) // 1024, "KB")
    return s

a["soccer_xl"] = enc(os.path.join(media, "image17.jpg"), 1900, 66)
a["mtb_xl"] = enc(os.path.join(media, "image18.jpg"), 1900, 66)
a["ring_xl"] = enc(os.path.join(media, "image7.jpg"), 1080, 72)
a["track_pov"] = enc(os.path.join(ig, "p5_1001c.jpg"), 1100, 66, crop=(0, 0.02, 1, 0.98))
json.dump(a, open(os.path.join(sp, "assets2.json"), "w"))
print("total KB", sum(len(v) for v in a.values()) // 1024)
