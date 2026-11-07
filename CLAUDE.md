# Agrosan sayti

Agrosan firmasining bir sahifali veb sayti. Firma agro stimulyatorlar va bio ozuqalar ishlab chiqaradi, 5 yillik tajribaga ega.
Bu foydalanuvchining vibecoding kursidagi 1-uy vazifasi, lekin sayt haqiqatan ham firma uchun kerak.

- Instagram: `agrosan_uz` → https://instagram.com/agrosan_uz
- Telefon: +998 50 100 30 30 (`tel:+998501003030`), ikkinchi: +998 91 131 00 07 (aloqa blokida)
- Shior: "Agrosan — bir qadam oldinda." (varaqalardagi shior: "Boy fermer — sog'lom hosil!")
- Sayt tili: o'zbek (lotin). Foydalanuvchi bilan ham o'zbekcha gaplashiladi.

## GitHub va jonli sayt

- Repo: https://github.com/Faxa-riddin/agrosan- (nom oxirida chiziqcha bor), branch `main`
- Jonli sayt (GitHub Pages, `main` / root): https://faxa-riddin.github.io/agrosan-/
- Yangilash: commit → `git push`; Pages 1–2 daqiqada o'zi yangilanadi. Kirish Git Credential Manager'da saqlangan; agar so'rasa, push'ni Terminal panelida ishga tushiring (foydalanuvchi brauzerda Authorize bosadi).

## VPS (Hetzner) va domen

- Asosiy manzil: https://agrosan.uz (Cloudflare proxy orqali). Server IP va kirish yo'li repoda yozilmaydi (repo ochiq), ular shaxsiy xotira faylida.
- Ubuntu, nginx, sayt `/var/www/agrosan` (GitHub repodan), Let's Encrypt sertifikati avtomatik yangilanadi. Serverga faqat SSH kalit bilan kiriladi.
- Serverda cron har 10 daqiqada `git pull` qiladi: push qilingan narsa o'zi saytga tushadi. Sozlash skripti: `tools/server-setup.sh`.

## Fayllar

```
index.html        sahifa tuzilishi (HTML ichida style="" ham, <script> ham yo'q — shunday qolsin)
css/style.css     barcha dizayn
js/script.js      katalog saralash, kartochka foni (--img), chap paneldagi faol bo'lim
js/maqolalar.js   maqolalarni JSON'dan chizadi (bosh sahifa, ro'yxat, bitta maqola)
maqolalar.html    barcha maqolalar va bitta maqola (?id=...)
data/maqolalar.json  maqolalar: yangisi ro'yxat boshiga qo'shiladi
tools/rasm.py     Wikimedia Commons'dan bepul rasm topadi va 16:10 qilib saqlaydi
tools/story.py    maqoladan 1080x1920 Instagram story rasmi yasaydi (rasmlar/story/<id>.jpg)
qoralama/         kunlik qoralamalar (gitignore, tasdiqlanmaguncha saytga chiqmaydi)
rasmlar/          logo.jpg, mahsulot rasmlari (photo_2026-10-24_*.jpg), nutrimax/redline/ultra-npk.jpg
rasmlar/pdf/      har bir mahsulotning PDF varaqasi (DL Flyer) — kartochkalardagi tavsiflar shulardan olingan
.claude/launch.json  ko'rish uchun lokal server: `python -m http.server 8080`
```

Brauzer panelida faylni to'g'ridan-to'g'ri ochganda rasmlar chiqmaydi, `sayt` serveri (localhost:8080) orqali ko'rish kerak.

## Sahifa tartibi

1. **Chap panel (dock)** — ekran chap devorida, shaffof shisha: logo, Biz haqimizda, Mahsulotlar, Aloqa, Qo'ng'iroq. Ikonkalar 44px, hover'da nomi chiqadi. Telefonda pastga gorizontal tushadi. Yuqorida menyu (header) yo'q.
2. **Bosh qism (hero)** — Dribbble "Meridian" shotining tuzilishi: grid, ko'rinadigan sarlavha yo'q (h1 faqat qidiruv uchun yashirin), tepada fondagi tiniq Agrosan emblemasi (`.hero-emblem` + `rasmlar/hero-emblem-mask.png`), o'ngda sekin aylanuvchi tekis mahsulotlar halqasi (orbit, 45 s, 3D emas, markazda logo), hosildorlik ustunlari va o'sish grafigi sekin o'sadi (12 s tsikl), pastda: chapda tugma + "Hosildorlik +30–40%" kartochkasi, o'rtada Eco Power rasmi, o'ngda "O'simlik o'sishi" grafigi. Fon — 5 ta shisha rasmi (`photo_..._19-23-34.jpg`) ozgina xiralashtirilgan (blur 4px) + yupqa to'q parda.
   - Tugma va kartochkalar shaffof shisha.
