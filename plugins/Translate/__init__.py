from traceback import print_exc
from utils import *

__libs__ = [['googletrans', 'googletrans==3.1.0a0']]


def extract_text(msg, offset):
    if msg.text:
        if offset == 2:
            _, _, *text = msg.text.split(maxsplit=2)
        elif offset == 3:
            _, _, _, *text = msg.text.split(maxsplit=3)
        text = " ".join(text) if text else None
    if text:
        return text
    if msg.quote_text:
        return msg.quote_text
    elif msg.reply_to_message and msg.reply_to_message.text:
        return msg.reply_to_message.text
    elif msg.reply_to_message and msg.reply_to_message.caption:
        return msg.reply_to_message.caption
    return None

async def main(app: Client, mod: Module):

    from googletrans import Translator, LANGUAGES
    
    translator = Translator()

    cmd = mod.cmd

    LANGS = ''
    for key, lang in LANGUAGES.items():
        LANGS += f"{code(key)}: {lang}\n"

    @cmd(['tr', 'translate'])
    async def _tr(_, msg):
        try:
            _, ln, *__ = msg.text.split(maxsplit=2)
            
            text = extract_text(msg, 2)
            if text is None:
                return await msg.edit("Неверный ввод данных! 1")
        
            tr = translator.translate(text, ln)
            await msg.edit(
                f"{b(tr.src)}:\n{bq(text)}\n{b(tr.dest)}:\n{bq(tr.text)}"
            )
        except Exception as e:
            print_exc()
            if 'text' not in locals().keys():
                return await msg.edit("Неверный ввод данных! 2 ")
            await msg.edit(f"{bq(text)}\n{b(f'{e.__class__.__name__}')}: {bq(str(e))}")
            
    @cmd(['trf', 'translatefrom', 'trfrom'])
    async def _trf(_, msg):
        _, src, ln, *__ = (msg.text or msg.caption).split(maxsplit=3)

        text = extract_text(msg, 3)
        if text is None:
            return await msg.edit("Неверный ввод данных! 1")
        
        try:
            tr = translator.translate(text, ln, src)
            await msg.edit(
                f"{b(tr.src)}:\n{bq(text)}\n{b(tr.dest)}:\n{bq(tr.text)}"
            )
        except Exception as e:
            if 'text' not in locals().keys():
                return await msg.edit("Неверный ввод данных!")
            await msg.edit(f"{bq(text)}\n{b(f'{e.__class__.__name__}')}: {bq(str(e))}")

    @cmd('trlangs')
    async def _trlangs(_, msg):
        await msg.edit(b("Доступные языки:\n")+LANGS) 
        

helplist.add_module(
    HModule(
        __package__,
        description="Google переводчик",
        author="built-in (@RimMirK)",
        version="1.1.4",
    ).add_command(
        Command(['tr', 'translate'], [Arg("целевой язык"), Arg("текст/ответ")], "Перевести текст")
    ).add_command(
        Command(['trf', 'translatefrom', 'trfrom'], [Arg("Язык оригинала"), Arg("целевой язык"), Arg("текст/ответ")], "Перевести текст")
    ).add_command(
        Command(['trlangs'], [], "Список языков и их код")
    )
)