import sys
sys.dont_write_bytecode = True

import logging
from utils._logs import install_log
from utils.bot_helper import _load_bot_helper_handlers
logger = logging.getLogger('RimTUB')
install_log(logger)

if __name__ == '__main__':
    logger.info("Запускаюсь...")

import os
import asyncio
import threading
from pyrogram import idle
from pyrogram.enums.parse_mode import ParseMode
from config import (
    API_ID, API_HASH,
    PHONES, PLAY_SOUND,
    BOT_TOKEN, SHOW_NOTIFICATION,
    PROXY,
    CL_DEVICE_MODEL,
    CL_SYSTEM_VERSION,
    CL_LANG_PACK,
    CL_LANG_CODE,
    CL_SYSTEM_LANG_CODE,
    CL_CLIENT_PLATFORM
)
from utils import get_script_directory, ModifyPyrogramClient, clients
from sys import argv
from telebot.async_telebot import AsyncTeleBot 

version = '2.1.1'
version_tuple = (2, 1, 1, 'release', 0)



def start():
    bot = AsyncTeleBot(BOT_TOKEN, 'html', colorful_logs=True)
    bot_logger = logging.getLogger('TeleBot')
    install_log(bot_logger, bot=True)
    for i, PHONE in enumerate(PHONES):
        account_logger = logging.getLogger(f'RimTUB [{i}]')
        
        install_log(account_logger)

        cl = ModifyPyrogramClient(
            name="RimTUB" + (f'({i})' if i > 0 else ''),
            api_id=API_ID,
            api_hash=API_HASH,
            phone_number=PHONE,
            app_version=version,
            device_model = CL_DEVICE_MODEL,
            system_version = CL_SYSTEM_VERSION,
            lang_pack = CL_LANG_PACK,
            lang_code = CL_LANG_CODE,
            system_lang_code = CL_SYSTEM_LANG_CODE,
            proxy = PROXY,
            client_platform = CL_CLIENT_PLATFORM,
            workdir=os.path.join(get_script_directory(), "sessions"),
            hide_password=True,
            parse_mode=ParseMode.HTML,
            sleep_threshold=30,
            num=i,
            logger=account_logger,
            bot=bot
        )

        with threading.Lock():
            cl.start()

        clients.append(cl)

    
    _load_bot_helper_handlers(bot)
    
    asyncio.get_event_loop().create_task(bot.polling(non_stop=True))

    for client in clients:
        asyncio.get_event_loop().run_until_complete(client._start_on_readys())

    is_restart = len(argv) > 1

    if not is_restart and PLAY_SOUND:
        try:
            
            from os import environ
            environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

            from pygame.mixer import Sound, init

            init()

            Sound('started.mp3').play()
        except:
            logger.warning("Can not play sound(", exc_info=True)

    if not is_restart and SHOW_NOTIFICATION:
        import plyer
        plyer.notification.notify(
            title=f'RimTUB v. {version} Запущен!',
            message=f'Не закрывай консоль, иначе RimTUB прекратит работу',
            app_name='RimTUB',
            app_icon=f'{get_script_directory()}\\logo.ico',
        )


    logger.info("\n\n- RimTUB Запущен и готов к работе! -\n")


    idle()

    for cl in clients:
        cl.stop()


if __name__ == '__main__':
    start()