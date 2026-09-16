# -*- coding: utf-8 -*-
"""Генерация чёрно-белых схем для НИР Полыги (стиль graphviz/ГОСТ)."""
import os
import html as H

OUT = r"C:/Users/iasti/AppData/Local/Temp/claude/C--Users-iasti--local-bin/f248cfb0-7747-4b8f-bcb4-0e1888feec3c/scratchpad/fig"
os.makedirs(OUT, exist_ok=True)

FONT = "'Times New Roman', Times, serif"


def esc(s):
    return H.escape(s)


def box(x, y, w, h, lines, size=22, bold=False, fill="#ffffff", dash=None, lw=1.6, anchor_lines=None):
    """Прямоугольник с центрированным многострочным текстом."""
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    out = ['<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="#000" stroke-width="%g"%s/>'
           % (x, y, w, h, fill, lw, d)]
    n = len(lines)
    lh = size * 1.25
    y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
    for i, ln in enumerate(lines):
        fw = 'bold' if (bold and i == 0) else 'normal'
        out.append('<text x="%g" y="%g" font-family="%s" font-size="%g" font-weight="%s" '
                   'text-anchor="middle" fill="#000">%s</text>'
                   % (x + w / 2, y0 + i * lh, FONT, size, fw, esc(ln)))
    return "\n".join(out)


def text(x, y, s, size=22, anchor="middle", bold=False, italic=False):
    st = ' font-style="italic"' if italic else ''
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" font-weight="%s" '
            'text-anchor="%s" fill="#000"%s>%s</text>'
            % (x, y, FONT, size, 'bold' if bold else 'normal', anchor, st, esc(s)))


def line(x1, y1, x2, y2, dash=None, lw=1.6):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#000" stroke-width="%g"%s/>' % (x1, y1, x2, y2, lw, d)


def arrow(x1, y1, x2, y2, lw=1.6, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="#000" stroke-width="%g"%s '
            'marker-end="url(#ah)"/>' % (x1, y1, x2, y2, lw, d))


