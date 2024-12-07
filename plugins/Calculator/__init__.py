from pyrogram import types
from utils import *


helplist.add_module(
    Module(
        __package__,
        version='1.1.2',
        author='built-in (@RimMirK)',
        description="Калькулятор",
    ).add_command(
        Command(
            ['calc'],
            [Arg("Выражение (пример)")],
            "Посчитать"
        )
    )
)

async def main(app):

    cmd = app.cmd(app.get_group(__package__))

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
            await msg.edit(f"<emoji id=5472164874886846699>✨</emoji> {equations} = {code(pe)}")
        except Exception as ex:
            import traceback
            traceback.print_tb(ex.__traceback__)
            await msg.edit(f"<emoji id=5465665476971471368>❌</emoji> Error!\n\nДля исправления: {code(f'{PREFIX}{msg.command[0]} {equations}')}")