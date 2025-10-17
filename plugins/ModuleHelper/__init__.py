import hashlib
from pathlib import Path
from traceback import format_exc
from urllib.parse import urlparse
import requests
import shutil
import re
import os

from ..UserBot import build_module_help_text
from utils import *
from utils import M as Message


async def dml(app, mod: Module, msg, notify, url, no_alert=False):
    
    plugins = get_root(True) / 'plugins'

    if not no_alert:
        if urlparse(url).netloc not in Config.DML_WHITELIST:
            buttons = Buttons(
                [
                    [
                        Button("Все равно установить (небезопасно!)", callback_data='download_anyway', extra_data={'url': url})
                    ]
                ], general_extra_data={'msg': msg}
            )
            await mod.send_buttons(
                msg.chat.id,
                b("⚠️ Внимание! Вы загружаете модуль с неофициального сайта. "
                "Это может быть небезопасно — файл может содержать вредоносный код или нежелательные программы. "
                "Загрузка и использование этого модуля могут представлять угрозу для "
                "безопасности ваших данных а также аккаунта Telegram. "
                "Убедитесь, что доверяете источнику перед загрузкой.", False),
                buttons=buttons, message_thread_id=msg.message_thread_id
            )
            await msg.delete()
            return
    try:
        r = requests.get(url, stream=True, timeout=Config.DML_TIMEOUT)
        if 'Content-Disposition' in r.headers:
            filename = r.headers['Content-Disposition'].split('filename=')[-1].strip('";')
        else:
            await notify(f"{emoji(5240241223632954241, '🚫')} Ошибка! Модуль не найден, либо поврежден!")
            return

        if not filename.endswith('.rimtub-module'):
            await notify(f"{emoji(5240241223632954241, '🚫')} Ошибка! Файл не является файлом модуля RimTUB!")
            return

        save_path = plugins / 'ModuleHelper' / filename
        with open(save_path, 'wb') as file:
            for chunk in r.iter_content(chunk_size=8192):
                file.write(chunk)

        unpack_module(save_path, plugins / os.path.splitext(filename)[0])
        os.remove(save_path)
        
        await app.load_module(os.path.splitext(filename)[0], restart=True, exception=True, all_clients=True)

        for client in clients:
            r = await client._start_on_ready(os.path.splitext(filename)[0])
            if r[0] == 'error':
                raise r[1]

        await notify(f"{emoji(5206607081334906820, '✅')} Модуль {b(os.path.splitext(filename)[0])} успешно загружен и установлен!")

    except requests.exceptions.RequestException as e:
        await notify(
            b(f"{emoji(5240241223632954241, '🚫')} Произошла ошибка! {escape(e.__class__.__name__)}.\n", False)
            + f"Возможно ссылка на скачивание неверна либо содержит ошибку"
        )  
    except Exception as e:
        await notify(
            b(f"{emoji(5240241223632954241, '🚫')} Произошла ошибка: {escape(e.__class__.__name__)}:\n", False)
            + escape(e) + f"\n{await paste(format_exc())}"
        )
        mod.logger.error('dml error', exc_info=True)

