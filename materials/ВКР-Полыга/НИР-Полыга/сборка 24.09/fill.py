import pymupdf, sys
d = pymupdf.open(sys.argv[1] if len(sys.argv) > 1 else "nirs2.pdf")
H = d[0].rect.height
rows = []
for i, p in enumerate(d):
    bl = [b for b in p.get_text("blocks") if b[4].strip() and not (b[1] > H - 80 and b[4].strip().isdigit())]
    top = min(b[1] for b in bl) if bl else 0
    bot = max(b[3] for b in bl) if bl else 0
    rows.append((i + 1, top, bot, bl[0][4].strip()[:40].replace("\n", " ") if bl else ""))
full = sorted(r[2] for r in rows)[int(len(rows) * 0.8)]   # низ «полной» страницы
TOP = 56.7
for n, top, bot, first in rows:
    ratio = (bot - TOP) / (full - TOP)
    if ratio < 0.7: print(f"стр. {n}: заполнено {ratio:.0%}  | начинается с: {first}")
print("страниц:", len(rows))
