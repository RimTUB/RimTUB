import hashlib
from traceback import format_exc, print_exc
from urllib.parse import urlparse
import requests
import shutil
import re
import os

from pyrogram.types import Message
from telebot.types import (
    CallbackQuery as C, 
    InlineQueryResultArticle as RArticle, InputTextMessageContent as TMC,
    InlineKeyboardMarkup as IM, InlineKeyboardButton as IB
)

from ..UserBot import build_module_help_text
from utils import *
from config import DMF_TIMEOUT, DML_TIMEOUT, CHECK_HASH_URL, DML_WHITELIST



helplist.add_module(
    Module(
        __package__,
        description="Ваш помощник модулей",
        author="built-in (@RimMirK)",
        version='2.1'
    ).add_command(
        Command(['dmf'], [Arg("ответ с <u>файлом</u> модуля")], "Скачать/обновить модуль")
    ).add_command(
        Command(['sm'], [Arg("Название модуля")], "Отправить модуль")
    ).add_command(
        Command(['delm'], [Arg("Название модуля")], "Удалить модуль")
    ).add_command(
        Command(['relm'], [Arg("Название модуля")], 'Перезагрузить модуль')
    ).add_command(
        Command(['offm', 'stopm'], [Arg("Название модуля")], 'Выключить модуль')
    ).add_command(
        Command(['onm', 'startm'], [Arg("Название модуля")], 'Включить модуль')
    )
)

def remove_emoji_tags(text):
    return re.sub(r'<emoji[^>]*>(.*?)<\/emoji>', r'\1', text)

async def download_anyway(app: Client, c: C, url):
    return await dml(app, None, lambda text: app.bot.edit_message_text(remove_emoji_tags(text), inline_message_id=c.inline_message_id), url, True)

async def download_anyway_dmf(app: Client, c: C, file_path, name):
    return await dmf(app, None, lambda text: app.bot.edit_message_text(remove_emoji_tags(text), inline_message_id=c.inline_message_id), file_path, name, True)


async def alert(app: Client, i, url):
    await app.bot.answer_inline_query(i.id, [RArticle(0, '.', TMC(
        b("⚠️ Внимание! Вы загружаете модуль с неофициального сайта. "
        "Это может быть небезопасно — файл может содержать вредоносный код или нежелательные программы. "
        "Загрузка и использование этого модуля могут представлять угрозу для безопасности ваших данных а также аккаунта Telegram. "
        "Убедитесь, что доверяете источнику перед загрузкой.", False), 'html'),
        reply_markup=IM().add(IB(('Все равно установить (небезопасно!)'), callback_data=format_callback(app, download_anyway, url=url)
    )))], cache_time=0)

async def alert_dmf_cant_check(app, i, file_path, name):
    await app.bot.answer_inline_query(i.id, [RArticle(0, '.', TMC(
        b("⚠️ Внимание! Не получилось проверить модуль на подлинность! "
        "Файл может содержать вредоносный код или нежелательные программы. "
        "Загрузка и использование этого модуля могут представлять угрозу для безопасности ваших данных а также аккаунта Telegram. "
        "Убедитесь, что доверяете источнику перед загрузкой.", False), 'html'),
        reply_markup=IM().add(IB(('Все равно установить (небезопасно!)'), callback_data=format_callback(app, download_anyway_dmf, file_path=file_path, name=name)
    )))], cache_time=0)

async def alert_dmf(app, i, file_path, name):
    await app.bot.answer_inline_query(i.id, [RArticle(0, '.', TMC(
        b("⚠️ Внимание! Данный модуль не найден на официальном сайте и не прошёл проверку на подлинность! "
        "Файл может содержать вредоносный код или нежелательные программы. "
        "Загрузка и использование этого модуля могут представлять угрозу для безопасности ваших данных а также аккаунта Telegram. "
        "Убедитесь, что доверяете источнику перед загрузкой.", False), 'html'),
        reply_markup=IM().add(IB(('Все равно установить (небезопасно!)'), callback_data=format_callback(app, download_anyway_dmf, file_path=file_path, name=name)
    )))], cache_time=0)

