from pathlib import Path
import sys
from typing import Callable, Optional, Union

import inspect
sys.dont_write_bytecode = True


import asyncio

# Фикс для IPython/Jupyter
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
    
import pyrogram
from pyrogram import client
pyrogram.client = client

import logging
from utils._logs import install_log
from utils.bot_helper import _load_bot_helper_handlers
logger = logging.getLogger('RimTUB')
install_log(logger)

if __name__ == '__main__':
    logger.info("Запускаюсь...")

import os
import threading

from pyrogram import idle, Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.filters import Filter
from pyrogram.methods.decorators.on_callback_query import OnCallbackQuery
from pyrogram.handlers import RawUpdateHandler
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.dispatcher import Dispatcher
from pyrogram.types import CallbackQuery
from utils.config import Config
from utils import get_root, ModifyPyrogramClient, clients
from sys import argv

Conf = Config()

from pyrogram.methods.utilities.start import log


async def handler_worker(self, lock):
    while True:
        packet = await self.updates_queue.get()

        if packet is None:
            break

        try:
            update, users, chats = packet
            parser = self.update_parsers.get(type(update), None)

            parsed_update, handler_type = (
                await parser(update, users, chats)
                if parser is not None
                else (None, type(None))
            )

            async with lock:
                for group in self.groups.values():
                    for handler in group:
                        args = None

                        if isinstance(handler, handler_type):
                            try:
                                if await handler.check(self.client, parsed_update):
                                    args = (parsed_update,)
                            except Exception as e:
                                log.exception(e)
                                continue

                        elif isinstance(handler, RawUpdateHandler):
                            try:
                                if await handler.check(self.client, update):
                                    args = (update, users, chats)
                            except Exception as e:
                                log.exception(e)
                                continue

                        if args is None:
                            continue

                        try:
                            if inspect.iscoroutinefunction(handler.callback):
                                if isinstance(handler, CallbackQueryHandler): # fix callback
                                    await handler.callback(*args)
                                else:
                                    await handler.callback(self.client, *args)
                            else:
                                await self.client.loop.run_in_executor(
                                    self.client.executor,
                                    handler.callback,
                                    self.client,
                                    *args
                                )
                        except pyrogram.StopPropagation:
                            raise
                        except pyrogram.ContinuePropagation:
                            continue
                        except Exception as e:
                            log.exception(e)

                        break
        except pyrogram.StopPropagation:
            pass
        except Exception as e:
            log.exception(e)

async def start():
    
    root = get_root(True)
    (root / 'sessions').mkdir(exist_ok=True)
    (root / 'storage' ).mkdir(exist_ok=True)
    (root / 'plugins' ).mkdir(exist_ok=True)
    
    bot_logger = logging.getLogger('RimTUB [BOT]')
    install_log(bot_logger, bot=True)
    bot = Client(
        name="RimTUB (Bot)",
        api_id=Conf.API_ID,
        api_hash=Conf.API_HASH,
        bot_token=Conf.BOT_TOKEN,
        app_version=Config.VERSION,
        device_model = Conf.CL_DEVICE_MODEL,
        system_version = Conf.CL_SYSTEM_VERSION,
        lang_pack = Conf.CL_LANG_PACK,
        lang_code = Conf.CL_LANG_CODE,
        system_lang_code = Conf.CL_SYSTEM_LANG_CODE,
        proxy = Conf.PROXY,
        client_platform = Conf.CL_CLIENT_PLATFORM,
        workdir=os.path.join(get_root(), "sessions"),
        hide_password=True,
        parse_mode=ParseMode.HTML,
        sleep_threshold=30,
    )
    bot.logger = bot_logger
    bot.dispatcher.handler_worker = lambda lock: handler_worker(bot.dispatcher, lock)
    await bot.start()
    for i, PHONE in enumerate(Conf.PHONES):
        account_logger = logging.getLogger(f'RimTUB [{i}]')
        
        install_log(account_logger)

        cl = ModifyPyrogramClient(
            name="RimTUB" + (f'({i})' if i > 0 else ''),
            api_id=Conf.API_ID,
            api_hash=Conf.API_HASH,
            phone_number=PHONE,
            app_version=Config.VERSION,
            device_model = Conf.CL_DEVICE_MODEL,
            system_version = Conf.CL_SYSTEM_VERSION,
            lang_pack = Conf.CL_LANG_PACK,
            lang_code = Conf.CL_LANG_CODE,
            system_lang_code = Conf.CL_SYSTEM_LANG_CODE,
            proxy = Conf.PROXY,
            client_platform = Conf.CL_CLIENT_PLATFORM,
            workdir=os.path.join(get_root(), "sessions"),
            hide_password=True,
            parse_mode=ParseMode.HTML,
            sleep_threshold=30,
            # max_message_cache_size = 10,
            # max_topic_cache_size = 10,
            # fetch_topics = False,
            # fetch_stories = False,
            num=i,
            logger=account_logger,
            bot=bot
        )

        await cl.start()

        clients.append(cl)

    
    _load_bot_helper_handlers(bot)


    async def storage_cleaner():
        from utils.scripts import cleanup_expired_storage_files
        while True:
            cleanup_expired_storage_files()
            logger.debug("Cleaned expired pickle storage files")
            await asyncio.sleep(Config.CLEANUP_EXPIRED_PICKLE_STORAGE_FILES_INTERVAL)
            

    # ev = asyncio.get_event_loop()
    # ev.create_task(storage_cleaner())

    for client in clients:
        await client._start_on_readys()

    is_restart = len(argv) > 1

    if not is_restart and Conf.PLAY_SOUND:
        try:
            from playsound import playsound

            playsound('started.mp3')
        except:
            logger.warning("Can not play sound(")

    if not is_restart and Conf.SHOW_NOTIFICATION:
        try:
            import plyer
            plyer.notification.notify(
                title=f'RimTUB {Config.VERSION} Запущен!',
                message=f'Не закрывай консоль, иначе RimTUB прекратит работу',
                app_name='RimTUB',
                app_icon=str(Path(get_root(), 'logo.ico'))
            )
        except:
            logger.warning("Can not show notification(")


    logger.info("\n\n- RimTUB Запущен и готов к работе! -\n")


    await idle()

    for cl in clients:
        await cl.stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())