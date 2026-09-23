import copy, os, re, sys
from docx import Document
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nirs2_content as C

SRC = sys.argv[1]; OUT = sys.argv[2]

# матрица Полыги из генератора файлов «по образцу Мальцевой»
ns = {}
exec(open(os.path.join(HERE, "gen_maltseva.py"), encoding="utf-8").read().split("pat = re.compile")[0], ns)
M = ns["matrix"](ns["P"]["Полыги"])   # 4 строки × 6 колонок

doc = Document(SRC)
body = doc.element.body
blocks = [e for e in body if e.tag in (qn("w:p"), qn("w:tbl"))]
sectPr = body.find(qn("w:sectPr"))
T = lambda i: copy.deepcopy(blocks[i])

# образцы (ищутся по тексту, а не по номеру)
def ptext0(e): return "".join(t.text or "" for t in e.iter(qn("w:t")))
def after_cap(prefix):
    i = next(k for k, e in enumerate(blocks) if ptext0(e).startswith(prefix))
    return next(e for e in blocks[i:] if e.tag == qn("w:tbl"))
ilit = next(k for k, e in enumerate(blocks) if k > 100 and ptext0(e) == "СПИСОК ЛИТЕРАТУРЫ")
i1 = next(k for k, e in enumerate(blocks) if k > ilit and ptext0(e).startswith("1 "))
TPL = dict(pb=blocks[61], h1c=blocks[62], blank_h=blocks[63], p=blocks[64], pb2=blocks[113], h1=blocks[114],
           blank=blocks[118], h2=blocks[119], cap=blocks[131], after_tbl=blocks[133], lit=blocks[i1], h1lit=blocks[ilit])
TBL = dict(T_COMP=after_cap("Таблица 1 "), T_STAT=after_cap("Таблица 2 "), T_NORM=after_cap("Таблица 3 "),
           tpl3=after_cap("Таблица 6 "), tpl4=after_cap("Таблица 4 "))
LITSTART = i1
def strip_marks(el):
    for tag in ("w:bookmarkStart", "w:bookmarkEnd"):
        for b in el.iter(qn(tag)): b.getparent().remove(b)
    return el

def set_text(p, text):
    runs = p.findall(qn("w:r"))
    rpr = None
    for r in runs:
        if r.find(qn("w:rPr")) is not None: rpr = copy.deepcopy(r.find(qn("w:rPr"))); break
    for ch in list(p):
        if ch.tag != qn("w:pPr"): p.remove(ch)
    r = p.makeelement(qn("w:r"), {})
    if rpr is not None: r.append(rpr)
    t = r.makeelement(qn("w:t"), {}); t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(t); p.append(r)
    return p

def para(kind, text=None):
    p = strip_marks(copy.deepcopy(TPL[kind]))
    if text is not None: set_text(p, text)
    return p

def ptext(p): return "".join(t.text or "" for t in p.iter(qn("w:t")))

def set_jc(p, val):
    ppr = p.find(qn("w:pPr"))
    jc = ppr.find(qn("w:jc"))
    if jc is None: jc = ppr.makeelement(qn("w:jc"), {}); ppr.append(jc)
    jc.set(qn("w:val"), val)

def old_table(name):
    t = strip_marks(copy.deepcopy(TBL[name]))
    for p in t.iter(qn("w:p")):
        s = ptext(p)
        s2 = re.sub(r"(ГОСТ Р \d+)-\d{4}", r"\1", s)
        s2 = re.sub(r"\[([\d ,\-]+)\]", r"[[\1]]", s2)
        if s2 != s: set_text(p, s2)
    return t

WIDTHS = {3: None}
def set_widths(t, cms):
    tw = [int(c * 567) for c in cms]
    grid = t.find(qn("w:tblGrid"))
    for g, w in zip(grid.findall(qn("w:gridCol")), tw): g.set(qn("w:w"), str(w))
    for tr in t.findall(qn("w:tr")):
        for tc, w in zip(tr.findall(qn("w:tc")), tw):
            tcw = tc.find(qn("w:tcPr")).find(qn("w:tcW"))
            tcw.set(qn("w:w"), str(w)); tcw.set(qn("w:type"), "dxa")

def new_table(rows):
    tpl = TBL["tpl3"] if len(rows[0]) == 3 else TBL["tpl4"]
    t = strip_marks(copy.deepcopy(tpl))
    trs = t.findall(qn("w:tr"))
    head, bodyrow = trs[0], trs[1]
    for tr in trs[1:]: t.remove(tr)
    for c, txt in zip(head.findall(qn("w:tc")), rows[0]):
        ps = c.findall(qn("w:p")); [c.remove(x) for x in ps[1:]]; set_text(ps[0], txt)
    for row in rows[1:]:
        tr = copy.deepcopy(bodyrow)
        for j, (c, txt) in enumerate(zip(tr.findall(qn("w:tc")), row)):
            ps = c.findall(qn("w:p")); [c.remove(x) for x in ps[1:]]; set_text(ps[0], txt)
            set_jc(ps[0], "center" if txt.startswith("Глава") else "left")
        t.append(tr)
    if rows is C.NEW_TABLES.get("T_TASKS"): set_widths(t, [8.5, 6.5, 2.5])
    elif rows is C.NEW_TABLES.get("T_CALC"): set_widths(t, [2.4, 5.4, 3.7, 6.0])
    else: set_widths(t, [2.8, 7.3, 7.4])
    return t

