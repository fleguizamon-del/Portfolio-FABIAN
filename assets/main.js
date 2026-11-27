// Menú mobile, "volver arriba" y formulario de contacto (mailto).
(function () {
  var btn = document.querySelector('.hamburger');
  var menu = document.getElementById('responsive-nav');
  function setOpen(open) {
    if (!menu) return;
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('nav-open', open);
    if (open) {
      menu.hidden = false;
      requestAnimationFrame(function () { menu.classList.add('open'); });
    } else {
      menu.classList.remove('open');
      setTimeout(function () { menu.hidden = true; }, 200);
    }
  }
  if (btn && menu) {
    btn.addEventListener('click', function () { setOpen(true); });
    menu.querySelector('.close-nav').addEventListener('click', function () { setOpen(false); });
    menu.querySelectorAll('nav a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 932) setOpen(false); });
  }

  var top = document.querySelector('.back-to-top');
  if (top) top.addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Sitio estático: el formulario arma un email en el cliente de correo del visitante.
  var form = document.querySelector('.contact-form');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = form.elements;
    var subject = 'Contacto desde el portfolio – ' + f.name.value;
    var body = f.message.value + '\n\n' + f.name.value + ' (' + f.email.value + ')';
    window.location.href = 'mailto:' + form.dataset.email +
      '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });
})();
