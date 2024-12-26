from hashlib import sha256
from typing import Callable, Coroutine, Iterable, List
import asyncio, gc, importlib, itertools, os, sys, pip
from types import FunctionType
from logging import Logger

from telebot.async_telebot import AsyncTeleBot

from pyromod.config import config
config.disable_startup_logs = True  # settings in this shit (pyromod) don't work
from pyromod import Client

from .misc import NCmd, helplist, clients
from .exceptions import LoadError
from .module import Module



__all__ = [
    'ModifyPyrogramClient'
]


class ModifyPyrogramClient(Client):
    """
    Расширенный клиент Pyrogram с поддержкой модулирования и работы с базой данных.

    Attributes:
        num (int): Номер клиента.
        logger (Logger): Логгер для ведения журнала.
        bot (AsyncTeleBot): Асинхронный TeleBot.
        bot_username (str): Имя пользователя бота.
        _module_tasks (dict[str, asyncio.Task]): Словарь с задачами модулей.
        _group_counter (Iterable): Счетчик групп.
        _module_groups (dict[int, List[str]]): Словарь групп модулей.
    """
    num: int
    logger: Logger
    info: Logger.info
    warning: Logger.warning
    error: Logger.error
    debug: Logger.debug
    critical: Logger.critical
    fatal: Logger.fatal  # type: ignore
    log: Logger.log
    bot: AsyncTeleBot
    bot_username: str
    _module_tasks: dict[str, asyncio.Task]
    _group_counter: Iterable
    _module_groups: dict[int, List[str]]

    def __init__(self, *args, num: int, logger: Logger, bot: AsyncTeleBot, **kwargs):
        """
        Инициализирует экземпляр ModifyPyrogramClient.

        :param args: Позиционные аргументы для инициализации родительского класса.
        :param num: Уникальный номер клиента.
        :param logger: Объект логгера для записи журналов.
        :param bot: Асинхронный Telegram-бот.
        :param kwargs: Дополнительные именованные аргументы для инициализации.
        """
        
        if not os.path.exists(kwargs.get('workdir')):
            os.makedirs(kwargs.get('workdir'))

        super().__init__(*args, **kwargs)

        self.num = num
        self.app_hash = sha256(bytes(str(self.phone_number).encode())).hexdigest()

        self.logger = logger
        self.info = logger.info
        self.warning = logger.warning
        self.error = logger.error
        self.debug = logger.debug
        self.critical = logger.critical
        self.fatal = logger.fatal
        self.log = logger.log

        self.bot = bot

        self._module_tasks = {}
        self._group_counter = itertools.count()
        self._module_groups = {}
        self._on_ready_funcs = []
    
    async def _load_dialogs(self):
        """
        Асинхронно загружает диалоги для клиента.

        :return: None
        """
        [_ async for _ in self.get_dialogs()]

    def start(self, *args, **kwargs):
        """
        Запускает клиента и загружает необходимые модули.

        :param args: Позиционные аргументы для родительского метода.
        :param kwargs: Именованные аргументы для родительского метода.
        :return: Результат вызова метода родительского класса.
        """
        r = super().start(*args, **kwargs)

        self.add_task('_core', self._load_dialogs())

        self.bot_username = self.loop.run_until_complete(self.bot.get_me()).username

        self.loop.run_until_complete(self.load_modules())
        self.logger.debug("Modules loaded!")

        return r
    
    def on_ready(self, group: int) -> Callable:
        """
        # Устарело! Используй mod.on_ready вместо app.on_ready(group)!
        """
        def decorator(func: FunctionType):
            self._on_ready_funcs.append((group, func))
        return decorator

    async def _start_on_readys(self):
        for module_name in self._module_groups:
            await self._start_on_ready(module_name)
                    

    async def _start_on_ready(self, module_name):
        if module_name in self._module_groups:
            for group in self._module_groups[module_name]:
                for gr, func in self._on_ready_funcs:
                    if group == gr:
                        try:
                            self.logger.debug(f"Running @on_ready (module {module_name}) ...")
                            r = await func(self)
                            self.logger.debug(f"Done")
                            return 'ok', r
                        except Exception as e:
                            self.logger.error(f"Error in @on_ready (module {module_name})", exc_info=True)
                            return 'error', e
        return 'ok', None

    def cmd(self, group: int):
        """
        # Устарело! Используй mod.cmd вместо app.cmd(group)!

        Возвращает объект NCmd для обработки команд в указанной группе.

        :param group: Номер группы команд.
        :return: Объект NCmd, связанный с данной группой.

        ## Пример
        .. code-block:: python
            cmd = app.cmd(app.get_group(__package__))

            @cmd(['cmd', 'my_command'])
            async def _cmd(app: Client, msg: M):
                ...
        """
        return NCmd(self, group)

    async def load_module(self, module_name, restart=False, exception=False, unload_help=False, all_clients=False):
        """
        Загружает указанный модуль.

        :param module_name: Имя модуля для загрузки.
        :param restart: Флаг, указывающий, следует ли перезагрузить модуль.
        :param exception: Флаг, указывающий, следует ли вызывать исключение в случае ошибки.
        :param unload_help: Флаг, указывающий, следует ли удалить модуль из хелплиста.
        :param all_clients: Флаг, указывающий, следует ли загрузить модуль для всех клиентов.
        :return: None
        :raises LoadError: Исключение, если возникла ошибка загрузки.
        """
        if all_clients:
            for client in clients:
                await client.load_module(module_name, restart=restart, exception=exception, unload_help=unload_help, all_clients=False)
            return
        try:
            if restart:
                await self.stop_module(module_name, unload_help=unload_help, delete_from_sys_modules=False)
                if module_name in self._module_groups:
                    for group in self._module_groups[module_name]:
                        for row in self._on_ready_funcs.copy():
                            if group == row[0]:
                                self._on_ready_funcs.remove(row)

                module = importlib.import_module(f'plugins.{module_name}')
                if 'plugins.'+module_name in sys.modules.keys():
                    module = importlib.reload(sys.modules['plugins.'+module_name])
                
            else:
                module = importlib.import_module(f'plugins.{module_name}')
            
            libs = getattr(module, '__libs__', [])
            if isinstance(libs, str): libs = [libs]
            for lib in libs:
                if isinstance(lib, str):
                    to_import, to_install = lib.split('==')[0], lib
                else:
                    to_import, to_install = lib
                try:
                    importlib.import_module(to_import)
                except ImportError:
                    self.logger.debug(f"installing {to_install}...")
                    pip.main(['install', to_install])

            await module.main(self, await Module(module_name).init(self))

            

        except Exception as e:
            if exception:
                raise LoadError from e
            self.logger.error(f"Error in module {module_name}: {e}", exc_info=True)

        else:
            self.logger.debug(f'Module loaded: {module_name}')

    async def stop_module(self, module_name, unload_help=False, all_clients=False, delete_from_sys_modules=True):
        """
        Останавливает указанный модуль.

        :param module_name: Имя модуля для остановки.
        :param unload_help: Флаг, указывающий, следует ли удалить модуль из хелплиста.
        :param all_clients: Флаг, указывающий, следует ли остановить модуль для всех клиентов.
        :return: None
        """
        if all_clients:
            for client in clients:
                await client.stop_module(module_name, unload_help=unload_help, all_clients=False)
            return
        self.logger.debug(f"Stopping module {module_name}")
        if delete_from_sys_modules:
            try: 
                del sys.modules['plugins.' + module_name]
            except: 
                pass
            else: 
                self.logger.debug(f"Unloaded {module_name} from memory")
    
        for task in self._module_tasks.get(module_name, []).copy():
            try: 
                task.cancel()
            except Exception as e: 
                self.logger.warning(f"Failed to cancel Task {task} (module {module_name})", exc_info=True)
            else:
                self.logger.debug(f"Task {task} (module {module_name}) canceled")
                self._module_tasks[module_name].remove(task)
        gc.collect()
        for group in self._module_groups.get(module_name, []):
            for handler in self.dispatcher.groups.get(group, []):
                self.remove_handler(handler, group)
                self.logger.debug(f"Handler {handler} (module {module_name}, group {group}) removed")
        if unload_help:
            try: 
                del helplist.modules[module_name]
            except: 
                pass
            self.logger.debug(f"Module {module_name} has been deleted from HelpList")

    async def load_modules(self):
        """
        Загружает все доступные модули из папки `plugins`.

        :return: None
        """
        modules_path = os.path.join(self.WORKDIR, 'plugins')
        mod = await Module('ModuleHelper').init(self)
        disabled_modules = await mod.db.get('disabled_modules', [])
        self.logger.debug(f"Disabled modules: {', '.join(disabled_modules)}")
        for _, folders, __ in os.walk(modules_path):
            for module in folders:
                if not module.startswith('__'):
                    if module in disabled_modules:
                        self.logger.debug(f'module {module} is disabled. Skipping...')
                        continue
                    self.logger.debug(f'loading {module}...')
                    await self.load_module(module)
            break

    def add_task(self, module_name: str, coro: Coroutine) -> asyncio.Task:
        """
        # Устарело! Используй mod.add_task(coro) вместо app.add_task(__package__, coro)!

        Добавляет новую задачу в очередь выполнения.

        :param module_name: Имя модуля, с которым связана задача.
        :param coro: Корутин, представляющий задачу.
        :return: Объект задачи asyncio.Task.

        ## Пример
        .. code-block:: python
            async def worker(arg):
                ...

            app.add_task(__package__, worker(arg))
        """
        async def __wrapper(coro, logger: Logger):
            try:
                await coro
            except:
                logger.error(f'Error in {module_name} module', exc_info=True)
        module_name = module_name.removeprefix('plugins.')
        if module_name not in self._module_tasks:
            self._module_tasks[module_name] = []
        ev = asyncio.get_event_loop()
        task = ev.create_task(__wrapper(coro, self.logger))
        self._module_tasks[module_name].append(task)
        self.logger.debug(f'Task {task} was created (module {repr(module_name)})')
        return task

    def get_group(self, module):
        """
        # Устарело! Используй mod.group вместо app.get_group(__package__)!


        Получает следующую группу для указанного модуля.

        :param module: Имя модуля.
        :return: Номер группы.
        
        
        ## Пример
        .. code-block:: python
            cmd = app.cmd(app.get_group(__package__))
        """
        group = next(self._group_counter)
        module = module.removeprefix('plugins.')
        groups = self._module_groups.get(module, [])
        groups.append(group)
        self._module_groups[module] = groups
        return group
