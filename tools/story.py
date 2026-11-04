"""Maqoladan Instagram story rasmi (1080x1920) yasaydi.

  python -I tools/story.py data/maqolalar.json maqola-id rasmlar/story/maqola-id.jpg
Rasm yo'li loyiha ildiziga nisbatan olinadi; qoralama uchun "fayl" qoralama/ ichida bo'ladi.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ILDIZ = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
SHRIFT = r"C:\Windows\Fonts"
TURLAR = {"yangilik": "YANGILIK", "maslahat": "MASLAHAT", "layfxak": "LAYFXAK", "kasallik": "KASALLIK VA YECHIM"}
TO_Q = (15, 31, 18)
LIME = (181, 227, 82)
W, H = 1080, 1920
PAST_B = 300


def font(nom, o):
    return ImageFont.truetype(os.path.join(SHRIFT, nom), o)


def qator(d, matn, f, en):
    qatorlar, joriy = [], ""
    for soz in matn.split():
        sinov = (joriy + " " + soz).strip()
        if d.textlength(sinov, font=f) <= en:
            joriy = sinov
        else:
            qatorlar.append(joriy)
            joriy = soz
    if joriy:
        qatorlar.append(joriy)
    return qatorlar


def yasash(json_fayl, mid, chiqish):
    with open(json_fayl, encoding="utf-8") as f:
        m = next(x for x in json.load(f) if x["id"] == mid)
    kanvas = Image.new("RGB", (W, H), TO_Q)
    d = ImageDraw.Draw(kanvas)
    for o in (82, 74, 66, 58):
        s = font("georgiab.ttf", o)
        qs = qator(d, m["sarlavha"], s, W - 128)
        if len(qs) <= 5:
            break
    p = font("segoeui.ttf", 40)
    ps = qator(d, m["qisqa"], p, W - 128)[:4]
    # matn balandligiga qarab rasm o'lchami tanlanadi, pastki yozuvga tegmaydi
    matn_b = 104 + len(qs) * int(o * 1.2) + 22 + len(ps) * 54
    rasm_b = H - PAST_B - matn_b - 40 + 30

    im = Image.open(os.path.join(ILDIZ, m["rasm"]["fayl"])).convert("RGB")
    k = max(W / im.width, rasm_b / im.height)
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - rasm_b) // 2
    kanvas.paste(im.crop((x, y, x + W, y + rasm_b)), (0, 0))

    # rasmdan to'q fonga yumshoq o'tish
    parda = Image.new("L", (1, 280))
    for i in range(280):
        parda.putpixel((0, i), int(255 * i / 279))
    kanvas.paste(Image.new("RGB", (W, 280), TO_Q), (0, rasm_b - 280), parda.resize((W, 280)))

    # Instagram ustki paneli ostida qolmasligi uchun logo pastroqda
    logo = Image.open(os.path.join(ILDIZ, "rasmlar", "logo.jpg")).convert("RGB").resize((132, 132), Image.LANCZOS)
    maska = Image.new("L", (528, 528), 0)
    ImageDraw.Draw(maska).ellipse((0, 0, 527, 527), fill=255)
    kanvas.paste(logo, (64, 170), maska.resize((132, 132), Image.LANCZOS))

    y = rasm_b - 30
    teg = font("segoeuib.ttf", 34)
    tm = TURLAR.get(m["tur"], m["tur"].upper())
    d.rounded_rectangle((64, y, 64 + d.textlength(tm, font=teg) + 56, y + 68), 34, fill=LIME)
    d.text((92, y + 11), tm, font=teg, fill=TO_Q)
    y += 104

    for q in qs:
        d.text((64, y), q, font=s, fill="white")
        y += int(o * 1.2)
    y += 22

    for q in ps:
        d.text((64, y), q, font=p, fill=(214, 224, 212))
        y += 54

    # pastki 250px Instagram tugmalari uchun bo'sh qoladi
    d.text((64, H - PAST_B), "Batafsil saytimizda va @agrosan_uz", font=font("segoeuib.ttf", 40), fill=LIME)
    izoh = "Rasm: " + m["rasm"]["muallif"][:45] + ", " + m["rasm"]["litsenziya"]
    d.text((64, H - PAST_B + 54), izoh, font=font("segoeui.ttf", 24), fill=(150, 165, 150))
    os.makedirs(os.path.dirname(chiqish) or ".", exist_ok=True)
    kanvas.save(chiqish, quality=88, optimize=True)
    print(chiqish)


if __name__ == "__main__":
    yasash(*sys.argv[1:4])
