<div align="center">

# NfGram

**An advanced, high-performance Telegram client fork with enhanced privacy, battery optimizations, authentic exteraGram personalization, and a powerful Python plugin engine.**

[![Telegram Version](https://img.shields.io/badge/Telegram-12.10.6-2b2b2b.svg?style=flat-square)](https://telegram.org)
[![Android Version](https://img.shields.io/badge/Android-8.0+--15+-2b2b2b.svg?style=flat-square)](https://www.android.com)
[![Architecture](https://img.shields.io/badge/Arch-arm64--v8a%20%7C%20armeabi--v7a-2b2b2b.svg?style=flat-square)]()
[![Release](https://img.shields.io/badge/Release-12.10.6-2b2b2b.svg?style=flat-square)]()
[![License](https://img.shields.io/badge/License-GPL--3.0-2b2b2b.svg?style=flat-square)](LICENSE)

[Overview](#overview) • [Fork Notice](#fork-notice) • [Key Features](#key-features) • [Compatibility](#compatibility) • [Building from Source](#building-from-source) • [License & Attribution](#license--attribution) • [Русская версия](#русская-версия)

</div>

---

## Overview

**NfGram** is a feature-rich, high-performance open-source client fork built on the foundation of **AyuGram** and **Telegram for Android**, incorporating custom modifications, visual aesthetics from **exteraGram**, and cutting-edge client enhancements.

NfGram bridges the gap between maximum messaging speed, uncompromising privacy, and seamless modern Android integration. It introduces multi-threaded parallel uploads, aggressive zero-overhead battery optimizations, an authentic exteraGram settings hub, and an error-resilient Python plugin runtime powered by Chaquopy.

---

## Fork Notice

> [!IMPORTANT]
> **NfGram is an independent open-source fork of [AyuGram](https://github.com/AyuGram/AyuGramAndroid) and [Telegram for Android](https://github.com/DrKLO/Telegram), incorporating visual and functional components from [exteraGram](https://github.com/exteraSquad/exteraGram).**
> - This project is distributed under the terms of the **GNU General Public License v3.0 (GNU GPLv3)**.
> - NfGram is **not** an official release of Telegram FZ-LLC, the AyuGram development team, or exteraSquad.
> - Modifications, parallel uploads, battery optimizations, Python plugin runtime fixes, and custom enhancements are developed and maintained by **NothingFlare**.
> - Inquiries, bug reports, and pull requests relating to this fork should be submitted directly to this repository.

---

## Key Features

- **High-Speed Parallel Upload Engine (`ParallelDispatchQueue`)**
  - Dynamic multi-threaded work pool streaming media concurrently across cores, saturating modern high-bandwidth connections.
  - Capped at 4 concurrent streams to prevent CPU pinning, out-of-memory errors, and device overheating while charging.

- **Intelligent Proximity & Ear Sensor Optimization**
  - Calibrated ear sensor proximity threshold from 5.0cm to 2.0cm, preventing accidental triggers when hands or shadows pass over the display.
  - Raised vertical tilt verification threshold from 14° to 35° (5.5 m/s²), ensuring earpiece mode and voice playback only activate when deliberately raised to the ear.

- **Thermal & Fast-Charging Overheating Protection**
  - Controlled parallel upload queues preventing 100% CPU utilization and battery thermal runaway during fast charging.
  - Neutralized 0ms deadline `KeepAliveJob` background churn, eliminating constant wakeups.
  - Optimized hardware acceleration and rendering profile preventing Mali GPU driver hangs and thermal crashes (`CEM`).

- **Error-Resilient Python Plugin Runtime (Chaquopy Engine)**
  - Enhanced plugin lifecycle management preventing disappearance upon toggling master switch.
  - Cython dynamic import path caching ensuring seamless hot-reloading of custom plugins.
  - Safe-mode recovery and strict Dalvik/ART bytecode verification compatibility.

- **Aggressive Battery & Resource Optimizations**
  - **Sensors & Polling**: Neutralized background orientation/ambient sensor polling when unnecessary, eliminating battery drain in idle states.
  - **GPU Shader Overhead**: Disabled heavy real-time GPU chat blurs (`canBlurChat`, `chatBlurEnabled`, `useNewBlur`), saving graphics pipeline cycles and battery temperature.
  - **Alarm Wakeups**: Replaced aggressive RTC wakeup alarms with passive non-wakeup timers (15m batching), significantly reducing deep-sleep wake locks.
  - **System Power Saver Sync**: `powerSaverFollowSystem` enabled by default to immediately honor Android battery saver modes.
  - **Logging Elimination**: Fully suppressed verbose internal logging (`LOGS_ENABLED = false`) to reduce unnecessary flash I/O cycles.

- **Authentic exteraGram Personalization Hub**
  - Fully redesigned settings hub reflecting authentic exteraGram aesthetics.
  - Dedicated hub with custom brand vectors, authentic color palette (`#ffe83030`), and streamlined navigation.
  - Custom category headers, distinct icons, and direct access to both AyuGram privacy features and exteraGram modifications.

- **Resilient Python Plugin Engine**
  - Embedded Chaquopy runtime with lazy on-demand SDK initialization (zero impact on cold app launch times).
  - Robust module resolution: automatically injects plugin directories into `sys.path` so third-party dependencies load seamlessly.
  - Crash-proof metadata parsing: prevents malformed plugin packages from crashing the client or triggering bootloops.
  - Fully functional toggle switches with real-time UI state synchronization and clean lifecycle management (`init` / `shutdown`).

- **Ghost Mode & Message History (Inherited from AyuGram)**
  - View deleted and edited messages with full revision history.
  - Send without read marks, conceal online status, and prevent typing indicators.
  - Screenshot protection bypass in secret chats and restricted media channels.

---

## Compatibility

| Environment | Supported Versions | Details |
| :--- | :--- | :--- |
| **Android OS** | Android 8.0 (API 26) – Android 15+ (API 35+) | Full support for modern Android runtimes, ART JIT, and dynamic permission models |
| **Architectures** | `arm64-v8a`, `armeabi-v7a` | Native binaries optimized with NEON vectorization |
| **Security** | Passcode, Biometric Fingerprint, Device PIN | Cryptographic KeyStore & hardware keystore |
| **Python Engine**| Python 3.8 – 3.11 (Chaquopy) | Sandboxed plugin runtime with isolated module import caches |

---

## Building from Source

### Prerequisites
- **JDK 17** or **JDK 21**
- **Android SDK & NDK** (API 34/35, NDK r23+)
- **Python 3.8+** (for pipeline build tools and DEX patching)
- **Git**

### 1. Build via Gradle
```bash
git clone https://github.com/NothingFlare/NfGram.git
cd NfGram
./gradlew assembleRelease --no-daemon
```

### 2. Standalone Release Build & Sign Pipeline
To produce a fully patched, zipaligned, and signed universal APK using the integrated tooling:
```bash
python Tools/build_nfgram.py
```
The resulting signed universal APK will be created at:
```text
NfGram-12.10.6-universal.apk
```

---

## License & Attribution

NfGram is licensed under the **GNU General Public License v3.0 (GNU GPLv3)**.

- **Original Telegram Project**:  
  Copyright (C) 2013–2024 Nikolai Kudashov, Telegram FZ-LLC  
  Repository: [https://github.com/DrKLO/Telegram](https://github.com/DrKLO/Telegram)

- **AyuGram Project**:  
  Copyright (C) 2023–2024 Radolyn  
  Repository: [https://github.com/AyuGram/AyuGramAndroid](https://github.com/AyuGram/AyuGramAndroid)

- **exteraGram Project**:  
  Copyright (C) 2021–2024 exteraSquad  
  Repository: [https://github.com/exteraSquad/exteraGram](https://github.com/exteraSquad/exteraGram)

- **NfGram Modifications & Additions**:  
  Copyright (C) 2026 NothingFlare  
  Licensed under GNU GPLv3.

For full license terms and conditions, refer to the [LICENSE](LICENSE) file.

---

# Русская версия

<div align="center">

# NfGram

**Продвинутый высокопроизводительный форк Telegram с усиленной приватностью, оптимизацией батареи, аутентичным меню exteraGram и встроенным движком Python-плагинов.**

[![Версия Telegram](https://img.shields.io/badge/Telegram-12.10.6-2b2b2b.svg?style=flat-square)](https://telegram.org)
[![Версия Android](https://img.shields.io/badge/Android-8.0+--15+-2b2b2b.svg?style=flat-square)](https://www.android.com)
[![Архитектура](https://img.shields.io/badge/Arch-arm64--v8a%20%7C%20armeabi--v7a-2b2b2b.svg?style=flat-square)]()
[![Релиз](https://img.shields.io/badge/Release-12.10.6-2b2b2b.svg?style=flat-square)]()
[![Лицензия](https://img.shields.io/badge/License-GPL--3.0-2b2b2b.svg?style=flat-square)](LICENSE)

[Обзор](#обзор) • [Уведомление о форке](#уведомление-о-форке) • [Ключевые особенности](#ключевые-особенности) • [Совместимость](#совместимость) • [Сборка из исходников](#сборка-из-исходников) • [Лицензия и авторство](#лицензия-и-авторство)

</div>

---

## Обзор

**NfGram** — это модифицированный клиент с открытым исходным кодом, созданный на базе **AyuGram** и официального клиента **Telegram для Android**, объединяющий передовые наработки **exteraGram** и авторские улучшения производительности.

Проект создан для пользователей, которым необходима бескомпромиссная скорость работы, надёжная защита приватности и гибкая кастомизация с поддержкой расширений на Python.

---

## Уведомление о форке

> [!IMPORTANT]
> **NfGram является независимым форком проектов [AyuGram](https://github.com/AyuGram/AyuGramAndroid) и [Telegram для Android](https://github.com/DrKLO/Telegram) с включением элементов из [exteraGram](https://github.com/exteraSquad/exteraGram).**
> - Проект распространяется на условиях лицензии **GNU General Public License v3.0 (GNU GPLv3)**.
> - NfGram **не** является официальным продуктом Telegram FZ-LLC, команды разработчиков AyuGram или exteraSquad.
> - Модификации, многопоточная загрузка, оптимизация энергопотребления и доработки движка разработаны и поддерживаются разработчиком **NothingFlare**.
> - Все вопросы, сообщения об ошибках и предложения направляются непосредственно в данный репозиторий.

---

## Ключевые особенности

- **Высокоскоростная параллельная загрузка (`ParallelDispatchQueue`)**
  - Многопоточный пул передачи файлов, оптимизированный для максимальной пропускной способности.
  - Ограничение до 4 параллельных потоков для предотвращения перегрузки процессора и перегрева при зарядке.

- **Интеллектуальная калибровка датчика приближения к уху**
  - Порог срабатывания датчика приближения откалиброван с 5.0 см до 2.0 см — устранены ложные срабатывания при свайпах, движениях пальцев и падении тени.
  - Минимальный угол вертикального наклона увеличен с 14° до 35° (5.5 м/с²), гарантируя включение голосового динамика только при реальном поднесении смартфона к уху.

- **Защита от перегрева и вылетов при зарядке**
  - Оптимизация параллельных сетевых потоков, предотвращающая троттлинг и перегрев аккумулятора во время быстрой зарядки.
  - Полное отключение цикличного фонового сервиса `KeepAliveJob` (устранена постоянная нагрузка на планировщик задач).
  - Сбалансированный профиль аппаратного рендеринга — предотвращает сбои видеодрайвера Mali и принудительное закрытие клиента системой при нагреве.

- **Стабильный движок плагинов Python (Chaquopy Engine)**
  - Устранена проблема исчезновения плагинов при отключении и последующем включении главного переключателя.
  - Автоматическое кэширование путей импорта Cython для надёжной горячей перезагрузки модулей.
  - Устранены ошибки верификации Dalvik/ART при инициализации базовых классов плагинов.

- **Глубокая оптимизация энергопотребления и батареи**
  - **Датчики и сенсоры**: Отключен фоновый поллинг гироскопа и ориентации при отсутствии необходимости, предотвращая фоновый разряд аккумулятора.
  - **Снижение нагрузки на GPU**: Отключены ресурсоёмкие шейдеры размытия в чатах (`canBlurChat`, `chatBlurEnabled`, `useNewBlur`), что значительно снижает нагрев устройства и нагрузку на видеочип.
  - **Энергосберегающие таймеры**: Агрессивные RTC-будильники заменены на пакетные неразбуждающие интервалы (15 минут), что позволяет устройству спокойно уходить в глубокий сон (Deep Sleep).
  - **Следование энергосбережению системы**: Опция `powerSaverFollowSystem` включена по умолчанию.
  - **Устранение фонового логирования**: Отключены избыточные циклы записи системных логов на флеш-память (`LOGS_ENABLED = false`).

- **Аутентичный хаб настроек exteraGram**
  - Полностью воссозданный интерфейс настроек с фирменным оформлением.
  - Оригинальная цветовая палитра (`#ffe83030`), раздельные плашки категорий, кастомные векторные иконки.
  - Прямой и удобный доступ к настройкам приватности AyuGram и функционалу exteraGram в одном месте.

- **Отказоустойчивый движок Python-плагинов**
  - Ленивая загрузка среды Chaquopy — SDK инициализируется по требованию, не замедляя холодный старт Telegram.
  - Автоматическое добавление родительских директорий плагинов в `sys.path` для корректного импорта сторонних модулей.
  - Защита от сбоев: парсер метаданных плагинов не крашит клиент при синтаксических ошибках в манифесте плагина.
  - Корректная работа переключателей: состояние тумблеров синхронизируется с интерфейсом, плагины корректно включаются и отключаются на лету.

- **Призрак и история сообщений (из AyuGram)**
  - Чтение удалённых сообщений и просмотр полной истории правок.
  - Режим призрака: скрытие статуса «онлайн», отсутствие отметок о прочтении и индикаторов набора текста.
  - Обход запрета на создание скриншотов в защищённых чатах.

---

## Совместимость

| Платформа | Поддерживаемые версии | Описание |
| :--- | :--- | :--- |
| **Android OS** | Android 8.0 (API 26) – Android 15+ (API 35+) | Полная поддержка современного рантайма ART JIT и динамических разрешений |
| **Архитектуры** | `arm64-v8a`, `armeabi-v7a` | Оптимизированные нативные библиотеки с поддержкой NEON |
| **Безопасность** | Код-пароль, отпечаток пальца, PIN устройства | Защищённое хранилище Android KeyStore |
| **Python** | Python 3.8 – 3.11 (Chaquopy) | Изолированная среда выполнения плагинов с кэшированием импортов |

---

## Сборка из исходников

### Требования
- **JDK 17** или **JDK 21**
- **Android SDK & NDK** (API 34/35, NDK r23+)
- **Python 3.8+** (для скриптов сборки и патчинга DEX)
- **Git**

### 1. Сборка через Gradle
```bash
git clone https://github.com/NothingFlare/NfGram.git
cd NfGram
./gradlew assembleRelease --no-daemon
```

### 2. Сборка готового подписанного универсального APK
Для сборки через автоматизированный пайплайн с выравниванием (zipalign) и подписью:
```bash
python Tools/build_nfgram.py
```
Собранный и подписанный файл появится в корне и на рабочем столе:
```text
NfGram-12.10.6-universal.apk
```

---

## Лицензия и авторство

NfGram распространяется под свободной лицензией **GNU General Public License v3.0 (GNU GPLv3)**.

- **Оригинальный проект Telegram**:  
  Copyright (C) 2013–2024 Nikolai Kudashov, Telegram FZ-LLC  
  Репозиторий: [https://github.com/DrKLO/Telegram](https://github.com/DrKLO/Telegram)

- **Проект AyuGram**:  
  Copyright (C) 2023–2024 Radolyn  
  Репозиторий: [https://github.com/AyuGram/AyuGramAndroid](https://github.com/AyuGram/AyuGramAndroid)

- **Проект exteraGram**:  
  Copyright (C) 2021–2024 exteraSquad  
  Репозиторий: [https://github.com/exteraSquad/exteraGram](https://github.com/exteraSquad/exteraGram)

- **Модификации и дополнения NfGram**:  
  Copyright (C) 2026 NothingFlare  
  Лицензировано под GNU GPLv3.

Полный текст лицензии доступен в файле [LICENSE](LICENSE).
