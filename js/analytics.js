// Google Analytics (GA4). ID kelgach faqat shu qatorni o'zgartiring.
var GA_ID = 'G-P5R45XDJ3D';

(function () {
  // ID hali qo'yilmagan bo'lsa yoki sayt lokal ochilgan bo'lsa, hech narsa qilmaydi
  if (!/^G-[A-Z0-9]+$/.test(GA_ID) || GA_ID === 'G-XXXXXXXXXX') return;
  if (location.hostname !== 'agrosan.uz' && location.hostname !== 'www.agrosan.uz') return;

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', GA_ID);
})();
