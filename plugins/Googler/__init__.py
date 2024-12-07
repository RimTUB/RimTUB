from pyrogram.types import Message
from utils import *

__libs__ = ('googlesearch', 'googlesearch-python'),

helplist.add_module(
    Module(
        __package__,
        description='Поиск в Google',
        author='built-in (@RimMirK)',
        version='1.0'
    ).add_command(
        Command(['g', 'google'], [
            Argument('запрос'),
            Argument('-c кол-во результатов', False),
            Argument('-r регион',             False),
            Argument('-l язык',               False),
            Argument('-unsafe (выкл безопасный режим)', False),
        ], "Загуглить" )
    ).add_command(
        Command('glang', [Argument("код языка")], "Установить язык результатов")
    ).add_command(
        Command(['gregion', 'greg'], [Argument("код страны/региона")], "Установить регион результатов")
    )
)

async def main(app: Client):

    from googlesearch import search
    from urllib.parse import urlparse

    cmd = app.cmd(app.get_group(__package__))

    @cmd(['g', 'google'])
    async def _google(_, msg):
        await msg.edit(b("Загрузка..."))
        try:
            request, args, kwargs = parse_args(get_args(msg.text))
            request = ' '.join(request)
            if not request:
                return await msg.edit(b("Введи запрос!"))
            t = f'{bq(request)}\n\n'
            for r in search(
                request,
                advanced=True,
                lang=kwargs.get('-l',   await app.db.get(__package__, 'lang',   'ru')),
                region=kwargs.get('-r', await app.db.get(__package__, 'region', None)),
                num_results=int(kwargs.get('-c', 10)),
                safe='-unsafe' not in args
            ):
                t += bq(
                    a(b(r.title) + " · " + urlparse(r.url).netloc, r.url, False) + "\n" + 
                    r.description, True, False
                ) + '\n\n'
            await msg.edit(t, disable_web_page_preview=True)
        except Exception as e:
            await msg.edit(b(f"Произошла ошибка! {e}"))
    
    @cmd('glang')
    async def _glang(_, msg: Message):
        lang = get_args(msg.text)
        if not lang:
            return await msg.edit(b("Введи значение!"))
        await app.db.set(__package__, 'lang', lang)
        await msg.edit(b(f"Язык обновлен на {lang}!"))
    
    
    @cmd(['gregion', 'greg'])
    async def _gregion(_, msg: Message):
        region = get_args(msg.text)
        if not region:
            return await msg.edit(b("Введи значение!"))
        await app.db.set(__package__, 'region', region)
        await msg.edit(b(f"Регион обновлен на {region}!"))