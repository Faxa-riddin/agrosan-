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

## Fayllar

```
index.html        sahifa tuzilishi (HTML ichida style="" ham, <script> ham yo'q — shunday qolsin)
css/style.css     barcha dizayn
js/script.js      katalog saralash, kartochka foni (--img), chap paneldagi faol bo'lim
js/maqolalar.js   maqolalarni JSON'dan chizadi (bosh sahifa, ro'yxat, bitta maqola)
maqolalar.html    barcha maqolalar va bitta maqola (?id=...)
data/maqolalar.json  maqolalar: yangisi ro'yxat boshiga qo'shiladi
rasmlar/          logo.jpg, mahsulot rasmlari (photo_2026-10-24_*.jpg), nutrimax/redline/ultra-npk.jpg
rasmlar/pdf/      har bir mahsulotning PDF varaqasi (DL Flyer) — kartochkalardagi tavsiflar shulardan olingan
.claude/launch.json  ko'rish uchun lokal server: `python -m http.server 8080`
```

Brauzer panelida faylni to'g'ridan-to'g'ri ochganda rasmlar chiqmaydi, `sayt` serveri (localhost:8080) orqali ko'rish kerak.

## Sahifa tartibi

1. **Chap panel (dock)** — ekran chap devorida, shaffof shisha: logo, Biz haqimizda, Mahsulotlar, Aloqa, Qo'ng'iroq. Ikonkalar 44px, hover'da nomi chiqadi. Telefonda pastga gorizontal tushadi. Yuqorida menyu (header) yo'q.
2. **Bosh qism (hero)** — Dribbble "Meridian" shotining tuzilishi: grid, chapda katta sarlavha, o'ngda mahsulotlar aylanasi (orbit, markazda logo), pastda: chapda tugma + "Hosildorlik +30–40%" kartochkasi, o'rtada Eco Power rasmi, o'ngda "O'simlik o'sishi" grafigi. Fon — 5 ta shisha rasmi (`photo_..._19-23-34.jpg`) ozgina xiralashtirilgan (blur 4px) + yupqa to'q parda.
   - Sarlavha shrifti Playfair Display, harflar ichi shaffof shisha (background-clip:text + text-stroke).
   - Tugma va kartochkalar shaffof shisha.
3. **Biz haqimizda** — `.intro`: chapda kichik yozuv, o'ngda katta sarlavha; matn + 3 ta statistika.
4. **Mahsulotlar katalogi** — macOS segmented control bilan saralash (Hammasi / Biostimulyatorlar / Gel o'g'itlar / NPK gel). 14 ta kartochka. Har kartochka foni — o'z mahsulot rasmi xira va shaffof (`.card::before`, rasm manzili JS orqali `--img` ga to'liq URL bilan beriladi, aks holda CSS uni `css/` dan qidiradi).
5. **Daladan natijalar** (`#natijalar`) — 3 ta Instagram reels kartochkasi (muqova `rasmlar/reel-*.jpg`, bosilganda Instagram ochiladi); telefonda yonma-yon suriladi.
6. **Foydali ma'lumotlar** (`#foydali`) — eng yangi 3 ta maqola, "Barcha maqolalar" `maqolalar.html` ga olib boradi. Har faktda ishonchli manba bo'lsin, matn ko'chirilmaydi, yangilik to'qilmaydi, me'yor taxmin qilinmaydi.
7. **Nega Agrosan** — 01–04 raqamli 4 sabab.
8. **Aloqa** — to'q yashil blok, Bio Energy Active rasmi, telefon va Instagram tugmalari.

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
- Shrift: Inter (asosiy), Playfair Display (faqat hero sarlavhasi).
- Har o'zgarishdan keyin brauzerda kompyuter (1440px) va telefon (375px) o'lchamida tekshirish; telefonda gorizontal scroll bo'lmasin.
