# -*- coding: utf-8 -*-
"""Сборка отчёта по НИР Полыги К. Ю. из черновика ВКР и новых разделов."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.table import Table
from docx.text.paragraph import Paragraph

import nir_content as C
import nir_content2 as C2

SRC = r"C:/Users/iasti/OneDrive/Desktop/Пример/Main/"
FIG = r"C:/Users/iasti/AppData/Local/Temp/claude/C--Users-iasti--local-bin/f248cfb0-7747-4b8f-bcb4-0e1888feec3c/scratchpad/fig/"
OUT = r"C:/Users/iasti/OneDrive/Desktop/НИР-Полыга/Полыга К.Ю. НИР.docx"

# ------------------------------------------------------------------ источники
def load(name):
    d = Document(SRC + name)
    paras, tables = [], []
    for child in d.element.body.iterchildren():
        if child.tag.endswith('}p'):
            paras.append(Paragraph(child, d).text)
        elif child.tag.endswith('}tbl'):
            t = Table(child, d)
            tables.append([[c.text.strip() for c in r.cells] for r in t.rows])
    return paras, tables

INTRO, _ = load("Полыга К.Ю. ВКР — Введение.docx")
CH1, CH1T = load("Полыга К.Ю. ВКР — Глава 1.docx")
LIT, _ = load("Полыга К.Ю. ВКР — Список литературы.docx")

REPL = [
    ("выполняются в третьем разделе работы", "выполняются в рамках выпускной квалификационной работы"),
    ("составляет содержание второго раздела работы", "составляет содержание дальнейшего исследования"),
    ("устанавливается в третьем разделе работы", "устанавливается в рамках дальнейшего исследования"),
    ("что выполняется в третьем разделе работы", "что выполняется в рамках дальнейшего исследования"),
    ("реализуемого в пятом разделе работы", "реализуемого разрабатываемой интеллектуальной системой"),
    ("приведён в таблице 2", "приведён в таблице 4"),
    ("приведено в таблице 3", "приведено в таблице 5"),
    ("приведены в таблице 4", "приведены в таблице 6"),
    ("Таблица 2 – Техники", "Таблица 4 – Техники"),
    ("Таблица 3 – Сопоставление", "Таблица 5 – Сопоставление"),
    ("Таблица 4 – Сравнительный", "Таблица 6 – Сравнительный"),
]


def fix(t):
    for a, b in REPL:
        t = t.replace(a, b)
    return t


def P(i, src=CH1):
    return fix(src[i])


def PP(a, b, src=CH1):
    return [("p", fix(src[i])) for i in range(a, b + 1)]


# ------------------------------------------------------------------ структура
blocks = []
add = blocks.append

# --- ВВЕДЕНИЕ
add(("h1", "ВВЕДЕНИЕ"))
add(("p", INTRO[51]))
add(("p", C.STAT_FOREIGN_INTRO))
add(("p", C.STAT_RUSSIAN_INTRO))
for i in range(54, 58):
    add(("p", INTRO[i]))
for i in range(58, 63):
    add(("li", INTRO[i]))
for i in range(63, 67):
    add(("p", INTRO[i]))
for i in range(67, 72):
    add(("li", INTRO[i]))
add(("p", INTRO[72]))

add(("p", "Решение поставленных задач позволило сформировать следующие результаты, выносимые на защиту:"))
add(("li", "– модель объекта защиты в виде декомпозиции кластера на активы и границы доверия "
           "и построенное на ней дерево угроз и индуцированных рисков;"))
add(("li", "– база знаний троек «недостаток конфигурации кластера – эксплуатирующая техника – "
           "наступающий ущерб», покрывающая все выделенные активы объекта защиты;"))
add(("li", "– методика и реализующий её алгоритм расчёта меры риска компрометации контейнерного "
           "приложения, определяемой как произведение вероятности наступления ущерба на его величину;"))
add(("li", "– множество сценариев компрометации, представленных путями в графе достижимости, "
           "и риск-ландшафт кластера, построенный по осям «актив кластера», «техника эксплуатации» "
           "и «мера риска»;"))
add(("li", "– программное обеспечение интеллектуальной системы с моделью классификации рабочих нагрузок "
           "по уровню риска и комплекс мер регулирования риск-ландшафта кластера с оценкой достигаемого "
           "снижения меры риска."))
add(("p", "Новизна полученных результатов заключается в следующем:"))
add(("li", "– впервые дерево угроз построено для кластера как связной системы, в которой компрометация "
           "контейнерного приложения выступает начальным, а не конечным событием, что позволяет включить "
           "в рассмотрение переходы между границами доверия;"))
add(("li", "– впервые недостатки конфигурации Kubernetes, не обладающие идентификаторами уязвимостей, "
           "поставлены в однозначное соответствие техникам их эксплуатации и представлены в форме, "
           "пригодной для машинной обработки;"))
add(("li", "– впервые количественная оценка критичности получена для недостатков без идентификатора "
           "уязвимости за счёт переноса метрик на контекст кластера: уровень привилегий пода, пересекаемую "
           "границу доверия и доступность плоскости управления;"))
add(("li", "– впервые риск кластера определяется не суммой независимых несоответствий профилю, "
           "а достижимостью целевых активов по графу сценариев, что учитывает взаимное усиление "
           "недостатков конфигурации;"))
add(("li", "– впервые уровень риска рабочей нагрузки определяется обученной моделью по совокупности "
           "параметров её манифеста, а меры регулирования оцениваются величиной снижения меры риска, "
           "а не фактом соответствия профилю безопасности."))

add(("p", INTRO[79]))
for i in range(80, 85):
    add(("li", INTRO[i]))
add(("p", INTRO[85]))
for i in range(86, 91):
    add(("li", INTRO[i]))
add(("p", INTRO[91]))
add(("p", INTRO[92]))
add(("p", "Отчёт о научно-исследовательской работе состоит из введения, двух разделов, заключения, "
         "списка литературы и двух приложений. В первом разделе выполняется исследование инфраструктуры "
         "контейнеризации Kubernetes как объекта защиты: проводится декомпозиция кластера на активы "
         "и границы доверия, устанавливается соответствие нормативных требований параметрам конфигурации, "
         "анализируются информационное обеспечение риск-анализа и существующие средства анализа "
         "защищённости контейнерных сред, строятся дерево угроз и индуцированных ими рисков и "
         "риск-ландшафт объекта защиты, выявляются противоречия, ставятся задачи исследования "
         "и формируются требования к разрабатываемому обеспечению. Во втором разделе вырабатывается "
         "комплекс мер риск-регулирования, классифицированных по масштабности и профильности, "
         "разрабатываются частные регламенты выявления, реагирования и ликвидации последствий инцидентов "
         "и выполняется оценка достигаемого снижения меры риска."))

# --- РАЗДЕЛ 1
add(("h1", "1 Инфраструктура контейнеризации Kubernetes как объект защиты "
           "и анализ средств оценки её киберрисков"))
add(("p", P(1)))
add(("p", "Задачами раздела являются построение модели инфраструктуры контейнеризации Kubernetes "
          "как объекта защиты, выполнение её декомпозиции на активы и границы доверия, установление "
          "соответствия между нормативными требованиями к защите информации и параметрами конфигурации "
          "кластера, классификация недостатков конфигурации, анализ информационного обеспечения "
          "риск-анализа контейнерных сред и существующих средств анализа защищённости, построение дерева "
          "угроз и индуцированных ими рисков и риск-ландшафта объекта защиты, выявление противоречий, "
          "постановка задач исследования и формирование требований к разрабатываемому методическому, "
          "алгоритмическому и программному обеспечению."))

add(("h2", P(3)))
add(("h3", P(4)))
blocks += PP(5, 7)
add(("h3", P(8)))
blocks += PP(9, 11)
add(("tbl", P(12), CH1T[0]))
add(("p", P(14)))
add(("h3", P(15)))
add(("p", C.STAT_FOREIGN_CH))
add(("tbl", C.STAT_TABLE_TITLE, C.STAT_TABLE))
add(("p", C.STAT_FOREIGN_CH_AFTER))
add(("p", C.STAT_RUSSIAN_CH))
add(("p", P(18)))

add(("h2", P(19)))
add(("p", P(20)))
add(("fig", "fig1", P(22)))
blocks += PP(23, 25)

# новый 1.3
for b in C.NORM:
    add(b)

# бывший 1.3 -> 1.4
add(("h2", "1.4 Недостатки конфигурации кластера как источник киберрисков"))
add(("p", P(27)))
add(("fig", "fig2", P(29)))
blocks += PP(30, 35)

# бывший 1.4 -> 1.5
add(("h2", "1.5 Информационное обеспечение риск-анализа контейнерных сред"))
add(("h3", "1.5.1 Базы данных уязвимостей и угроз: CVE, NVD, банк данных угроз ФСТЭК России"))
blocks += PP(38, 40)
add(("h3", "1.5.2 Профили безопасности NIST SP 800-190 и CIS Kubernetes Benchmark"))
blocks += PP(42, 44)
add(("h3", "1.5.3 Матрица MITRE ATT&CK for Containers"))
add(("p", P(46)))
add(("tbl", P(47), CH1T[1]))
add(("p", P(49)))
add(("p", P(50)))
add(("tbl", P(51), CH1T[2]))

# бывший 1.5 -> 1.6
add(("h2", "1.6 Анализ существующих средств анализа защищённости контейнерных сред"))
add(("p", P(54)))
add(("tbl", P(55), CH1T[3]))
add(("p", P(57)))
add(("p", P(58)))

# бывший 1.6 -> 1.7
add(("h2", "1.7 Дерево угроз и индуцированных ими рисков инфраструктуры контейнеризации"))
add(("p", P(60)))
add(("fig", "fig3", P(62)))
add(("p", P(63)))
for i in range(64, 68):
    add(("li", P(i)))
blocks += PP(68, 71)

# новый 1.8
for b in C.RISK:
    add(b)

# новый 1.9
add(("h2", "1.9 Выявление противоречий и постановка задач исследования"))
add(("p", C.CONTRA_INTRO))
add(("p", "Первое противоречие следует из принятой модели объекта защиты (подраздел 1.2): величина ущерба "
          "определяется множеством активов, достижимых при компрометации рабочей нагрузки, тогда как "
          "сложившаяся практика оценивает защищённость по отдельным образам и обнаруженным в них "
          "уязвимостям, считая компрометацию приложения конечным событием. Второе противоречие "
          "установлено при анализе информационного обеспечения (подраздел 1.5.1): недостатки конфигурации "
          "кластера не получают идентификатора и не регистрируются в реестрах уязвимостей, ориентированных "
          "на дефекты программного кода. Третье противоречие вытекает оттуда же: калькуляторы критичности "
          "CVSS и EPSS принимают на вход уязвимость с присвоенным идентификатором и накопленной "
          "статистикой эксплуатации, отсутствующими у конфигурационных недостатков. Четвёртое "
          "противоречие установлено при анализе средств анализа защищённости (подраздел 1.6) "
          "и подтверждено построенным риск-ландшафтом (подраздел 1.8): риск определяется протяжённостью "
          "пути в графе достижимости, тогда как проверки существующих средств носят пообъектный характер. "
          "Пятое противоречие следует из установленной зависимости риск-ландшафта от текущего состава "
          "рабочих нагрузок: действующие методики предполагают разовое обследование по фиксированному "
          "профилю соответствия."))
add(("p", C.CONTRA_AFTER))
add(("tbl", C.CONTRA_TABLE_TITLE, C.CONTRA_TABLE))
add(("p", C.CONTRA_TAIL))

# новый 1.10
for b in C.REQ:
    add(b)

# выводы
add(("h2", "1.11 Выводы по первому разделу"))
add(("p", P(73)))
for i in range(74, 80):
    add(("li", P(i)))
add(("li", "– установлено соответствие между мерами защиты информации, предусмотренными приказами "
           "ФСТЭК России и национальными стандартами, и параметрами конфигурации кластера, посредством "
           "которых эти меры реализуются, чем определено множество контролируемых параметров объекта защиты;"))
add(("li", "– построен риск-ландшафт инфраструктуры контейнеризации: сформирован граф достижимости "
           "активов кластера, выделены десять типовых сценариев компрометации и для каждого вычислена "
           "мера риска как произведение вероятности наступления ущерба на его величину, что позволило "
           "упорядочить сценарии по величине риска и установить, что сценарии критического уровня "
           "не требуют эксплуатации уязвимостей программного обеспечения;"))
add(("li", "– выявлены пять противоречий, поставлены пять задач исследования, сформулированы пять "
           "выносимых на защиту результатов и сформированы восемь требований к разрабатываемому "
           "методическому, алгоритмическому и программному обеспечению."))
add(("p", "Полученные результаты обосновывают постановку задач исследования. Установленная "
          "неприменимость реестров уязвимостей к недостаткам конфигурации кластера определяет "
          "необходимость формирования базы знаний соответствий недостатков конфигурации и эксплуатирующих "
          "их техник с привязкой каждой пары к наступающему ущербу. Отсутствие количественной оценки "
          "критичности у недостатков без идентификатора уязвимости определяет необходимость разработки "
          "методики количественной оценки вероятности успешной компрометации контейнерного приложения "
          "и величины наступающего ущерба. Пообъектный характер существующих проверок определяет "
          "необходимость формирования типовых сценариев компрометации в виде путей достижимости активов. "
          "Статичность действующих методик определяет необходимость создания интеллектуальной системы, "
          "выполняющей классификацию рабочих нагрузок по уровню риска и пересчёт риск-ландшафта "
          "при смене снимка конфигурации. Выработка мер риск-регулирования, приводящих меру риска "
          "к допустимым значениям, составляет содержание второго раздела настоящей работы."))

# --- РАЗДЕЛ 2
for b in C2.SECTION2:
    add(b)

# --- ЗАКЛЮЧЕНИЕ
for b in C2.CONCLUSION:
    add(b)

# --- ЛИТЕРАТУРА
add(("h1", "СПИСОК ЛИТЕРАТУРЫ"))
lit_items = []
for t in LIT:
    t = t.strip()
    if re.match(r"^\d+\.\s", t):
        lit_items.append(re.sub(r"^\d+\.\s*", "", t))
for i, t in enumerate(lit_items, 1):
    add(("lit", "%d. %s" % (i, t)))
n0 = len(lit_items)
for j, t in enumerate(C2.EXTRA_LIT, 1):
    add(("lit", "%d. %s" % (n0 + j, t)))

# --- ПРИЛОЖЕНИЯ
add(("app", C2.APP_A_TITLE, C2.APP_A_SUB))
add(("tbl", C2.APP_A_TABLE_TITLE, C2.APP_A_TABLE))
add(("app", C2.APP_B_TITLE, C2.APP_B_SUB, True))

MATRIX = [
    ["№", "Противоречия между", "Задачи исследования", "Результаты исследования", "Новизна результатов",
     "Практическая ценность результатов", "Теоретическая ценность результатов"],
]
import openpyxl
wb = openpyxl.load_workbook(r"C:/Users/iasti/OneDrive/Desktop/Пример/Примеры/Матрица целеполагания - Полыга.xlsx",
                            data_only=True)
ws = wb.worksheets[0]
rows = list(ws.iter_rows(values_only=True))
for r in rows[2:7]:
    MATRIX.append([("" if c is None else str(c).strip()) for c in r[:7]])
add(("tbl-land", C2.APP_B_TABLE_TITLE, MATRIX))

# ------------------------------------------------------------------ оценка страниц
WORDS_PER_PAGE = 285


def est(bl):
    kind = bl[0]
    if kind in ("p", "li", "lit"):
        return len(bl[1].split()) / WORDS_PER_PAGE
    if kind in ("h1",):
        return 0.12
    if kind in ("h2", "h3"):
        return 0.10
    if kind == "fig":
        return 0.55
    if kind in ("tbl", "tbl-land"):
        rows_ = bl[2]
        cells_txt = sum(len(" ".join(r).split()) for r in rows_)
        return 0.16 + cells_txt / 420.0
    if kind == "list":
        return sum(len(x.split()) for x in bl[1]) / WORDS_PER_PAGE
    if kind == "app":
        return 0.25
    return 0


# реальные страницы, снятые из Word на предыдущем прогоне (если файл есть)
PAGEMAP = {}
tsv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "txt", "pages.tsv")
if os.path.exists(tsv):
    for ln in open(tsv, encoding="utf-8").read().splitlines():
        parts = ln.split("\t")
        if len(parts) == 2 and parts[0].isdigit():
            PAGEMAP.setdefault(parts[1].strip(), int(parts[0]))

toc = []
page = 3.0
for bl in blocks:
    if bl[0] == "h1":
        page = float(int(page) + 1) if page != int(page) else page
        toc.append((1, bl[1], PAGEMAP.get(bl[1], int(page))))
    elif bl[0] == "h2":
        toc.append((2, bl[1], PAGEMAP.get(bl[1], int(page))))
    elif bl[0] == "h3":
        toc.append((3, bl[1], PAGEMAP.get(bl[1], int(page))))
    elif bl[0] == "app":
        page = float(int(page) + 1)
        toc.append((1, bl[1] + ". " + bl[2], PAGEMAP.get(bl[1], int(page))))
    page += est(bl)

# ------------------------------------------------------------------ рендер
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
sec.left_margin, sec.right_margin = Cm(2.0), Cm(1.0)

st = doc.styles['Normal']
st.font.name = 'Times New Roman'
st.font.size = Pt(14)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
pf = st.paragraph_format
pf.line_spacing = 1.5
pf.space_after = Pt(0)
pf.space_before = Pt(0)
pf.first_line_indent = Cm(1.25)
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def par(text="", align=None, indent=None, bold=False, size=None, spacing=None, keep=False, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(indent if indent is not None else 1.25)
    p.paragraph_format.alignment = align if align is not None else WD_ALIGN_PARAGRAPH.JUSTIFY
    if spacing is not None:
        p.paragraph_format.line_spacing = spacing
    if keep:
        p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    return p


def page_break():
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.add_run().add_break(WD_BREAK.PAGE)


def col_widths(rows_, total_cm, ch_cm=0.21):
    """Ширины колонок: минимум под самое длинное слово + распределение остатка."""
    n = len(rows_[0])
    mins, weights = [], []
    for j in range(n):
        col = [str(r[j]) for r in rows_]
        longest = max((max((len(w) for w in v.replace("→", " ").split()), default=1) for v in col), default=1)
        mins.append(min(3.6, longest * ch_cm + 0.32))
        body = [str(r[j]) for r in rows_[1:]] or col
        weights.append(max(1.0, sum(len(v) for v in body) / max(1, len(body))))
    base = sum(mins)
    if base > total_cm:
        k = total_cm / base
        return [m * k for m in mins]
    rest = total_cm - base
    ws = sum(weights)
    return [mins[j] + rest * weights[j] / ws for j in range(n)]


def add_table(title, rows_, landscape_font=False, total_cm=18.0):
    par(title, align=WD_ALIGN_PARAGRAPH.LEFT, indent=1.25, spacing=1.0, keep=True)
    t = doc.add_table(rows=0, cols=len(rows_[0]))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    tblPr = t._tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)
    widths = col_widths(rows_, total_cm)
    fs = 10 if (landscape_font or len(rows_[0]) >= 7) else (11 if len(rows_[0]) >= 5 else 12)
    for ri, row in enumerate(rows_):
        cells = t.add_row().cells
        for ci, val in enumerate(row):
            cell = cells[ci]
            cell.width = Cm(widths[ci])
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.alignment = (WD_ALIGN_PARAGRAPH.CENTER if ri == 0 or len(str(val)) < 12
                                            else WD_ALIGN_PARAGRAPH.LEFT)
            r = p.add_run(str(val))
            r.font.size = Pt(fs)
            r.font.name = 'Times New Roman'
            r.bold = (ri == 0)
        if ri == 0:
            tr = t.rows[0]._tr
            trPr = tr.get_or_add_trPr()
            el = OxmlElement('w:tblHeader')
            trPr.append(el)
    par("", spacing=1.0)


def add_figure(name, caption):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(FIG + name + ".png", width=Cm(16.5))
    par(caption, align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0)
    par("", spacing=1.0)


# --- титульный лист
def title_page():
    par("МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ",
        align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, size=12)
    par("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ "
        "ВЫСШЕГО ОБРАЗОВАНИЯ", align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, size=12)
    par("«ВОРОНЕЖСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ»",
        align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, size=12, bold=True)
    par("(ФГБОУ ВО «ВГТУ», ВГТУ)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, size=12)
    par("", spacing=1.0)
    par("Факультет информационных технологий и компьютерной безопасности",
        align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, size=12)
    par("Кафедра систем информационной безопасности",
        align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, size=12)
    for _ in range(4):
        par("", spacing=1.0)
    par("ОТЧЁТ", align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, bold=True, size=16)
    par("по научно-исследовательской работе студента",
        align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, size=14)
    par("", spacing=1.0)
    par("Тема: «Разработка интеллектуальной системы оценки и регулирования киберрисков инфраструктуры "
        "контейнеризации Kubernetes в условиях компрометации контейнерных приложений»",
        align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0)
    par("", spacing=1.0)
    par("РАСЧЁТНО-ПОЯСНИТЕЛЬНАЯ ЗАПИСКА", align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0, size=13)
    for _ in range(2):
        par("", spacing=1.0)
    par("Разработал студент", align=WD_ALIGN_PARAGRAPH.LEFT, indent=0, spacing=1.0, size=13)
    par("гр. ИБ-201\t\t«____»____________\t\tК. Ю. Полыга",
        align=WD_ALIGN_PARAGRAPH.LEFT, indent=0, spacing=1.0, size=13)
    par("\t\t\t    подпись, дата\t\t\tинициалы, фамилия",
        align=WD_ALIGN_PARAGRAPH.LEFT, indent=0, spacing=1.0, size=10)
    par("", spacing=1.0)
    par("Руководитель работы:", align=WD_ALIGN_PARAGRAPH.LEFT, indent=0, spacing=1.0, size=13)
    par("д-р техн. наук, проф.\t«____»____________\t\tО. Н. Чопоров",
        align=WD_ALIGN_PARAGRAPH.LEFT, indent=0, spacing=1.0, size=13)
    par("     должность\t\t    подпись, дата\t\t\tинициалы, фамилия",
        align=WD_ALIGN_PARAGRAPH.LEFT, indent=0, spacing=1.0, size=10)
    for _ in range(2):
        par("", spacing=1.0)
    par("Защищена ____________________\t\tОценка ____________________",
        align=WD_ALIGN_PARAGRAPH.LEFT, indent=0, spacing=1.0, size=13)
    par("\t\t дата", align=WD_ALIGN_PARAGRAPH.LEFT, indent=0, spacing=1.0, size=10)
    for _ in range(3):
        par("", spacing=1.0)
    par("Воронеж 2026", align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0)
    page_break()


def toc_page():
    par("СОДЕРЖАНИЕ", align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, bold=True, spacing=1.0)
    par("", spacing=1.0)
    for lvl, name, pg in toc:
        p = doc.add_paragraph()
        pfm = p.paragraph_format
        pfm.first_line_indent = Cm(0)
        pfm.left_indent = Cm(0.75 * (lvl - 1))
        pfm.line_spacing = 1.5
        pfm.space_after = Pt(0)
        pfm.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pfm.tab_stops.add_tab_stop(Cm(17.4 - 0.75 * (lvl - 1)), 2, 1)  # RIGHT, DOTS
        r = p.add_run("%s \t%d" % (name, pg))
        r.font.size = Pt(14)
        r.bold = (lvl == 1)
    page_break()


def page_numbers():
    footer = doc.sections[0].footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run()
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    r = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '28')
    rpr.append(sz)
    r.append(rpr)
    t = OxmlElement('w:t')
    t.text = "1"
    r.append(t)
    fld.append(r)
    p._p.append(fld)
    # первая страница (титул) без номера
    sectPr = doc.sections[0]._sectPr
    tp = OxmlElement('w:titlePg')
    sectPr.append(tp)


title_page()
toc_page()

for bl in blocks:
    k = bl[0]
    if k == "h1":
        if bl[1] != "ВВЕДЕНИЕ":
            page_break()
        par(bl[1], align=WD_ALIGN_PARAGRAPH.CENTER if bl[1].isupper() else WD_ALIGN_PARAGRAPH.LEFT,
            indent=0 if bl[1].isupper() else 1.25, bold=True, keep=True)
        par("", spacing=1.0)
    elif k == "h2":
        par("", spacing=1.0)
        par(bl[1], align=WD_ALIGN_PARAGRAPH.LEFT, indent=1.25, bold=True, keep=True)
    elif k == "h3":
        par(bl[1], align=WD_ALIGN_PARAGRAPH.LEFT, indent=1.25, bold=True, keep=True)
    elif k == "p":
        par(bl[1])
    elif k == "li":
        par(bl[1])
    elif k == "list":
        for x in bl[1]:
            par(x)
    elif k == "lit":
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(1.25)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run(bl[1])
    elif k == "tbl":
        add_table(bl[1], bl[2])
    elif k == "tbl-land":
        add_table(bl[1], bl[2], landscape_font=True, total_cm=26.0)
    elif k == "fig":
        add_figure(bl[1], bl[2])
    elif k == "app":
        if len(bl) > 3 and bl[3]:
            ns = doc.add_section(WD_SECTION.NEW_PAGE)
            ns.orientation = WD_ORIENT.LANDSCAPE
            ns.page_width, ns.page_height = Cm(29.7), Cm(21.0)
            ns.top_margin, ns.bottom_margin = Cm(2.0), Cm(2.0)
            ns.left_margin, ns.right_margin = Cm(2.0), Cm(1.0)
        else:
            page_break()
        par(bl[1], align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, bold=True, spacing=1.0)
        par("", spacing=1.0)
        par(bl[2], align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, spacing=1.0)
        par("", spacing=1.0)

page_numbers()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)

words = sum(len(b[1].split()) for b in blocks if b[0] in ("p", "li", "lit"))
print("сохранено:", OUT)
print("блоков:", len(blocks), "| слов в тексте:", words, "| оценка страниц:", int(page))
print("источников:", n0 + len(C2.EXTRA_LIT))
