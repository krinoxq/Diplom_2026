---
name: doc-pdf-toolchain
description: Чем на этой машине читать docx и pdf и как делать PDF — poppler и LibreOffice не установлены
metadata: 
  node_type: memory
  type: reference
  originSessionId: 55e3ff99-b897-49b9-adc3-cd3f70bfc47a
  modified: 2026-09-06T15:16:20.246Z
---

На машине **нет** poppler/pdftotext, LibreOffice и node, поэтому встроенный рендер PDF в Read не работает («pdftoppm is not installed»).

Что работает:
- **docx** — это zip: распаковать `word/document.xml`, заменить `</w:p>` на перевод строки, снять теги регуляркой, прогнать через unescape. Файл, открытый в Word, залочен — сначала копировать во временный каталог.
- **pdf → текст** — `python -m pip install pypdf`, затем `PdfReader(...).pages[i].extract_text()`. Python 3.14 есть в WindowsApps.
- **html → pdf** — headless Chrome: `"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=20000 --print-to-pdf="out.pdf" "file:///..."`. Edge лежит рядом и умеет то же. Шрифты Google Fonts подгружаются и вшиваются в PDF, кириллица нормальная.

Вывод кириллицы в Bash-инструменте ломается в mojibake — писать в файл и читать через Read, либо ставить `PYTHONIOENCODING=utf-8`. В PowerShell помогает `[Console]::OutputEncoding=[System.Text.Encoding]::UTF8`.

**Why:** без этого каждый раз уходит несколько попыток на подбор рабочего способа, а часть инструментов молча выдаёт нечитаемый результат.

**How to apply:** для печатной версии артефакта делать отдельный файл с `<!doctype html>`, `<meta charset="utf-8">`, `data-theme="light"` на корне и блоком `@media print`, иначе страница уедет в тёмную тему и порвёт таблицы.
