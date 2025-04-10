import os
import time
from traceback import format_exc
from pyrogram.raw.functions.messages.search_custom_emoji import SearchCustomEmoji
from pyrogram.raw.base import EmojiList
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from utils import *
from .schema import emojis
from bs4 import BeautifulSoup

from .tgs_gif_converter import convert

import re


def extract_emojis(text: str) -> list:
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0\U000024C2-\U0001F251]+",
        re.UNICODE,
    )
    return emoji_pattern.findall(text)



async def main(app: Client, mod: Module):


    cmd = mod.cmd

    @cmd('fms')
    async def _fms(app: Client, msg: M):
        emoticons = set(extract_emojis(msg.text) + extract_emojis(msg.reply_to_message.text if msg.reply_to_message else ''))
        t = ''
        for emoticon in emoticons:
            d: EmojiList = await app.invoke(SearchCustomEmoji(emoticon=emoticon, hash=0))
            t += emoticon + ": "
            for eid in d.document_id:
                t += emoji(eid, emoticon) + " "
            t += '\n'
        if t.strip():
            await msg.edit(t)
        else:
            await msg.edit("Емодзи не найдены!")


    @cmd(['emj', 'emjs'])
    async def _emj(_, msg: M):
        html = getattr(msg.text, 'html', None) or getattr(msg.caption, 'html', None) or ''
        if r := msg.reply_to_message:
            html += getattr(getattr(msg.quote, 'text', None), 'html', None) or getattr(r.caption, 'html', None) or getattr(r.text, 'html', None) or ''
            
        bs = BeautifulSoup(html, 'lxml')
        emjs = bs.find_all('emoji')
        
        emojis = {}
        for emj in emjs:
            emojis[str(emj)] = (emj.attrs['id'], emj.text)
        
        q1 = '"'
        q2 = "'"

    
        t = b('Custom Emojis:\n')
        for html, (id_, emoticon) in emojis.items():
            t += (
                f"{html} : {code(id_)}\n{code(html)}\n"
                f"{code(html.replace(q1, q2))}\n"
                f"{code(html.replace(q1, ''))}\n"
                f"{code(f'emoji({id_}, {q1}{emoticon}{q1})')}\n"
                f"{code(f'emoji({id_}, {q2}{emoticon}{q2})')}\n"
                f"\n\n"
            )
            
        await msg.edit(t)

    
    @cmd('et')
    async def _et(_, msg):
        if len(msg.text.split()) > 1:
            text = msg.text.split(maxsplit=1)[1]

        r = msg.reply_to_message

        t = (text or getattr(msg.quote, 'text', None) or getattr(r, 'text')).lower() 
        tr = t.maketrans(emojis)
        t = t.translate(tr)

        await msg.edit(t)

    @cmd('set_gef_api_data')
    async def _set_gef_api_data(_, msg: M):
        try:
            client_id, api_key = get_args(msg).split()
            int(client_id)
        except:
            return await msg.edit("Неверный ввод")
    
        await mod.db.set('api_data', {'client_id': client_id, 'api_key': api_key})
        await msg.edit('Готово!')
    
    @cmd('gef')
    async def _gef(_, msg: M):
        try:
            html = getattr(msg.text, 'html', None) or getattr(msg.caption, 'html', None) or ''
            if r := msg.reply_to_message:
                html += getattr(getattr(msg.quote, 'text', None), 'html', None) or getattr(r.caption, 'html', None) or getattr(r.text, 'html', None) or ''
                
            bs = BeautifulSoup(html, 'lxml')
            emjs = bs.find_all('emoji')
            
            emojis = {}
            for emj in emjs:
                emojis[str(emj)] = int(emj.attrs['id'])

            stickers = await app.get_custom_emoji_stickers(list(emojis.values()))
            for emoji, sticker in zip(emojis.keys(), stickers):
                if sticker.mime_type == 'image/webp':
                    file = await app.download_media(sticker, in_memory=True)
                    file.name = f'{sticker.file_id}.png'
                    am= await msg.reply_photo(file, caption=emoji)
                    await am.reply_document(file, caption='В виде файла', quote=True, force_document=True)
                elif sticker.mime_type == 'video/webm':
                    file = await app.download_media(sticker, in_memory=True)
                    file.name = f'{sticker.file_id}.gif'
                    am = await msg.reply_animation(file, caption=emoji)
                    await am.reply_document(file, caption='В виде файла', quote=True, force_document=True)
                elif sticker.mime_type == 'application/x-tgsticker':
                    api_data = await mod.db.get('api_data', {})
                    if not api_data:
                        return await msg.edit('api_data не задана! Конвертация невозможна.')
                    
                    t = f"Конвертирую емодзи {emoji}. Это займет около минуты."
                    lm = await msg.reply(t)
                    
                    file_path = mod.path / f'{int(time.time())}{generate_random_identifier(5)}.tgs'
                    out_path  = mod.path / f'{int(time.time())}{generate_random_identifier(5)}.gif'
                    await app.download_media(sticker, file_path)
                    
                    async def loading(status, percents, error_message):
                        try:
                            if percents:
                                await lm.edit(t+f'\nКонвертация {percents}%')
                            else:
                                if status == 'error':
                                    await lm.edit(t+f'\nОшибка! {error_message}')
                                else:
                                    await lm.edit(t+f'\nСтатус конвертации: {status}')
                        except MessageNotModified:
                            pass
                    
                    await convert(file_path, out_path, loading=loading)
                    am = await lm.reply_animation(out_path, caption=emoji, quote=True)
                    await am.reply_document(out_path, caption='В виде файла', quote=True, force_document=True)
                    try_(os.remove(out_path))
                else:
                    await msg.reply(f"Упс! Формат емодзи {emoji} ({sticker.mime_type}) не поддерживается!")
        except:
            await msg.edit(f"Ошибка!\n{await paste(format_exc())}")
