from functools import lru_cache

__all__ = [
    'escape', 'format_tag',
    'code', 'pre', 'emoji', 
    'blockquote', 'bq',
    'b', 'i', 'a', 'u',
    's', 'spoiler',
    'remove_emoji_tags'
]


def cache_with_signature(func):
    
    def wrapper(*args, **kwargs):
        return lru_cache()(func)(*args, **kwargs)
    
    return wrapper

@cache_with_signature
def escape(text: str) -> str:
    """
    Экранирует специальные HTML символы в строке.

    :param str text: Текст для экранирования.
    :return str: Экранированный текст.
    """
    text = str(text)
    chars = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    if text is None:
        return ""
    for old, new in chars.items():
        text = text.replace(old, new)
    return text

@cache_with_signature
def format_tag(tag_name: str, content: str = "", escape_content=True, close_tag=True, **kwargs) -> str:
    """
    Генерирует HTML тег.

    :param str tag_name: Имя тега. Например "a" или "div".
    :param str content: Содержимое тега, defaults to "".
    :param bool escape_content: Нужно ли экранировать контент, defaults to True.
    :param bool close_tag: Нужен ли закрывающий тег, defaults to True.
    :param kwargs: Атрибуты тега. Названия атрибутов можно указывать с "_".
    :return str: Сгенерированный HTML тег.
    """
    return (
        f"""<{escape(tag_name)}{''.join([f' {k.removeprefix("_")}="{escape(v)}"' for k,v in kwargs.items()])}>""" +
        ((escape(content) if escape_content else content) if close_tag else "") +
        ((f"</{escape(tag_name)}>") if close_tag else "")
    )

@cache_with_signature
def code(text: str, escape_html=True) -> str:
    """
    Создает HTML тег для кода.

    :param str text: Код для размещения в теге.
    :param bool escape_html: Нужно ли экранировать HTML в коде, defaults to True.
    :return str: Сгенерированный HTML тег для кода.
    """
    return format_tag('code', text, escape_content=escape_html)

@cache_with_signature
def pre(text: str, lang: str = '', escape_html=True) -> str:
    """
    Генерирует HTML тег для отображения блока кода.

    :param str text: Код для отображения в теге.
    :param str lang: Язык программирования, defaults to ''.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для отображения блока кода.
    """
    return format_tag('pre', text, language=lang, escape_content=escape_html)

# @cache_with_signature
def blockquote(text: str, expandable=False, escape_html=True) -> str:
    """
    Создает HTML тег для блока цитаты.

    :param str text: Текст для размещения в теге.
    :param bool expandable: Можно ли разворачивать цитату, defaults to False.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для блока цитаты.
    """
    if expandable:
        return format_tag('blockquote', text, escape_content=escape_html, expandable='')
    return format_tag('blockquote', text, escape_content=escape_html)



def bq(text: str, expandable=False, escape_html=True) -> str:
    """
    Тоже самое что и blockquote.
    Создает HTML тег для блока цитаты.

    :param str text: Текст для размещения в теге.
    :param bool expandable: Можно ли разворачивать цитату, defaults to False.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для блока цитаты.
    """
    if expandable:
        return format_tag('blockquote', text, escape_content=escape_html, expandable='')
    return format_tag('blockquote', text, escape_content=escape_html)


@cache_with_signature
def b(text: str, escape_html=True) -> str:
    """
    Создает HTML тег для жирного текста.

    :param str text: Текст для размещения в теге.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для жирного текста.
    """
    return format_tag('b', text, escape_content=escape_html)

@cache_with_signature
def i(text: str, escape_html=True) -> str:
    """
    Создает HTML тег для курсива.

    :param str text: Текст для размещения в теге.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для курсива.
    """
    return format_tag('i', text, escape_content=escape_html)

@cache_with_signature
def a(text: str, url: str, escape_html=True) -> str:
    """
    Создает HTML тег для ссылки.

    :param str text: Текст ссылки.
    :param str url: URL для ссылки.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для ссылки.
    """
    return format_tag('a', text, href=url, escape_content=escape_html)

@cache_with_signature
def u(text: str, escape_html=True) -> str:
    """
    Создает HTML тег для подчеркивания текста.

    :param str text: Текст для размещения в теге.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для подчеркивания текста.
    """
    return format_tag('u', text, escape_content=escape_html)

@cache_with_signature
def s(text: str, escape_html=True) -> str:
    """
    Создает HTML тег для зачеркнутого текста.

    :param str text: Текст для размещения в теге.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для зачеркнутого текста.
    """
    return format_tag('s', text, escape_content=escape_html)

@cache_with_signature
def spoiler(text: str, escape_html=True) -> str:
    """
    Создает HTML тег для спойлера.

    :param str text: Текст для размещения в теге.
    :param bool escape_html: Нужно ли экранировать HTML, defaults to True.
    :return str: Сгенерированный HTML тег для спойлера.
    """
    return format_tag('tg-spoiler', text, escape_content=escape_html)

@cache_with_signature
def emoji(id: int, emoticon: str) -> str:
    """
    создает тег для premium emoji
    
    :param int id: custom (premium) emoji id
    :param str emoticon: стандартный емодзи который будет показывается если у юзера не будет Telegram Premium
    :return str: Сгенерированный HTML тег для custom emoji
    """
    return format_tag('emoji', emoticon, False, True, id=id)

import re

@cache_with_signature
def remove_emoji_tags(text: str) -> str:
    """
    Удаляет из текста премиум емодзи
    
    :param str text: текст с емодзи
    :return str: текст без емодзи
    """
    return re.sub(r'<emoji[^>]*>(.*?)<\/emoji>', r'\1', text)