out = []
def add(e): out.append(e)
def P(text): add(para("p", text))
def items(lst):
    for i, s in enumerate(lst):
        add(para("p", "- " + s + (";" if i < len(lst) - 1 else ".")))
import json
SPLITS = json.load(open(os.path.join(HERE, "splits.json"))) if os.path.exists(os.path.join(HERE, "splits.json")) else {}
def section(lst):
    for x in lst:
        if isinstance(x, tuple):
            cap = C.CAPS[x[1]]; n = cap.split()[1]
            t = old_table(x[1]) if x[1] in TBL else new_table(C.NEW_TABLES[x[1]])
            sp = SPLITS.get(n)
            if sp == 0: add(para("pb2"))
            add(para("cap", cap))
            if sp:   # разбиение: строки с sp — во вторую часть с повтором шапки
                t2 = copy.deepcopy(t); trs, trs2 = t.findall(qn("w:tr")), t2.findall(qn("w:tr"))
                for tr in trs[sp - 1:]: t.remove(tr)
                for tr in trs2[1:sp - 1]: t2.remove(tr)
                add(t); pc = para("cap", f"Продолжение таблицы {n}")
                pc.find(qn("w:pPr")).insert(0, pc.makeelement(qn("w:pageBreakBefore"), {})); add(pc); add(t2)
            else: add(t)
            add(para("after_tbl", ""))
        else: P(x)

def low(s): return s[0].lower() + s[1:]
def fix_list(s): return s.replace(". Оценка эффективности", ", а также оценка эффективности")

# ---- ВВЕДЕНИЕ ----
add(para("pb")); add(para("h1c", "ВВЕДЕНИЕ")); add(para("blank_h"))
section(C.INTRO_HEAD)
items([r[0] for r in M])
section(C.INTRO_OBJ)
items([low(fix_list(r[1])) for r in M])
P(C.INTRO_METHODS)
P("Решение поставленных задач позволяет получить следующие результаты, выносимые на защиту:")
items([low(fix_list(r[2])) for r in M])
P("Новизна полученных результатов заключается в следующем:"); items([low(r[3]) for r in M])
P("Практическая ценность полученных результатов состоит в следующем:"); items([low(r[4]) for r in M])
P("Теоретическая значимость результатов исследования определяется следующим образом:"); items([low(r[5]) for r in M])
section(C.INTRO_TAIL)

# ---- ГЛАВА 1 ----
add(para("pb2")); add(para("h1", C.CH1)); add(para("blank_h"))
section(C.CH1_INTRO)
for title, content in zip(C.SUB, [C.S11, C.S12, C.S13, C.S14, C.S15, C.S16, C.S17]):
    add(para("blank")); add(para("h2", title)); add(para("blank_h"))
    section(content)

# ---- ссылки: нумерация по первому появлению ----
MARK = re.compile(r"\[\[([^\]]+)\]\]")
def keys_of(inner):
    ks = []
    for part in [x.strip() for x in inner.split(",")]:
        m = re.fullmatch(r"(\d+)-(\d+)", part)
        if m: ks += [str(n) for n in range(int(m.group(1)), int(m.group(2)) + 1)]
        else: ks.append(part)
    return ks
order = []
allp = [p for e in out for p in ([e] if e.tag == qn("w:p") else e.iter(qn("w:p")))]
for p in allp:
    for m in MARK.finditer(ptext(p)):
        for k in keys_of(m.group(1)):
            if k not in order: order.append(k)
num = {k: i + 1 for i, k in enumerate(order)}
def fmt(inner):
    ns_ = sorted(num[k] for k in keys_of(inner))
    runs, cur = [], [ns_[0]]
    for n in ns_[1:]:
        if n == cur[-1] + 1: cur.append(n)
        else: runs.append(cur); cur = [n]
    runs.append(cur)
    return "[" + ", ".join(f"{r[0]}-{r[-1]}" if len(r) > 1 else str(r[0]) for r in runs) + "]"
for p in allp:
    s = ptext(p)
    if "[[" in s: set_text(p, MARK.sub(lambda m: fmt(m.group(1)), s))

# ---- СПИСОК ЛИТЕРАТУРЫ ----
oldlit = {}
for b in blocks[LITSTART:]:
    m = re.match(r"(\d+) (.*)", ptext(b))
    if m: oldlit[m.group(1)] = m.group(2)
add(para("pb2")); add(para("h1lit", "СПИСОК ЛИТЕРАТУРЫ")); add(para("blank_h"))
for k in order:
    add(para("lit", f"{num[k]} " + (C.NEW_REFS[k] if k in C.NEW_REFS else oldlit[k])))

# ---- замена тела после содержания ----
for e in blocks[61:]: body.remove(e)
for e in out: sectPr.addprevious(e)
doc.save(OUT)

unused = [k for k in oldlit if k not in num]
print("источников:", len(order), "| новых:", [k for k in order if k in C.NEW_REFS], "| не вошли из старых:", unused)
