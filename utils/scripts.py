from typing import List, TextIO, Tuple, Dict, Callable, Any
import os, sys, gc, time, re

from utils.modify_pyrogram_client import ModifyPyrogramClient


__all__ = [
    'get_script_directory',
    'get_args',
    'parse_args',
    'pnum',
    'sec_to_str',
    'plural',
    'restart',
    'check_ping',
    'get_numbers_from_string',
    'find_function_by_id',
    'tail',
    'try_',
    'get_tree',
    'find_file',
    'find_directory',
]


def get_script_directory() -> str:
    """
    Возвращает путь к директории, в которой находится текущий исполняемый скрипт.

    :return str: путь к директории скрипта.
    """
    path = os.path.realpath(sys.argv[0])
    if os.path.isdir(path):
        return path
    else:
        return os.path.dirname(path)


def get_args(text: str, default: Any = '') -> str | Any:
    """
    Извлекает аргументы из текста.

    :param str text: исходный текст с аргументами.
    :param Any default: значение по умолчанию, если аргумент отсутствует.
    :return str | Any: строка с аргументом или значение по умолчанию.

    ## Пример
    .. code-block:: python
        # msg.text = '.command some text'
        text = get_args(msg.text)
        print(text) # some text
    """
    try:
        return text.split(maxsplit=1)[1]
    except IndexError:
        return default


def parse_args(input_str: str) -> Tuple[List[str], List[str], Dict[str, Any]]:
    """
    Парсит строку аргументов и разделяет на позиционные, флаги и параметры с ключами и значениями.

            
    :param str input_str: строка с аргументами, разделёнными пробелами.

    :return Tuple[List[str], List[str], Dict[str, Any]]: список позиционных аргументов, список флагов, словарь параметров.

    
    ## Пример
    .. code-block:: python
        # msg.text = '.command some text -photo -size X'
        args, flags, kwargs = parse_args(get_args(msg.text))
        print(args) # ['some', 'text']
        print(flags) # ['-photo']
        print(kwargs) # {'-size': 'X'}
    """
    pattern = r'(-\w)(?:\s+(\S+))?'
    positional_args = []
    flags = []
    key_value_args = {}

    words = input_str.split()
    skip_next = False
    for i, word in enumerate(words):
        if skip_next:
            skip_next = False
            continue

        match = re.match(pattern, word)
        if match:
            flag = match.group(1)
            value = match.group(2)

            if value is not None:
                key_value_args[flag] = value
            else:
                if i + 1 < len(words) and not words[i + 1].startswith('-'):
                    key_value_args[flag] = words[i + 1]
                    skip_next = True
                else:
                    flags.append(flag)
        else:
            positional_args.append(word)

    return positional_args, flags, key_value_args


def pnum(num: int | float) -> int | float:
    """
    Приводит число к целому, если оно эквивалентно по значению, иначе оставляет дробным.

    :param int | float num: число для преобразования.
    :return int | float: преобразованное число.
    """
    return int(num) if int(num) == float(num) else float(num)


def sec_to_str(seconds: str, round: bool = True) -> str:
    """
    Преобразует количество секунд в строковое представление формата "д.ч.м.с."

    :param str seconds: количество секунд для преобразования.
    :param bool round: округлять ли число секунд до целого (по умолчанию True).
    :return str: строка, представляющая время.

    ## Пример
    .. code-block:: python
        print(sec_to_str(66666)) # 18ч. 31m. 6c.
    """
    seconds = float(seconds)
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    o = ''
    if seconds:
        o += str(int(seconds) if round else pnum(seconds)) + "c."
    if minutes:
        o = str(int(minutes)) + 'м.\xa0' + o
    if hours:
        o = str(int(hours)) + 'ч.\xa0' + o
    if days:
        o = str(int(days)) + 'д.\xa0' + o
    if o == '':
        o = '0c.'

    return o


def plural(count: int, words: List[str]) -> str:
    """
    Определяет правильную форму слова в зависимости от количества.

    :param int count: количество объектов.
    :param List[str] words: список форм слова (ед.ч., дв., мн.).
    :return str: правильная форма слова.

    ## Пример
    .. code-block:: python
        plural(1, ['модуль', 'модуля', 'модулей']) # модуль
        plural(3, ['модуль', 'модуля', 'модулей']) # модуля
        plural(15,['модуль', 'модуля', 'модулей']) # модулей
    """
    if count % 10 == 1 and count % 100 != 11:
        return words[0]
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return words[1]
    else:
        return words[2]


def restart(app_id: int, chat_id: int = None, msg_id: int = None) -> None:
    """
    Перезапускает текущий процесс с передачей аргументов.

    :param int app_id: ID клиента 
    :param int chat_id: (опционально) идентификатор чата для изменения сообщения.
    :param int msg_id: (опционально) идентификатор сообщения для изменения.
    """
    os.execl(sys.executable, sys.executable, sys.argv[0],
             'restart', str(app_id),
             str(time.perf_counter()),
             str(chat_id), str(msg_id)
             )


async def check_ping(app: ModifyPyrogramClient) -> float:
    """
    Проверяет пинг, отправляя сообщение самому себе и измеряя задержку.

    :param Any app: объект приложения, через который выполняется отправка сообщения.
    :return float: значение пинга в миллисекундах.
    """
    import time

    a = time.perf_counter()
    m = await app.send_message('me', '.')
    b = time.perf_counter()
    await m.delete()
    c = time.perf_counter()

    delta = ((b - a) + (c - b)) / 2
    ping_ms = delta * 1000
    return ping_ms

def get_numbers_from_string(string: str) -> List[float]:
    """
    Извлекает все числа из строки.

    :param str string: строка для поиска чисел.
    :return List[float]: список чисел в строковом представлении.
    """
    nums = re.findall(r'\d*\.\d+|\d+', string)
    return [float(i) for i in nums]


