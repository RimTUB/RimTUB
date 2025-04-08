import time
from utils import *
from pyrogram.types import Message
from .runner import CodeRunner, File

async def main(app: Client, mod: Module):
    
    runner = CodeRunner()
    
    @mod.cmd(["exec"])
    async def cmd_exec(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Выполнение кода...</b>")
        try:
            _, lang, code = msg.text.split(maxsplit=2)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали язык или код</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute(lang, [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=4985712614039355997>🖥</emoji> <code>{lang}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit(text=(
                    "<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка, "
                    "возможно вы указали неверный язык"
                ))
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}")
            
    @mod.cmd(["epy"])
    async def cmd_epy(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Интерпритация кода...</b>")
        try:
            _, code = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали код!</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute("python3", [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<emoji id=4985930888572306287>🖥</emoji> Python 3"
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit("<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка")
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}", exc_info=True)
            
    @mod.cmd(["ejs"])
    async def cmd_ejs(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Интерпритация кода...</b>")
        try:
            _, code = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали код!</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute("javascript", [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<emoji document_id=4985930888572306287>🖥</emoji> JavaScript"
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit("<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка")
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}")
            
    @mod.cmd(["elua"])
    async def cmd_elua(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Интерпритация кода...</b>")
        try:
            _, code = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали код!</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute("lua", [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<emoji document_id=4985930888572306287>🖥</emoji> Lua"
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit("<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка")
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}")
        
    @mod.cmd(["ecsh"])
    async def cmd_esh(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Компиляция кода...</b>")
        try:
            _, code = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали код!</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute("csharp", [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<emoji document_id=4985930888572306287>🖥</emoji> C#"
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit("<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка")
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}")
            
    @mod.cmd(["ec"])
    async def cmd_ec(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Компиляция кода...</b>")
        try:
            _, code = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали код!</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute("c", [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<emoji document_id=4985930888572306287>🖥</emoji> C"
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit("<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка")
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}")

    @mod.cmd(["ecpp"])
    async def cmd_ecpp(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Компиляция кода...</b>")
        try:
            _, code = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали код!</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute("c++", [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<emoji document_id=4985930888572306287>🖥</emoji> C++"
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit("<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка")
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}")

    @mod.cmd(["ers"])
    async def cmd_ers(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Компиляция кода...</b>")
        try:
            _, code = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали код!</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute("rust", [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<emoji document_id=4985930888572306287>🖥</emoji> Rust"
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit("<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка")
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}")

    @mod.cmd(["ejava"])
    async def cmd_epy(_, msg: Message):
        await msg.edit("<b><emoji id=5328274090262275771>🕐</emoji> Выполнение кода...</b>")
        try:
            _, code = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b><emoji id=5447644880824181073>⚠️</emoji> Вы не указали код!</b>")
            return

        try:
            t1 = time.time()
            result = await runner.execute("java", [File(code)])
            t2 = time.time()
            await msg.edit(text=(
                f"<emoji document_id=4985930888572306287>🖥</emoji> Java"
                f"<pre>{code}</pre>\n"
                f"<code>{result}</code>\n"
                f"<emoji id=5298728804074666786>⏱</emoji> <code>{t2-t1}</code>"
            ))
        except Exception as err:
            await msg.edit("<emoji id=5447644880824181073>⚠️</emoji> Произошла неизвестная ошибка")
            mod.logger.warning(f"Ошибка в модуле CodeExecutor: {err}")
    