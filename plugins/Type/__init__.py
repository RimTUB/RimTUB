import asyncio
from pyrogram.enums import ParseMode
from utils import *

helplist.add_module(
    HModule(
        __name__,
        description=(
            "Создает эффект печатанья текста в реальном времени\n\n"
            "⚠️ Внимание! Этот модуль может быть опасным и вызвать проблемы с TG аккаунтом. "
            "Используйте этот модуль на свой страх и риск! 🚨"
        ),
        version='1.0.1',
        author='@RimMirK'
    ).add_command(
        Command(['type'], [Arg('текст')], 'Напечатать текст')
    )
)

async def main(app: Client, mod: Module):

    cmd = mod.cmd
    
    @cmd(['type'])
    async def _type(_, msg: M):
        text = get_args(msg.text.html)
        t = ''
        for l in text:
            t += l
            await msg.edit(t+'▌', parse_mode=ParseMode.DISABLED)
            await asyncio.sleep(0.1)
        
        await msg.edit(t, parse_mode=ParseMode.HTML)

