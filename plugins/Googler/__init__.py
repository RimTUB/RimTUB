from pyrogram.types import Message, LinkPreviewOptions
from utils import *
from googlesearch import search
from urllib.parse import urlparse


async def main(app: Client, mod: Module):


    cmd = mod.cmd

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
                lang=kwargs.get('-l',   await mod.db.get('lang',   'ru')),
                region=kwargs.get('-r', await mod.db.get('region', None)),
                num_results=int(kwargs.get('-c', 10)),
                safe='-unsafe' not in args
            ):
                t += bq(
                    a(b(r.title) + " · " + urlparse(r.url).netloc, r.url, False) + "\n" + 
                    r.description, True, False
                ) + '\n\n'
            await msg.edit(t, LinkPreviewOptions(is_disabled=True))
        except Exception as e:
            await msg.edit(b(f"Произошла ошибка! {e}"))
    
    @cmd('glang')
    async def _glang(_, msg: Message):
        lang = get_args(msg.text)
        if not lang:
            return await msg.edit(b("Введи значение!"))
        await mod.db.set('lang', lang)
        await msg.edit(b(f"Язык обновлен на {lang}!"))
    
    
    @cmd(['gregion', 'greg'])
    async def _gregion(_, msg: Message):
        region = get_args(msg.text)
        if not region:
            return await msg.edit(b("Введи значение!"))
        await mod.db.set('region', region)
        await msg.edit(b(f"Регион обновлен на {region}!"))