#!/usr/bin/env python3
"""Hoja de contacto de un carrusel: todas las diapositivas en una sola imagen, numeradas.

Uso:
  python3 hoja_contacto.py --out hoja.jpg <url_o_ruta_1> <url_o_ruta_2> ...

Acepta URLs (p. ej. las raw de GitHub que usa Buffer) o rutas locales.
Pensada para pegarla en línea en el email de aprobación.
"""
import argparse, io, math, urllib.request
from PIL import Image, ImageDraw, ImageFont

def load(src):
    if src.startswith("http"):
        with urllib.request.urlopen(src, timeout=30) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    return Image.open(src).convert("RGB")

def font(size):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cols", type=int, default=0, help="columnas (por defecto 3, o 2 si hay 4 o menos)")
    ap.add_argument("--ancho", type=int, default=420, help="ancho de cada miniatura en px")
    ap.add_argument("srcs", nargs="+")
    a = ap.parse_args()
    imgs = [load(s) for s in a.srcs]
    cols = a.cols or (2 if len(imgs) <= 4 else 3)
    rows = math.ceil(len(imgs) / cols)
    tw = a.ancho
    th = round(tw * imgs[0].height / imgs[0].width)
    gap = 16
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * th + (rows + 1) * gap), (240, 236, 230))
    d = ImageDraw.Draw(sheet)
    f = font(26)
    for i, im in enumerate(imgs):
        x = gap + (i % cols) * (tw + gap)
        y = gap + (i // cols) * (th + gap)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        bx, by = x + tw - 56, y + th - 56  # esquina inferior derecha: no tapa logotipo ni titulares
        d.ellipse([bx, by, bx + 42, by + 42], fill=(243, 86, 71))
        n = str(i + 1)
        w = d.textlength(n, font=f)
        d.text((bx + 21 - w / 2, by + 6), n, fill="white", font=f)
    sheet.save(a.out, quality=82, optimize=True)
    print(a.out, sheet.size)

if __name__ == "__main__":
    main()
