from pyrogram import types
from utils import *




async def main(app: Client, mod: Module):

    cmd = mod.cmd

    @cmd(['calc'])
    async def calc(_, msg: types.Message):
        _, equations = msg.text.split(maxsplit=1)
        
        i = (equations
            .replace('^','**')
            .replace('x', '*')
            .replace('х', '*')
            .replace('•', '*')
            .replace('·', '*')
            .replace('∙', '*')
            .replace(':', '/')
            .replace('÷', '/')
            .replace('√', 'math.sqrt')
        )
        try:
            import math, utils
            
            def root(n: int|float, k: int|float = 2) -> float:
                return n ** (1/k)

            e = eval(i, globals(), locals())

            try: pe = int(e) if int(e) == e else e
            except: pe = e
            await msg.edit(f"{emoji(5472164874886846699, '✨')} {equations} = {code(pe)}")
        except Exception as ex:
            await msg.edit(f"{emoji(5465665476971471368, '❌')} Error!\n\nДля исправления: {code(f'{Config.PREFIX}{msg.command[0]} {equations}')}")