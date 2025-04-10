from difflib import get_close_matches
from typing import Any, Dict, List, Self
from .scripts import singleton


__all__ = [
    'Argument',
    'Section',
    'HModule',
    'Command',
    'Feature',
    'HelpList'
]




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


class Section:
    """
    Класс, представляющий секцию модуля. 

    :param str name: Имя секции.
    :param str description: Описание секции.
    """
    name: str
    description: str
    commands: List[Command]
    features: List[Feature]

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.commands = []
        self.features = []

    def add_command(self, command: Command) -> Self:
        """
        Добавляет команду в секцию.

        :param Command command: Команда для добавления.
        :return Self: Текущая секция.
        """
        self.commands.append(command)
        return self

    def add_feature(self, feature: Feature) -> Self:
        """
        Добавляет функциональность в секцию.

        :param Feature feature: Функциональность для добавления.
        :return Self: Текущая секция.
        """
        self.features.append(feature)
        return self

    def get_commands(self) -> List[Command]:
        """
        Возвращает список команд секции.

        :return List[Command]: Список команд.
        """
        return self.commands

    def get_features(self) -> List[Feature]:
        """
        Возвращает список функциональностей секции.

        :return List[Feature]: Список функциональностей.
        """
        return self.features

    def get_commands_count(self) -> int:
        """
        Возвращает количество команд в секции.

        :return int: Количество команд.
        """
        return len(self.commands)

    def get_features_count(self) -> int:
        """
        Возвращает количество функциональностей в секции.

        :return int: Количество функциональностей.
        """
        return len(self.features)
    

class HModule:
    """
    Класс, представляющий модуль с командами, секциями и функциональностями.

    :param str name: Имя модуля.
    :param str|None description: Описание модуля, defaults to ''.
    :param str|None author: Автор модуля, defaults to ''.
    :param Any|None version: Версия модуля, defaults to None.
    :param List[Command] commands: Список команд модуля, defaults to None.
    :param List[Feature] features: Список функциональностей модуля, defaults to None.
    """
    sections: Dict[str, Section]
    name: str
    description: str
    author: str
    version: Any

    def __init__(self, name, *, description='', author='', version=None, ok=False):
        if not ok:
            raise RuntimeError()
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.sections = {}

    def add_section(self, section: Section) -> Section:
        """
        Добавляет секцию в модуль.

        :param name: Имя секции.
        :param description: Описание секции.
        :return: Добавленная секция.
        """
        self.sections[section.name] = section
        return section

    def get_section(self, name: str) -> Section | None:
        """
        Возвращает секцию по имени.

        :param str name: Имя секции.
        :return Section | None: Найденная секция или None.
        """
        return self.sections.get(name)

    def get_sections_count(self) -> int:
        """
        Возвращает количество секций в модуле.

        :return int: Количество секций.
        """
        return len(self.sections)

    def get_sections(self) -> Dict[str, Section]:
        """
        Возвращает словарь всех секций модуля.

        :return Dict[str, Section]: Словарь секций.
        """
        return self.sections

    def get_commands_count(self) -> int:
        """
        Возвращает общее количество команд во всех секциях модуля.

        :return int: Общее количество команд.
        """
        return sum(section.get_commands_count() for section in self.sections.values())
    
    def get_features_count(self) -> int:
        """
        Возвращает общее количество функциональностей во всех секциях модуля.

        :return int: Общее количество функциональностей.
        """
        return sum(section.get_features_count() for section in self.sections.values())

@singleton
class HelpList:
    """
    Класс для управления модулями и их командами.

    Хранит все модули и предоставляет методы для их добавления и получения.
    """
    modules: Dict[str, HModule]
    _inited = False

    def __init__(self) -> None:
        if not self._inited:
            self.modules = {}
            self._inited = True
    
    def add_module(self, module: HModule, /) -> Self:
        """
        Добавляет модуль в список.

        :param Module module: Модуль для добавления.
        :return Self: Текущий экземпляр HelpList.
        """
        self.modules[module.name] = module
        return self
    
    def get_module(self, name: str, default: Any = None, lower: bool = False, similarity_threshold: float = 0.6) -> HModule | Any:
        """
        Получает модуль по имени или наиболее похожему имени.

        :param str name: Имя модуля.
        :param Any default: Значение по умолчанию, если модуль не найден, defaults to None.
        :param bool lower: Нужно ли игнорировать регистр, defaults to False.
        :param float similarity_threshold: Минимальный порог похожести, defaults to 0.6.
        :return Any: Найденный модуль или значение по умолчанию.
        """
        modules_dict = self.modules

        if lower:
            modules_dict = dict(zip(
                map(lambda k: k.lower(), self.modules.keys()),
                self.modules.values()
            ))
            name = name.lower()

        closest_matches = get_close_matches(name, modules_dict.keys(), n=1, cutoff=similarity_threshold)
        if closest_matches:
            return modules_dict[closest_matches[0]]
        return default

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
    
    def get_modules(self) -> List[HModule]:
        """
        Возвращает список всех модулей.

        :return List[Module]: Список модулей.
        """
        return sorted(self.modules.values(), key=lambda m: m.name.lower())
