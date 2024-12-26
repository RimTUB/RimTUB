from functools import lru_cache
import os
from ._logs import install_log
from .database import ModuleDB, DictStorage
from .scripts import get_script_directory
from config import DEFAULT_MODULE_LOGGER_LEVEL

from pathlib import Path
from logging import Logger, getLogger

__all__ = [
    'Module'
]

class SingletonByAttribute:
    _instances = {}

    def __new__(cls, attr):
        if (cls, attr) not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[(cls, attr)] = instance
            instance.attr = attr
        return cls._instances[(cls, attr)]
    


class Module(SingletonByAttribute):
    """
    Класс для работы с модулями в системе RimTUB.

    Атрибуты:
        name (str): Имя модуля.
        path (Path): Путь к папке модуля. Полезно для хранения файлов
        db (ModuleDB): База данных модуля
        logger (Logger): Логгер модуля.
        st (DictStorage): Локальное хранилище данных.

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

    _inited = False

    def __init__(self, name: str):
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
            self.path = Path(get_script_directory(), 'plugins', self.name)

            self.logger = getLogger(f'RimTUB [{self.client.num}] [{self.name}]')
            install_log(self.logger)
            self.logger.setLevel(DEFAULT_MODULE_LOGGER_LEVEL)

            db_path = Path(get_script_directory(), 'databases', self.name)
            db_path.mkdir(parents=True, exist_ok=True)
            self.db = ModuleDB(db_path / f'database_{self.client.me.id}.db')
            await self.db.bootstrap()

            self.st = DictStorage()

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
