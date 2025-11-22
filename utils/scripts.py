from difflib import get_close_matches
import importlib
import logging
from pathlib import Path
from typing import List, TextIO, Tuple, Dict, Callable, Any
import os, sys, gc, time, re
import yaml
import random
import string
from .config import Config
import subprocess
import pickle
import json
import os


__all__ = [
    'get_root',
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
    'read_yaml',
    'singleton',
    'save_pickle',
    'load_pickle',
    'generate_random_identifier'
]


def get_root(as_path=False) -> str|Path:
    """
    Возвращает путь к директории, в которой находится RimTUB.

    :return str: путь к корню RimTUB.
    """
    path = os.path.realpath(sys.argv[0])
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return Path(path) if as_path else path


def get_args(text: str, default: Any = '') -> str | Any:
    """
    Extracts arguments from a command text.

    Handles prefix and optional whitespace, like: ".command arg" or ". command arg"

    :param str text: the original text containing command and arguments
    :param Any default: the default value if no argument is present
    :return str | Any: the extracted argument string or the default value
    """
    text = text.strip()
    if not text.startswith(Config.PREFIX):
        return default
    text_wo_prefix = text[len(Config.PREFIX):].lstrip()
    parts = text_wo_prefix.split(maxsplit=1)
    return parts[1] if len(parts) > 1 else default


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

def fnum(num: int, threshold: int = 10000) -> str:
    """
    Форматирует число с разделением тысяч, если оно больше или равно указанному порогу
    Возвращает число как строку без запятой, если оно меньше порога

    :param int num: число для преобразования
    :param int threshold: пороговое значение для разделения тысяч
    :return str: отформатированное число в виде строки

    ## Пример
    .. code-block:: python
        print(fnum(1000))     # '1000'
        print(fnum(10000))    # '10,000'
        print(fnum(1000000))  # '1,000,000'
        print(fnum(666))      # '666'
        print(fnum(1200, threshold=1000))  # '1,200'
    """
    if num >= threshold:
        return f"{num:,}"
    else:
        return str(num)


def sec_to_str(seconds: int, round: bool = True) -> str:
    """
    Преобразует количество секунд в строковое представление формата "д.ч.м.с."

    :param int seconds: количество секунд для преобразования.
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
        module = ['модуль', 'модуля', 'модулей']
        plural(1,  module) # модуль
        plural(3,  module) # модуля
        plural(15, module) # модулей
    """
    if count % 10 == 1 and count % 100 != 11:
        return words[0]
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return words[1]
    else:
        return words[2]


def restart(app_id: int, chat_id: int = None, msg_id: int = None) -> None:
    """
    Перезапускает RimTUB

    :param int app_id: ID клиента 
    :param int chat_id: (опционально) идентификатор чата для изменения сообщения.
    :param int msg_id: (опционально) идентификатор сообщения для изменения.
    """
    os.execl(sys.executable, sys.executable, sys.argv[0],
             'restart', str(app_id),
             str(time.perf_counter()),
             str(chat_id), str(msg_id)
             )


