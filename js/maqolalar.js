// Foydali ma'lumotlar: maqolalar data/maqolalar.json faylidan olinadi
const TURLAR = { yangilik: "Yangilik", maslahat: "Maslahat" };

function el(teg, klass, matn) {
  const e = document.createElement(teg);
  if (klass) e.className = klass;
  if (matn) e.textContent = matn;
  return e;
}

function tegi(m) {
  const chip = el("span", "chip");
  chip.append(el("span", "dot"), TURLAR[m.tur] || m.tur);
  return chip;
}

function rasmi(m, klass) {
  const img = el("img", klass);
  img.src = m.rasm.fayl;
  img.alt = m.rasm.alt;
  img.loading = "lazy";
  return img;
}

function kartochka(m) {
  const a = el("a", "post");
  a.href = "maqolalar.html?id=" + encodeURIComponent(m.id);
  a.dataset.t = m.tur;
  const past = el("span", "post-foot");
  past.append(el("span", "", m.sana), el("span", "post-more", "O'qish →"));
  const tana = el("span", "post-body");
  tana.append(tegi(m), el("h3", "", m.sarlavha), el("p", "", m.qisqa), past);
  a.append(rasmi(m, "post-pic"), tana);
  return a;
}

function maqolaniChiz(joy, m) {
  document.title = m.sarlavha + " — Agrosan";
  const orqaga = el("a", "article-back", "← Barcha maqolalar");
  orqaga.href = "maqolalar.html";
  const b = el("article", "article");
  const bosh = el("div", "article-meta");
  bosh.append(tegi(m), el("span", "", m.sana));
  b.append(rasmi(m, "article-pic"), bosh, el("h1", "", m.sarlavha), el("p", "article-lead", m.qisqa));
  m.matn.forEach(q => {
    if (Array.isArray(q)) {
      const ul = el("ul");
      q.forEach(s => ul.append(el("li", "", s)));
      b.append(ul);
    } else {
      b.append(el("p", "", q));
    }
  });
  if (m.tur === "maslahat") {
    b.append(el("p", "article-note", "Bu umumiy ma'lumot. Aniq me'yor uchun qadoqdagi yo'riqnomaga amal qiling va mutaxassis bilan maslahatlashing."));
  }
  const manba = el("div", "article-sources");
  manba.append(el("h2", "", "Manbalar"));
  const ol = el("ul");
  m.manbalar.forEach(s => {
    const li = el("li");
    const a = el("a", "", s.nom);
    a.href = s.url; a.target = "_blank"; a.rel = "noopener";
    li.append(a);
    ol.append(li);
  });
  manba.append(ol);
  const izoh = el("p", "article-credit", "Rasm: " + m.rasm.muallif + ", " + m.rasm.litsenziya + " (kesilgan). ");
  const rl = el("a", "", "Asl rasm");
  rl.href = m.rasm.url; rl.target = "_blank"; rl.rel = "noopener";
  izoh.append(rl);
  manba.append(izoh);
  const tel = el("a", "btn btn-primary", "Savolingiz bormi? Qo'ng'iroq qiling");
  tel.href = "tel:+998501003030";
  b.append(manba, tel);
  joy.replaceChildren(orqaga, b);
}

function royxatniChiz(maqolalar) {
  const royxat = document.getElementById("maqola-royxat");
  const karta = maqolalar.map(kartochka);
  royxat.replaceChildren(...karta);
  const tugmalar = document.querySelectorAll("#maqola-filtr button");
  tugmalar.forEach(t => t.addEventListener("click", () => {
    tugmalar.forEach(b => b.classList.toggle("on", b === t));
    karta.forEach(k => { k.hidden = t.dataset.f !== "all" && k.dataset.t !== t.dataset.f; });
  }));
}

async function boshla() {
  const bosh = document.getElementById("maqola-bosh");
  const sahifa = document.getElementById("maqola-sahifa");
  if (!bosh && !sahifa) return;
  let maqolalar;
  try {
    const javob = await fetch("data/maqolalar.json", { cache: "no-cache" });
    maqolalar = await javob.json();
  } catch {
    (bosh || document.getElementById("maqola-royxat")).textContent = "Maqolalarni yuklab bo'lmadi. Sahifani yangilang.";
    return;
  }
  if (bosh) {
    bosh.replaceChildren(...maqolalar.slice(0, 3).map(kartochka));
    return;
  }
  const id = new URLSearchParams(location.search).get("id");
  if (id) {
    const m = maqolalar.find(x => x.id === id);
    if (m) { maqolaniChiz(sahifa, m); return; }
  }
  royxatniChiz(maqolalar);
}

const yil = document.getElementById("yil");
if (yil) yil.textContent = new Date().getFullYear();

boshla();
