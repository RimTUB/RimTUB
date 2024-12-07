from utils import *

__libs__ = 'pytimeparse2',

helplist.add_module(
    Module(
        __package__,
        author='@RimMirK',
        version='1.0.01',
        description="Делает из нечитаемого читаемое"
    ).add_command(
        Command(['pnum'], [Arg('число')], 'Вывести красиво число')
    ).add_command(
        Command(['ps2s', 'psec_to_str'], [Arg('секунды')], 'секунды в читаемое время')
    ).add_command(
        Command(['pt2s', 'ptext_to_str'], [Arg('время')], 'время в секунды')
    )
)

async def main(app):
    
    from pytimeparse2 import parse as timeparse

    cmd = app.cmd(app.get_group(__package__))

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