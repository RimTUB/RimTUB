from contextlib import redirect_stderr, redirect_stdout
from traceback import print_exc
import asyncio, time, sys
from io import StringIO

from utils import *
code_html = code


helplist.add_module(
    Module(
        "PythonRunner",
        description='Запускает код на Python',
        author="built-in (@RimMirK на основе модуля от @KurimuzonAkuma)",
        version='1.2.0'
    ).add_command(
        Command(['py'], [Arg('Код')], "Запустить код")
    ).add_command(
        Command(['rpy'], [Arg('Ответ на сообщение/цитата')], "Запускает код из отвеченного сообщения")
    ).add_command(
        Command(['eval'], [Arg('Выражение')], "Запускает eval()")
    )
)

async def aexec(code, app, msg, timeout=None):
    
    
    
    
    
    
    
    
    import utils
    
    exec(
        f"async def __todo(app, msg, *args):\n"
        " client = self = app;"
        " m = message = msg;"
        " r = msg.reply_to_message;"
        " u = msg.from_user;"
        " p = print;"
        " q = msg.quote_text;"
        " t = msg.message_thread_id;"
        " import pyrogram, utils, asyncio;"
        " from asyncio import sleep;"
        " from inspect import getsource;"
        " ru = getattr(r, 'from_user', None);"
        f" from utils import {', '.join(filter(lambda e: not e.startswith('__'), dir(utils)))}"
        + "".join(f"\n {_l}" for _l in code.split("\n"))
    )
     
    f = StringIO()
    with redirect_stdout(f):
        await asyncio.wait_for(locals()["__todo"](app, msg), timeout=timeout)

    return f.getvalue()


async def main(app):

    pv = sys.version.split()[0]

    cmd = app.cmd(app.get_group(__package__))

    @cmd(["py", "rpy"])
    async def python_exec(app, msg):
        async def _todo():
            if len(msg.command) == 1 and msg.command[0] != "rpy":
                return await msg.edit_text(b("Введи код!"))

            if msg.command[0] == "rpy":
                if not msg.reply_to_message:
                    return await msg.edit_text(b("Ответь на сообщение!"))
                code = msg.quote_text or msg.reply_to_message.text or msg.reply_to_message.caption
            else:
                code = (msg.text or msg.caption).split(maxsplit=1)[1]

            await msg.edit_text(
                b("<emoji id=5418368536898713475>🐍</emoji> Python " + pv, False) + "\n\n" +
                pre(code, 'python') + "\n\n" + b("<emoji id=5821116867309210830>⏳</emoji> Выполняю...", False)
            )
        


            try:
                start_time = time.perf_counter()
                result = await aexec(code, app, msg, timeout=300)
                stop_time = time.perf_counter()

                result = result.strip()

                result = result.replace(app.me.phone_number, "*****")

                
                t = (
                    b("<emoji id=5418368536898713475>🐍</emoji> Python " + pv, False) + "\n\n" +
                    pre(code, 'python') + "\n\n" + (
                        b("<emoji id=5472164874886846699>✨</emoji> Вывод:\n", False) +
                        code_html(result) + '\n' if result.strip() != ''
                        else b("<emoji id=5465665476971471368>❌</emoji> Вывода нет\n", False)
                    ) + "\n" +
                    b(f"<emoji id=5298728804074666786>⏱</emoji> Выполнено за {round(stop_time - start_time, 5)}s.", False)
                )

                if len(t) > 4096:
                    result = await paste(result)
                
                    t = (
                        b("<emoji id=5418368536898713475>🐍</emoji> Python " + pv, False) + "\n\n" +
                        pre(code, 'python') + "\n\n" + (
                            b("<emoji id=5472164874886846699>✨</emoji> Вывод:\n", False) +
                            result + '\n' if result.strip() != ''
                            else b("<emoji id=5465665476971471368>❌</emoji> Вывода нет\n", False)
                        ) + "\n" +
                        b(f"<emoji id=5298728804074666786>⏱</emoji> Выполнено за {round(stop_time - start_time, 5)}s.", False)
                    )

                
                return await msg.edit_text(t, disable_web_page_preview=True,)
            except TimeoutError:
                                return await msg.edit_text(
                    b("<emoji id=5418368536898713475>🐍</emoji> Python " + pv, False) + "\n\n" +
                    pre(code, 'python') + "\n\n" +
                    b("<emoji id=5465665476971471368>❌</emoji> Время на исполнение кода исчерпано! TimeoutError", False),

                    disable_web_page_preview=True,
                )
            except Exception as e:
                err = StringIO()
                with redirect_stderr(err):
                    print_exc()
                ex = err.getvalue()
                tr = await paste(ex)
                text = (
                    b("<emoji id=5418368536898713475>🐍</emoji> Python " + pv, False) + "\n\n" +
                    pre(code, 'python') + "\n\n" +
                    f"<emoji id=5465665476971471368>❌</emoji> {b(e.__class__.__name__)}: {b(e)}\n"
                    f"Traceback: {tr}"
                )
                await msg.edit(text, disable_web_page_preview=True)
        
        app.add_task(__package__, _todo())


    @cmd(['eval'])
    async def _eval(app, msg):
        async def _todo():
            m = message = msg
            r = msg.reply_to_message
            u = msg.from_user
            p = print
            q = msg.quote_text
            ru = getattr(r, 'from_user', None)
            t = msg.message_thread_id
            import pyrogram, utils, asyncio
            from asyncio import sleep
            import asyncio
            import pyrogram

            code = msg.text.split(maxsplit=1)[-1]
            try:
                result = eval(code, globals(), locals())
            except Exception as ex:
                result = str(ex)

            result = str(result).replace(app.me.phone_number, "*****")

            await msg.edit(code_html(code)  + ' = ' + code_html(result))
            
        app.add_task(__package__, _todo())