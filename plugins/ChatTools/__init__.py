import asyncio
from utils import *



helplist.add_module(
    HModule(
        __package__,
        description="Инструменты для работы с чатами",
        version="1.2.2",
        author="built-in (@RimMirK)"
    ).add_command(
        Command(['chatid', 'cid'], [], "Показать ID чата")
    ).add_command(
        Command(['chat'], [], "Получить всю информацию о чате")
    ).add_command(
        Command(['uid', 'userid'], [Arg("ответ")], "Показать ID пользователя")
    ).add_command(
        Command(['online'], [], "Сделать себя всегда онлайн")
    ).add_command(
        Command(['offline'], [], "Отменить всегда онлайн")
    ).add_command(
        Command(['ping'], [], "Узнать пинг")
    )
)



async def main(app: Client, mod: Module):

    cmd = mod.cmd

    @cmd(['chatid', 'cid'])
    async def _cid(_, msg):
        await msg.edit("ID Чата: " + code(msg.chat.id))

    @cmd(['uid', 'userid'])
    async def _uid(_, msg):
        if r := msg.reply_to_message:
            await msg.edit("ID пользователя: " + code(r.from_user.id))
        else:
            await msg.edit("Ответь на сообщение!")

    @cmd(['chat'])
    async def _chat(_, msg):
        await msg.edit("Объект чата: " + pre(str(msg.chat), 'js'))

    @cmd(['ping'])
    async def _ping(app, msg):
        ping = await check_ping(app)

        if ping <= 100:
            e = '<emoji id="5294160616729096737">🟢</emoji>'
        elif ping <= 200:
            e = '<emoji id="5294234838058938175">🟡</emoji>'
        else:
            e = '<emoji id="5291899179008798421">🔴</emoji>'
            
        await msg.edit(b(f"Pong!{e}\nPing: {ping:.1f}ms", False))

            
    @cmd(['online'])
    async def _online(app, msg):
        await msg.edit(
            "<emoji id=5427009714745517609>✅</emoji> "
            "Теперь ты всегда в сети!\n"
            "Для отмены пиши " + code(PREFIX + 'offline')
        )
        await mod.db.set('online', True)
        while await mod.db.get('online', False):
            omsg = await app.send_message('me', '.')
            await omsg.delete()

            await asyncio.sleep(10)
    
    @cmd(['offline'])
    async def _offline(app, msg):
        await mod.db.set('online', False)
        await msg.edit("<emoji id=5427009714745517609>✅</emoji> Теперь ты не в сети!")
