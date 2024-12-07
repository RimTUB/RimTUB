from typing import overload, Awaitable

from pyrogram.raw.types import UpdateNewChannelMessage

from telebot.types import (
    InlineQuery, CallbackQuery as C, 
    InlineQueryResultArticle as RArticle, InputTextMessageContent as TMC,
    InlineKeyboardMarkup as IM, InlineKeyboardButton as IB
)

from utils.misc import _objects
from utils import ModifyPyrogramClient, clients
from pyrogram import Client


__all__ = [
    'create_buttons',
    'format_callback',
    '_load_bot_helper_handlers'
]


async def create_buttons(app: ModifyPyrogramClient | Client, chat_id: int|str, formatted_callback: str, **kwargs) -> None:
    """
    Автоматически создает сообщение с кнопками.

    ## Example:
    .. code-block:: python
        async def buttons(app, c, text):
            await app.bot.edit_message_text(
                text, reply_markup=get_rm(app),
                inline_message_id=c.inline_message_id
            )

        create_buttons(app, msg.chat.id, format_callback(app, buttons, text='hello'))

    Подробнее смотри в документации в разделе кнопок.

    :param ModifyPyrogramClient | Client app: объект клиента.
    :param chat_id int | str: id чата, в котором создать кнопки.
    :param formatted_callback: форматированная колбек дата.
    :param **kwargs: параметры для передачи send_inline_bot_result
    :return None:

    """
    callback = format_callback(
        app, lambda app, i: app.bot.answer_inline_query(i.id, [RArticle(0, '.', TMC('⏳'), reply_markup=IM().add(IB("⏳",callback_data=formatted_callback)))])
    )
    r = await app.get_inline_bot_results(app.bot_username, callback)
    u = await app.send_inline_bot_result(chat_id, r.query_id, '0', **kwargs)
    for upd in u.updates:
        if hasattr(upd, 'message'):
            m = upd.message
            break
    await app.request_callback_answer(chat_id, m.id, m.reply_markup.rows[0].buttons[0].data)


@overload
def format_callback(app: ModifyPyrogramClient | Client, func: Awaitable, is_personal: bool=True, *args, **kwargs) -> str: ...
@overload
def format_callback(user_id: int, func: Awaitable, is_personal: bool=True, *args, **kwargs) -> str: ...

def format_callback(user: int | ModifyPyrogramClient | Client, func: Awaitable, is_personal: bool=True, *args, **kwargs) -> str:
    """
    Форматирует строку callback_data. Нужно для правильного составления кнопок.

    ## Example:
    .. code-block:: python
        async def click(app, c, text):
            print(text) # hello

        format_callback(app, buttons, text='hello')

    Подробнее смотри в документации в разделе кнопок.

    :param int | ModifyPyrogramClient | Client user: ID клиента 
        или объект клиента, который инициировал запрос.
    :param Awaitable func: вызываемая асинхронная функция-обработчик.
    :param bool is_personal: True если кнопка для тебя (по умолчанию).
        Если False - ее может нажать кто угодно.
    :param *args: позиционные аргументы для передачи обработчику.
    :param **kwargs: именные аргументы для передачи обработчику.
    :return str: callback_data для подстановки в кнопку.


    """
    args_id = id(args)
    func_id = id(func)
    kwargs_id = id(kwargs)
    _objects[func_id] = func
    _objects[args_id] = args
    _objects[kwargs_id] = kwargs
    return f"0:{user if isinstance(user, int) else user.me.id}:{int(is_personal)}:{func_id}:{args_id}:{kwargs_id}"


def _load_bot_helper_handlers(bot):
    @bot.inline_handler(lambda i: i.query.startswith('0:'))
    async def _all_inline(i: InlineQuery):
        _, user_id, is_personal, func_id, args_id, kwargs_id = map(int, i.query.split(':'))
        if is_personal:
            if i.from_user.id != user_id:
                return
        func = _objects[func_id]
        args = _objects[args_id]
        kwargs = _objects[kwargs_id]
        for client in clients:
            if client.me.id == user_id:
                await func(client, i, *args, **kwargs)
                break
                

    @bot.callback_query_handler(lambda c: c.data.startswith('0:'))
    async def _all_callback(c: C):
        _, user_id, is_personal, func_id, args_id, kwargs_id = map(int, c.data.split(':'))
        if is_personal:
            if c.from_user.id != user_id:
                return await bot.answer_callback_query(c.id, "❗️Это не твоя кнопка!", True)
        try:
            func = _objects[func_id]
            args = _objects[args_id]
            kwargs = _objects[kwargs_id]
        except KeyError:
            await bot.answer_callback_query(c.id, "Упс! Функция не найдена! Возможно, Вы пытаетесь нажать на кнопку после перезагрузки RimTUB", True)

        for client in clients:
            if client.me.id == user_id:
                await func(client, c, *args, **kwargs)
                break
        await bot.answer_callback_query(c.id)



