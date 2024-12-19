import sys, time

from pyrogram import __version__
from pyrogram.types import Message as M

from telebot.types import (
    CallbackQuery as C, 
    InlineQueryResultArticle as RArticle, InputTextMessageContent as TMC,
    InlineKeyboardMarkup as IM, InlineKeyboardButton as IB
)

from utils import *
from main import version
from config import PREFIX, SHOW_HEADER_IN_HELP, DISABLE_STARTUP_MESSAGE


def build_module_help_text(mod, header=True):
    help_text = (
        ((HEADER + '\n\n' if SHOW_HEADER_IN_HELP else '') if header else '') +
        f"Модуль {b(mod.name)}\n\n" +
        (f"Версия: {b(mod.version)}\n" if mod.version else '') +
        (f"Автор: {b(mod.author, False)}\n" if mod.author else '') +
        (f"Описание: {b(mod.description, False)}\n" if mod.description else '') +
        ("\n\n" if any((mod.version, mod.author, mod.description)) else '') +
        b(f"Команды ({mod.get_commands_count()}):") + "\n"
    )
    for c in mod.get_commands():
        help_text += (
            "  " + b(c.description) + "\n" +
            "  " + ("|".join((code(PREFIX+command) for command in c.commands))) + "  " + 
            (" ".join(list(map(escape, c.args)))) + '\n\n'
        )

    help_text += b(f"\nВозможности ({mod.get_features_count()})")
    help_text += ":\n" if mod.get_features_count() > 0 else "\n"
    for f in mod.get_features():
        help_text += "  " + b(f.name) + ":\n"
        help_text += "    " + "\n    ".join(escape(f.description.split('\n')))
        help_text += "\n\n"

    help_text += f"\n{b('Легенда: ')}\n   {code('< >')} – обязательный аргумент\n   {code('[ ]')} – необязательный аргумент.\n   {code(' / ')} – или"

    return help_text

async def click(app: Client, c: C):
    with open('logs/last_run.log', encoding='utf-8') as f:
        lnk = await paste(f.read(), 'log')
    await app.bot.edit_message_text(f"Лог запуска: {lnk}", inline_message_id=c.inline_message_id)

async def restarted(app: Client, i):
    await app.bot.answer_inline_query(i.id, [
        RArticle(0, '.', TMC(f'Перезапущено за <b>{app.st.get("_core.restart.delta", 0):.2f}s.</b>', parse_mode='html'), reply_markup=IM(   
            ).add(IB("посмотреть лог запуска", callback_data=format_callback(app, click))))
    ])

async def started(app: Client, i):
    await app.bot.answer_inline_query(i.id, [
        RArticle(0, '.', TMC(f'<b>RimTUB Запущен!</b>', parse_mode='html'), reply_markup=IM(   
            ).add(IB("посмотреть лог запуска", callback_data=format_callback(app, click))))
    ])

async def main(app: Client):

    cmd = app.cmd(G:=app.get_group(__package__))

    @app.on_ready(G)
    async def _onr(app):
        if len(sys.argv) >= 2:
            _, type_, *values = sys.argv
            if type_ == 'restart':
                app_hash, time_, chat_id, msg_id = values
                if app.app_hash != app_hash:
                    return
                now = time.perf_counter()
                delta = now - float(time_)
                app.st.set('_core.restart.delta', delta)
                r = await app.get_inline_bot_results(app.bot_username, format_callback(app, restarted))
                await app.send_inline_bot_result(int(chat_id), r.query_id, "0")
                await app.delete_messages(int(chat_id), int(msg_id))
        else:
            if not DISABLE_STARTUP_MESSAGE:
                r = await app.get_inline_bot_results(app.bot_username, format_callback(app, started))
                await app.send_inline_bot_result('me', r.query_id, "0")
            

    @cmd(['me', 'start', 'menu'])
    async def _me(_, msg: M):
        me_text = (
            HEADER + '\n'
            f"Версия: {b( version )}\n"
            f"Разработчик: {b(a('@RimMirK', 'https://t.me/RimMirK'), False)}\n"
            f"Канал: {b(a('@RimTUB', 'https://t.me/RimTUB'), False)}\n"
            f"Время работы: {b( sec_to_str(time.perf_counter() - bot_uptime))}\n"
            f"\n"
            f"<emoji id=5418368536898713475>🐍</emoji> Python: {b( sys.version.split()[0] )}\n"
            f"<emoji id=5246743576485832125>🔥</emoji> Pyrogram: {b( __version__ )}\n"
            f"<emoji id=5215186239853964761>💿</emoji> ОС: {b( sys.platform )}\n"
            f"\n"
            f"Модули (плагины): {b(helplist.get_modules_count())}\n"
            f"Всего команд: {b(sum([*map(lambda i: i.get_commands_count(), helplist.get_modules())]))}\n"
            f"Всего возможностей: {b(sum([*map(lambda i: i.get_features_count(), helplist.get_modules())]))}"
        )
        await msg.edit(me_text)



    @cmd(['help', 'h'])
    async def _help(_, msg: M):
        if mod_name := get_args(msg.text or msg.caption).lower():
            mod = helplist.get_module(mod_name, lower=True)
            if not mod:
                return await msg.edit(f"Модуль {mod_name} не найден!\nПосмотреть список модулей: "+code(PREFIX+'help'))
            

            return await msg.edit(build_module_help_text(mod))

        help_text = (
            (HEADER + "\n" if SHOW_HEADER_IN_HELP else '') + 
            "\n"
            f"Модули (плагины): {b(helplist.get_modules_count())}\n"
        )
        commands_count = 0
        features_count = 0
        for module in helplist.get_modules():
            _commands_count = module.get_commands_count()
            _features_count = module.get_features_count()
            commands_count += _commands_count
            features_count += _features_count
            help_text += (
                f"    {code(module.name)}   " + (
                    f"({b(_commands_count)} {plural(_commands_count, ('команда', 'команды', 'команд'))}"
                    if _commands_count > 0 else ''
                ) + (' и ' if _commands_count > 0 and _features_count > 0 else '') + (
                    f"{ b(_features_count)} {plural(_features_count, ('возможность', 'возмоожности', 'возможностей'))})\n"
                    if _features_count > 0 else ')\n'
                )
            )


        help_text += (
            f"(всего {b(commands_count)} {plural(commands_count, ('команда', 'команды', 'команд'))} и \n"
            f"{b(features_count)} {plural(features_count, ('возможность', 'возмоожности', 'возможностей'))})\n"
            f'\nДля получения списка команд модуля\nиспользуйте {code(PREFIX+"help")} [\xa0название\xa0модуля\xa0]'
        )

        await msg.edit(help_text)




    @cmd(['restart', 'reload'])
    async def _resatrt(app, msg):
        await msg.edit("Перезагружаюсь...")
        restart(app.app_hash, msg.chat.id, msg.id)

       



mod = Module(
    __package__,
    description="Главный модуль RimTUB. Помощь и управление тут",
    author="built-in (@RimMirK)",
    version=version
)

mod.add_command(Command(['me', 'start', 'menu'], [], "Открыть стартовое меню"))
mod.add_command(Command(['help', 'h'], [Arg('название модуля', False)], "Получить помощь"))
mod.add_command(Command(['restart', 'reload'], [], "Перезапустить RimTUB"))

helplist.add_module(mod)
