import asyncio
from typing import Any
import json

import aiosqlite

__all__ = [
    'DictStorage',
    'ModuleDB'
]



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
            mod.st.set('count', 20)
        """
        self[__key] = __value


class ModuleDB:
    """
    Класс базы данных модуля на базе aiosqlite

    Методы:
        set: Сохранить переменную
        get: Получить переменную
        delete: Удалить переменную
        getall: Получить все переменные

        sql: Выполнить SQL запрос

    Параметры:
        path: путь к файлу БД
        con: соединение с БД (aiosqlite.Connection)
    """
    path: str
    con: aiosqlite.Connection

    def __init__(self, path) -> None:
        self.path = path
        self.con = None
    
    def __del__(self):
        print('__del__')
        asyncio.run(self.teardown())
        print('__del__ done')

    async def bootstrap(self) -> None:
        if not self.con:
            self.con = await aiosqlite.connect(self.path)

        await self.sql(f"""
            CREATE TABLE IF NOT EXISTS `_variables` (
            `var`  TEXT NOT NULL,
            `val`  NOT NULL
        )
        """)


    async def teardown(self) -> None:
        await self.con.close()
        

    async def sql(self, sql: str, asdict: bool = False, **params) -> list | None:
        """
        Выполнить SQL запрос.

        :param bool asdict: Вернуть результат в формате словаря (колонка: значение)
        """
        cursor = await self.con.execute(sql, params)
        rows = await cursor.fetchall()
        
        if asdict:
            columns = [column[0] for column in cursor.description]
            await self.con.commit()
            return [dict(zip(columns, row)) for row in rows]
        
        await self.con.commit()
        return rows
    

    async def set(self, variable: str, value: Any) -> None:
        """
        Сохраняет значение переменной в базе данных для указанного модуля.

        :param variable: Имя переменной.
        :param value: Значение переменной, которое будет сохранено.
        
        ## Пример
        .. code-block:: python
            await mod.db.set('count', 10)
        """
        params = dict(var=variable, val=json.dumps(value))
        if (await self.sql(f"SELECT 1 FROM `_variables` WHERE var = :var", **params)) == []:
            await self.sql(f"INSERT INTO `_variables` (var, val) VALUES (:var, :val)", **params)
        else:
            await self.sql(f"UPDATE `_variables` SET val = :val WHERE var = :var ", **params)


    async def get(self, variable: str, default: Any = None) -> Any:
        """
        Получает значение переменной из базы данных для указанного модуля.

        :param variable: Имя переменной.
        :param default: Значение по умолчанию, которое будет возвращено, если переменная не найдена.
        :return: Значение переменной или значение по умолчанию.
        
        ## Пример
        .. code-block:: python
            count = await mod.db.get('count', 0)
        """
        c = await self.sql(
            f"SELECT `val` FROM `_variables` WHERE `var`=:var",
            var=variable
        )
        if c == []:
            return default
        return json.loads(c[0][0])

    async def getall(self, default: Any = None) -> dict[str, Any] | None:
        """
        Получает все значения переменных для указанного модуля.

        :param default: Значение по умолчанию, которое будет возвращено, если переменные не найдены.
        :return: Словарь с переменными и их значениями или значение по умолчанию.

        
        ## Пример
        .. code-block:: python
            all_values = await mod.db.getall()
        """
        c = await self.sql(
            f"SELECT `var` FROM `_variables`",
        )

        if c == []:
            return default

        vars = [item[0] for item in c]

        d = {}
        for var in vars:
            d[var] = await self.get(var)

        return d

    async def remove(self, variable: str) -> None:
        """
        Удаляет переменную из базы данных для указанного модуля.

        :param variable: Имя переменной, которую нужно удалить.

        ## Пример
        .. code-block:: python
            await mod.db.remove('count')
        """
        await self.sql(
            f"DELETE FROM `_variables` WHERE `var` = :var", var=variable
        )

    delete = remove