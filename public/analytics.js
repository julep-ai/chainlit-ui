// Wait for the page to load
window.addEventListener("load", function () {
  // Google tag (gtag.js)
  const script = document.createElement("script");
  script.src = "https://www.googletagmanager.com/gtag/js?id=G-PRBSQ355GE";
  script.async = true;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag("js", new Date());
  gtag("config", "G-PRBSQ355GE");
});