def path(dd, lw=1.6, arrowhead=True, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    m = ' marker-end="url(#ah)"' if arrowhead else ''
    return '<path d="%s" fill="none" stroke="#000" stroke-width="%g"%s%s/>' % (dd, lw, d, m)


def svg(w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#000"/></marker></defs>'
            '<rect width="100%%" height="100%%" fill="#fff"/>%s</svg>' % (w, h, w, h, body))


def write(name, w, h, body):
    doc = ('<!doctype html><html><head><meta charset="utf-8">'
           '<style>html,body{margin:0;padding:0;background:#fff}</style></head>'
           '<body>%s</body></html>' % svg(w, h, body))
    p = os.path.join(OUT, name + ".html")
    open(p, "w", encoding="utf-8").write(doc)
    print(name, w, h)
    return p


# ---------------------------------------------------------------- рисунок 1
def fig1():
    W, Hh = 1680, 1000
    b = []
    # реестр образов
    b.append(box(640, 30, 400, 90, ["Реестр образов контейнеров", "(внешний или внутрикластерный)"], bold=True))
    b.append(path("M 640 75 C 460 75, 380 90, 300 195", dash="8 6"))
    b.append(text(430, 60, "Г4: кластер – реестр образов", size=21))

    # рабочие нагрузки
    b.append(box(40, 200, 520, 470, [], fill="#f7f7f7"))
    b.append(text(300, 240, "Рабочие нагрузки", size=24, bold=True))
    b.append(box(65, 265, 225, 175, ["Пространство", "имён A", "", "под, контейнеры,", "сервисный аккаунт"], size=20))
    b.append(box(310, 265, 225, 175, ["Пространство", "имён B", "", "под, контейнеры,", "сервисный аккаунт"], size=20))
    b.append(line(300, 255, 300, 450, dash="8 6"))
    b.append(text(300, 470, "Г3: пространство имён – пространство имён", size=19))
    b.append(box(65, 490, 470, 70, ["Привязки ролей RBAC и маркеры", "доступа сервисных аккаунтов"], size=19))
    b.append(box(65, 580, 470, 70, ["Манифесты развёртывания:", "параметры изоляции контейнера"], size=19))

    # граница Г1
    b.append(line(600, 190, 600, 690, dash="8 6", lw=2))
    b.append(text(600, 720, "Г1: контейнер – узел", size=21))

    # узлы
    b.append(box(640, 200, 440, 470, [], fill="#f7f7f7"))
    b.append(text(860, 240, "Вычислительные узлы", size=24, bold=True))
    b.append(box(665, 265, 390, 70, ["Агент узла kubelet"], size=20))
    b.append(box(665, 350, 390, 70, ["Среда исполнения контейнеров"], size=20))
    b.append(box(665, 435, 390, 70, ["Сетевой агент kube-proxy"], size=20))
    b.append(box(665, 520, 390, 130, ["Ядро и файловая система узла:", "пространства имён, контрольные группы,", "сокет среды исполнения"], size=20))

    # граница Г2
    b.append(line(1120, 190, 1120, 690, dash="8 6", lw=2))
    b.append(text(1120, 720, "Г2: узел – плоскость управления", size=21))

    # плоскость управления
    b.append(box(1160, 200, 480, 470, [], fill="#f7f7f7"))
    b.append(text(1400, 240, "Плоскость управления", size=24, bold=True))
    b.append(box(1185, 265, 430, 70, ["Сервер программных интерфейсов", ], size=20))
    b.append(box(1185, 350, 430, 70, ["Хранилище состояния etcd"], size=20))
    b.append(box(1185, 435, 430, 70, ["Планировщик kube-scheduler"], size=20))
    b.append(box(1185, 520, 430, 70, ["Менеджер контроллеров"], size=20))
    b.append(box(1185, 605, 430, 45, ["Контроллеры допуска нагрузок"], size=20))

    # стрелка расширения полномочий
    b.append(arrow(80, 810, 1600, 810, lw=3))
    b.append(text(840, 790, "Направление расширения полномочий нарушителя", size=23, bold=True))
    b.append(text(840, 850, "компрометация контейнерного приложения → права на узле → управление кластером", size=21, italic=True))
    b.append(text(840, 920, "Условные обозначения: Г1…Г4 – границы доверия объекта защиты", size=20))
    write("fig1", W, Hh, "\n".join(b))


# ---------------------------------------------------------------- рисунок 2
def fig2():
    W, Hh = 1760, 1260
    b = []
    rcy = Hh / 2
    b.append(box(40, rcy - 60, 300, 120, ["Недостатки", "конфигурации", "кластера"], bold=True, fill="#efefef"))
    groups = [
        ("Недостатки рабочих\nнагрузок", ["привилегированный режим пода",
                                          "монтирование каталогов узла",
                                          "пространства имён узла",
                                          "исполнение от суперпользователя"]),
        ("Недостатки сервисных\nаккаунтов и ролей", ["автомонтирование маркера доступа",
                                                     "привязка роли уровня кластера",
                                                     "права на чтение секретов",
                                                     "права на создание нагрузок"]),
        ("Недостатки плоскости\nуправления", ["анонимный доступ к API-серверу",
                                              "неполнота журналирования",
                                              "секреты без шифрования в etcd",
                                              "отсутствие политик допуска"]),
        ("Недостатки\nвычислительных узлов", ["доступный сокет среды исполнения",
                                              "неаутентифицированный kubelet",
                                              "отключённые модули безопасности ядра",
                                              "нет ограничений системных вызовов"]),
        ("Недостатки реестра\nобразов", ["произвольные внешние реестры",
                                         "отсутствие проверки подписи",
                                         "изменяемые теги образов",
                                         "нет контроля состава образа"]),
    ]
    gx, gw = 430, 330
    lx, lw_ = 820, 900
    y = 40
    rows = []
    for title, items in groups:
        hh = 46 * len(items) + 18
        rows.append((y, hh, title, items))
        y += hh + 46
    total = y - 46
    off = (Hh - total) / 2
    for y0, hh, title, items in rows:
        yy = y0 + off
        b.append(box(gx, yy + hh / 2 - 55, gw, 110, title.split("\n"), size=21, fill="#f7f7f7"))
        b.append(path("M 340 %g C 390 %g, 390 %g, %g %g" % (rcy, rcy, yy + hh / 2, gx, yy + hh / 2)))
        for i, it in enumerate(items):
            iy = yy + 9 + i * 46
            b.append(box(lx, iy, lw_, 38, [it], size=20))
            b.append(path("M %g %g C %g %g, %g %g, %g %g"
                          % (gx + gw, yy + hh / 2, gx + gw + 60, yy + hh / 2, lx - 60, iy + 19, lx, iy + 19)))
    write("fig2", W, Hh, "\n".join(b))


# ---------------------------------------------------------------- рисунок 3
def fig3():
    W, Hh = 1820, 1500
    b = []
    rcy = (Hh - 60) / 2
    b.append(box(40, rcy - 70, 300, 140, ["Системообразующее", "событие:", "компрометация", "контейнерного", "приложения"], size=21, bold=True, fill="#efefef"))
    threats = [
        ("У1. Выход за границы\nконтейнера", [
            "Р1.1 получение прав на узле через\nпривилегированную рабочую нагрузку",
            "Р1.2 доступ к файловой системе узла\nчерез примонтированный каталог",
            "Р1.3 управление контейнерами узла\nчерез сокет среды исполнения"]),
        ("У2. Компрометация узла\nи перемещение в кластере", [
            "Р2.1 извлечение секретов иных\nнагрузок того же узла",
            "Р2.2 доступ к сетевому окружению узла",
            "Р2.3 размещение посторонней нагрузки\nпри отсутствии политик допуска"]),
        ("У3. Компрометация\nплоскости управления", [
            "Р3.1 обращение к API-серверу с избы-\nточными полномочиями аккаунта",
            "Р3.2 чтение конфиденциальных\nпараметров кластера",
            "Р3.3 доступ к содержимому etcd –\nполному состоянию кластера"]),
        ("У4. Нарушение доступности\nи сокрытие следов", [
            "Р4.1 исчерпание вычислительных\nресурсов узла",
            "Р4.2 невозможность расследования\nпри неполноте журналирования",
            "Р4.3 сохранение присутствия через\nподменённый образ в реестре"]),
    ]
    tx, tw = 420, 330
    rx, rw = 830, 640
    fy, fw = 1540, 250
    y = 30
    rows = []
    for t, rs in threats:
        hh = 100 * len(rs)
        rows.append((y, hh, t, rs))
        y += hh + 40
    total = y - 40
    off = (Hh - 80 - total) / 2
    fh = 120
    finals = [("Утрата\nконфиденциальности\nинформации", rcy - 420),
              ("Нарушение\nцелостности\nинформации", rcy - fh / 2),
              ("Нарушение\nдоступности\nинформации", rcy + 360)]
    for name, fyy in finals:
        b.append(box(fy, fyy, fw, fh, name.split("\n"), size=21, fill="#f7f7f7"))
    # какому последствию соответствует каждый риск группы (индексы finals)
    linkmap = [[1, 0, 1], [0, 0, 1], [0, 0, 0], [2, 2, 1]]
    for gi, (y0, hh, t, rs) in enumerate(rows):
        yy = y0 + off
        cy = yy + hh / 2
        b.append(box(tx, cy - 60, tw, 120, t.split("\n"), size=21, bold=True))
        b.append(path("M 340 %g C 380 %g, 380 %g, %g %g" % (rcy, rcy, cy, tx, cy)))
        for i, r in enumerate(rs):
            ry = yy + i * 100
            b.append(box(rx, ry, rw, 82, r.split("\n"), size=20))
            b.append(path("M %g %g C %g %g, %g %g, %g %g"
                          % (tx + tw, cy, tx + tw + 50, cy, rx - 50, ry + 41, rx, ry + 41)))
            tgt = finals[linkmap[gi][i]]
            b.append(path("M %g %g C %g %g, %g %g, %g %g"
                          % (rx + rw, ry + 41, rx + rw + 40, ry + 41, fy - 40, tgt[1] + fh / 2, fy, tgt[1] + fh / 2), lw=1.0))
    b.append(text(910, Hh - 25, "Дуга означает, что реализация нижележащего события создаёт возможность наступления вышележащего", size=20, italic=True))
    write("fig3", W, Hh, "\n".join(b))


# ---------------------------------------------------------------- рисунок 4
def fig4():
    W, Hh = 1700, 980
    b = []
    nodes = {
        "wl": (60, 400, 300, 120, ["A1. Рабочая нагрузка", "(контейнерное", "приложение)"]),
        "sa": (60, 120, 300, 110, ["A2. Сервисный аккаунт", "рабочей нагрузки"]),
        "node": (500, 400, 300, 120, ["A3. Вычислительный", "узел", "(среда исполнения)"]),
        "ns": (500, 700, 300, 110, ["A4. Смежные нагрузки", "узла и их секреты"]),
        "api": (950, 260, 300, 120, ["A5. Сервер", "программных", "интерфейсов"]),
        "etcd": (1350, 120, 290, 110, ["A6. Хранилище", "состояния etcd"]),
        "reg": (950, 640, 300, 120, ["A7. Реестр", "образов", "контейнеров"]),
        "all": (1350, 430, 290, 140, ["A8. Все приложения", "и данные,", "обслуживаемые", "кластером"]),
    }
    for k, (x, y, w, h, lines) in nodes.items():
        fill = "#efefef" if k in ("all", "etcd") else "#ffffff"
        b.append(box(x, y, w, h, lines, size=21, fill=fill, bold=True))

    def c(k, side):
        x, y, w, h, _ = nodes[k]
        return {"r": (x + w, y + h / 2), "l": (x, y + h / 2), "t": (x + w / 2, y), "b": (x + w / 2, y + h)}[side]

    edges = [
        ("wl", "r", "node", "l", "T1611 Escape to Host"),
        ("wl", "t", "sa", "b", "T1552.007 Container API"),
        ("sa", "r", "api", "l", "T1078 Valid Accounts"),
        ("node", "b", "ns", "t", "T1609 Container Admin"),
        ("node", "r", "api", "l", "T1613 Discovery"),
        ("api", "r", "etcd", "l", "T1552 Unsecured Creds"),
        ("api", "b", "reg", "t", "T1610 Deploy Container"),
        ("reg", "r", "all", "l", "T1525 Implant Image"),
        ("etcd", "b", "all", "t", "полное состояние кластера"),
    ]
    for a, sa_, bb, sb, lab in edges:
        x1, y1 = c(a, sa_)
        x2, y2 = c(bb, sb)
        b.append(arrow(x1, y1, x2, y2))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 12
        b.append('<rect x="%g" y="%g" width="%g" height="26" fill="#fff" stroke="none"/>'
                 % (mx - len(lab) * 5.0, my - 18, len(lab) * 10.0))
        b.append(text(mx, my, lab, size=19))
    b.append(text(850, 900, "Путь в графе от A1 к A8 образует сценарий компрометации; дуги размечены техниками MITRE ATT&CK for Containers", size=21, italic=True))
    write("fig4", W, Hh, "\n".join(b))


# ---------------------------------------------------------------- рисунок 5
def fig5():
    W, Hh = 1500, 900
    b = []
    data = [("С1", 0.72), ("С2", 0.63), ("С3", 0.54), ("С4", 0.45), ("С5", 0.38),
            ("С6", 0.30), ("С7", 0.24), ("С8", 0.18), ("С9", 0.12), ("С10", 0.08)]
    x0, y0 = 170, 720
    plot_w, plot_h = 1200, 560
    # оси
    b.append(line(x0, y0, x0 + plot_w, y0, lw=2))
    b.append(line(x0, y0, x0, y0 - plot_h, lw=2))
    for i in range(0, 9):
        v = i * 0.1
        yy = y0 - v / 0.8 * plot_h
        b.append(line(x0 - 10, yy, x0 + plot_w, yy, dash="4 8", lw=0.8))
        b.append(text(x0 - 22, yy + 8, ("%.1f" % v).replace(".", ","), size=21, anchor="end"))
    bw = plot_w / len(data) * 0.56
    step = plot_w / len(data)
    hatches = ["#111111", "#555555", "#999999"]
    for i, (name, v) in enumerate(data):
        hgt = v / 0.8 * plot_h
        cx = x0 + step * (i + 0.5)
        lvl = 0 if v >= 0.5 else (1 if v >= 0.25 else 2)
        b.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="#000" stroke-width="1.4"/>'
                 % (cx - bw / 2, y0 - hgt, bw, hgt, hatches[lvl]))
        b.append(text(cx, y0 - hgt - 14, ("%.2f" % v).replace(".", ","), size=21))
        b.append(text(cx, y0 + 34, name, size=22))
    b.append(text(x0 + plot_w / 2, y0 + 80, "Сценарии компрометации кластера", size=23))
    b.append('<text x="60" y="%g" font-family="%s" font-size="23" text-anchor="middle" fill="#000" '
             'transform="rotate(-90 60 %g)">Мера риска R</text>' % (y0 - plot_h / 2, FONT, y0 - plot_h / 2))
    # легенда
    lg = [("критический уровень (R ≥ 0,50)", hatches[0]), ("высокий уровень (0,25 ≤ R &lt; 0,50)", hatches[1]),
          ("средний и низкий уровень (R &lt; 0,25)", hatches[2])]
    ly = 90
    for i, (lab, col) in enumerate(lg):
        yy = ly + i * 44
        b.append('<rect x="980" y="%g" width="36" height="26" fill="%s" stroke="#000" stroke-width="1.2"/>' % (yy, col))
        b.append('<text x="1030" y="%g" font-family="%s" font-size="21" fill="#000">%s</text>' % (yy + 21, FONT, lab))
    write("fig5", W, Hh, "\n".join(b))


fig1()
fig2()
fig3()
fig4()
fig5()
