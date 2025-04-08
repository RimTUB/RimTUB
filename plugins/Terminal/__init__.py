import asyncio, subprocess, platform
from pyrogram import types
from utils import *




async def execute_command(command):
    if command.lower() == "clear":
        os = platform.system()
        if os == "Windows":
            command = "cls"
        else:
            command = "clear"
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            return stderr.decode('utf-8')
    except Exception as e:
        return f"Неизвестная ошибка"


async def main(app: Client, mod: Module):

    cmd = mod.cmd

    @cmd(['t'])
    async def terminal(_, msg: types.Message):
        await msg.edit("<b>Uploading...</b>")
        try:
            _, text = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b>Вы не указали команду</b>")
            return

        output = await execute_command(text)
        if len(output) > 3000:
            await msg.edit("<b>Слишком большой вывод! В разработке вывод по ссылке</b>")
            return 
        await msg.edit(
            "<b>Команда</b>\n"
            f"<pre>{text}</pre>\n\n"
            "<b>Вывод</b>\n"
            f"<pre>{output}</pre>"
            )