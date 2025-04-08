import asyncio
from pyrogram.enums import ParseMode
from utils import *


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

