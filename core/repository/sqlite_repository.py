from inspect import get_annotations
import sqlite3
from core.repository.abstract_repository import AbstractRepository, T
from core.models.expense import Expense
from typing import Any


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteRepository(AbstractRepository[T]):

    db_file: str
    cls: type
    table_name: str
    fields: dict

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        # имя таблицы должно быть ловеркейсом от имени класса, ок
        self.fields = get_annotations(cls, eval_str=True)
        # и поля должны быть в точности такие же, как и аттрибуты
        self.fields.pop('pk')
        self.cls = cls

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(f'INSERT INTO {self.table_name} ({names}) VALUES({p})', values)
            obj.pk = cur.lastrowid

        con.close()
        return obj.pk

        """ Получить объект по id """
        #видимо, получаем объект заданного класса
    def get(self, pk: int) -> T | None:
        # открываем соединение и работаем
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.row_factory = dict_factory
            cur.execute("SELECT * FROM expense WHERE pk = ?;", (pk,))
            rows = cur.fetchall()
            print(rows)

        con.close()
        return self.cls(** rows[0])

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        print(1)

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        print(1)

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        print(1)


obj = SQLiteRepository("../../db/bookkeeper.db", Expense)
print(obj.fields)
print(obj.get(0))
### !!! видимо, мы при расходе помещаем сразу во все 3 таблицы данные?? или как?
