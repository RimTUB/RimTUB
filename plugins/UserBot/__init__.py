import sys, time

from pyrogram import __version__
from pyrogram.types import Message as M, LinkPreviewOptions as LPO

from utils import *



def build_module_help_text(mod, section_name='_', header=True):
    help_text = (
        ((HEADER + '\n\n' if Config.SHOW_HEADER_IN_HELP else '') if header else '') +
        f"Модуль {b(mod.name)}\n\n" + "<blockquote>" +
        ((b(f"Версия: ") + str(mod.version) + "\n") if mod.version else '') +
        ((b(f"Автор: ") + str(mod.author) + "\n") if mod.author else '') +
        ((b(f"Описание:\n") + str(mod.description)) if mod.description else '') +
        "</blockquote>" +
        ("\n\n\n" if any((mod.version, mod.author, mod.description)) else '')
    )

    section = mod.get_sections().get(section_name)
    if section_name != '_':
        help_text += f"Секция: {b(section_name)}" + "\n"
        help_text += (section.description or '') + '\n\n\n'

    help_text += b(f"Команды ({section.get_commands_count()}):") + "\n"
    help_text += "<blockquote>"
    if section.get_commands_count() > 0:
        help_text += '\n'
        for c in section.get_commands():
            help_text += (
                "" + b(c.description) + "\n" +
                "" + ("|".join((code(Config.PREFIX + command) for command in c.commands))) + " " +
                (" ".join(list(map(escape, c.args)))) + '\n\n'
            )
    else:
        help_text += "Нет команд в этой секции.\n"
    
    help_text += "</blockquote>"


    help_text += '\n'

    

    help_text += b(f"Возможности ({section.get_features_count()}):") + "\n"
    help_text += "<blockquote>"
    if section.get_features_count() > 0:
        help_text += '\n'
        for f in section.get_features():
            help_text += "" + b(f.name) + ":\n"
            help_text += "" + "\n".join(map(escape, f.description.split('\n')))
            help_text += "\n\n"
    else:
        help_text += "Нет возможностей в этой секции.\n"

    
    help_text += "</blockquote>"

    

    # other_sections = [sec for sec_name, sec in mod.get_sections().items() if sec_name != section_name]
    # help_text += b(f"Другие секции ({len(other_sections)}):") + "\n"
    # help_text += "<blockquote>"
    # if other_sections:
    #     help_text += '\n'
    #     for sec in other_sections:
            
    #         commands_count = sec.get_commands_count()
    #         features_count = sec.get_features_count()

    #         if sec.name != '_':
    #             section_text = b(f"{sec.name} ")
    #         else:
    #             section_text = b(f"Основная секция ")

    #         if commands_count > 0:
    #             section_text += f" ({commands_count} {plural(commands_count, ('команда', 'команды', 'команд'))}"
            
    #         if features_count > 0:
    #             if commands_count > 0:
    #                 section_text += ' и '
    #             else:
    #                 section_text += '('
    #             section_text += f"{features_count} {plural(features_count, ('возможность', 'возмоожности', 'возможностей'))})"
    #         else:
    #             if commands_count > 0:
    #                 section_text += ')'
            
    #         if sec.name != '_':
    #             section_text += f"\n{code(Config.PREFIX + 'h ' + mod.name + ':' + sec.name)} чтобы открыть"
    #             help_text += section_text + "\n\n"
    #         else:
    #             section_text += f"\n{code(Config.PREFIX + 'h ' + mod.name)} чтобы открыть"
    #             help_text += section_text + "\n\n"
    # else:
    #     help_text += "Нет других секций в этом модуле.\n"

        
    # help_text += "</blockquote>"

    help_text += f"\n\n{b('Легенда: ')}\n   {code('< >')} – обязательный аргумент\n   {code('[ ]')} – необязательный аргумент.\n   {code(' / ')} – или"

    return help_text



