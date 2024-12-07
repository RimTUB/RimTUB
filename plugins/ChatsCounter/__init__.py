from time import perf_counter
from pyrogram.enums.chat_type import ChatType
from utils import *

helplist.add_module(
    Module(
        __package__,
        description="Считает кол-во Ваших чатов",
        author="@RimMirK по заказу @DragonFire20",
        version='1.0',
    ).add_command(
        Command(['ccount'], [], 'Посчитать кол-во чатов')
    )
)


async def main(app):

    @app.cmd(app.get_group(__package__))(['ccount'])
    async def countcmd(app: Client, message):
        start = perf_counter()
        users = 0
        groups = 0
        supergroups = 0
        channels = 0
        bots = 0
        general = 0
        await message.edit("<b>Получаем информацию...</b>")
        async for dialog in app.get_dialogs():
            match dialog.chat.type:
                case ChatType.PRIVATE:
                    users += 1
                case ChatType.BOT:
                    bots += 1
                case ChatType.SUPERGROUP:
                    supergroups += 1
                case ChatType.CHANNEL:
                    channels += 1
                case ChatType.GROUP:
                    groups += 1
            general += 1
                
        end = perf_counter()
        ms = end - start
        await message.edit(
            "<b>Количество ваших чатов в Telegram:</b>\n\n"
            f'<emoji id="5373012449597335010">👤</emoji> Личных чатов: {b(users)}\n'
            f'<emoji id="5372926953978341366">👥</emoji> Групп: {b(groups)}\n'
            f'<emoji id="5370867268051806190">🫂</emoji> Супергрупп: {b(supergroups)}\n'
            f'<emoji id="5296502602266067656">📢</emoji> Каналов: {b(channels)}\n'
            f'<emoji id="5372981976804366741">🤖</emoji> Ботов: {b(bots)}\n\n'
            '<emoji id="5438496463044752972">⭐️</emoji> '
                + b(f"Всего: {general}\n\n") +
            f'<emoji id="5298728804074666786">⏱</emoji> Подсчитано за <b>{pnum(round(ms, 2))}</b> c.'
        )