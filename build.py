"""Genera el sitio estático a partir de content.json.

Uso (desde esta carpeta):  python build.py
Solo usa la biblioteca estándar de Python 3. Crea/actualiza:
  index.html, about.html, contact.html y proyectos/<slug>.html
Para cambiar textos o imágenes, editá content.json y volvé a correrlo.
"""
import json
import os
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(ROOT, "content.json"), encoding="utf-8"))
DIMS = json.load(open(os.path.join(ROOT, "assets/img/dims.json"), encoding="utf-8"))
SITE = C["site"]
PROJECTS = C["projects"]

# --- íconos (SVG propios, trazos simples) ---------------------------------
ICONS = {
    "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM12 3.6c2.7 0 3 0 4.1.1 2.7.1 4 1.4 4.1 4.1.1 1.1.1 1.4.1 4.1s0 3-.1 4.1c-.1 2.7-1.4 4-4.1 4.1-1.1.1-1.4.1-4.1.1s-3 0-4.1-.1c-2.7-.1-4-1.4-4.1-4.1C3.7 15 3.6 14.7 3.6 12s0-3 .1-4.1c.1-2.7 1.4-4 4.1-4.1C8.9 3.6 9.3 3.6 12 3.6zM12 2C9.3 2 8.9 2 7.9 2.1 4.2 2.2 2.2 4.2 2.1 7.9 2 8.9 2 9.3 2 12s0 3.1.1 4.1c.1 3.7 2.2 5.7 5.8 5.8 1 .1 1.4.1 4.1.1s3.1 0 4.1-.1c3.6-.1 5.7-2.2 5.8-5.8.1-1 .1-1.4.1-4.1s0-3.1-.1-4.1c-.1-3.6-2.2-5.7-5.8-5.8C15.1 2 14.7 2 12 2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3V5zm2 2v.4l7 4.6 7-4.6V7H5zm14 2.8-7 4.6-7-4.6V17h14V9.8z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5a9.4 9.4 0 0 0-8.1 14.2L2.5 21.5l4.9-1.3A9.4 9.4 0 1 0 12 2.5zm0 17.1c-1.4 0-2.8-.4-4-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A7.7 7.7 0 1 1 12 19.6zm4.3-5.8c-.2-.1-1.4-.7-1.6-.8-.2-.1-.4-.1-.5.1l-.7.9c-.1.2-.3.2-.5.1a6.3 6.3 0 0 1-3.1-2.7c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.7-1.7c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1c0 1.2.9 2.4 1 2.6.1.2 1.8 2.7 4.3 3.8 1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>',
    "up": '<svg viewBox="0 0 26 26" aria-hidden="true"><path d="M13 3.6 5.3 11.3l1.4 1.4L12 7.4V22h2V7.4l5.3 5.3 1.4-1.4z"/></svg>',
}


def socials(prefix=""):
    s = SITE
    links = [
        ("instagram", f"https://www.instagram.com/{s['instagram']}/", "Instagram"),
        ("whatsapp", f"https://wa.me/{s['whatsapp']}", "WhatsApp"),
        ("mail", f"mailto:{s['email']}", "Email"),
    ]
    ext = ' target="_blank" rel="noopener"'
    items = "".join(
        f'<li><a href="{u}" aria-label="{label}"{ext if u.startswith("http") else ""}>{ICONS[k]}</a></li>'
        for k, u, label in links
    )
    return f"<ul>{items}</ul>"


def img_tag(path, prefix, alt, sizes="(max-width: 932px) 100vw, 72vw", lazy=True):
    w, h = DIMS[path]
    lz = ' loading="lazy"' if lazy else ""
    return (f'<img src="{prefix}assets/img/{path}" width="{w}" height="{h}" alt="{escape(alt)}"'
            f' sizes="{sizes}"{lz} decoding="async">')


def layout(title, body, active, prefix="", description=""):
    nav = [("about", "About", f"{prefix}about.html"),
           ("portfolio", "Portfolio", f"{prefix}index.html"),
           ("contact", "Contact", f"{prefix}contact.html")]
    act = ' class="active" aria-current="page"'
    nav_html = "".join(
        f'<a href="{href}"{act if key == active else ""}>{label}</a>'
        for key, label, href in nav)
    full_title = SITE["name"] + (f" - {title}" if title else "")
    desc = description or f"{SITE['name']} – {SITE['tagline']}. Portfolio de ilustración editorial, musical y proyectos personales."
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(desc)}">
<link rel="stylesheet" href="{prefix}assets/fonts.css">
<link rel="stylesheet" href="{prefix}assets/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23111'/%3E%3Ctext x='16' y='22' font-family='monospace' font-weight='700' font-size='16' fill='%23fff' text-anchor='middle'%3EFL%3C/text%3E%3C/svg%3E">
</head>
<body>
<header class="site-header">
  <nav class="nav">{nav_html}</nav>
  <div class="logo-wrap"><a class="logo" href="{prefix}index.html">{escape(SITE['logo'])}</a></div>
  <div class="social nav-social">{socials(prefix)}</div>
  <button class="hamburger" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="responsive-nav"><i></i><i></i><i></i></button>
</header>
<div class="responsive-nav" id="responsive-nav" hidden>
  <button class="close-nav" type="button" aria-label="Cerrar menú"></button>
  <nav>{nav_html}</nav>
  <div class="social">{socials(prefix)}</div>
