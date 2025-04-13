# RimTUB

![Static Badge](https://img.shields.io/badge/UserBot%20for%20-Telegram-blue)
![Static Badge](https://img.shields.io/badge/Works%20on%20-%20Windows%2C%20Linux%2C%20macOS%2C%20MavisHost-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-GPLv3-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/RimTUB/RimTUB/total?color=magenta)
![GitHub Release](https://img.shields.io/github/v/release/RimTUB/RimTUB)
![GitHub last commit](https://img.shields.io/github/last-commit/RimTUB/RimTUB)


**RimTUB** — это мощный, удобный, а главное, бесплатный юзербот для Telegram, который можно настроить под себя. Всё, что нужно, уже есть в коде, а если хочется чего-то нового — качай модули!

> 🤖 ЮзерБоты — это скрипты, которые работают от лица твоего личного Telegram-аккаунта. Они могут делать всё, что может обычный пользователь.
>
> 😀 Например, можно сделать автоответчик, который сам будет реагировать на определённые сообщения.
>
> ✅ Обычно ЮБ используют как расширение Telegram — встроенный калькулятор, быстрый переводчик, автодобавление людей в чаты и т.д. Наверняка ты уже встречал такие штуки. Например, кто-то пишет `.calc 2+2`, и сообщение превращается в `4`.

---

## 🌟 Особенности RimTUB

- **Модульность** — функционал можно легко расширять модулями. Пиши свои или ставь чужие.
- **Удобство** — всё просто: скачал, настроил YAML-файл и запустил.
- **Гибкость** — хочешь изменить поведение Telegram? Вперед! Модули позволяют реализовать что угодно.
- **Кроссплатформенность** — работает на Windows, Linux и даже Termux (Android).
- **Открытый исходный код** — и лицензия GPLv3.

## 🔗 Наш сайт: [rimtub.pp.ua](https://rimtub.pp.ua)

Тут можно:
- Узнать больше о RimTUB
- Скачать или опубликовать модули
- Почитать статьи
- Получить помощь

---

## 🧠 Полезные команды "из коробки"

- `.me` — инфа о текущем юзерботе.
- `.ping` — проверка задержки.
- `.restart` — перезапуск бота.
- `.calc <выражение>` — калькулятор.
- `.tr <язык> <текст/ответ>` — переводчик.
- `.dml <ссылка>` — установка модуля по ссылке.
- `.dmf <реплай на файл>` — установка модуля с файла.
- `.help` — список всех команд.

---

## ⚙ Установка

<details>
<summary><strong>Windows</strong></summary>

1. Скачай последнюю версию с [GitHub Releases](https://github.com/RimTUB/RimTUB/releases)
2. Распакуй архив в папку, например, `C:\RimTUB`
3. Создай бота в [@BotFather](https://t.me/BotFather), включи Inline Mode
4. Настрой `config/config.yaml`:
   ```yaml
   phones:
     - "+380XXXXXXXXX"
   bot_token: "123456:ABC-DEF..."
   ```
5. Установи Python 3.11 с [python.org](https://www.python.org/)
6. Открой CMD:
   ```sh
   cd C:\RimTUB
   python -m venv .venv
   .venv\Scripts\activate.bat
   pip install -r requirements.txt
   python main.py
   ```
7. Введи код из Telegram и (если есть) пароль

</details>

<details>
<summary><strong>Linux</strong></summary>

1. Установи зависимости:
   ```sh
   sudo apt update
   sudo apt install git python3.11 python3.11-venv -y
   ```
2. Клонируй репозиторий:
   ```sh
   git clone https://github.com/RimTUB/RimTUB
   cd RimTUB
   ```
3. Настрой `config.yaml`:
   ```yaml
   phones:
     - "+380XXXXXXXXX"
   bot_token: "123456:ABC-DEF..."
   ```
4. Создай и активируй окружение:
   ```sh
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```
5. Установи зависимости и запусти:
   ```sh
   pip install -r requirements.txt
   python main.py
   ```

</details>

<details>
<summary><strong>Termux (Android)</strong></summary>

1. Установи Termux из F-Droid
2. Установи зависимости:
   ```sh
   pkg install git python -y
   git clone https://github.com/RimTUB/RimTUB
   cd RimTUB
   ```
3. Настрой конфиг:
   ```sh
   nano config.yaml
   ```
4. Установи библиотеки:
   ```sh
   pip install -r requirements.txt
   ```
5. Запускай:
   ```sh
   python main.py
   ```

</details>

---

## ❓ FAQ

- **Можно ли на телефон?**  
  > Да! Просто ставь через Termux.

- **Если не могу запустить на своём устройстве?**  
  > Пиши [@RimMirK](https://t.me/RimMirK), он может помочь с хостингом.

- **Можно заказать модуль?**  
  > Да, тоже пиши [@RimMirK](https://t.me/RimMirK)

- **Хочу добавить модуль на сайт**  
  > Без проблем, напиши [@RimMirK](https://t.me/RimMirK)

- **Обновления?**  
  > Планируются алиасы команд, динамический префикс, улучшения безопасности и т.п.

---

## 💬 Контакты

**Разработчик**: [@RimMirK](https://t.me/RimMirK)  
**Телеграм Канал**: [@RimTUB](https://t.me/RimTUB)
**Телеграм Чат**: [@RimTUB_chat](https://t.me/RimTUB_chat)

---
