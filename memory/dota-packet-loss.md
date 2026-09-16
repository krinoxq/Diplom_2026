---
name: dota-packet-loss
description: "Потери пакетов в Dota 2 (2-3 с, вход и исход): весь трафик идёт через sing-box+xray и WinDivert"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3faaf6a9-4719-48cb-9277-58432dc388b4
  modified: 2026-08-28T19:48:51.467Z
---

Заявлено 2026-08-28. Симптом: в оверлее статистики Доты вспышки потерь по исходящим
и входящим, длительностью 2-3 секунды. Пользователь подозревает провайдера.
Отдельная проблема от [[pc-freeze-diagnosis]], не путать.

**Два слоя софта, через которые проходит каждый игровой пакет (оба подтверждены конфигами):**

1. Happ / sing-box, `%LOCALAPPDATA%\Happ\config.json`: tun `happ-tun` c `auto_route: true`,
   `strict_route: true`, **`"final": "proxy"`**, direct-правила только для самих
   xray/sing-box/antifilter. Выход — SOCKS5 на `127.0.0.1:10808`, то есть xray.exe.
   Цепочка на каждый пакет: игра -> tun -> sing-box -> SOCKS5 -> xray -> Realtek.
   Гео-правила (`routing.json`, профиль RoscomVPN, `directSites` включает geosite:steam)
   применяет xray, но объезда userspace они не дают.
   Проверка: `Find-NetRoute -RemoteIPAddress 1.1.1.1` отдаёт ifIndex туннеля,
   а `tracert -d 8.8.8.8` отвечает за 1 хоп — туннель подделывает ICMP.
   **Пока Happ включён, любые внешние пинги/трассы бессмысленны.**

2. zapret ALT11 + `C:\zapret\utils\game_filter.enabled` = `all`, отчего
   `GameFilterTCP/UDP` = `1024-65535` и строка запуска winws.exe становится
   `--wf-tcp=...,1024-65535 --wf-udp=443,19294-19344,50000-50100,1024-65535`.
   WinDivert утаскивает в userspace практически весь трафик машины в обе стороны.
   При этом игровые правила desync привязаны к `lists/ipset-all.txt`, где лежит
   только заглушка `203.0.113.113/32` — то есть **накладные расходы есть, пользы ноль**.
   Discord прикрыт отдельно диапазонами 19294-19344 и 50000-50100, они от game filter
   не зависят.

Найдено попутно: в автозапуске uTorrent и uTorrent Web (в момент проверки не работали),
у MSI.CentralServer 835 UDP-сокетов. NIC чист: 0 discards и 0 errors, до роутера
0 % потерь. У Realtek включены EEE, Green Ethernet, Gigabit Lite, Power Saving Mode,
Flow Control Rx&Tx; на Ethernet висит NDIS-фильтр VBoxNetLwf.

Инструмент: `C:\Users\iasti\.local\bin\net-logger.ps1` (+ `start-net-logger.cmd`).
Пингует раз в секунду параллельно роутер, WAN-хоп и опорный IP, пишет CSV и находит
вспышки потерь от 2 с; в строке отмечает, работали ли winws/sing-box/xray/торрент.
Сам определяет туннель на маршруте и предупреждает, что мерить бессмысленно.
Логи → `%USERPROFILE%\Desktop\net-log`.

Порядок разбора: потери до роутера — кабель/NIC; чисто до роутера, но есть до WAN-хопа —
провайдер; везде чисто, а Дота потери рисует — виноват софтовый слой (туннель/WinDivert).

**Применено 2026-08-28 с согласия пользователя** (проверено, линк 1 Гбит, 0 потерь до роутера):
удалён `C:\zapret\utils\game_filter.enabled` (был `all`); на Realtek выключены
`*EEE`, `EnableGreenEthernet`, `GigaLite`, `PowerSavingMode`, `*FlowControl` (был 3);
отвязан `oracle_VBoxNetLwf`; убраны из HKCU Run записи `ut` и `utweb`.

**Частично откачено 2026-09-13:** `oracle_VBoxNetLwf` снова включён на Realtek (`Ethernet`).
Без него VirtualBox не видит ни одного адаптера для «Сетевого моста» — поле «Имя»
остаётся пустым и ВМ не сохраняется. Доказанной вины за фильтром нет, вернули сознательно.
Если потери в Доте возобновятся — это подозреваемый №1 после туннеля:
`Disable-NetAdapterBinding -Name Ethernet -ComponentID oracle_VBoxNetLwf` (нужен админ).
Остальные правки (EEE, GreenEthernet, GigaLite, PowerSaving, FlowControl, game_filter,
автозапуск торрентов) в силе.
Откат целиком: `%USERPROFILE%\Desktop\net-log\rollback\rollback-net-fixes.ps1`
(рядом `nic-settings.bak`, `game_filter.enabled.bak`, `utorrent-autostart.bak`,
`apply-net-fixes.log` с исходными значениями).
Оговорка: winws.exe читает game_filter при старте, поэтому до перезапуска
`general (ALT11).bat` в памяти живёт старая команда с диапазоном 1024-65535.

**Happ намеренно не трогали** — это решение пользователя, пользоваться ли VPN,
а не настройка. Туннель остаётся главным неподтверждённым подозреваемым.

Следующий шаг: катка с выключенными Happ и zapret при запущенном
`start-net-logger.cmd` — чистая линия. Если на ней потерь нет, а с включённым Happ
возвращаются, виноват туннель. Данных с net-logger пока нет ни одной сессии.