</div>
<main class="site-content">
{body}
</main>
<footer class="site-footer"><div class="social">{socials(prefix)}</div></footer>
<a class="back-to-top" href="#top" aria-label="Volver arriba">{ICONS['up']}</a>
<script src="{prefix}assets/main.js" defer></script>
</body>
</html>
"""


def cover(p, prefix, small=False):
    w, h = DIMS[p["cover"]]
    desc = "" if small else f'<span class="description">{escape(p["description"])}</span>'
    return f"""<a class="project-cover" href="{prefix}proyectos/{p['slug']}.html">
  <img src="{prefix}assets/img/{p['cover']}" width="{w}" height="{h}" alt="{escape(p['title'])}" loading="lazy" decoding="async">
  <span class="details"><span class="details-inner">
    <span class="title">{escape(p['title'])}</span>
    {desc}
  </span></span>
</a>"""


def row(paths, prefix, alt, captions):
    if len(paths) == 1:
        p = paths[0]
        cap = f'<figcaption>{escape(captions[p])}</figcaption>' if p in captions else ""
        return f'<figure class="module module-image">{img_tag(p, prefix, alt)}{cap}</figure>'
    items = []
    for p in paths:
        w, h = DIMS[p]
        cap = f'<figcaption>{escape(captions[p])}</figcaption>' if p in captions else ""
        sz = f"(max-width: 932px) {100 // len(paths)}vw, {72 // len(paths)}vw"
        # flex-grow = relación de aspecto: todas las imágenes de la fila quedan con la misma altura
        items.append(f'<figure style="flex:{w / h:.4f} 1 0">{img_tag(p, prefix, alt, sizes=sz)}{cap}</figure>')
    return f'<div class="module module-collection">{"".join(items)}</div>'


def project_page(p):
    prefix = "../"
    i = PROJECTS.index(p)
    others = (PROJECTS[i + 1:] + PROJECTS[:i])[:4]
    rows = "\n".join(row(r, prefix, p["title"], p.get("captions", {})) for r in p["rows"])
    body = f"""<article class="page">
  <header class="page-header">
    <h1 class="title">{escape(p['title'])}</h1>
    <p class="description">{escape(p['description'])} ({escape(p['year'])})</p>
  </header>
  <div class="module module-text two-col">
    <div class="rich-text"><p><small>ESP.</small> <b class="cat">{escape(p['category'])}.</b> {p['esp']}</p></div>
    <div class="rich-text"><p><small>ENG.</small> {p['eng']}</p></div>
  </div>
{rows}
</article>
<section class="other-projects">
  <h2 class="other-projects-title">Otros proyectos / Other projects:</h2>
  <div class="covers covers--others">{''.join(cover(q, prefix, small=True) for q in others)}</div>
</section>"""
    return layout(p["title"], body, "", prefix,
                  f"{p['title']} – {p['description']} ({p['year']}). Ilustración de {SITE['name']}.")


def index_page():
    body = f'<section class="covers covers--grid">{"".join(cover(p, "") for p in PROJECTS)}</section>'
    return layout("", body, "portfolio")


def about_page():
    a = C["about"]
    imgs = row(a["images"], "", SITE["name"], {})
    esp = "".join(f"<p>{'<small>ESP.</small> ' if n == 0 else ''}{escape(t)}</p>" for n, t in enumerate(a["esp"]))
    eng = "".join(f"<p>{'<small>ENG.</small> ' if n == 0 else ''}{escape(t)}</p>" for n, t in enumerate(a["eng"]))
    lists = "".join(
        f'<div class="rich-text"><p class="list-title">{escape(l["title"])}</p><ul>{"".join(f"<li>{escape(x)}</li>" for x in l["items"])}</ul></div>'
        for l in a["lists"])
    body = f"""<article class="page">
  <header class="page-header"><h1 class="title">{escape(a['title'])}</h1></header>
{imgs}
  <div class="module module-text"><div class="rich-text">{esp}</div></div>
  <div class="module module-text"><div class="rich-text">{eng}</div></div>
  <div class="module module-text two-col">{lists}</div>
</article>"""
    return layout(a["title"], body, "about")


def contact_page():
    s = SITE
    body = f"""<article class="page">
  <header class="page-header">
    <h1 class="title">Contact</h1>
    <p class="description">¡Hablemos! / Let's talk!</p>
  </header>
  <div class="module module-text"><div class="rich-text">
    <p>¡Hablemos! / Let's talk! :)<br><a href="mailto:{s['email']}">{s['email']}</a></p>
    <p>Instagram: <a href="https://www.instagram.com/{s['instagram']}/" target="_blank" rel="noopener">@{s['instagram']}</a><br>
    WhatsApp: <a href="https://wa.me/{s['whatsapp']}" target="_blank" rel="noopener">{s['phone']}</a></p>
  </div></div>
  <form class="module contact-form" data-email="{s['email']}">
    <label>Nombre / Name *<input name="name" required placeholder="Tu nombre..."></label>
    <label>Email *<input name="email" type="email" required placeholder="Tu email..."></label>
    <label>Mensaje / Message *<textarea name="message" required placeholder="Tu mensaje..."></textarea></label>
    <button type="submit">Enviar / Send</button>
    <p class="form-note">Se abrirá tu programa de correo con el mensaje listo para enviar.</p>
  </form>
</article>"""
    return layout("Contact", body, "contact")


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


write("index.html", index_page())
write("about.html", about_page())
write("contact.html", contact_page())
for p in PROJECTS:
    write(f"proyectos/{p['slug']}.html", project_page(p))
print(f"OK: {3 + len(PROJECTS)} páginas generadas")
