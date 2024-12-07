from utils import *

__libs__ = 'googletrans==3.1.0a0',

async def main(app):

    from googletrans import Translator, LANGUAGES
    
    translator = Translator()

    cmd = app.cmd(app.get_group(__package__))

    LANGS = ''
    for key, lang in LANGUAGES.items():
        LANGS += f"{code(key)}: {lang}\n"

    @cmd(['tr', 'translate'])
    async def _tr(_, msg):
        try:
            _, ln, *text = (msg.text or msg.caption).split(maxsplit=2)
            if text == []:
                if msg.reply_to_message:
                    text = msg.quote_text or msg.reply_to_message.text
                else:
                    return await msg.edit("Неверный ввод данных!")
        
            tr = translator.translate(text, ln)
            await msg.edit(
                f"{b(tr.src)}:\n{bq(text)}\n{b(tr.dest)}:\n{bq(tr.text)}"
            )
        except Exception as e:
            if 'text' not in locals().keys():
                return await msg.edit("Неверный ввод данных!")
            await msg.edit(f"{bq(text)}\n{b(f'{e.__class__.__name__}')}: {bq(str(e))}")
            
    @cmd(['trf', 'translatefrom', 'trfrom'])
    async def _trf(_, msg):
        _, src, ln, *text = (msg.text or msg.caption).split(maxsplit=3)
        if text == []:
            if msg.reply_to_message:
                text = msg.quote_text or msg.reply_to_message.text
            else:
                return await msg.edit("Неверный ввод данных!")
        else:
            text = text[0]
        
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
    Module(
        __package__,
        description="Google переводчик",
        author="built-in (@RimMirK)",
        version="1.1.2",
    ).add_command(
        Command(['tr', 'translate'], [Arg("целевой язык"), Arg("текст/ответ")], "Перевести текст")
    ).add_command(
        Command(['trf', 'translatefrom', 'trfrom'], [Arg("Язык оригинала"), Arg("целевой язык"), Arg("текст/ответ")], "Перевести текст")
    ).add_command(
        Command(['trlangs'], [], "Список языков и их код")
    )
)