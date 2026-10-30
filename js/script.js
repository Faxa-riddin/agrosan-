document.getElementById("yil").textContent = new Date().getFullYear();

// Mahsulotlarni turi bo'yicha saralash
const buttons = document.querySelectorAll(".segmented button");
const cards = document.querySelectorAll(".card");
buttons.forEach(btn => {
  btn.addEventListener("click", () => {
    buttons.forEach(b => b.classList.toggle("on", b === btn));
    cards.forEach(card => {
      card.hidden = btn.dataset.f !== "all" && card.dataset.c !== btn.dataset.f;
    });
  });
});

// Har bir kartochka foniga o'z mahsulot rasmini berish
cards.forEach(card => {
  const img = card.querySelector(".pic img");
  // img.src to'liq manzil beradi (aks holda CSS uni css/ papkasidan qidiradi)
  if (img) card.style.setProperty("--img", `url("${img.src}")`);
});

// Chap paneldagi hozirgi bo'lim belgisini yoqish
const dockLinks = document.querySelectorAll(".dock-nav a");
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    dockLinks.forEach(a => a.classList.toggle("on", a.getAttribute("href") === "#" + entry.target.id));
  });
}, { rootMargin: "-45% 0px -50% 0px" });
dockLinks.forEach(a => observer.observe(document.querySelector(a.getAttribute("href"))));