async def dml(app, msg, notify, url, no_alert=False):

    if not no_alert:
        if urlparse(url).netloc not in DML_WHITELIST:
            r = await app.get_inline_bot_results(app.bot_username, format_callback(app, alert, url=url))
            await msg.reply_inline_bot_result(r.query_id, "0", False)
            await msg.delete()
            return
    try:
        r = requests.get(url, stream=True, timeout=DML_TIMEOUT)
        if 'Content-Disposition' in r.headers:
            filename = r.headers['Content-Disposition'].split('filename=')[-1].strip('";')
        else:
            await notify("<emoji id='5240241223632954241'>🚫</emoji> Ошибка! Модуль не найден, либо поврежден!")
            return

        if not filename.endswith('.rimtub-module'):
            await notify("<emoji id='5240241223632954241'>🚫</emoji> Ошибка! Файл не является файлом модуля RimTUB!")
            return

        save_path = f'plugins/ModuleHelper/{filename}'
        with open(save_path, 'wb') as file:
            for chunk in r.iter_content(chunk_size=8192):
                file.write(chunk)

        unpack_module(save_path, f'plugins/{os.path.splitext(filename)[0]}/')
        os.remove(save_path)
        
        await app.load_module(os.path.splitext(filename)[0], restart=True, exception=True, all_clients=True)

        for client in clients:
            r = await client._start_on_ready(os.path.splitext(filename)[0])
            if r[0] == 'error':
                raise r[1]

        await notify(f"<emoji id=5206607081334906820>✅</emoji> Модуль <b>{os.path.splitext(filename)[0]}</b> успешно загружен и установлен!")

    except requests.exceptions.RequestException as e:
        await notify(
            b(f"<emoji id='5240241223632954241'>🚫</emoji> Произошла ошибка! {escape(e.__class__.__name__)}.\n", False)
            + f"Возможно ссылка на скачивание неверна либо содержит ошибку"
        )  
    except Exception as e:
        await notify(
            b(f"<emoji id='5240241223632954241'>🚫</emoji> Произошла ошибка: {escape(e.__class__.__name__)}:\n", False)
            + escape(e) + f"\n{await paste(format_exc())}"
        )

async def dmf(app: Client, msg, notify, file_path, name, no_alert=False):
    if not no_alert:
        with open(file_path, 'rb') as f:
            data = f.read()
        hash = hashlib.sha256(data).hexdigest()
        try:
            raise ... # this check does not work anyway
            r = requests.get(CHECK_HASH_URL.format(hash=hash), timeout=DMF_TIMEOUT)
        except Exception:
            r = await app.get_inline_bot_results(app.bot_username, format_callback(app, alert_dmf_cant_check, file_path=file_path, name=name))
            await msg.reply_inline_bot_result(r.query_id, "0", False)
            await msg.delete()
            return
        if not r.json()['exists']:
            r = await app.get_inline_bot_results(app.bot_username, format_callback(app, alert_dmf, file_path=file_path, name=name))
            await msg.reply_inline_bot_result(r.query_id, "0", False)
            await msg.delete()
            return 
        return
    try:
        isset = os.path.exists(f'plugins//{name}')
        unpack_module(file_path, f'plugins/{name}/')
        os.remove(file_path)
        await app.load_module(name, restart=isset, exception=True, all_clients=True)    

        for client in clients:
            r = await client._start_on_ready(name)
            if r[0] == 'error':
                raise r[1]

        try:
            cap = bq(
                build_module_help_text(
                    helplist.get_module(
                        name,
                    ), False
                ), True, False
            )
            
        except:
            cap = ''
        if isset:
            return await notify("<emoji id='5206607081334906820'>✅</emoji> Модуль обновлен и перезапущен!" + "\n\n" + cap)
        await notify(
            "<emoji id='5206607081334906820'>✅</emoji> Модуль загружен и запущен!" + "\n\n" + cap
        )
    except Exception as e:
        await notify(
            b(f"<emoji id='5240241223632954241'>🚫</emoji> Произошла ошибка!\n{await paste(format_exc())}", False)
        )


