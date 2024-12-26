import logging
import os
import shutil
from pyrogram import __version__
from pyrogram.types import Message as M

from utils import *

from utils.html_tags import blockquote
from utils.scripts import find_file, get_tree

helplist.add_module(
    HModule(
        __package__,
        description="Просмотр логов RimTUB",
        author="built-in (@RimMirK)",
        version='1.0.2'
    ).add_command(
        Command(['logtail'], [Arg("число строк", False)], "Получить последние n строк из лога")
    ).add_command(
        Command(['glog'], [Arg("имя файла", False)], "получить лог")
    ).add_command(
        Command(['glogs'], [], "Посмотреть все файлы лога")
    ).add_command(
        Command(['dellogs'], [], "Удалить все логи")
    )
)

async def main(app: Client, mod: Module):

    cmd = mod.cmd

    @cmd(['logtail'])
    async def _ltail(_, msg: M):
        lines = int(get_args(msg.text, 10))
        with open('logs\last_run.log', 'r', encoding='utf-8') as f:
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

    def get_folder_size(path):
        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for file in filenames:
                filepath = os.path.join(dirpath, file)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size

    def format_size(size_in_bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024


    def delete_files_in_folder(folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except: pass


    @cmd(['dellogs'])
    async def _gellogs(_, msg: M):
        logging.shutdown()

        size = 0
        if os.path.isdir('logs'):
            size = format_size(get_folder_size('logs'))
            delete_files_in_folder('logs')

        for i, client in enumerate(clients):
            logger = logging.getLogger(f'RimTUB [{i}]')
            install_log(logger)
            client.logger = logger

        logger = logging.getLogger(f'TeleBot')
        install_log(logger, bot=True)
        
        
        await msg.edit(f"Все логи удалены! Освобождено {size} памяти")