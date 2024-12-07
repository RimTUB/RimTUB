from typing import Any
import asyncio
import json

import aiosqlite

__all__ = [
    'DatabaseFactory',
    'Database',
    'DictStorage'
]

class DatabaseFactory:
    def __init__(self, file: str) -> None:
        self.file = file

    async def connect_db(self):
        self.connection = await aiosqlite.connect(self.file)

    def get_db(self, id):
        ev = asyncio.get_event_loop()
        ev.create_task(self.connection.execute(f"""
            CREATE TABLE IF NOT EXISTS `{id}` (
            `mod`  TEXT NOT NULL,
            `var`  TEXT NOT NULL,
            `val`  NOT NULL
        )
        """))
        return Database(id, self.connection)

class Database:
    connect: aiosqlite.Connection = None
    id: int

    def __init__(self, id, connect):
        self.id = id
        self.connect = connect

    async def set(self, module: str, variable: str, value: Any) -> None:
        """
        Сохраняет значение переменной в базе данных для указанного модуля.

        :param module: Имя модуля, к которому относится переменная.
        :param variable: Имя переменной.
        :param value: Значение переменной, которое будет сохранено.
        
        ## Пример
        .. code-block:: python
            await app.db.set(__package__, 'count', 10)
        """
        params = dict(mod=module, var=variable, val=json.dumps(value))
        if await (await self.connect.execute(f"SELECT 1 FROM `{self.id}` WHERE mod = :mod AND var = :var", params)).fetchall() == []:
            await self.connect.execute(f"INSERT INTO `{self.id}` (mod, var, val) VALUES (:mod, :var, :val)", params)
        else:
            await self.connect.execute(f"UPDATE `{self.id}` SET val = :val WHERE mod = :mod AND var = :var ", params)

        await self.connect.commit()

    async def get(self, module: str, variable: str, default: Any = None) -> Any:
        """
        Получает значение переменной из базы данных для указанного модуля.

        :param module: Имя модуля, к которому относится переменная.
        :param variable: Имя переменной.
        :param default: Значение по умолчанию, которое будет возвращено, если переменная не найдена.
        :return: Значение переменной или значение по умолчанию.
        
        ## Пример
        .. code-block:: python
            count = await app.db.get(__package__, 'count', 0)
        """
        c = await (await self.connect.execute(
            f"SELECT `val` FROM `{self.id}` WHERE `mod`=:mod AND `var`=:var",
            {'mod': module, 'var': variable}
        )).fetchall()
        if c == []:
            return default
        return json.loads(c[0][0])

    async def getall(self, module: str, default: dict[str, Any] = None) -> dict[str, Any] | None:
        """
        Получает все значения переменных для указанного модуля.

        :param module: Имя модуля, для которого нужно получить все переменные.
        :param default: Значение по умолчанию, которое будет возвращено, если переменные не найдены.
        :return: Словарь с переменными и их значениями или значение по умолчанию.

        
        ## Пример
        .. code-block:: python
            all_values = await app.db.getall(__package__)
        """
        c = await (await self.connect.execute(
            f"SELECT `var` FROM `{self.id}` WHERE `mod` = :mod",
            {'mod': module}
        )).fetchall()

        if c == []:
            return default

        vars = [item[0] for item in c]

        d = {}
        for var in vars:
            d[var] = await self.get(module, var)

        return d

    async def remove(self, module: str, variable: str) -> None:
        """
        Удаляет переменную из базы данных для указанного модуля.

        :param module: Имя модуля, к которому относится переменная.
        :param variable: Имя переменной, которую нужно удалить.

        ## Пример
        .. code-block:: python
            await app.db.remove(__package__, 'count')
        """
        await self.connect.execute(
            f"DELETE FROM `{self.id}` WHERE `mod` = :mod AND `var` = :var",
            {'mod': module, 'var': variable}
        )
        await self.connect.commit()

    delete = remove

    async def exec(self, sql: str) -> list | None:
        """
        Выполняет произвольный SQL-запрос к базе данных.

        *нежелательно для использования*

        :param sql: SQL-запрос, который нужно выполнить.
        :return: Результат выполнения запроса.
        """
        result = await (await self.connect.execute(sql)).fetchall()
        await self.connect.commit()
        return result

    sql = exec

class DictStorage(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set(self, __key: str, __value: Any) -> Any:
        """
        Устанавливает значение для указанного ключа.

        :param __key: Ключ, для которого нужно установить значение.
        :param __value: Значение, которое нужно установить.

        ## Пример
        .. code-block:: python
            app.st.set(f'{__package__}.count', 20)
        """
        self[__key] = __value
