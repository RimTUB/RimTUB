from pyrogram import types
from utils import *



async def main(app: Client, mod: Module):

    import io
    import aiohttp

    cmd = mod.cmd

    @cmd(['x0'])
    async def x0(_, msg: types.Message):
        await msg.edit("<b>Uploading...</b>")

        reply = msg.reply_to_message
        if not reply:
            await msg.edit(
                f'<emoji id="5447644880824181073">⚠️</emoji> Отправьте ответом на сообщение')
            return

        media = reply.media
        if not media:
            file = io.BytesIO(bytes(reply.text, "utf-8"))
            file_name = "txt.txt"
        else:
            file_path = await reply.download()
            file = open(file_path, "rb")
            if reply.document:
                file_name = reply.document.file_name
            elif reply.photo:
                file_name = f"{reply.photo.file_id}.jpg"
            elif reply.video:
                file_name = f"{reply.video.file_id}.mp4"
            else:
                file_name = "unknown"

        try:
            async with aiohttp.ClientSession() as session:
                data = aiohttp.FormData()
                data.add_field('file', file, filename=file_name)
                async with session.post("https://x0.at", data=data) as resp:
                    if resp.status == 200:
                        url = await resp.text()
                    else:
                        await msg.edit(
                            f'<b><emoji id="5420323339723881652">⚠️</emoji>Error</b>\n<code>HTTP {resp.status}</code>')
                        return
        except aiohttp.ClientError as e:
            await msg.edit(
                f'<b><emoji id="5420323339723881652">⚠️</emoji>Error</b>\n<code>{e}</code>')
            return
        finally:
            if not media:
                file.close()
            else:
                if isinstance(file, io.BytesIO):
                    file.close()
                else:
                    file.close()
                    import os
                    os.remove(file_path)
        output = f'<a href="{url}">URL: </a><code>{url}</code>'
        await msg.edit(output)

    @cmd(['x0inf'])
    async def x0inf(_, msg: types.Message):
        output = """
<b>Помощь по модулю x0</b>
<pre>
Максимально допустимый размер файла - 222 MiB.

Файлы хранятся минимум 3, а максимум 100 дней.

Срок хранения файла зависит от его размера. Большие файлы удаляются раньше 
чем маленькие. Эта зависимость нелинейна и смещена в пользу маленьких 
файлов.
</pre>
        """
        await msg.edit(output)