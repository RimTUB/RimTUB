from time import perf_counter
from pyrogram.enums.chat_type import ChatType
from utils import *




async def main(app: Client, mod: Module):

    @mod.cmd(['ccount'])
    async def countcmd(app: Client, message):
        start = perf_counter()
        users = 0
        groups = 0
        supergroups = 0
        channels = 0
        bots = 0
        general = 0
        await message.edit(b("Получаем информацию..."))
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
            b("Количество ваших чатов в Telegram:\n\n") +
            f"{emoji(5373012449597335010, '👤')} Личных чатов: {b(users)}\n"
            f"{emoji(5372926953978341366, '👥')} Групп: {b(groups)}\n"
            f"{emoji(5370867268051806190, '🫂')} Супергрупп: {b(supergroups)}\n"
            f"{emoji(5296502602266067656, '📢')} Каналов: {b(channels)}\n"
            f"{emoji(5372981976804366741, '🤖')} Ботов: {b(bots)}\n\n"
            f"{emoji(5438496463044752972, '⭐️')} {b(f'Всего: {general}')}\n\n"
            f"{emoji(5298728804074666786,  '⏱')} Подсчитано за {b(pnum(round(ms, 2)))} c."
        )