# RimTUB - RimMirK's Telegram User Bot

![Banner]()

<a href="https://www.youtube.com/watch?v=nybtOIxlku8"><img alt="Made in Ukraine" src="https://img.shields.io/badge/Ukraine-blue?style=for-the-badge&label=Made%20in&labelColor=yellow&link=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DnybtOIxlku8" height="50px" algin="center"></a>


![UserBot for Telegram](https://img.shields.io/badge/UserBot%20for%20-Telegram-blue)
![Works on Windows, Linux, macOS, MavisHost](https://img.shields.io/badge/Works%20on%20-%20Windows%2C%20Linux%2C%20macOS%2C%20MavisHost-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-GPLv3-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/RimTUB/RimTUB/total?color=magenta)
![GitHub Release](https://img.shields.io/github/v/release/RimTUB/RimTUB)
![GitHub last commit](https://img.shields.io/github/last-commit/RimTUB/RimTUB)
<a href="https://RimTUB.pp.ua">
![RimTUB.pp.ua Website Temporarily Unavailable](https://img.shields.io/badge/RimTUB.pp.ua%20-%20Temporarily%20Unavailable-yellow)</a>
<a href="https://docs.RimTUB.pp.ua">
![Website](https://img.shields.io/website?url=https%3A%2F%2Fdocs.RimTUB.pp.ua&up_message=works!&down_message=doesn't%20work%28&label=docs.RimTUB.pp.ua)
</a>



---

## Версия на русском тут -> [тык](README.ru.md)

**RimTUB** — is a powerful and convenient open-source Telegram userbot that's easy to adapt to your needs. Everything necessary is already built-in, and extending its capabilities only requires installing the modules you need. Simple to launch, flexible in configuration, and completely under your control — RimTUB is created to do more with less effort.

> 🤖 UserBots are scripts that work on behalf of your personal Telegram account. They can do everything a regular user can do.
>
> 😀 For example, you can create an auto-responder that will automatically react to specific messages.
>
> ✅ Usually, UserBots are used as Telegram extensions — a built-in calculator, quick translator, auto-adding people to chats, etc. You've probably already encountered such things. For instance, someone writes `.calc 2+2`, and the message transforms into `4`.

---

## 🌟 Why RimTUB is the best choice

- **Modularity** — extend functionality according to your wishes. Write your own modules or use ready-made ones.
- **Convenience** — everything is intuitive: download, configure, run.
- **Flexibility** — want to change Telegram's behavior? Modules allow you to implement **anything**!
- **Multi-account** — connect multiple Telegram accounts and manage them without issues, everything works smoothly.
- **Cross-platform** — works on Windows, Linux, macOS, and even Android (Termux).
- **Easy deployment on hosting** — our partner [**MavisHost**](https://t.me/MavisHostNews/28) allows you to launch RimTUB in just a few clicks, without the need to configure servers.
- **Open source** — with GPLv3 license.

## 🔗 Our website: [RimTUB.pp.ua](https://rimtub.pp.ua)

Here you can:
- Learn more about RimTUB
- Download modules
- Read articles

---

## 🧠 Useful "out of the box" commands

- `.me` — info about the userbot (version, uptime, etc.).
- `.help` — help on userbot.
- `.ping` — ping test.
- `.restart` — restart the userbot.
- `.calc <expression>` — calculator.
- `.tr <language> <text/reply/quote>` — translator.
- `.dml <link>` — install module from link (from website, for example).
- `.dmf <reply to file>` — install module from file.

---

## ⚙ Installation

<details>
<summary><strong>Windows</strong></summary>

<a id="Windows"></a>

### 🔹 Step 1. Download RimTUB
1. Go to: [GitHub Releases](https://github.com/RimTUB/RimTUB/releases)  
2. Click on the item with the `Latest` badge (this is the latest version).
3. Below, click on assets (file list)
4. In the file list, find an archive named like `RimTUB-XXX.zip` (XXX is the userbot version) — click on it to download.  
5. When it's downloaded — open the folder with the file, right-click on the archive and select **"Extract All"**.  
6. Enter a path, for example: `C:\RimTUB`, and click **"Extract"**.

---

### 🔹 Step 2. Create a Telegram bot
1. Open Telegram and find user [@BotFather](https://t.me/BotFather).  
2. Click **Start** or type `/start` if the bot is silent.  
3. Type `/newbot`, set a name and link for the bot (for example, `RimTUB_nickname_bot`).  
4. BotFather will send you a long **token** — **copy it** (it looks like `123456:ABC-DEF...`).  
5. Type `/setinline`, select your bot, and type any text, for example `asdfjwekjdsf`

---

### 🔹 Step 3. Configure RimTUB
1. Go to the `C:\RimTUB` folder that you just unpacked.  
2. Find the `config.yaml` file there.  
3. Open it with a double click. If nothing happens — right-click and select **"Open with → Notepad"**.  
4. Insert your data there. Example:
   ```yaml
   PHONES:
     - +12345678990 # Your phone number linked to Telegram
     - +380XXXXXXXX # You can add multiple accounts
   BOT_TOKEN: 123456:ABC-DEF...  # Token provided by BotFather
   ```
5. Save the file: **File → Save**.

---

### 🔹 Step 4. Install Python
1. Go to [python.org](https://www.python.org/).  
2. Hover over "Downloads" and select **Windows**.  
3. Click **"Download Python 3.11.9"**. 
4. When the installer downloads — **MAKE SURE to check "Add Python to PATH"**, then click **"Install Now"**.  
5. Wait for the installation to complete and close the window.

---

### 🔹 Step 5. Launch RimTUB
1. Press **Win + R** keys, a window will appear.  
2. Type `cmd` and press **Enter** — a black window will open (command prompt).  
3. Enter the following commands one by one (press **Enter** after each):

   ```sh
   cd C:\RimTUB
   python -m venv .venv
   .venv\Scripts\activate.bat
   pip install -r requirements.txt
   python main.py
   ```

   ⚠ If a window appears asking for permission to access the internet — click **"Allow"**.

---

### 🔹 Step 6. Confirm login
1. After launching, the bot will ask you to enter a code.  
2. Telegram will send you an SMS — enter this code in the console.  
3. If you have two-factor authentication enabled (password when logging into Telegram) — enter it as well.
You'll only need to do this once

---

🎉 Done! RimTUB is running! Hooray!


</details>

<details>
<summary><strong>Linux</strong></summary>

<a id="Linux"></a>

### 🔹 Step 1. Install necessary dependencies
1. Open terminal.
2. Enter the following command to update packages and install dependencies:
   ```sh
   sudo apt update
   sudo apt install git python3.11 python3.11-venv -y
   ```

---

### 🔹 Step 2. Clone the RimTUB repository
1. In terminal, enter the command:
   ```sh
   git clone https://github.com/RimTUB/RimTUB
   ```

---

### 🔹 Step 3. Create a Telegram bot
1. Open Telegram and find user [@BotFather](https://t.me/BotFather).  
2. Click **Start** or type `/start` if the bot is silent.  
3. Type `/newbot`, set a name and link for the bot (for example, `RimTUB_nickname_bot`).  
4. BotFather will send you a long **token** — **copy it** (it looks like `123456:ABC-DEF...`).  
5. Type `/setinline`, select your bot, and type any text, for example `asdfjwekjdsf`.

---

### 🔹 Step 4. Configure RimTUB
1. In terminal, navigate to the folder where you just cloned RimTUB:
   ```sh
   cd RimTUB
   ```
2. Open the configuration file `config.yaml` using a text editor, for example, `nano`:
   ```sh
   nano config.yaml
   ```
3. Insert your data there. Example:
   ```yaml
   PHONES:
     - +12345678990 # Your phone number linked to Telegram
     - +380XXXXXXXX # You can add multiple accounts
   
   BOT_TOKEN: 123456:ABC-DEF...  # Token provided by BotFather
   ```
4. To save the file in `nano`, press **Ctrl + S** to save. Then exit by pressing **Ctrl + X**.

---

### 🔹 Step 5. Create and activate a virtual environment
1. Enter the command to create a virtual environment:
   ```sh
   python3.11 -m venv .venv
   ```
2. Activate the virtual environment:
   ```sh
   source .venv/bin/activate
   ```

---

### 🔹 Step 6. Install dependencies and launch RimTUB
1. Install all necessary libraries:
   ```sh
   pip install -r requirements.txt
   ```
2. Launch RimTUB:
   ```sh
   python main.py
   ```

---

### 🔹 Step 7. Confirm login
1. After launching, the bot will ask you to enter a code.
2. Telegram will send you an SMS — enter this code in the console.
3. If you have two-factor authentication enabled (password when logging into Telegram) — enter it as well. You'll only need to do this once.

---

🎉 Done! RimTUB is working on your Linux! Hooray!

</details>

<details>
<summary><strong>macOS</strong></summary>

<a id="macOS"></a>

### 🔹 Step 1. Install necessary dependencies
1. Open **Terminal**.
2. Enter the command to install `Homebrew` (if it's not installed):
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   Follow the instructions in the terminal to complete the installation.
   
3. Install Python 3.11 and Git through Homebrew:
   ```sh
   brew install git python@3.11
   ```

---

### 🔹 Step 2. Clone the RimTUB repository
1. Enter the command to clone the repository:
   ```sh
   git clone https://github.com/RimTUB/RimTUB
   ```

---

### 🔹 Step 3. Create a Telegram bot
1. Open Telegram and find user [@BotFather](https://t.me/BotFather).  
2. Click **Start** or type `/start` if the bot is silent.  
3. Type `/newbot`, set a name and link for the bot (for example, `RimTUB_nickname_bot`).  
4. BotFather will send you a long **token** — **copy it** (it looks like `123456:ABC-DEF...`).  
5. Type `/setinline`, select your bot, and type any text, for example `asdfjwekjdsf`.

---

### 🔹 Step 4. Configure RimTUB
1. In terminal, navigate to the project folder:
   ```sh
   cd RimTUB
   ```
2. Open the configuration file `config.yaml` using a text editor, for example, `nano`:
   ```sh
   nano config.yaml
   ```
3. Insert your data. Example:
   ```yaml
   PHONES:
     - +12345678990 # Your phone number linked to Telegram
     - +380XXXXXXXX # You can add multiple accounts
   BOT_TOKEN: 123456:ABC-DEF...  # Token provided by BotFather
   ```
4. To save the file in `nano`, press **Ctrl + O**, then **Enter** to confirm. After that, exit by pressing **Ctrl + X**.

---

### 🔹 Step 5. Create and activate a virtual environment
1. Enter the command to create a virtual environment:
   ```sh
   python3.11 -m venv .venv
   ```
2. Activate the virtual environment:
   ```sh
   source .venv/bin/activate
   ```

---

### 🔹 Step 6. Install dependencies and launch RimTUB
1. Install all necessary libraries:
   ```sh
   pip install -r requirements.txt
   ```
2. Launch RimTUB:
   ```sh
   python main.py
   ```

---

### 🔹 Step 7. Confirm login
1. After launching, the bot will ask you to enter a code.
2. Telegram will send you an SMS — enter this code in the console.
3. If you have two-factor authentication enabled (password when logging into Telegram) — enter it as well. You'll only need to do this once.

---

🎉 Done! RimTUB is working on your Mac! Hooray!

</details>


<details>
<summary><strong>UserLAnd (Android)</strong></summary>

<a id="UserLAnd"></a>

### 🔹 Step 1. Install UserLAnd
1. Go to [Play Marker](https://play.google.com/store/apps/details?id=tech.ula) and download **UserLAnd**.
2. Install it on your device.

---

### 🔹 Step 2. Download Python and RimTUB
1. Open **UserLAnd**.
2. Chose **Debian Termial only**
3. In Terminal run following commands: (It will take up to 40 minutes)
```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y wget build-essential libssl-dev zlib1g-dev \
libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev \
tk-dev uuid-dev libffi-dev

cd /tmp
wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz
tar -xvf Python-3.11.9.tgz
cd Python-3.11.9

./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall

sudo ln -sf /usr/local/bin/python3.11 /usr/bin/python
sudo ln -sf /usr/local/bin/python3.11 /usr/bin/python3
sudo ln -sf /usr/local/bin/python3.11 /usr/bin/py
sudo ln -sf /usr/local/bin/python3.11 /usr/bin/py3

py -m ensurepip

sudo ln -sf /usr/local/bin/pip3.11 /usr/bin/pip
sudo ln -sf /usr/local/bin/pip3.11 /usr/bin/pip3

cd ..
cd ..

sudo apt install -y git
sudo apt install -y nano

git clone https://github.com/RimTUB/RimTUB

cd RimTUB

py -m venv .venv

source .venv/bin/activate

sudo pip install -r requirements.txt

```

---

### 🔹 Step 3. Create a Telegram bot
1. Open Telegram and find user [@BotFather](https://t.me/BotFather).  
2. Click **Start** or type `/start` if the bot is silent.  
3. Type `/newbot`, set a name and link for the bot (for example, `RimTUB_nickname_bot`).  
4. BotFather will send you a long **token** — **copy it** (it looks like `123456:ABC-DEF...`).  
5. Type `/setinline`, select your bot, and type any text, for example `asdfjwekjdsf`.

---

### 🔹 Step 4. Configure RimTUB
1. Open the configuration file `config.yaml` using a text editor, for example, `nano`:
   ```sh
   nano config.yaml
   ```
2. Insert your data. Example:
   ```yaml
   PHONES:
     - +12345678990 # Your phone number linked to Telegram
     - +380XXXXXXXX # You can add multiple accounts
   BOT_TOKEN: 123456:ABC-DEF...  # Token provided by BotFather
   ```
3. To save the file in `nano`, press **Ctrl + S**. After that, exit by pressing **Ctrl + X**.

---

### 🔹 Step 5. Launch RimTUB
1. After all dependencies are installed, launch RimTUB:
   ```sh
   python main.py
   ```

---

### 🔹 Step 6. Confirm login
1. After launching, the bot will ask you to enter a code.
2. Telegram will send you an SMS — enter this code in the console.
3. If you have two-factor authentication enabled (password when logging into Telegram) — enter it as well. You'll only need to do this once.

---

🎉 Done! RimTUB is working on your phone! Hooray!

</details>


<details>
<summary><strong>Termux (Android)</strong></summary>

<a id="Termux"></a>

### 🔹 Step 1. Install Termux
1. Go to [F-Droid](https://f-droid.org/packages/com.termux/) and download **Termux**.
2. Install it on your device.

---

### 🔹 Step 2. Clone the RimTUB repository
1. Open **Termux**.
2. Clone the RimTUB repository:
   ```sh
   git clone https://github.com/RimTUB/RimTUB
   ```

---

### 🔹 Step 3. Create a Telegram bot
1. Open Telegram and find user [@BotFather](https://t.me/BotFather).  
2. Click **Start** or type `/start` if the bot is silent.  
3. Type `/newbot`, set a name and link for the bot (for example, `RimTUB_nickname_bot`).  
4. BotFather will send you a long **token** — **copy it** (it looks like `123456:ABC-DEF...`).  
5. Type `/setinline`, select your bot, and type any text, for example `asdfjwekjdsf`.

---

### 🔹 Step 4. Configure RimTUB
1. In **Termux**, navigate to the project folder:
   ```sh
   cd RimTUB
   ```
2. Open the configuration file `config.yaml` using a text editor, for example, `nano`:
   ```sh
   nano config.yaml
   ```
3. Insert your data. Example:
   ```yaml
   PHONES:
     - +12345678990 # Your phone number linked to Telegram
     - +380XXXXXXXX # You can add multiple accounts
   BOT_TOKEN: 123456:ABC-DEF...  # Token provided by BotFather
   ```
4. To save the file in `nano`, press **Ctrl + O**, then **Enter** to confirm. After that, exit by pressing **Ctrl + X**.

---

### 🔹 Step 5. Run Termux.sh to install dependencies
1. In **Termux**, enter the command to execute the `termux.sh` script, which will install all necessary dependencies:
   ```sh
   bash termux.sh
   ```
2. Wait for the dependencies installation to complete.

---

### 🔹 Step 6. Launch RimTUB
1. After all dependencies are installed, launch RimTUB:
   ```sh
   python main.py
   ```

---

### 🔹 Step 7. Confirm login
1. After launching, the bot will ask you to enter a code.
2. Telegram will send you an SMS — enter this code in the console.
3. If you have two-factor authentication enabled (password when logging into Telegram) — enter it as well. You'll only need to do this once.

---

🎉 Done! RimTUB is working on your phone! Hooray!

</details>

---

## 📚 Module documentation: **[docs.rimtub.pp.ua](https://docs.rimtub.pp.ua)**

Here you'll find everything you need to write your own module for RimTUB:

- **Step-by-step instructions** on writing and module structure.
- **Complete description of available functions** and methods for working with RimTUB.
- **Code examples** that will help you quickly start development.

If you want to create your own cool modules, be sure to study the documentation. It has everything! And if you don't understand something, you can ask the developer for help (contacts below)

---

## ❓ FAQ

- **Can I run it on my phone?**  
  > Yes! Just install it through Termux.

- **What if I can't run it on my device?**  
  > Contact [@RimMirK](https://t.me/RimMirK), he can help with hosting.

- **Can I order a custom module?**  
  > Yes, also contact [@RimMirK](https://t.me/RimMirK)

- **I want to add a module to the website**  
  > No problem, write to [@RimMirK](https://t.me/RimMirK)


---

## 💬 Contacts and Links

- **Developer**: [@RimMirK](https://t.me/RimMirK) 
- **Telegram Channel**: [@RimTUB](https://t.me/RimTUB)
- **Telegram Chat**: [@RimTUB_chat](https://t.me/RimTUB_chat)
- **Official website**: [RimTUB.pp.ua](https://rimtub.pp.ua/)
- **Documentation**: [docs.RimTUB.pp.ua](https://docs.rimtub.pp.ua/)
- **Partner MavisHost**: [@MavisHostNews](https://t.me/MavisHostNews/28)

---
