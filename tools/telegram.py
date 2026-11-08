"""Story rasmlarini foydalanuvchining shaxsiy Telegram akkauntidan Tavakkalga yuboradi (Telethon).

Kirish kaliti repoda EMAS: gaz loyihasidagi sessiya ishlatiladi
    D:\\KUNLIK GAZ TARQATISH\\telegram\\config.json  (api_id, api_hash)
    D:\\KUNLIK GAZ TARQATISH\\telegram\\sessiya.session
Boshqa joyda bo'lsa: TELEGRAM_DIR muhit o'zgaruvchisi bilan ko'rsating.

Ishlatish:
    python -I tools/telegram.py --tekshir          sessiya ishlayaptimi, Tavakkal topiladimi
    python -I tools/telegram.py <id> [<id> ...]    rasmlar/story/<id>.jpg ni Tavakkalga yuboradi
"""
import asyncio
import json
import os
import sys

from telethon import TelegramClient

sys.stdout.reconfigure(encoding="utf-8")
ILDIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TG = os.environ.get("TELEGRAM_DIR", r"D:\KUNLIK GAZ TARQATISH\telegram")
TAVAKKAL = 639315668          # Telegram'dagi "Тавакал" kontakti
TAVAKKAL_TEL = "1310007"      # telefon oxiri (+998 91 131 00 07) - xato odamga ketmasligi uchun


def maqola(id_):
    with open(os.path.join(ILDIZ, "data", "maqolalar.json"), encoding="utf-8") as f:
        for m in json.load(f):
            if m["id"] == id_:
                return m
    return None


async def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = os.path.join(TG, "config.json")
    if not os.path.exists(cfg):
        sys.exit(f"XATO: {cfg} topilmadi (Telegram sessiyasi yo'q).")
    c = json.load(open(cfg, encoding="utf-8"))
    cl = TelegramClient(os.path.join(TG, "sessiya"), c["api_id"], c["api_hash"])
    await cl.connect()
    try:
        if not await cl.is_user_authorized():
            sys.exit("XATO: Telegram sessiyasidan chiqilgan, qaytadan kirish kerak.")
        kim = await cl.get_entity(TAVAKKAL)
        if not (kim.phone or "").endswith(TAVAKKAL_TEL):
            sys.exit("XATO: Tavakkal kontakti raqami mos kelmadi, hech narsa yuborilmadi.")
        if sys.argv[1] == "--tekshir":
            print("OK: sessiya ishlayapti, Tavakkal topildi:", kim.first_name)
            return
        xato = 0
        for id_ in sys.argv[1:]:
            rasm = os.path.join(ILDIZ, "rasmlar", "story", id_ + ".jpg")
            if not os.path.exists(rasm):
                print(f"{id_}: story rasmi yo'q ({rasm})")
                xato += 1
                continue
            m = maqola(id_)
            izoh = (m["sarlavha"] + "\n\n" if m else "") + \
                f"Link stikeri: https://agrosan.uz/maqolalar.html?id={id_}"
            try:
                await cl.send_file(kim, rasm, caption=izoh)
                print(f"{id_}: yuborildi")
            except Exception as e:
                print(f"{id_}: XATO {e}")
                xato += 1
        if xato:
            sys.exit(1)
    finally:
        await cl.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
