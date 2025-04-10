import asyncio
from utils import *


async def main(app: Client, mod: Module):

    cmd = mod.cmd

    async def worker():
        while True:
            if await mod.db.get('online', False):
                omsg = await app.send_message('me', '.')
                await omsg.delete()
            await asyncio.sleep(10)

    @mod.on_ready
    async def _onr(_):
        mod.add_task(worker())

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
            e = emoji(5294160616729096737, '🟢')
        elif ping <= 200:
            e = emoji(5294234838058938175, '🟡')
        else:
            e = emoji(5291899179008798421, '🔴')
            
        await msg.edit(b(f"Pong!{e}\nPing: {ping:.1f}ms", False))

            
    @cmd(['online'])
    async def _online(app, msg):
        await msg.edit(
            f"{emoji(5427009714745517609, '✅')} "
            "Теперь ты всегда в сети!\n"
            "Для отмены пиши " + code(Config.PREFIX + 'offline')
        )
        await mod.db.set('online', True)

    
    @cmd(['offline'])
    async def _offline(app, msg):
        await mod.db.set('online', False)
        await msg.edit(f"{emoji(5427009714745517609, '✅')} Теперь ты не в сети!")
