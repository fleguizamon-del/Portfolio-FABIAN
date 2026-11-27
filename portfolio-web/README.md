# Portfolio web – Fabián Leguizamón

Sitio estático (HTML + CSS + un poco de JS) que replica la estructura y el estilo de
https://juandellacha.com/cartas-gempa (Adobe Portfolio) con el contenido del PDF
`Portfolio2026-2.pdf`.

## Verlo
- Rápido: doble clic en `index.html`.
- Como servidor (recomendado, igual a cómo se verá online):
  `python -m http.server 8000` en esta carpeta y abrir http://localhost:8000

## Páginas
| Referencia (juandellacha.com) | Local |
|---|---|
| /work (grilla Portfolio) | `index.html` |
| /cartas-gempa (página de proyecto) | `proyectos/<slug>.html` (10 proyectos) |
| /about | `about.html` |
| /contact | `contact.html` |

## Editar contenido
1. Textos, orden de proyectos, portadas y filas de imágenes: `content.json`.
   - Cada elemento de `rows` es una fila: 1 imagen = ancho completo; 2 o 3 = fila con altura igualada.
2. Regenerar las páginas: `python build.py` (Python 3, sin dependencias).
3. Imágenes nuevas: copiarlas a `assets/img/<proyecto>/` y agregar sus medidas en
   `assets/img/dims.json` (ancho, alto), o volver a correr `tools/process_images.py`.

`tools/process_images.py` documenta cómo se extrajeron las imágenes del PDF
(`pdfimages -all -p Portfolio2026-2.pdf raw/img` y luego el script; necesita Pillow).

## Diferencias conocidas con la referencia
- Tipografías: la referencia usa fuentes de Adobe Typekit con licencia para su dominio.
  Se reemplazaron por Space Mono (títulos/menú) y Jost (texto), ambas libres (OFL), alojadas en `assets/fonts`.
- El logo es texto en caja negra (la referencia usa una imagen).
- El formulario de contacto abre el programa de correo del visitante (mailto:) porque el sitio no tiene servidor.
- Los textos de cada proyecto son breves y salen de los datos del PDF: conviene que Fabián los amplíe.

## Publicarlo
Cualquier hosting estático sirve: GitHub Pages, Netlify o Vercel (arrastrar la carpeta).
