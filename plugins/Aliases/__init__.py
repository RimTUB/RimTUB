from utils import *



helplist.add_module(
    Module(
        __package__,
        description='Управление алиасами комманд',
        author='built-in (@RimMirK)',
        version='beta_1.0.0'
    ).add_command(
        Command('addalias', [Arg('алиас'), Arg("Команда")], 'Добавить алиас')
    ).add_command(
        Command('delalias', [Arg('алиас')], 'Удалить алиас')
    ).add_command(
        Command('aliases', [], 'Посмотреть алиасы')
    )
)


def find_callback_by_command(app, command):
    
    groups = app.dispatcher.groups
    for group in groups:
        for handler in app.dispatcher.groups[group]:
            try:
                if command in handler.filters.base.base.commands:
                    return handler.original_callback
            except: pass
    

async def main(app: Client):

    M = __package__

    group = app.get_group(M)
    cmd = app.cmd(group)


    @app.on_ready(group)
    async def _onr(_):
        aliases = await app.db.get(M, 'aliases', {})

        for alias, command in aliases.items():

            callback = find_callback_by_command(app, command)
            if callback:
                exec(f"@cmd(alias)\n"
                     f"async def _{command}_alias_{alias}(app, msg):\n"
                     "    await callback(app, msg)", dict(callback=callback),
                     dict(cmd=cmd, alias=alias, callback=callback))
            else:
                app.logger.warning(f"Aliases: command {command} not found! Alias {alias} can't be created")
    

    @cmd('addalias')
    async def _addalias(_, msg):
        try:    
            _, alias, command = msg.text.split(maxsplit=2)
            
            callback = find_callback_by_command(app, command)
            if callback:
                @cmd(alias)
                async def _alias(_, msg): await callback(app, msg)

                aliases: dict = await app.db.get(M, 'aliases', {})
                aliases.update({alias: command})
                await app.db.set(M, 'aliases', aliases)

                await msg.edit(f"Алиас добавлен!\n"
                               f"<code>{PREFIX}{alias}</code>  <code>-></code>  "
                               f"<code>{PREFIX}{command}</code>")
            else:
                await msg.edit("Команда не найдена!")
        except:
            await msg.edit(f"Используй <code>{PREFIX}{msg.command[0]}</code> " + escape("<алиас> <команда>"))
    
    @cmd('delalias')
    async def _delalias(_, msg):
        try:
            _, alias = msg.text.split(maxsplit=1)
            
            aliases: dict = await app.db.get(M, 'aliases', {})
            del aliases[alias]
            await app.db.set(M, 'aliases', aliases)

            await msg.edit(f"Алиас <b>{alias}</b> удален! Перезагрузи юб для приминения!")
        except:
            await msg.edit(f"Используй <code>{PREFIX}{msg.command[0]}</code> " +escape("<алиас>"))

    @cmd('aliases')
    async def _aliases(_, msg):
        aliases: dict = await app.db.get(M, 'aliases', {})
        t = b("Твои алиасы:\n")
        for alias, command in aliases.items():
            t += code(PREFIX+alias) + '  ' + code('->') + '  ' + code(PREFIX+command) + '\n'
        await msg.edit(t)

