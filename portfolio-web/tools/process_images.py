"""Convierte las imágenes extraídas del PDF (pdfimages -all -p) a JPG web.
Uso: python3 process_images.py <carpeta_raw> <carpeta_salida>
"""
import sys, json, os
from PIL import Image

RAW, OUT = sys.argv[1], sys.argv[2]
MAP = {
  "en-el-cielo": ["003-002","003-003","004-008","004-009","005-013","005-015"],
  "sindrome-nuremberg": ["006-016","006-017"],
  "diversicaf": ["007-019","007-020"],
  "atamay": ["008-021","009-022","010-023"],
  "el-pacto": ["011-024","012-025","012-027","012-028","012-029"],
  "ventanas": ["013-030"],
  "album-diez": ["014-038","014-037","015-040","015-039","015-041"],
  "lugares-comunes": ["016-042","016-043","017-044","017-045","018-046","018-047"],
  "exposiciones": ["019-048","019-049"],
  "proyectos-personales": ["001-000","021-055","020-050","020-052","021-054","022-056","023-057","023-058"],
  "about": ["002-001","024-059"],
}
files = {f.split('.')[0][4:]: f for f in os.listdir(RAW)}
dims = {}
for slug, ids in MAP.items():
    os.makedirs(os.path.join(OUT, slug), exist_ok=True)
    for i, k in enumerate(ids, 1):
        im = Image.open(os.path.join(RAW, files[k])).convert("RGB")
        im.thumbnail((2000, 2000), Image.LANCZOS)
        name = f"{slug}/{slug}-{i:02d}.jpg"
        im.save(os.path.join(OUT, name), "JPEG", quality=84, optimize=True, progressive=True)
        dims[name] = im.size
json.dump(dims, open(os.path.join(OUT, "dims.json"), "w"), indent=1)
print(len(dims), "imágenes")

# Nota: proyectos-personales-03 y -04 son las dos mitades de una doble página;
# en el sitio se unieron en una sola imagen (proyectos-personales-03.jpg, 1952x976).