async def dmf(app: Client, mod: Module, msg, notify, file_path, name, no_alert=False, no_alert_version=False):
    if not no_alert:
        with open(file_path, 'rb') as f:
            data = f.read()
        hash = hashlib.sha256(data).hexdigest()
        try:
            raise ... # this check does not work anyway
            r = requests.get(CHECK_HASH_URL.format(hash=hash), timeout=DMF_TIMEOUT)
        except Exception:
            buttons = Buttons(
                [
                    [
                        Button(
                            "Все равно установить (небезопасно!)",
                            callback_data='download_anyway_dmf',
                            extra_data={
                                'file_path': file_path,
                                'name': name
                            }
                        )
                    ]
                ], general_extra_data={'msg': msg}
            )
            await mod.send_buttons(
                msg.chat.id,
                b("⚠️ Внимание! Не удалось проверить модуль на подлинность! "
                "Это может быть небезопасно — файл может содержать вредоносный код или нежелательные программы. "
                "Загрузка и использование этого модуля могут представлять угрозу для "
                "безопасности ваших данных а также аккаунта Telegram. "
                "Убедитесь, что доверяете источнику перед загрузкой.", False),
                buttons=buttons, message_thread_id=msg.message_thread_id,
                reply_to_message_id=msg.reply_to_message_id if msg else None
            )
            await msg.delete()
            return
        
        if not r.json()['exists']:
            buttons = Buttons(
                [
                    [
                        Button(
                            "Все равно установить (небезопасно!)",
                            callback_data='download_anyway_dmf',
                            extra_data={
                                'file_path': file_path,
                                'name': name
                            }
                        )
                    ]
                ], general_extra_data={'msg': msg}
            )
            await mod.send_buttons(
                msg.chat.id,
                b("⚠️ Внимание! Данный модуль не найден на официальном сайте и не прошёл проверку на подлинность! "
                "Это может быть небезопасно — файл может содержать вредоносный код или нежелательные программы. "
                "Загрузка и использование этого модуля могут представлять угрозу для "
                "безопасности ваших данных а также аккаунта Telegram. "
                "Убедитесь, что доверяете источнику перед загрузкой.", False),
                buttons=buttons, message_thread_id=msg.message_thread_id,
                reply_to_message_id=msg.reply_to_message_id if msg else None
            )
            await msg.delete()
            return
        
        return
    try:
        await notify(f"{emoji(5386367538735104399, '⌛')} Загружаю {b(name)}")
        mpath = Path(get_root()) / 'plugins' / name
        isset = os.path.exists(mpath)
        unpack_module(file_path, mpath)
        manifest = read_yaml(mpath / 'manifest.yaml')
        if not no_alert_version:
            if versions := list(map(str, manifest.get('available_RimTUB_versions', []))):
                if Config.VERSION not in versions:
                    buttons = Buttons(
                        [
                            [
                                Button(
                                    'Info',
                                    callback_data='info',
                                    extra_data={
                                        'module_versions': versions
                                    })
                            ],
                            [
                                Button(
                                    "Все равно установить (может поломать юб!)",
                                    callback_data='download_anyway_dmf_version',
                                    extra_data={
                                        'file_path': file_path,
                                        'name': name
                                    }
                                )
                            ],
                            [
                                Button(
                                    "Отмена (удалить модуль)",
                                    callback_data='delete',
                                    extra_data={
                                        'file_path': file_path,
                                    }
                                )
                            ]
                        ], general_extra_data={'msg': msg}
                    )
                    await mod.send_buttons(
                        msg.chat.id,
                        b("⚠️ Внимание! Данный модуль предназначен для "
                          "другой версии RimTUB и может быть несовместим! "
                          "Его использование может привести к некорректной работе, "
                          "критическим ошибкам и полному выходу из строя юзербота. "
                          "Устанавливайте модуль на свой страх и риск.", False),
                        buttons=buttons, message_thread_id=msg.message_thread_id
                    )
                    if not hasattr(msg, '_client'):
                        msg._client = app
                    elif not msg._client:
                        msg._client = app
                    if msg._client:
                        await msg.delete()
                    return
                
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
                    ), '_', False
                ), True, False
            )
            
        except:
            cap = ''
        if isset:
            return await notify(f"{emoji(5206607081334906820, '✅')} Модуль обновлен и перезапущен!" + "\n\n" + cap)
        await notify(
            f"{emoji(5206607081334906820, '✅')} Модуль загружен и запущен!" + "\n\n" + cap
        )
    except Exception as e:
        await notify(
            b(f"{emoji(5240241223632954241, '🚫')} Произошла ошибка!\n{await paste(format_exc())}", False)
        )
        mod.logger.error('dmf error', exc_info=True)


