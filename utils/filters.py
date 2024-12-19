from typing import List

from pyrogram.filters import *


__all__ = [
    'account_filter',
    'text_filter',
    'thread_filter'
]


def account_filter(id: int) -> Filter:
    """
    Создает фильтр для проверки на ID клиента

    :param int id: ID клиента: `ModifyPyrogramClient.me.id`.
    :return Filter: Фильтр, который проверяет, совпадает ли идентификатор пользователя с указанным.
    """
    return create(lambda _, app, __: app.me.id == id)

def text_filter(text: str | List[str]) -> Filter:
    """
    Создает фильтр для проверки текста сообщения.

    :param str|List[str] text: Текст или список текстов для фильтрации.
    :return Filter: Фильтр, который проверяет, совпадает ли текст сообщения с указанным.
    """
    return create(lambda _, __, msg: msg.text and msg.text in (text if isinstance(text, list) else [text]))

def thread_filter(message_thread_id: int) -> Filter:
    """
    Создает фильтр для проверки топика.

    :param int message_thread_id: ID топика: `Message.message_thread_id`.
    :return Filter: Фильтр, который проверяет, совпадает ли идентификатор потока с указанным.
    """
    return create(lambda _, __, msg: msg.message_thread_id == message_thread_id)
