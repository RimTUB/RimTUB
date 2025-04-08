from pyrogram.types import Message
from utils import *



async def main(app, mod: Module):

    cmd = mod.cmd

    @cmd(["addnote", 'setnote'])
    async def _naddnote(app: Client, msg: Message):
        r = msg.reply_to_message
        if not r:
            return await msg.edit(b("Ответь на сообщение!"))
        try:
            name = msg.text.split(maxsplit=1)[1]
        except:
            return await msg.edit(b("Напиши название заметки!"))
        saved_msg = await r.copy('me')
        warning_msg = await saved_msg.reply(b("Не удаляй это сообщение! Оно нужно для работы заметок!"), quote=True)
        await mod.db.set(name, saved_msg.id)
        await mod.db.set(f"{name}_warning", warning_msg.id)
        await msg.edit(b("Заметка ") + code(name) + b(" сохранена!"))

    @cmd(['note', 'cnote'])
    async def _nnote(app: Client, msg: Message):
        try:
            name = msg.text.split(maxsplit=1)[1]
        except:
            return await msg.edit(b("Напиши название заметки!"))
        
        note_msg_id = await mod.db.get(name)
        if note_msg_id is None:
            return await msg.edit(b("Заметка ") + code(name) + b(" не найдена!"))
        await app.copy_message(
            msg.chat.id, 'me', note_msg_id,
            reply_to_message_id=msg.reply_to_message_id,
            message_thread_id=msg.message_thread_id
        )
        await msg.delete()

    @cmd(["notes", "mynotes"])
    async def _mynotes(app: Client, msg):
        d = await mod.db.getall()

        if d:
            
            for e in d.copy():
                if e.endswith('_warning'):
                    del d[e]

            m = b('Твои заметки:\n')
            for name, note_msg_id in d.items():
                note_msg = await app.get_messages('me', note_msg_id)
                m += " - " + code(name) + " : "
                if note_msg.text:
                    m += (
                        (note_msg.text[:15].replace("\n", ' ') + '...')
                        if len(note_msg.text) > 15
                        else note_msg.text.replace("\n", ' ')
                    )
                elif note_msg.video:
                    m += i('Видео')
                elif note_msg.photo:
                    m += i("Фото")
                elif note_msg.sticker:
                    m += i("Стикер")
                elif note_msg.animation:
                    m += i("ГИФ")
                elif note_msg.document:
                    m += i("Файл")
                elif note_msg.voice:
                    m += i("ГС")
                elif note_msg.video_note:
                    m += i("Кружочек")
                if note_msg.caption:
                    m += " " + (
                        (note_msg.caption[:15].replace("\n", ' ') + '...')
                        if len(note_msg.caption) > 15
                        else note_msg.caption.replace("\n", ' ')
                    )
                m += '\n'
                
                
            
        else:
            m = b('пусто!')
        await msg.edit(m)

    @cmd("delnote")
    async def _delnote(app: Client, msg):
        try:
            name = msg.text.split(maxsplit=1)[1]
        except:
            return await msg.edit(b("Напиши название заметки!"))

        note_msg_id = await mod.db.get(name)
        if note_msg_id is None:
            return await msg.edit(b("Заметка не найдена!"))
        
        await app.delete_messages('me', note_msg_id)
        await app.delete_messages('me', await mod.db.get(f"{name}_warning"))
        
        await mod.db.remove(name)
        await mod.db.remove(f"{name}_warning")

        await msg.edit(b("Заметка ") + code(name) + b(" удалена!"))