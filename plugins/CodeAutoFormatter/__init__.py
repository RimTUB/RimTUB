from utils import *




async def main(app: Client, mod: Module):

    cmd = mod.cmd

    @cmd(["caf"])
    async def _caf(_, msg):
        r = msg.reply_to_message
        if not r:
            return await msg.edit(emoji(5240241223632954241, '🚫') + " Ответь на сообщение!")
        f = r.edit if r.outgoing else msg.edit
        await f(pre(r.text or r.caption, get_args(msg.text) or ""))
        if r.outgoing: await msg.delete()