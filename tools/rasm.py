"""Wikimedia Commons'dan bepul litsenziyali rasm topish va saqlash.

  python -I tools/rasm.py qidir "peach leaf curl" papka
      papka/sheet.jpg (raqamlangan rasmlar) va papka/nomzod.json yaratadi
  python -I tools/rasm.py ol papka/nomzod.json 2 chiqish.jpg
      2-rasmni 16:10 qilib saqlaydi, muallif va litsenziyani JSON qilib chiqaradi
"""
import io, json, os, re, subprocess, sys, urllib.parse
from PIL import Image, ImageDraw

LITSENZIYA = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? ?[234])", re.I)


def ol_url(url):
    return subprocess.run(
        ["curl", "-sSfL", "--max-time", "60", "-A", "AgrosanSitePhotoSearch/1.0", url],
        capture_output=True, check=True,
    ).stdout


def qidir(soz, papka):
    os.makedirs(papka, exist_ok=True)
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": soz + " filetype:bitmap", "gsrlimit": 40, "prop": "imageinfo",
        "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 960,
    }
    data = json.loads(ol_url("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)))
    sahifalar = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    nomzod = []
    for p in sahifalar:
        ii = p["imageinfo"][0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if ii["mime"] != "image/jpeg" or ii["width"] < ii["height"] or ii["width"] < 700 or not LITSENZIYA.match(lic):
            continue
        muallif = re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()
        nomzod.append({"nom": p["title"], "litsenziya": lic, "muallif": muallif, "rasm": ii["thumburl"], "url": ii["descriptionurl"]})
        if len(nomzod) == 8:
            break
    W, H = 300, 200
    varaq = Image.new("RGB", (W * 4, (H + 24) * 2), "white")
    d = ImageDraw.Draw(varaq)
    for i, n in enumerate(nomzod):
        x, y = (i % 4) * W, (i // 4) * (H + 24)
        im = Image.open(io.BytesIO(ol_url(n["rasm"]))).convert("RGB")
        im.thumbnail((W, H))
        varaq.paste(im, (x, y + 24))
        d.text((x + 4, y + 6), str(i), fill="black")
    varaq.save(os.path.join(papka, "sheet.jpg"), quality=80)
    with open(os.path.join(papka, "nomzod.json"), "w", encoding="utf-8") as f:
        json.dump(nomzod, f, ensure_ascii=False, indent=1)
    print(len(nomzod), "ta nomzod:", os.path.join(papka, "sheet.jpg"))


def ol(nomzod_fayl, raqam, chiqish):
    with open(nomzod_fayl, encoding="utf-8") as f:
        n = json.load(f)[int(raqam)]
    im = Image.open(io.BytesIO(ol_url(n["rasm"]))).convert("RGB")
    w, h = im.size
    t = int(w * 10 / 16)
    if h > t:
        y = (h - t) // 2
        im = im.crop((0, y, w, y + t))
    else:
        s = int(h * 16 / 10)
        x = (w - s) // 2
        im = im.crop((x, 0, x + s, h))
    os.makedirs(os.path.dirname(chiqish) or ".", exist_ok=True)
    im.save(chiqish, quality=82, optimize=True)
    print(json.dumps({"muallif": n["muallif"], "litsenziya": n["litsenziya"], "url": n["url"]}, ensure_ascii=True))


if __name__ == "__main__":
    {"qidir": qidir, "ol": ol}[sys.argv[1]](*sys.argv[2:])
