// Eski GitHub Pages manzilidan asosiy saytga (agrosan.uz) o'tkazadi; agrosan.uz'da hech narsa qilmaydi
if (location.hostname.endsWith("github.io")) {
  const yol = location.pathname.replace(/^\/agrosan-/, "") || "/";
  location.replace("https://agrosan.uz" + yol + location.search + location.hash);
}