async def main(app: Client):

    cmd = app.cmd(app.get_group(__package__))

    @cmd(['dmf'])
    async def _dmf(_, msg: Message):
        try:
            if r:= msg.reply_to_message:
                if r.document:
                    if r.document.mime_type in ('application/zip') and r.document.file_name.endswith('.rimtub-module'):
                        pass
                    else:
                        return await msg.edit("<emoji id='5210952531676504517'>❌</emoji> Ошибка: Файл не является модулем!")
                else:
                    return await msg.edit("<emoji id='5210952531676504517'>❌</emoji> Ошибка: Ответь на сообщение с модулем!")
            else:
                return await msg.edit("<emoji id='5274099962655816924'>❗️</emoji> Ответь на сообщение!")
            await msg.edit(
                "<emoji id='5386367538735104399'>⌛</emoji> Загружаю..."
            )

            name = r.document.file_name.split(".", 1)[0]
            path = await r.download(f'plugins//ModuleHelper//{r.document.file_name}')
            await dmf(app, msg, msg.edit, path, name)
            
        except:
            await msg.edit(f'Не удалось загрузить модуль!\n{await paste(format_exc())}')
            raise

    @cmd(['dml'])
    async def _dml(_, msg: Message, url=None):
        try:
            url = msg.text.split(maxsplit=1)[1]
        except IndexError:
            await msg.edit("<emoji id='5447644880824181073'>⚠️</emoji> Вставь ссылку!")
            return

        return await dml(app, msg, msg.edit, url, False)
        


    @cmd(['sm'])
    async def _sm(_, msg: Message):
        try:
            _, name = msg.text.split(maxsplit=1)
        except ValueError:
            return await msg.edit("<emoji id='5274099962655816924'>❗️</emoji> Напиши название модуля!")

        module_path = find_directory(name, 'plugins', 1)

        if not module_path:
            return await msg.edit("<emoji id='5447644880824181073'>⚠️</emoji> Такой модуль не найден!")

        cap = f"❗️Модуль ТОЛЬКО на @RimTUB версии 2.0 и выше❗️\n\n"
        try:
            cap += bq(
                build_module_help_text(helplist.get_module(name.lower(), lower=True), False),
                True, False
            )
        except: pass

        try:
            module_file = pack_module(module_path, f'plugins/ModuleHelper/{os.path.split(module_path)[-1]}.rimtub-module')
        except:
            print_exc()
            return await msg.edit(f"Упс! Не получилось запаковать модуль!\n{await paste(format_exc())}")

        try:
            await msg.reply_document(module_file, caption=cap)
            await msg.delete()
        except:
            await msg.edit(f"<emoji id='5260293700088511294'>⛔️</emoji> Произошла неизвестная ошибка!\n{await paste(format_exc())}")
        finally:
            os.remove(module_file)
            
    @cmd('delm')
    async def _delm(app, msg):
        try:
            _, name = msg.text.split(maxsplit=1)
        except ValueError:
            return await msg.edit("<emoji id='5274099962655816924'>❗️</emoji> Напиши название модуля!")
        
        module_path = find_directory(name, 'plugins', 1)
        if not module_path:
            return await msg.edit("<emoji id='5447644880824181073'>⚠️</emoji> Такой модуль не найден!")
        
        shutil.rmtree(module_path)
        await app.stop_module(os.path.split(module_path)[-1], unload_help=True, all_clients=True)

        await msg.edit(
            f"<emoji id='5445267414562389170'>🗑</emoji> Модуль {b(os.path.split(module_path)[-1])} удален!"
        )


    @cmd('relm')
    async def _relm(app: Client, msg):
        module_name = msg.text.split(maxsplit=1)[1]
        try:
            module_path = find_directory(module_name, 'plugins', 1)
            if not module_path:
                return await msg.edit("<emoji id='5447644880824181073'>⚠️</emoji> Такой модуль не найден!")
            name = os.path.basename(module_path)
            await app.load_module(name, restart=True, exception=True, all_clients=True)

            for client in clients:
                r = await client._start_on_ready(name)
                if r[0] == 'error':
                    raise r[1]

        except Exception as e:
            await msg.edit(f'Не удалось перезагрузить модуль!\n{await paste(format_exc())}')
            
        else:
            await msg.edit(f"<emoji id='5206607081334906820'>✅</emoji> Модуль {b(os.path.basename(module_path))} перезагружен!")

    @cmd(['offm', 'stopm'])
    async def _offm(app: Client, msg):
        module_name = msg.text.split(maxsplit=1)[1]
        try:
            module_path = find_directory(module_name, 'plugins', 1)
            if not module_path:
                return await msg.edit("<emoji id='5447644880824181073'>⚠️</emoji> Такой модуль не найден!")
            name = os.path.split(module_path)[-1]

            disabled_modules = await app.db.get('core.modules', 'disabled_modules', [])
            if name not in disabled_modules:
                await app.stop_module(name)
                disabled_modules.append(name)
                await app.db.set('core.modules', 'disabled_modules', disabled_modules)
        except Exception as e:
            await msg.edit(f'Не удалось выключить модуль!\n{await paste(format_exc())}')
        else:
            await msg.edit(f"<emoji id='5206607081334906820'>✅</emoji> Модуль {b(name)} выключен!")


    @cmd(['onm', 'startm'])
    async def _onm(app: Client, msg):
        module_name = msg.text.split(maxsplit=1)[1]
        try:
            module_path = find_directory(module_name, 'plugins', 1)
            if not module_path:
                return await msg.edit("<emoji id='5447644880824181073'>⚠️</emoji> Такой модуль не найден!")
            name = os.path.split(module_path)[-1]

            
            disabled_modules: list = await app.db.get('core.modules', 'disabled_modules', [])
            if name in disabled_modules:
                await app.load_module(name, restart=False, exception=True)
                disabled_modules.remove(name)
                await app.db.set('core.modules', 'disabled_modules', disabled_modules)

        except Exception as e:
            await msg.edit(f'Не удалось включить модуль!\n{await paste(format_exc())}')
            print_exc(e.__traceback__)
        else:
            await msg.edit(f"<emoji id='5206607081334906820'>✅</emoji> Модуль {b(name)} включен!")

    @cmd(['offms'])
    async def _offms(app: Client, msg):
        disabled_modules = await app.db.get('core.modules', 'disabled_modules', [])
        if not disabled_modules:
            t = 'Нет выключенных модулей!'
        else:
            t = f'Выключенные модули: {",  ".join(map(code, disabled_modules))}'
        await msg.edit(t + f"\n\nЧтобы выключить модуль используй {code(PREFIX+'offm')}\xa0[Название\xa0модуля].\n"
                       f"Чтобы включить: {code(PREFIX+'onm')}\xa0[Название\xa0модуля]")