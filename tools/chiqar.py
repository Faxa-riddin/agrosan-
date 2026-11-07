"""Qoralama maqolalarni tekshirib, o'tganlarini saytga chiqaradi.

  python -I tools/chiqar.py            faqat tekshiradi, hech narsa o'zgartirmaydi
  python -I tools/chiqar.py --chiqar   o'tganlarini data/maqolalar.json ga qo'shadi, rasm va story'ni ko'chiradi
  python -I tools/chiqar.py --chiqar --push   shu bilan birga commit va push qiladi

Xato topilgan maqola qoralamada qoladi va sababi chiqariladi.
"""
import json, os, re, shutil, subprocess, sys

ILDIZ = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
QORALAMA = os.path.join(ILDIZ, "qoralama", "maqolalar.json")
SAYT = os.path.join(ILDIZ, "data", "maqolalar.json")
TURLAR = {"yangilik", "maslahat", "layfxak", "kasallik"}
LITSENZIYA = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? ?[234])", re.I)


def oqi(yol):
    if not os.path.exists(yol):
        return []
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def yoz(yol, data):
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def link_holati(url):
    # sekin saytlar uchun bir marta qayta urinadi
    kod = "000"
    for _ in range(2):
        kod = bitta_urinish(url)
        if kod != "000":
            break
    return kod


def bitta_urinish(url):
    r = subprocess.run(
        ["curl", "-s", "-L", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "45",
         "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AgrosanSiteCheck/1.0", url],
        capture_output=True, text=True,
    )
    return r.stdout.strip() or "000"


def tekshir(m, band):
    xato, ogoh = [], []
    for k in ("id", "tur", "sana", "sarlavha", "qisqa", "matn", "manbalar", "rasm"):
        if not m.get(k):
            xato.append(f"'{k}' yo'q")
    if xato:
        return xato, ogoh
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", m["id"]):
        xato.append("id faqat kichik lotin harf, raqam va '-' bo'lsin")
    if m["id"] in band:
        xato.append("bu id saytda bor")
    if m["tur"] not in TURLAR:
        xato.append(f"noma'lum tur: {m['tur']}")
    if len(m["sarlavha"]) > 90:
        xato.append("sarlavha 90 belgidan uzun")
    if len(m["qisqa"]) > 260:
        xato.append("qisqa matn 260 belgidan uzun")
    matn = json.dumps(m["matn"], ensure_ascii=False)
    if re.search(r"<[a-z/]", matn) or re.search(r"TODO|lorem", matn, re.I):
        xato.append("matnda HTML yoki to'ldirilmagan joy bor")
    r = m["rasm"]
    for k in ("fayl", "alt", "muallif", "litsenziya", "url"):
        if not r.get(k):
            xato.append(f"rasm '{k}' yo'q")
    if r.get("url") and not r["url"].startswith("https://"):
        xato.append(f"rasm linki https:// bilan boshlanmaydi: {r['url']}")
    if r.get("fayl") and not re.fullmatch(r"(rasmlar/maqola|qoralama(/rasmlar)?)/[a-z0-9-]+\.jpg", r["fayl"]):
        xato.append(f"rasm fayli rasmlar/maqola/ yoki qoralama/ ichida emas: {r['fayl']}")
    if r.get("litsenziya") and not LITSENZIYA.match(r["litsenziya"]):
        xato.append(f"rasm litsenziyasi mos emas: {r['litsenziya']}")
    if r.get("fayl") and not os.path.exists(os.path.join(ILDIZ, r["fayl"])):
        xato.append(f"rasm fayli yo'q: {r['fayl']}")
    if not os.path.exists(os.path.join(ILDIZ, "qoralama", "story", m["id"] + ".jpg")):
        ogoh.append("story rasmi yo'q")
    for s in m["manbalar"]:
        url = s.get("url", "")
        if not url.startswith("https://") and not url.startswith("http://"):
            xato.append(f"manba linki noto'g'ri: {url}")
            continue
        kod = link_holati(url)
        if kod in ("404", "410", "000"):
            xato.append(f"manba ochilmadi ({kod}): {url}")
        elif not kod.startswith(("2", "3")):
            ogoh.append(f"manba {kod} qaytardi (bot himoyasi bo'lishi mumkin): {url}")
    return xato, ogoh


def main():
    chiqar = "--chiqar" in sys.argv
    qoralama, sayt = oqi(QORALAMA), oqi(SAYT)
    band = {x["id"] for x in sayt}
    otdi, qoldi = [], []
    for m in qoralama:
        xato, ogoh = tekshir(m, band)
        holat = "XATO" if xato else "OK"
        print(f"[{holat}] {m.get('id')} | {m.get('sarlavha')}")
        for x in xato:
            print("   xato:", x)
        for x in ogoh:
            print("   ogohlantirish:", x)
        (qoldi if xato else otdi).append(m)
        if not xato:
            band.add(m["id"])
    if not chiqar or not otdi:
        print(f"\n{len(otdi)} ta tayyor, {len(qoldi)} ta xato." + ("" if chiqar else " Chiqarish uchun: --chiqar"))
        return
    fayllar = [os.path.relpath(SAYT, ILDIZ)]
    for m in otdi:
        manba = os.path.join(ILDIZ, m["rasm"]["fayl"])
        yangi = f"rasmlar/maqola/{m['id']}.jpg"
        if os.path.abspath(manba) != os.path.abspath(os.path.join(ILDIZ, yangi)):
            shutil.copyfile(manba, os.path.join(ILDIZ, yangi))
        m["rasm"]["fayl"] = yangi
        fayllar.append(yangi)
        story = os.path.join(ILDIZ, "qoralama", "story", m["id"] + ".jpg")
        if os.path.exists(story):
            os.makedirs(os.path.join(ILDIZ, "rasmlar", "story"), exist_ok=True)
            shutil.copyfile(story, os.path.join(ILDIZ, "rasmlar", "story", m["id"] + ".jpg"))
            fayllar.append(f"rasmlar/story/{m['id']}.jpg")
    yoz(SAYT, otdi + sayt)
    yoz(QORALAMA, qoldi)
    print(f"\n{len(otdi)} ta maqola saytga qo'shildi, {len(qoldi)} ta qoralamada qoldi.")
    if "--push" in sys.argv:
        git = ["git", "-C", ILDIZ]
        subprocess.run(git + ["add", "--"] + fayllar, check=True)
        nomlar = ", ".join(m["id"] for m in otdi)
        xabar = f"Yangi maqolalar: {nomlar}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
        subprocess.run(git + ["commit", "-q", "-m", xabar, "--"] + fayllar, check=True)
        subprocess.run(git + ["push", "-q"], check=True)
        print("GitHub'ga yuborildi. Server 10 daqiqa ichida yangilanadi.")


if __name__ == "__main__":
    main()
