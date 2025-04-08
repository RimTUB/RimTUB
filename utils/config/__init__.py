import logging
from pathlib import Path
from types import ModuleType
from typing import get_type_hints
from .default_config import DefaultConfig
from pyrogram.enums import ClientPlatform
import os, sys, yaml

def get_root() -> str:
    """
    Возвращает путь к директории, в которой находится текущий исполняемый скрипт.

    :return str: путь к директории скрипта.
    """
    path = os.path.realpath(sys.argv[0])
    if os.path.isdir(path):
        return path
    else:
        return os.path.dirname(path)

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


def get_required_attrs(cls):
    annotations = get_type_hints(cls)
    defaults = {k for k in dir(cls) if hasattr(cls, k)}
    return [attr for attr in annotations if attr not in defaults]


@singleton
class Config(DefaultConfig):
    _loaded = False

    def __init__(self):
        if not self._loaded:
            self.logger = logging.getLogger('RimTUB')
            r = self.load_yaml()
            if not r:
                sys.exit(0)
            self.__class__._loaded = True

    def load_yaml(self):
        data = read_yaml(Path(get_root(), 'config.yaml'))

        for attr in get_required_attrs(self):
            if not data.get(attr):
                self.logger.error(f"Укажи {attr} в config.yaml !")
                return False
        
        data['PHONES'] = [f"+{p}" for p in data['PHONES'] if not str(p).startswith('+')]

        for k, v in data.items():
            if 'LOGGING_LEVEL' in k:
                v = logging.__dict__.get(v)
            
            if 'CL_CLIENT_PLATFORM' in k:
                v = ClientPlatform.__getitem__(v)

            data[k] = v
                
            

        for param, value in data.items():
            setattr(self, param, value)
            setattr(self.__class__, param, value)
        

        return True

    def __getattr__(self, item):
        if hasattr(self.__class__, item):
            return getattr(self.__class__, item)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

