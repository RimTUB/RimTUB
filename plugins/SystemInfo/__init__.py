import time, platform

from pyrogram.types import Message

from utils import *

import psutil



async def main(app: Client, mod: Module):

 
    @mod.cmd(["sinfo"])
    async def sping_cmd(app: Client, msg: Message):
        buttons = await get_kb(app)
        await mod.send_buttons(msg.chat.id, "📊 Главное меню", buttons, message_thread_id=msg.message_thread_id)
        await msg.delete()
    
        
    async def get_kb(app: Client, ping=None):
        return await mod.prepare_buttons(
            Buttons([
                [
                    Button(f"🚀 Пинг(тг): {ping or await get_ping(app)} мс", callback_data='ping'),
                ],
                [
                    Button(f"💻 Система", callback_data='sys_stats'),
                ],
                [
                    Button(f"🔄 Обновить", callback_data='update'),
                ]
            ])
        )

    @mod.callback('ping')
    async def call_ping(call: C):
        ping = await get_ping(app)
        await call.answer(f"Пинг: {ping} мс")
        await call_menu(call.original_callback, ping)
    
    @mod.callback('update')
    @mod.callback('menu')
    async def call_menu(call: C, ping=None):
        await call.edit_message_text(
            "📊 Главное меню",
            reply_markup=await get_kb(app, ping=ping)
        )
    
    @mod.callback('sys_stats')
    async def call_sys_stats(call: C):
        txt = (
            f"<b>💻 Системная информация:\n\n"
            f"🔧 CPU: {psutil.cpu_percent()}% | Ядер: {psutil.cpu_count()} (физ. {psutil.cpu_count(logical=False)})\n"
            f"📊 Память: {format_storage(psutil.virtual_memory().used, psutil.virtual_memory().total)}\n"
            f"💾 Диск: {format_storage(psutil.disk_usage('/').used, psutil.disk_usage('/').total)}\n"
            f"🐍 Python: {platform.python_version()} | {platform.python_implementation()}\n"
            f"🖥 ОС: {platform.system()} {platform.release()} | {platform.machine()}\n"
            f"🕒 Аптайм: {sec_to_str(int(time.time() - psutil.boot_time()))}\n\n</b>"
        )
        buttons = await mod.prepare_buttons(
            Buttons(
                [
                    [
                        Button("⬅️ Назад", callback_data='menu')
                    ]
                ]
            )
        )
        await call.edit_message_text(
            text=txt,
            reply_markup=buttons,
        )

        
async def get_ping(client: Client):
    start = time.perf_counter()
    await client.get_me()
    return round((time.perf_counter() - start) * 1000, 2)
    
def format_storage(used, total):
    used_gb = used / (1024**3)
    total_gb = total / (1024**3)
    percent = (used / total) * 100
    
    return f"{used_gb:.2f}GB/{total_gb:.0f}GB ({percent:.0f}%)"
