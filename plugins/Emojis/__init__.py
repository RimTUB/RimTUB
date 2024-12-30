from utils import *


__libs__ = ('bs4', 'beautifulsoup4'), 'lxml'

async def main(app: Client, mod: Module):

    from bs4 import BeautifulSoup

    cmd = mod.cmd

    @cmd(['emj', 'emjs'])
    async def _emj(_, msg):
        html = getattr(msg.text, 'html', None) or getattr(msg.caption, 'html', None) or ''
        if r := msg.reply_to_message:
            html += getattr(msg.quote_text, 'html', None) or getattr(r.caption, 'html', None) or getattr(r.text, 'html', None) or ''
            
        bs = BeautifulSoup(html, 'lxml')
        emjs = bs.find_all('emoji')
        
        emojis = {}
        for emj in emjs:
            emojis[str(emj)] = (emj.attrs['id'])
        
        q1 = '"'
        q2 = "'"
        
        t = b('Custom Emojis:\n')
        for html, id_ in emojis.items():
            t += f"{html} : {code(id_)}\n{code(html)}\n{code(html.replace(q1, q2))}\n\n"
            
        await msg.edit(t)
        

helplist.add_module(
    HModule(
        __package__,
        description="Смотреть айди премиум емодзи",
        author='built-in (@RimMirK)',
        version='1.0.1'
    ).add_command(
        Command(['emj', 'emjs'], [Arg('текст с емодзи и/или ответ на сообщение с емодзи')], 'показать айди емодзи')
    )
)