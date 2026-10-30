"""
Arma el sitio catalogo.aranti.mx en la carpeta dist/ (Netlify lo corre en cada deploy).

- Convierte cada página de catalogo.pdf en una imagen ligera (WebP) para que el
  catálogo abra rápido en celular.
- Genera una versión comprimida del PDF para el botón de descarga.
- Copia el admin y demás archivos.

Si alguien sube un catalogo.pdf nuevo (desde el admin o GitHub), las imágenes se
regeneran solas. Las páginas donde empieza cada sección se editan en secciones.json.
"""
import hashlib, io, json, os, shutil, sys, zlib

import pypdfium2 as pdfium
import pikepdf
from pikepdf import Name, PdfImage
from PIL import Image

SRC = "catalogo.pdf"
OUT = "dist"
ANCHO = 903          # ancho en px de cada página
CALIDAD = 74         # calidad WebP


def comprimir_pdf(origen, destino):
    """Baja la resolución de las fotos del PDF (~93 ppi) sin tocar texto ni diseño."""
    pdf = pikepdf.open(origen)
    for o in list(pdf.objects):
        if not isinstance(o, pikepdf.Stream) or o.get("/Subtype") != "/Image":
            continue
        if o.get("/BitsPerComponent", 8) != 8 or o.get("/ImageMask"):
            continue
        cs = o.get("/ColorSpace")
        if isinstance(cs, pikepdf.Array) and cs[0] == "/Indexed":
            continue
        crudo = len(o.read_raw_bytes())
        if crudo < 6000:
            continue
        try:
            im = PdfImage(o).as_pil_image()
        except Exception:
            continue
        im = im.convert("RGB") if im.mode != "L" else im
        nw, nh = max(1, int(im.width * 0.62)), max(1, int(im.height * 0.62))
        im2 = im.resize((nw, nh), Image.LANCZOS)
        b = io.BytesIO()
        im2.save(b, "JPEG", quality=62, optimize=True, progressive=True)
        if len(b.getvalue()) >= crudo * 0.9:
            continue
        try:
            sm = o.SMask if "/SMask" in o else None
            smi = PdfImage(sm).as_pil_image().convert("L").resize((nw, nh), Image.LANCZOS) if sm is not None else None
        except Exception:
            continue
        o.write(b.getvalue(), filter=Name.DCTDecode)
        o.Width, o.Height = nw, nh
        o.ColorSpace = Name.DeviceRGB if im2.mode == "RGB" else Name.DeviceGray
        for k in ("/DecodeParms", "/Decode"):
            if k in o:
                del o[k]
        if smi is not None:
            sm.write(zlib.compress(smi.tobytes(), 9), filter=Name.FlateDecode)
            sm.Width, sm.Height = nw, nh
            sm.ColorSpace = Name.DeviceGray
            for k in ("/DecodeParms", "/Decode"):
                if k in sm:
                    del sm[k]
    pdf.save(destino, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    datos = open(SRC, "rb").read()
    version = hashlib.sha1(datos).hexdigest()[:10]
    carpeta = f"paginas-{version}"
    os.makedirs(os.path.join(OUT, carpeta))

    doc = pdfium.PdfDocument(SRC)
    total = len(doc)
    w0, h0 = doc[0].get_size()
    alto = round(ANCHO * h0 / w0)
    for i in range(total):
        pagina = doc[i]
        w, _ = pagina.get_size()
        img = pagina.render(scale=ANCHO / w).to_pil().convert("RGB")
        img.save(os.path.join(OUT, carpeta, f"{i+1:03d}.webp"), "WEBP", quality=CALIDAD, method=6)
        if i == 0:
            img.resize((img.width // 2, img.height // 2), Image.LANCZOS).save(
                os.path.join(OUT, "portada.jpg"), quality=80)
        print(f"página {i+1}/{total}", flush=True)
    doc.close()

    try:
        comprimir_pdf(SRC, os.path.join(OUT, "catalogo.pdf"))
    except Exception as e:  # si algo falla, se publica el PDF original
        print("No se pudo comprimir el PDF, se usa el original:", e)
        shutil.copy(SRC, os.path.join(OUT, "catalogo.pdf"))
    print("PDF:", round(os.path.getsize(os.path.join(OUT, "catalogo.pdf")) / 1e6, 1), "MB")

    secciones = json.load(open("secciones.json", encoding="utf-8"))
    html = open("index.html", encoding="utf-8").read()
    config = (f"const TOTAL = {total};\nconst CARPETA = '{carpeta}';\n"
              f"const ANCHO = {ANCHO}, ALTO = {alto};\n"
              f"const SECCIONES = {json.dumps(secciones, ensure_ascii=False)};")
    inicio, fin = "/*CONFIG*/", "/*FIN CONFIG*/"
    a, b = html.index(inicio) + len(inicio), html.index(fin)
    html = html[:a] + "\n" + config + "\n" + html[b:]
    html = html.replace("{{CARPETA}}", carpeta)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)

    shutil.copytree("admin", os.path.join(OUT, "admin"))
    shutil.copy("_headers", os.path.join(OUT, "_headers"))
    print(f"Listo: {total} páginas en {carpeta}")


if __name__ == "__main__":
    sys.exit(main())