async def main(app: Client, mod: Module):

    cmd = mod.cmd

    @mod.callback('download_anyway')
    async def _download_anyway(c: C):
        return await dml(
            app, mod, c.extra_data['msg'],
            lambda text: c.edit_message_text(remove_emoji_tags(text)),
            c.extra_data['url'], True
        )

    @mod.callback('download_anyway_dmf')
    async def _download_anyway_dmf(c: C):
        return await dmf(
            app, mod, c.extra_data['msg'],
            lambda text: c.edit_message_text(remove_emoji_tags(text)),
            c.extra_data['file_path'], c.extra_data['name'], True
        )
    
    @mod.callback('download_anyway_dmf_version')
    async def _download_anyway_dmf_version(c: C):
        return await dmf(
            app, mod, c.extra_data['msg'],
            lambda text: c.edit_message_text(remove_emoji_tags(text)),
            c.extra_data['file_path'], c.extra_data['name'], True, True
        )
    
    @mod.callback('info')
    async def _info(c: C):
        return await c.answer(
            f"Твоя версия RimTUB: {Config.VERSION}\n"
            f"Доступные версии RimTUB: {', '.join(map(str, c.extra_data['module_versions']))}",
            show_alert=True
        )
    @mod.callback('delete')
    async def _info(c: C):
        os.remove(c.extra_data['file_path'])
        await c.edit_message_text("Модуль удален")

    @cmd(['dmf'])
    async def _dmf(_, msg: Message):
        try:
            if r:= msg.reply_to_message:
                if r.document:
                    if r.document.mime_type in ('application/zip') and r.document.file_name.endswith('.rimtub-module'):
                        pass
                    else:
                        return await msg.edit(f"{emoji(5210952531676504517, '❌')} Ошибка: Файл не является модулем!")
                else:
                    return await msg.edit(f"{emoji(5210952531676504517, '❌')} Ошибка: Ответь на сообщение с модулем!")
            else:
                return await msg.edit(f"{emoji(5274099962655816924, '❗️')} Ответь на сообщение!")
            await msg.edit(
                f"{emoji(5386367538735104399, '⌛')} Загружаю..."
            )

            name = r.document.file_name.rsplit(".", 1)[0]
            path = await r.download(mod.path / r.document.file_name)
            await dmf(app, mod, msg, msg.edit, path, name, Config.DISABLE_MODULE_CHECKING, Config.DISABLE_MODULE_VERSION_CHECKING)
            
        except Exception as e:
            await msg.edit(f'Не удалось загрузить модуль!\n{await paste(format_exc())}')
            raise LoadError() from e

    @cmd(['dml'])
    async def _dml(_, msg: Message, url=None):
        try:
            url = msg.text.split(maxsplit=1)[1]
        except IndexError:
            await msg.edit(f"{emoji(5447644880824181073, '⚠️')} Вставь ссылку!")
            return

        return await dml(app, mod, msg, msg.edit, url, Config.DISABLE_MODULE_CHECKING)
        


    @cmd(['sm'])
    async def _sm(_, msg: Message):
        try:
            _, name = msg.text.split(maxsplit=1)
        except ValueError:
            return await msg.edit(f"{emoji(5274099962655816924, '❗️')} Напиши название модуля!")

        module_path = Path(find_directory(name, 'plugins', 1))

        if not module_path:
            return await msg.edit(f"{emoji(5447644880824181073, '⚠️')} Такой модуль не найден!")

        manifest = read_yaml(module_path / 'manifest.yaml')

        cap = f"❗️Модуль ТОЛЬКО на @RimTUB версии {', '.join(map(str, manifest.get('available_RimTUB_versions', [])))}❗️\n\n"
        try:
            cap += bq(
                build_module_help_text(helplist.get_module(name.lower(), lower=True), '_', False),
                True, False
            )
        except:
            mod.logger.error("Не удалось сформировать хелп текст. Ошибка в дебаге")
            mod.logger.debug('.', exc_info=True)

        try:
            module_file = pack_module(module_path, mod.path / f"{os.path.split(module_path)[-1]}.rimtub-module")
        except:
            mod.logger.error("Не удалось запаковать модуль. Ошибка в дебаге")
            mod.logger.debug('.', exc_info=True)
            return await msg.edit(f"Упс! Не получилось запаковать модуль!\n{await paste(format_exc())}")

        try:
            await msg.reply_document(module_file, caption=cap)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"{emoji(5260293700088511294, '⛔️')} Произошла неизвестная ошибка!\n{await paste(format_exc())}")
            raise LoadError() from e
        finally:
            os.remove(module_file)
            
    @cmd('delm')
    async def _delm(app, msg):
        try:
            _, name = msg.text.split(maxsplit=1)
        except ValueError:
            return await msg.edit(f"{emoji(5274099962655816924, '❗️')} Напиши название модуля!")
        
        module_path = find_directory(name, 'plugins', 1)
        if not module_path:
            return await msg.edit(f"{emoji(5447644880824181073, '⚠️')} Такой модуль не найден!")
        
        shutil.rmtree(module_path)
        await app.stop_module(os.path.split(module_path)[-1], unload_help=True, all_clients=True)

        await msg.edit(
            f"{emoji(5445267414562389170, '🗑')} Модуль {b(os.path.split(module_path)[-1])} удален!"
        )


    @cmd('relm')
    async def _relm(app: Client, msg):
        try:
            module_name = msg.text.split(maxsplit=1)[1]
        except IndexError:
            await msg.edit("Введи название модуля!")
        try:
            module_path = find_directory(module_name, 'plugins', 1)
            if not module_path:
                return await msg.edit(f"{emoji(5447644880824181073, '⚠️')} Такой модуль не найден!")
            name = os.path.basename(module_path)
            await app.load_module(name, restart=True, exception=True, all_clients=True)

            for client in clients:
                r = await client._start_on_ready(name)
                if r[0] == 'error':
                    raise r[1]

        except Exception as e:
            await msg.edit(f'Не удалось перезагрузить модуль!\n{await paste(format_exc())}')
            raise LoadError() from e
            
        else:
            await msg.edit(f"{emoji(5206607081334906820, '✅')} Модуль {b(os.path.basename(module_path))} перезагружен!")

    @cmd(['offm', 'stopm'])
    async def _offm(app: Client, msg):
        module_name = msg.text.split(maxsplit=1)[1]
        try:
            module_path = find_directory(module_name, 'plugins', 1)
            if not module_path:
                return await msg.edit(f"{emoji(5447644880824181073, '⚠️')} Такой модуль не найден!")
            name = os.path.split(module_path)[-1]

            disabled_modules = await mod.db.get('disabled_modules', [])
            if name not in disabled_modules:
                await app.stop_module(name)
                disabled_modules.append(name)
                await mod.db.set('disabled_modules', disabled_modules)
        except Exception as e:
            await msg.edit(f'Не удалось выключить модуль!\n{await paste(format_exc())}')
            raise LoadError() from e
        else:
            await msg.edit(f"{emoji(5206607081334906820, '✅')} Модуль {b(name)} выключен!")


    @cmd(['onm', 'startm'])
    async def _onm(app: Client, msg):
        module_name = msg.text.split(maxsplit=1)[1]
        try:
            module_path = find_directory(module_name, 'plugins', 1)
            if not module_path:
                return await msg.edit(f"{emoji(5447644880824181073, '⚠️')} Такой модуль не найден!")
            name = os.path.split(module_path)[-1]

            
            disabled_modules: list = await mod.db.get('disabled_modules', [])
            if name in disabled_modules:
                await app.load_module(name, restart=False, exception=True)
                disabled_modules.remove(name)
                await mod.db.set('disabled_modules', disabled_modules)

        except Exception as e:
            await msg.edit(f'Не удалось включить модуль!\n{await paste(format_exc())}')
            raise LoadError() from e
        else:
            await msg.edit(f"{emoji(5206607081334906820, '✅')} Модуль {b(name)} включен!")

    @cmd(['offms'])
    async def _offms(app: Client, msg):
        disabled_modules = await mod.db.get('disabled_modules', [])
        if not disabled_modules:
            t = 'Нет выключенных модулей!'
        else:
            t = f'Выключенные модули: {",  ".join(map(code, disabled_modules))}'
        await msg.edit(t + f"\n\nЧтобы выключить модуль используй {code(Config.PREFIX+'offm')}\xa0[Название\xa0модуля].\n"
                       f"Чтобы включить: {code(Config.PREFIX+'onm')}\xa0[Название\xa0модуля]")
