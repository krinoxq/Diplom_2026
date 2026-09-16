---
name: ssh-hosts-mobaxterm
description: MobaXterm Home Edition режет число сессий (~14); рабочий путь к 85 хостам — ssh config + автодополнение в PowerShell
metadata:
  type: project
---

Список из 85 SSH-хостов (рабочие: hh, sunpbx, selectel, cprt.su, megafon и т.д.)
лежит в `C:\Users\iasti\.ssh\config` — 14.09.2026 туда перенесён файл `config (2)`
с рабочего стола (бэкап прежнего: `config.bak-20260914-001128`, в нём остались
`vpn_now`, `sunpbx`, `8800_97` и vps1-3 на внутренних 172.16.15.36-38).

**MobaXterm 26.1 Home Edition отображает не больше ~14 сохранённых сессий.**
Именно поэтому у пользователя «сессии иногда не запоминались, надо было вводить
заново». Обход через раскладку по 10 папкам (≤12 в каждой) НЕ сработал: папки
видны, содержимое пустое. Файл `MobaXterm.ini` при этом на диске целый — режет
GUI по лицензии, а не парсер. Снимать ограничение он просил — отказано.

**Why:** повторно диагностировать этот лимит дорого, а выглядит он как баг.

**How to apply:** не предлагать MobaXterm-сессии как способ хранить много хостов.
Рабочие пути: `ssh <имя>` в локальном терминале MobaXterm (его `$HOME/.ssh/config`
= `AppData\Roaming\MobaXterm\home\.ssh\config`, ключ подаёт встроенный MobAgent)
или PowerShell с профилем `OneDrive\Документы\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`
(Register-ArgumentCompleter для ssh/scp/sftp + Tab → MenuComplete; требует
ExecutionPolicy RemoteSigned для CurrentUser — ставил сам пользователь, мне
эту команду блокирует классификатор).
Записи `systeme123/124` в config нерабочие: `#` в имени хоста ssh читает как
начало комментария.
