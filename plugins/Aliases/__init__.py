from utils import *



def find_callback_by_command(app, command):
    
    groups = app.dispatcher.groups
    for group in groups:
        for handler in app.dispatcher.groups[group]:
            try:
                if command in handler.filters.base.base.commands:
                    return handler.original_callback
            except: pass
    

async def main(app: Client, mod: Module):

    cmd = mod.cmd


    @mod.on_ready
    async def _onr(_):
        aliases = await mod.db.get('aliases', {})

        for alias, command in aliases.items():

            callback = find_callback_by_command(app, command)
            if callback:
                exec(f"@cmd(alias)\n"
                     f"async def _{command}_alias_{alias}(app, msg):\n"
                     "    await callback(app, msg)", dict(callback=callback),
                     dict(cmd=cmd, alias=alias, callback=callback))
            else:
                mod.logger.warning(f"Aliases: command {command} not found! Alias {alias} can't be created")
    

    @cmd('addalias')
    async def _addalias(_, msg):
        try:    
            _, alias, command = msg.text.split(maxsplit=2)
            
            callback = find_callback_by_command(app, command)
            if callback:
                @cmd(alias)
                async def _alias(_, msg): await callback(app, msg)

                aliases: dict = await mod.db.get('aliases', {})
                aliases.update({alias: command})
                await mod.db.set('aliases', aliases)

                await msg.edit(f"Алиас добавлен!\n"
                               f"<code>{Config.PREFIX}{alias}</code>  <code>-></code>  "
                               f"<code>{Config.PREFIX}{command}</code>")
            else:
                await msg.edit("Команда не найдена!")
        except:
            await msg.edit(f"Используй <code>{Config.PREFIX}{msg.command[0]}</code> " + escape("<алиас> <команда>"))
    
    @cmd('delalias')
    async def _delalias(_, msg):
        try:
            _, alias = msg.text.split(maxsplit=1)
            
            aliases: dict = await mod.db.get('aliases', {})
            del aliases[alias]
            await mod.db.set('aliases', aliases)

            await msg.edit(f"Алиас <b>{alias}</b> удален! Перезагрузи юб для приминения!")
        except:
            await msg.edit(f"Используй <code>{Config.PREFIX}{msg.command[0]}</code> " +escape("<алиас>"))

    @cmd('aliases')
    async def _aliases(_, msg):
        aliases: dict = await mod.db.get('aliases', {})
        t = b("Твои алиасы:\n")
        for alias, command in aliases.items():
            t += code(Config.PREFIX+alias) + '  ' + code('->') + '  ' + code(Config.PREFIX+command) + '\n'
        await msg.edit(t)