def find_function_by_id(func_id: int) -> Callable | None:
    """
    Ищет функцию по её идентификатору в памяти.

    :param int func_id: идентификатор функции.
    :return Callable | None: функция, если найдена, иначе None.
    """
    for obj in gc.get_objects():
        if id(obj) == func_id:
            return obj
    return None


def tail(f: TextIO, lines: int = 1, _buffer: int = 4098) -> str:
    """
    Получает последние строки из файла.

    :param TextIO f: объект файла.
    :param int lines: количество строк для извлечения.
    :param int _buffer: размер буфера чтения.
    :return str: последние строки файла.

    ## Пример
    .. code-block:: python
        with open('file.txt', 'r', encoding='utf-8') as f:
            print(tail(f, 2)) # последние\\nдве строки
    """
    lines_found = []
    block_counter = -1

    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()
        block_counter -= 1

    return "".join(lines_found[-lines:])

def try_(
    func_to_try: Callable, 
    func_to_except: Callable = None,
    func_to_else: Callable = None,
    func_to_finally: Callable = None,
    default: Any = None
) -> Any:
    """
    Универсальная функция для обработки исключений, выполняет разные действия в зависимости от результата.

    :param Callable func_to_try: основная функция, которую нужно выполнить.
    :param Callable func_to_except: функция, выполняемая при исключении (по умолчанию None).
    :param Callable func_to_else: функция, выполняемая, если исключение не возникло (по умолчанию None).
    :param Callable func_to_finally: функция, выполняемая в любом случае после завершения основной функции (по умолчанию None).
    :param Any default: значение по умолчанию, возвращаемое при исключении (по умолчанию None).
    :return Any: результат выполнения функций.
    """
    try:
        r = func_to_try()
    except:
        r = func_to_except() if func_to_except else default
    else:
        r = func_to_else() if func_to_else else r
    finally:
        r = func_to_finally() if func_to_finally else r
    return r


def get_tree(directory: str, prefix: str = "", html: bool = False) -> str:
    """
    Рекурсивно строит дерево файлов и директорий в указанной папке.

    :param str directory: путь к директории, для которой строится дерево.
    :param str prefix: строка префикса для отображения уровней вложенности (по умолчанию пустая строка).
    :param bool html: форматировать ли результат как HTML (по умолчанию False).
    :return str: строковое представление дерева директорий и файлов.
    """
    result = ""
    files = os.listdir(directory)
    files_count = len(files)
    
    for index, file in enumerate(files):
        is_last = index == files_count - 1
        result += prefix + ("└── " if is_last else "├── ") + (f"<b>{file}</b>" if html else file) + "\n"
        path = os.path.join(directory, file)
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            result += get_tree(path, new_prefix, html=html)
    
    return result


def find_file(
    filename: str, 
    search_path: str, 
    max_depth: int = None, 
    extensions: List[str] = None, 
    case_sensitive: bool = False, 
    default: Any = None
) -> str | Any:
    """
    Ищет файл по имени в указанной директории и её подпапках с возможностью настройки глубины поиска,
    фильтрации по расширениям и учёта регистра.

    :param str filename: имя файла, который необходимо найти.
    :param str search_path: путь к директории, в которой будет осуществляться поиск.
    :param int max_depth: максимальная глубина рекурсивного поиска (по умолчанию нет ограничения).
    :param List[str] extensions: список расширений для фильтрации (по умолчанию любые файлы).
    :param bool case_sensitive: учитывать ли регистр имени файла (по умолчанию False).
    :param Any default: значение по умолчанию, возвращаемое при отсутствии файла.
    :return str | Any: полный путь к файлу или значение default, если файл не найден.
    """
    search_path = os.path.abspath(search_path)

    if extensions:
        extensions = [ext.lower() if not case_sensitive else ext for ext in extensions]

    def match(file: str) -> bool:
        file_name_without_ext = os.path.splitext(file)[0]
        
        if not case_sensitive:
            return filename.lower() == file.lower() or filename.lower() == file_name_without_ext.lower()
        return filename == file or filename == file_name_without_ext

    def valid_extension(file: str) -> bool:
        if not extensions:
            return True
        file_ext = os.path.splitext(file)[1].lower() if not case_sensitive else os.path.splitext(file)[1]
        return file_ext in extensions

    for root, dirs, files in os.walk(search_path):
        current_depth = root[len(search_path):].count(os.sep)

        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []

        for file in files:
            if match(file) and valid_extension(file):
                return os.path.join(root, file)

    return default


def find_directory(
    dirname: str, 
    search_path: str, 
    max_depth: int = None, 
    case_sensitive: bool = False, 
    default: Any = None
) -> str | Any:
    """
    Ищет директорию по имени в указанной директории и её подпапках с возможностью настройки глубины поиска
    и учёта регистра.

    :param str dirname: имя директории, которую необходимо найти.
    :param str search_path: путь к директории, в которой будет осуществляться поиск.
    :param int max_depth: максимальная глубина рекурсивного поиска (по умолчанию нет ограничения).
    :param bool case_sensitive: учитывать ли регистр имени директории (по умолчанию False).
    :param Any default: значение по умолчанию, возвращаемое при отсутствии директории.
    :return str | Any: полный путь к директории или значение default, если директория не найдена.
    """
    search_path = os.path.abspath(search_path)

    def match(folder: str) -> bool:
        if not case_sensitive:
            return dirname.lower() == folder.lower()
        return dirname == folder

    for root, dirs, files in os.walk(search_path):
        current_depth = root[len(search_path):].count(os.sep)

        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []

        for folder in dirs:
            if match(folder):
                return os.path.join(root, folder)

    return default
