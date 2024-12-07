from utils import *

from .scheme import emojis


helplist.add_module(
    Module(
        __package__,
        version='beta 1.0',
        description="ТОЛЬКО ТЕЛЕГРАМ ПРЕМИУМ!\n\nПишет текст рукописным шрифтом через премиум емодзи",
        author='built-in (@RimMirK)'
    ).add_command(
        Command('et', [Arg('текст/ответ/цитата')], 'написать текст рукописным шрифтом через премиум емодзи')
    )
)


async def main(app):

    cmd = app.cmd(app.get_group(__package__))


    @cmd('et')
    async def _et(_, msg):
        if len(msg.text.split()) > 1:
            text = msg.text.split(maxsplit=1)[1]

        r = msg.reply_to_message

        t = (text or msg.quote_text or getattr(r, 'text')).lower() 
        tr = t.maketrans(emojis)
        t = t.translate(tr)

        await msg.edit(t)