async def check_ping(app) -> float:
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
    :return List[float]: список чисел
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
    r = default
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
    Ищет файл с самым похожим именем в указанной директории и её подпапках.

    :param str filename: имя файла, который необходимо найти.
    :param str search_path: путь к директории, в которой будет осуществляться поиск.
    :param int max_depth: максимальная глубина рекурсивного поиска (по умолчанию нет ограничения).
    :param List[str] extensions: список расширений для фильтрации (по умолчанию любые файлы).
    :param bool case_sensitive: учитывать ли регистр имени файла (по умолчанию False).
    :param Any default: значение по умолчанию, возвращаемое при отсутствии файла.
    :return str | Any: полный путь к самому похожему файлу или значение default, если файл не найден.
    """
    search_path = os.path.abspath(search_path)

    if extensions:
        extensions = [ext.lower() if not case_sensitive else ext for ext in extensions]

    collected_files = []
    original_files = []

    for root, dirs, files in os.walk(search_path):
        current_depth = root[len(search_path):].count(os.sep)

        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []

        for file in files:
            file_ext = os.path.splitext(file)[1].lower() if not case_sensitive else os.path.splitext(file)[1]
            if not extensions or file_ext in extensions:
                full_path = os.path.join(root, file)
                collected_files.append(file.lower() if not case_sensitive else file)
                original_files.append(full_path)

    if not case_sensitive:
        filename = filename.lower()

    closest_matches = get_close_matches(filename, collected_files, n=1, cutoff=0.6)
    if closest_matches:
        best_match_index = collected_files.index(closest_matches[0])
        return original_files[best_match_index]
    return default

def find_directory(
    dirname: str,
    search_path: str,
    max_depth: int = None,
    case_sensitive: bool = False,
    default: Any = None
) -> str | Any:
    """
    Ищет директорию с самым похожим именем в указанной директории и её подпапках.

    :param str dirname: имя директории, которую необходимо найти.
    :param str search_path: путь к директории, в которой будет осуществляться поиск.
    :param int max_depth: максимальная глубина рекурсивного поиска (по умолчанию нет ограничения).
    :param bool case_sensitive: учитывать ли регистр имени директории (по умолчанию False).
    :param Any default: значение по умолчанию, возвращаемое при отсутствии директории.
    :return str | Any: полный путь к самой похожей директории или значение default, если директория не найдена.
    """
    search_path = os.path.abspath(search_path)

    collected_dirs = []
    original_dirs = []

    for root, dirs, files in os.walk(search_path):
        current_depth = root[len(search_path):].count(os.sep)

        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []

        for folder in dirs:
            full_path = os.path.join(root, folder)
            collected_dirs.append(folder.lower() if not case_sensitive else folder)
            original_dirs.append(full_path)

    if not case_sensitive:
        dirname = dirname.lower()

    closest_matches = get_close_matches(dirname, collected_dirs, n=1, cutoff=0.6)
    if closest_matches:
        best_match_index = collected_dirs.index(closest_matches[0])
        return original_dirs[best_match_index]
    return default


def install_requirements(requirements: dict):
    logger = logging.getLogger('RimTUB')
    try:
        for req in requirements.values():
            logger.debug(f'Checking requirement...\n{req["check"]}')
            try: exec(req['check'])
            except (ImportError, AssertionError):
                logger.debug('Requirement not found')
                logger.debug(f"installing {req['install']}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", req['install'], *req.get('params', [])])
                except:
                    logger.error(f"Can\'t install {req['install']}(", exc_info=True)
                logger.debug(f"done!")
            except:
                logger.error("Can\'t install requirements, invalid check code")
            else:
                logger.debug('Requirement exist!')
    except KeyError as key:
        logger.error(f'Can\'t install requirements, key `{key}` not found in requirement')
    except TypeError:
        logger.error("Can\'t install requirements, invalid type", exc_info=True)


def read_yaml(file_path: str):
    """
    Чтение YAML файла

    :param str file_path: Путь к YAML файлу

    :return dict: Данные в виде словаря

    error `FileNotFoundError`: когда файл не найден
    error `yaml.scanner.ScannerError`: при ошибке парсинга
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
    

from typing import TypeVar, Type, Dict, Any, Callable, cast

T = TypeVar('T')

def singleton(cls):
    """
    Декоратор для реализации паттерна Singleton.

    :param type cls: Класс, для которого нужно создать единственный экземпляр.
    :return: Класс-обертка для получения единственного экземпляра класса.
    """
    instances: Dict[Type[T], T] = {}

    original_new = cls.__new__

    def singleton_new(cls_: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls_ not in instances:
            instances[cls_] = original_new(cls_, *args, **kwargs)
        return instances[cls_]

    cls.__new__ = singleton_new  # type: ignore

    return cls




# Путь к JSON с мета-данными
META_FILE = Path(get_root(), 'storage', 'files_meta.json')

def load_meta():
    """Загрузка метаданных из файла"""
    if os.path.exists(META_FILE):
        with open(META_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_meta(meta):
    """Сохранение метаданных в файл"""
    with open(META_FILE, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=4)

Config()

def save_pickle(path, data, ttl=Config.DEFAULT_PICKLE_STORAGE_FILES_TTL):
    """Сохраняет данные в pickle storage """
    if os.path.exists(path):
        raise FileExistsError(f'File {path} already exist (Pickle Storage)')
    
    with open(path, 'wb') as f:
        pickle.dump(data, f)

    meta = load_meta()
    expire_at = int(time.time()) + ttl
    meta[str(path)] = expire_at
    save_meta(meta)
    
    return Path(path).absolute()


def load_pickle(path):
    """Загружает данные из pickle storage"""
    if not os.path.exists(path):
        err = FileNotFoundError(f"Файл {path} не найден (Pickle Storage)")
        err.path = path
        raise err
    return pickle.load(open(path, 'rb'))


def cleanup_expired_storage_files():
    """Удаляет устаревшие storage pickle файлы по TTL"""
    meta = load_meta()
    now = int(time.time())
    updated_meta = {}

    for path, expire_at in meta.items():
        if now >= expire_at:
            if os.path.exists(path):
                os.remove(path)
        else:
            updated_meta[path] = expire_at

    save_meta(updated_meta)


def generate_random_identifier(length=10):
    """Генерирует уникальную комбинацию чисел указанной длинны"""
    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for __ in range(length)
    )

    
import os

def is_normal_linux() -> bool:
    # Termux
    if "PREFIX" in os.environ and "/data/data/com.termux" in os.environ.get("PREFIX", ""):
        return False

    # UserLAnd
    if os.path.exists("/usr/bin/.userland") or os.path.exists("/etc/userland-release"):
        return False

    return True
