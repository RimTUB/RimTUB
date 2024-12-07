from typing import Any, Dict, List, Self


__all__ = [
    'Argument',
    'Module',
    'Command',
    'Feature',
    'HelpList'
]


def singleton(cls):
    """
    Декоратор для реализации паттерна Singleton.

    :param type cls: Класс, для которого нужно создать единственный экземпляр.
    :return: Функция-обертка для получения единственного экземпляра класса.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

class Argument:
    """
    Класс, представляющий аргумент команды.

    :param str text: Описание аргумента.
    :param bool required: Обязателен ли аргумент, defaults to True.
    """
    text: str
    required: bool
    
    def __init__(self, text: str = None, required: bool = True) -> None:
        self.text = text
        self.required = required
    
    def __str__(self) -> str:
        if self.text:
            o_br, c_br = ('<', '>') if self.required else ('[', ']')
            return o_br + '\xa0' + self.text.replace(' ', '\xa0') + '\xa0' + c_br
        return ''

class Command:
    """
    Класс, представляющий команду с ее аргументами и описанием.

    :param list|str commands: Список команд или одна команда.
    :param list[Argument] args: Аргументы команды.
    :param str description: Описание команды.
    """
    commands: List[str]
    args: List[Argument]
    description: str

    def __init__(self, commands: list | str, args: list[Argument], description: str) -> None:
        self.commands = commands if isinstance(commands, list) else [commands]
        self.args = args
        self.description = description


class Feature:
    """
    Класс, представляющий функциональность модуля.

    :param str name: Имя функции.
    :param str description: Описание функции.
    """
    name: str
    description: str
    
    def __init__(self, name, /, description) -> None:
        self.name = name
        self.description = description


class Module:
    """
    Класс, представляющий модуль с командами и функциональностью.

    :param str name: Имя модуля.
    :param str|None description: Описание модуля, defaults to ''.
    :param str|None author: Автор модуля, defaults to ''.
    :param Any|None version: Версия модуля, defaults to None.
    :param List[Command] commands: Список команд модуля, defaults to None.
    :param List[Feature] features: Список функциональностей модуля, defaults to None.
    """
    commands: List[Command]
    features: List[Feature]
    name: str
    description: str
    author: str
    version: Any

    def __init__(
        self: Self,
        name: str,
        *,
        description: str | None = '',
        author: str | None = '',
        version: Any | None = None,
        commands: List[Command] = None,
        features: List[Feature] = None
    ) -> None:
        self.commands = commands if commands else []
        self.features = features if features else []
        self.name = name.removeprefix('plugins.')
        self.description = description
        self.author = author
        self.version = version

    def add_command(self: Self, command: Command, /) -> Self:
        """
        Добавляет команду в модуль.

        :param Command command: Команда для добавления.
        :return Self: Текущий экземпляр модуля.
        """
        self.commands.append(command)
        return self
    
    def get_commands_count(self) -> int:
        """
        Возвращает количество команд в модуле.

        :return int: Количество команд.
        """
        return len(self.commands)

    def get_commands(self) -> List[Command]:
        """
        Возвращает список команд модуля.

        :return List[Command]: Список команд.
        """
        return self.commands
    
    def add_feature(self: Self, feature: Feature, /) -> Self:
        """
        Добавляет функциональность в модуль.

        :param Feature feature: Функциональность для добавления.
        :return Self: Текущий экземпляр модуля.
        """
        self.features.append(feature)
        return self
    
    def get_features_count(self) -> int:
        """
        Возвращает количество функциональностей в модуле.

        :return int: Количество функциональностей.
        """
        return len(self.features)

    def get_features(self) -> List[Feature]:
        """
        Возвращает список функциональностей модуля.

        :return List[Feature]: Список функциональностей.
        """
        return self.features


@singleton
class HelpList:
    """
    Класс для управления модулями и их командами.

    Хранит все модули и предоставляет методы для их добавления и получения.
    """
    modules: Dict[str, Module]

    def __init__(self) -> None:
        self.modules = {}
    
    def add_module(self, module: Module, /) -> Self:
        """
        Добавляет модуль в список.

        :param Module module: Модуль для добавления.
        :return Self: Текущий экземпляр HelpList.
        """
        self.modules[module.name] = module
        return self
    
    def get_module(self, name: str, default: Any = None, lower: bool = False) -> Module:
        """
        Получает модуль по имени.

        :param str name: Имя модуля.
        :param Any default: Значение по умолчанию, если модуль не найден, defaults to None.
        :param bool lower: Нужно ли игнорировать регистр, defaults to False.
        :return Module: Найденный модуль или значение по умолчанию.
        """
        if not lower:
            return self.modules.get(name, default)
        else:
            return dict(zip(
                map(lambda k: k.lower(), self.modules.keys()),
                self.modules.values()
            )).get(name, default)

    def get_modules_count(self) -> int:
        """
        Возвращает количество модулей в списке.

        :return int: Количество модулей.
        """
        return len(self.modules)
    
    def get_modules_names(self) -> List[str]:
        """
        Возвращает имена всех модулей в алфавитном порядке.

        :return List[str]: Список имен модулей.
        """
        return sorted(self.modules.keys(), key=lambda e: e.lower())
    
    def get_modules(self) -> List[Module]:
        """
        Возвращает список всех модулей.

        :return List[Module]: Список модулей.
        """
        return sorted(self.modules.values(), key=lambda m: m.name.lower())
