from pyrogram import __version__
from pyrogram.types import Message as M

from utils import *

from utils.html_tags import blockquote
from utils.scripts import find_file, get_tree

helplist.add_module(
    Module(
        __package__,
        description="Просмотр логов RimTUB",
        author="built-in (@RimMirK)",
        version='beta 1.0'
    ).add_command(
        Command(['logtail'], [Arg("число строк", False)], "Получить последние n строк из лога")
    ).add_command(
        Command(['glog'], [Arg("имя файла", False)], "получить лог")
    ).add_command(
        Command(['glogs'], [], "Посмотреть все файлы лога")
    )
)

async def main(app: Client):

    cmd = app.cmd(app.get_group(__package__))

    @cmd(['logtail'])
    async def _ltail(_, msg: M):
        lines = int(get_args(msg.text, 10))
        with open('logs\general.log', 'r', encoding='utf-8') as f:
            r = tail(f, lines)
        link = await paste(r)
        await msg.edit(f"Последние {lines} строк: {link}")
    
    @cmd(['glog'])
    async def _lg(_, msg: M):
        logfile = get_args(msg.text, 'general')
        file = find_file(logfile, 'logs', 1, ['.log'])
        if not file:
            return await msg.edit(f"Файл {logfile} не найден!")
        await msg.reply_document(file)
        await msg.delete()
    
    @cmd(['glogs'])
    async def _glogs(_, msg: M):
        tree = blockquote(code('logs')+'\n'+get_tree('logs', html=True), expandable=True, escape_html=False)
        await msg.edit(tree if len(tree) <= 4096 else await paste(tree))