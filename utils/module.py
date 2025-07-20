from copy import deepcopy
from functools import lru_cache
import time

from utils.misc import clients
from ._logs import install_log
from .database import ModuleDB, DictStorage
from .scripts import generate_random_identifier, get_root, save_pickle, load_pickle, read_yaml
from utils import Config

from pathlib import Path
from logging import Logger, getLogger

from pathlib import Path
from typing import Any, List
import os
from logging import Logger


from pyromod.config import config
config.disable_startup_logs = True  # settings in this shit (pyromod) does't work

from utils.helplist import *
from utils.scripts import get_root
from utils.bot_helper import _objects, Button, Buttons

from pyrogram.types import InlineQueryResult
from pyrogram import filters



__all__ = [
    'Module'
]

class SingletonByAttribute:
    _instances = {}

    def __new__(cls, *attrs):
        if (cls, attrs) not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[(cls, attrs)] = instance
            instance.attr = attrs
        return cls._instances[(cls, attrs)]
    


class Module(SingletonByAttribute):
    """
    Класс для работы с модулями в системе RimTUB.

    Атрибуты:
        name (str): Имя модуля.
        path (Path): Путь к папке модуля. Полезно для хранения файлов
        db (ModuleDB): База данных модуля
        logger (Logger): Логгер модуля.
        st (DictStorage): Локальное хранилище данных.
        manifest (dict): Данные из manifest файла

    Проперти:
        group: Получить группу модуля
        примечание: mod.group возвращает закешированную группу, если нужно получить новую, используй mod.get_group()
        cmd: Получить объект NCmd для создания обработчиков команд
        on_ready: Декоратор on_ready, срабатывает при запуске юб
    
    Bound методы:
        add_task: Добавить задачу
        get_group: Получить новую группу модуля
    """
    name: str
    path: Path
    db: ModuleDB
    logger: Logger
    st: DictStorage
    manifest: dict

    _inited = False

    def __init__(self, name: str, num: int):
        """
        Создает объект модуля.

        :param str name: Имя модуля.
        """
        self.name = name

    async def init(self, client):
        """
        Инициализирует модуль: настраивает логирование, базу данных и хранилище.

        :param client: Клиент, связанный с модулем.
        :return Module: Инициализированный модуль.
        """
        if not self._inited:
            self.client = client
            self.path = Path(get_root(), 'plugins', self.name)

            self.logger = getLogger(f'RimTUB [{self.client.num}] [{self.name}]')
            install_log(self.logger)
            self.logger.setLevel(Config.DEFAULT_MODULE_LOGGING_LEVEL)

            db_path = Path(get_root(), 'databases', self.name)
            db_path.mkdir(parents=True, exist_ok=True)
            self.db = ModuleDB(db_path / f'database_{self.client.me.id}.db')
            await self.db.bootstrap()

            self.st = DictStorage()

            self.manifest = read_yaml(self.path / 'manifest.yaml')

            self._inited = True

        return self

    def get_group(self):
        """
        Получает следующую группу для модуля.

        :return: Группа модуля.
        """
        return self.client.get_group(self.name)

    @property
    @lru_cache
    def group(self):
        """
        Получает следующую группу модуля.

        Примечание: mod.group возвращает закешированную группу, если нужно получить новую, используй mod.get_group()

        :return: Группа модуля.
        """
        return self.get_group()

    @property
    def cmd(self):
        """
        Возвращает объект NCmd для обработки команд

        ## Пример
        .. code-block:: python
            cmd = mod.cmd

            @cmd(['cmd', 'my_command'])
            async def _cmd(app: Client, msg: M):
                ...

        :return: Объект команды.
        """
        return self.client.cmd(self.group)

    @property
    def on_ready(self):
        """
        Декоратор который вызывается когда юб запущен

        ## Пример
        .. code-block:: python

            @mod.on_ready
            async def _onr(app: Client):
                mod.logger.info("RimTUB запустился!")

        :return: Обработчик готовности.
        """
        return self.client.on_ready(self.group)

    def add_task(self, coro):
        """
        Добавляет новую задачу в очередь выполнения.

        ## Пример
        .. code-block:: python
            async def worker(arg):
                ...

            mod.add_task(worker(arg))


        :param coro: Корутина, которую нужно выполнить.
        :return: Результат добавления задачи.
        """
        return self.client.add_task(self.name, coro)


    async def prepare_buttons(self, buttons: Buttons):
        if getattr(buttons, '_prepared', False):
            return buttons
        for row in buttons.inline_keyboard:
            for button in row:
                if button.callback_data:
                    extra_data_id = ''
                    if not getattr(button, 'extra_data', None):
                        button.extra_data = {}
                    extra_data_id = generate_random_identifier()
                    button.extra_data_id = extra_data_id
                    button.extra_data.update(__extra_data_id=extra_data_id)
                    save_pickle(Path(get_root(), 'storage', f'{extra_data_id}.pkl'), button.extra_data)
                    if len(button.callback_data) + len(self.name) + len(extra_data_id) + 2 > 64:
                        return self.logger.error(f"callback_data in button {repr(button)} is too long! It must be 1-{64-len(self.name)-2-len(extra_data_id)} symbols")
                    button.callback_data = f"{self.name}:{extra_data_id}:{button.callback_data}"
        buttons._prepared = True
        return buttons


    async def send_buttons(self, chat_id, text, buttons: Buttons, input_text_message_content_params: dict = None, **kwargs):
        id = f"{time.time()}+{generate_random_identifier()}"

        if not getattr(buttons, '_prepared', False):
            buttons = await self.prepare_buttons(buttons)

        _objects[id] = dict(text=text, buttons=buttons, input_text_message_content_params=input_text_message_content_params or {})


        results = await self.client.get_inline_bot_results(self.client.bot_username, f"iqm:{id}")
        sent_message = await self.client.send_inline_bot_result(chat_id, results.query_id, results.results[0].id, **kwargs)
        
        for row in buttons.inline_keyboard:
            for button in row:
                try:
                    if not button.callback_data:
                        continue
                    
                    if button.extra_data_id:
                        extra_data_path = get_root(True) / 'storage' / f'{button.extra_data_id}.pkl'
                        extra_data: dict = load_pickle(extra_data_path)
                        os.remove(extra_data_path)
                    else:
                        extra_data_path = get_root(True) / 'storage' / f'{generate_random_identifier()}.pkl'
                        extra_data = dict()
                        
                    extra_data.update(message=sent_message)
                    save_pickle(extra_data_path, extra_data)
                    
                except:
                    self.logger.warning('[Buttons] Can\'t update extra_data with message object', exc_info=True)
                    


    def callback(
        self, callback_data='', startswith='', group=None,
        is_private=True, allowed_ids: List[int] = None, message="Это не твоя кнопка!", show_alert=True
    ):
        
        self.st.setdefault('__core__', {})
        self.st['__core__']['message'] = "DO NOT DELETE KEY `__core__`, IT IS USED FOR CALLBACK HANDLERS!!"
        self.st['__core__'].setdefault(f'{callback_data!r}_{startswith!r}', {})
        self.st['__core__'][f'{callback_data!r}_{startswith!r}']['allowed_ids'] = allowed_ids
        
        def _flt(data):
            module_name, _, moddata = data.split(':', 2)
            if module_name != self.name:
                return False
            elif not any([callback_data, startswith]):
                return True
            elif callback_data and moddata == callback_data:
                return True
            elif startswith and moddata.startswith(startswith):
                return True
            return False

            
        def decorator(func):


            @self.client.bot.on_callback_query(
                    filters.create(lambda _, __, c: _flt(c.data)),
                    group=group or self.get_group()
            )
            async def __wrapper(c, *args, **kwargs):
                try:

                    allowed_ids = self.st.get('__core__', {}).get(f'{callback_data!r}_{startswith!r}', {}).get('allowed_ids', [])

                    if is_private and not allowed_ids:
                        allowed_ids = [client.me.id for client in clients]

                    if allowed_ids:
                        if c.from_user.id not in allowed_ids:
                            await c.answer(message, show_alert)
                            return None
                    
                    c = getattr(c, 'original_callback', c)
                    _, extra_data_id, moddata = c.data.split(':', 2)
                    mc = deepcopy(c)
                    mc.original_data = deepcopy(c.data)
                    mc.original_callback = deepcopy(c)
                    mc.data = moddata
                    mc._client = self.client.bot
                    if extra_data_id:
                        data = load_pickle(Path(get_root(), 'storage', f"{extra_data_id}.pkl"))
                        mc.extra_data = data
                    try:
                        await func(mc, *args, **kwargs)
                        await self.client.bot.answer_callback_query(c.id)
                    except:
                        self.logger.error(f"Error in callback ({callback_data=!r}, {startswith=!r}, {group=!r}):", exc_info=True)
                except FileNotFoundError as e:
                    self.logger.error(f"Pickle storage file not found!: {e.path}")
                    await self.client.bot.answer_callback_query(c.id, 'Произошла ошибка! Подробности в консоли', True)
                except:
                    self.logger.error(f'Error in callback ({callback_data=!r}, {startswith=!r}):', exc_info=True)
                    await self.client.bot.answer_callback_query(c.id, 'Произошла ошибка! Подробности в консоли', True)
            return __wrapper
        
        return decorator
