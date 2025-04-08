from utils import *

from .scheme import emojis




async def main(app: Client, mod: Module):

    cmd = mod.cmd


    @cmd('et')
    async def _et(_, msg):
        if len(msg.text.split()) > 1:
            text = msg.text.split(maxsplit=1)[1]

        r = msg.reply_to_message

        t = (text or getattr(msg.quote, 'text', None) or getattr(r, 'text')).lower() 
        tr = t.maketrans(emojis)
        t = t.translate(tr)

        await msg.edit(t)
