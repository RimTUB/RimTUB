from pyrogram import types
from utils import *
from PIL import Image
from io import BytesIO
import aiohttp

async def main(app: Client, mod: Module):


    cmd = mod.cmd

    @cmd(['makeqr'])
    async def makeqr(app_, msg: types.Message):
        await msg.edit("<b>Uploading...</b>")
        try:
            _, text = msg.text.split(maxsplit=1)
        except ValueError:
            await msg.edit("<b>Вы не указали команду</b>")
            return

        file = False
        if text.startswith(("-file", "-f")):
            file = True
            if text.startswith("-f"):
                text = text[2:].strip()
            else:
                text = text[5:].strip()
        url = "https://api.qrserver.com/v1/create-qr-code/?data={}&size=512x512&charset-source=UTF-8&charset-target=UTF-8&ecc=L&color=0-0-0&bgcolor=255-255-255&margin=1&qzone=1&format=png"
        async with aiohttp.ClientSession() as session:
            async with session.get(url.format(text)) as r:
                if r.status != 200:
                    await msg.edit(f"<b>Ошибка при загрузке QR-кода (статус {r.status})</b>")
                    return
                qrcode_content = await r.read()

        qrcode = BytesIO(qrcode_content)
        qrcode.name = "qr.png" if file else "qr.webp"
        Image.open(qrcode).save(qrcode)
        qrcode.seek(0)
        await msg.delete()
        await app_.send_document(
            msg.chat.id, document=qrcode, force_document=file
        )

    @cmd(['readqr'])
    async def readqr(_, msg: types.Message):
        await msg.edit("В разработке...")
        return

        ok = await check(msg)
        if not ok:
            reply = msg.reply_to_message
            ok = await check(reply)
            if not ok:
                text = (
                    "<b>Это не изображение!</b>"
                    if reply
                    else "<b>Нечего не передано!</b>"
                )
                await msg.edit(text)
                return
        file = BytesIO()
        file.name = "qr.png"
        data = await reply.download(BytesIO())
        Image.open(data).save(file)
        url = "https://api.qrserver.com/v1/read-qr-code/?outputformat=json"
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field('file', file.getvalue(), filename='qr.png', content_type='image/png')
            async with session.post(url, data=form_data) as resp:
                if resp.status != 200:
                     await msg.edit(f"<b>Ошибка при чтении QR-кода (статус {resp.status})</b>")
                     return
                try:
                    resp_json = await resp.json()
                except aiohttp.ContentTypeError:
                    await msg.edit("<b>Не удалось декодировать JSON ответ</b>")
                    return
        text = resp_json[0]["symbol"][0]["data"]
        if not text:
            text = "<b>Невозможно распознать или QR пуст!</b>"
        await utils.answer(message, text)

async def check(msg):
    if msg and msg.media:
        if msg.photo:
            ok = msg.photo
        elif msg.document:
            ok = msg.media.document
        else:
            return False
    else:
        return False
    if not ok or ok is None:
        return False
    else:
        return ok