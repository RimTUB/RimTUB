from utils import *
from pytimeparse2 import parse as timeparse



async def main(app: Client, mod: Module):
    

    cmd = mod.cmd

    @cmd(['ps2s', 'psec_to_str'])
    async def _s2s(_, msg):
        try:
            await msg.edit(b(sec_to_str(float(msg.text.split()[1]), False)))
        except:
            await msg.edit(b("Ошибка!"))

    @cmd(['pnum'])
    async def _pnum(_, msg):
        try:
            await msg.edit(b(f"{pnum(float(msg.text.split()[1])):,}"))
        except:
            await msg.edit(b("Ошибка!"))

    @cmd(['pt2s', 'ptext_to_str'])
    async def _pt2s(_, msg):
        try:
            await msg.edit(b(f"{timeparse(msg.text.split()[1])}"))
        except:
            await msg.edit(b("Ошибка!"))