from gzip import compress
from requests import post

__all__ = ['paste']


async def paste(code: str, lang: str = 'python'):
    """
    Загружает код на сервер pastes.dev и возвращает ссылку на размещение.

    :param str code: Код, который необходимо разместить.
    :param str lang: Язык программирования кода, defaults to 'python'.
    :return str: Ссылка на размещенный код на pastes.dev.
    """
    try:
        headers = {
            'Content-Type': f'text/{lang}',
            'Content-Encoding': 'gzip',
        }

        gzip_data = compress(code.encode('utf-8'))

        response = post('https://bytebin.lucko.me/post', data=gzip_data, headers=headers)
        
        return 'https://pastes.dev/{}'.format(response.json()['key'])
    except Exception as e:
        return f"Pasting failed: {e}"