async def main(app: Client, mod: Module):

    cmd = mod.cmd

    @mod.on_ready
    async def _onr(app):

        with open('logs/last_run.log', encoding='utf-8') as f:
            link = await paste(f.read(), 'log')

        buttons = Buttons([
            [Button('Посмотреть лог запуска', callback_data='show_log', extra_data={'log': link})]
        ])

        if len(sys.argv) >= 2:
            _, type_, *values = sys.argv
            if type_ == 'restart':
                app_hash, time_, chat_id, msg_id = values
                if app.app_hash != app_hash:
                    return  
                now = time.perf_counter()
                delta = now - float(time_)
                await mod.send_buttons(int(chat_id), f"Перезапущено за <b>{delta:.2f}s.</b>", buttons)
                await app.delete_messages(int(chat_id), int(msg_id))
        else:
            if not Config.DISABLE_STARTUP_MESSAGE:
                await mod.send_buttons('me', f'<b>RimTUB {Config.VERSION} Запущен!</b>\nПрефикс: «<code>{escape(Config.PREFIX)}</code>»', buttons)
            
            

    @mod.callback('show_log')
    async def _show_log(c: C):
        if c.from_user.id != app.me.id:
            return c.answer('Это не твоя кнопка!', True)
        await c.edit_message_text(f"Лог запуска: {c.extra_data.get('log')}")
        
    @mod.callback(startswith='module:')
    async def _module(c: C):
        _, module, section = c.data.split(':')
        
        modul = helplist.get_module(module)
        
        buttons_list = []   
        for sect in modul.get_sections().keys():
            buttons_list.append([Button('Главная секция' if sect == '_' else sect, f'module:{module}:{sect}')])
        buttons = await mod.prepare_buttons(Buttons(buttons_list, c.extra_data))
        
        await c.edit_message_text(remove_emoji_tags(build_module_help_text(modul, section)), reply_markup=buttons, link_preview_options=LPO(is_disabled=True))


    @cmd(['help', 'h'])
    async def _help(_, msg: M):
        mod_name = get_args(msg.text or msg.caption).lower()

        if mod_name:
            modn = mod_name.split(':')[0]
            modul = helplist.get_module(modn, lower=True)
            if not modul:
                return await msg.edit(f"Модуль {mod_name} не найден!\nПосмотреть список модулей: {code(Config.PREFIX+'help')}")
            
            section_name = mod_name.split(':')[1] if ':' in mod_name else '_'

            other_sections = [sec for sec_name, sec in modul.get_sections().items() if sec_name != section_name]
            
            if other_sections:
                
                buttons_list = []
                for sect in modul.get_sections().keys():
                    buttons_list.append([Button('Главная секция' if sect == '_' else sect, f'module:{modul.name}:{sect}')])
                buttons = Buttons(buttons_list)
                
                await mod.send_buttons(
                    msg.chat.id,
                    remove_emoji_tags(build_module_help_text(modul, section_name)),
                    buttons, dict(link_preview_options=LPO(is_disabled=True))
                )
                await msg.delete()
            else:
                await msg.edit(build_module_help_text(modul, section_name))
            
            return 

        help_text = (HEADER + "\n" if Config.SHOW_HEADER_IN_HELP else '') + f"\nМодули (плагины): {b(helplist.get_modules_count())}\n"
        commands_count, features_count = 0, 0
        help_text += '<blockquote>'
        for module in helplist.get_modules():
            _commands_count = module.get_commands_count()
            _features_count = module.get_features_count()
            commands_count += _commands_count
            features_count += _features_count

            help_text += (
                (
                    f"{code(f'{Config.PREFIX}h {module.name}')}   "
                    if Config.SHOW_MODULES_WITH_COMMAND_IN_HELP
                    else f"  {code(module.name)}   "
                )+
                (f"({b(_commands_count)} {plural(_commands_count, ('команда', 'команды', 'команд'))}" if _commands_count > 0 else '(') +
                (' и ' if _commands_count > 0 and _features_count > 0 else '') +
                (f"{b(_features_count)} {plural(_features_count, ('возможность', 'возмоожности', 'возможностей'))})\n" if _features_count > 0 else ')\n')
            )
        help_text += '</blockquote>\n'
        help_text += (
            f"всего {b(commands_count)} {plural(commands_count, ('команда', 'команды', 'команд'))} и \n"
            f"{b(features_count)} {plural(features_count, ('возможность', 'возмоожности', 'возможностей'))}\n"
            f'\nДля получения списка команд модуля\nиспользуйте {code(Config.PREFIX+"help")} [название модуля]'
        )

        await msg.edit(help_text)

    @cmd(['me', 'start', 'menu'])
    async def _me(_, msg: M):
        me_text = (
            HEADER + '\n'
            f"Версия: {b( Config.VERSION )}\n"
            f"Разработчик: {b(a('@RimMirK', 'https://t.me/RimMirK'), False)}\n"
            f"Канал: {b(a('@RimTUB', 'https://t.me/RimTUB'), False)}\n"
            f"Время работы: {b( sec_to_str(time.perf_counter() - bot_uptime))}\n"
            f"\n"
            f"{emoji(5418368536898713475, '🐍')} Python: {b( sys.version.split()[0] )}\n"
            f"{emoji(5246743576485832125, '🔥')} Pyrogram: {b( __version__ )}\n"
            f"{emoji(5215186239853964761, '💿')} ОС: {b( sys.platform )}\n"
            f"\n"
            f"Модули (плагины): {b(helplist.get_modules_count())}\n"
            f"Всего команд: {b(sum([*map(lambda i: i.get_commands_count(), helplist.get_modules())]))}\n"
            f"Всего возможностей: {b(sum([*map(lambda i: i.get_features_count(), helplist.get_modules())]))}"
        )
        await msg.edit(me_text)


    @cmd(['restart', 'reload'])
    async def _resatrt(app, msg):
        await msg.edit("Перезагружаюсь...")
        restart(app.app_hash, msg.chat.id, msg.id)

       