3. **Foydali ma'lumotlar** (`#foydali`) — hero'dan keyin, eng yangi 3 ta maqola rasmi bilan, "Barcha maqolalar" `maqolalar.html` ga olib boradi. Har faktda ishonchli manba bo'lsin, matn ko'chirilmaydi, yangilik to'qilmaydi, me'yor taxmin qilinmaydi. Rasmlar `rasmlar/maqola/<id>.jpg`, faqat bepul litsenziyali (Wikimedia Commons), muallif va litsenziya JSON'dagi `rasm` maydonida.
4. **Biz haqimizda** — `.intro`: chapda kichik yozuv, o'ngda katta sarlavha; matn + 3 ta statistika.
5. **Mahsulotlar katalogi** — macOS segmented control bilan saralash (Hammasi / Biostimulyatorlar / Gel o'g'itlar / NPK gel). 14 ta kartochka. Har kartochka foni — o'z mahsulot rasmi xira va shaffof (`.card::before`, rasm manzili JS orqali `--img` ga to'liq URL bilan beriladi, aks holda CSS uni `css/` dan qidiradi).
6. **Daladan natijalar** (`#natijalar`) — 3 ta Instagram reels kartochkasi (muqova `rasmlar/reel-*.jpg`, bosilganda Instagram ochiladi); telefonda yonma-yon suriladi.
7. **Nega Agrosan** — 01–04 raqamli 4 sabab.
8. **Aloqa** — to'q yashil blok, Bio Energy Active rasmi, telefon va Instagram tugmalari.

## Kunlik maqolalar

- Har kuni 08:00 da `agrosan-kunlik-qoralama` vazifasi `qoralama/maqolalar.json` ga qoralama yozadi: 1 ta dunyodan ishonchli layfxak, 1 ta O'zbekistondagi mavsumiy kasallik yechimi (`tur`: `layfxak`, `kasallik`), haqiqiy yangilik bo'lsa 1 ta `yangilik`.
- Foydalanuvchi "chiqar" demaguncha hech narsa saytga chiqmaydi. Chiqarish: maqolani `data/maqolalar.json` boshiga, rasmni `rasmlar/maqola/` ga, story'ni `rasmlar/story/` ga ko'chirib, faqat shu fayllarni commit va push qilish.
- Instagram: hozircha story rasmi tayyorlanadi, foydalanuvchi o'zi joylaydi yoki Meta Business Suite'da rejalashtiradi. Avtomatik joylash uchun Instagram API ulanishi kerak (hali sozlanmagan).

## Mahsulotlar (14 ta)

- Biostimulyatorlar: Bio Energy Active, Eco Power, Amino Max, X-Agro Potencia, GrenRoot Energy, Energy Gumi Max Plus, Humi Pasta Root Power
- Gel o'g'itlar: Avangard Bio Active Gel, Humi Root Gel, Fruit Power PK 50, Humi Grow
- NPK gel: Nutrimax (25-25-25+TE), RedLine (15-10-50+2MgO+TE), Ultra NPK (15-65-15+TE)

X-Agro Potencia, Energy Gumi Max Plus, Humi Grow va Humi Pasta uchun PDF yo'q — tavsif qadoq / Instagram postidan olingan (Humi rasmlari Instagram skrinshotidan kesilib, 2x kattalashtirilgan: `rasmlar/humi-*.jpg`).

## Dizayn qoidalari (foydalanuvchi tanlagan)

- Minimalistik, Dribbble uslubi; tugmalar macOS'dagidek (8px burchak, yengil gradient, ingichka chegara).
- Shaffof / shisha (glass, backdrop-filter) elementlar yoqadi; "bachkana" bo'lib ketmasin — rang yumshoq bo'lsin.
- Ranglar o'zgarmasin: to'q yashil `--dark #0f1f12`, `--green #2f6b3a`, lime `--lime #b5e352`, yalpiz fon `--bg #ecf5e3`.
- Sahifa foni: och yashil gradient + sekin suzuvchi yashil yorug'lik dog'lari (`.bg-aurora`).
- Shrift: Inter.
- Hero animatsiyalari (halqa, ustunlar, grafik) foydalanuvchi talabi bilan telefonda `prefers-reduced-motion` yoqilganda ham ishlaydi.
- CSS yoki JS o'zgarsa, `index.html` va `maqolalar.html` dagi `?v=N` raqamini oshiring, aks holda telefonlar eski faylni ko'rsatishi mumkin.
- Har o'zgarishdan keyin brauzerda kompyuter (1440px) va telefon (375px) o'lchamida tekshirish; telefonda gorizontal scroll bo'lmasin.
