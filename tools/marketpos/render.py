import pypdfium2 as pdfium, sys, pathlib
pdf = pdfium.PdfDocument(sys.argv[1]); out = pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
print("pages", len(pdf))
for i in range(len(pdf)):
    pdf[i].render(scale=1.3).to_pil().save(out / f"p{i+1:02d}.png")
