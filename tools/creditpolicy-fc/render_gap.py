import pathlib, sys
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

pdf = pathlib.Path(sys.argv[1])
out = pathlib.Path(__file__).with_name("gappages")
out.mkdir(exist_ok=True)
for f in out.glob("*.png"):
    f.unlink()
doc = pdfium.PdfDocument(str(pdf))
n = len(doc)
thumbs = []
for i in range(n):
    img = doc[i].render(scale=1.4).to_pil().convert("RGB")
    img.save(out / "p{:02d}.png".format(i + 1))
    g = img.convert("L")
    dark = sum(1 for px in g.getdata() if px < 200) / (g.width * g.height)
    print("page {:2d}: ink {:.1%}".format(i + 1, dark))
    t = img.copy(); t.thumbnail((300, 425)); thumbs.append(t)
cols = 5
rows = (n + cols - 1) // cols
for start in range(0, n, 10):
    chunk = thumbs[start:start + 10]
    r = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 310, r * 445), "white")
    dr = ImageDraw.Draw(sheet)
    for k, t in enumerate(chunk):
        x, y = (k % cols) * 310 + 5, (k // cols) * 445 + 15
        sheet.paste(t, (x, y))
        dr.rectangle([x, y, x + t.width, y + t.height], outline="#999")
        dr.text((x, y - 13), "p{}".format(start + k + 1), fill="black")
    sheet.save(out / "sheet{}.png".format(start // 10 + 1))
print("pages", n)
