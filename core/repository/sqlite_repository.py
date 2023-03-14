from inspect import get_annotations
import sqlite3
from core.repository.abstract_repository import AbstractRepository, T
from core.models.expense import Expense
from core.models.category import Category
from core.models.budget import Budget
from typing import Any


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

    # метод, который преобразовывает выхлоп sqlite в словарь
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

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
            cur.row_factory = self.dict_factory
            cur.execute("SELECT * FROM " + self.table_name +
                        " WHERE pk =?;", (pk,))
            rows = cur.fetchall()
            print(rows)

        con.close()

        # обрабатываем случай, когда записи с таким ключом не нашлось
        if not rows:
            return None

        return self.cls(** rows[0])

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.row_factory = self.dict_factory

            # создадим строку условий
            values = []
            cond = ""
            if where != {}:
                cond = " WHERE"
                i = 0
                for field in (list(self.fields.keys()) + ["pk"]):
                    print(field)
                    if where.get(field) is not None:
                        if i != 0:
                            cond += " AND "
                            i += 1

                        cond += "(" + field + " = ?)"
                        values.append(where.get(field))

            print("SELECT * FROM " + self.table_name + cond + ";")
            print(values)
            cur.execute("SELECT * FROM " + self.table_name + cond + ";", values)
            rows = cur.fetchall()
            print(rows)

        con.close()

        if not rows:
            return []
        # возвращаем список объектов
        return [self.cls(** row) for row in rows]

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        print(1)

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        print(1)


objE = SQLiteRepository("../../db/bookkeeper.db", Expense)
print(objE.fields)
print(objE.get(10))
objC = SQLiteRepository("../../db/bookkeeper.db", Category)
print(objC.fields)
print(objC.get(0))
objB = SQLiteRepository("../../db/bookkeeper.db", Budget)
print(objB.fields)
print(objB.get(0))
print(', '.join("?" * 5))

print(objE.get_all({"pk" : 0}))

objE.add(Expense(**{'pk': 1, 'amount': 500.0,
                    'category': 0, 'expense_date': '13-03-2023',
                    'added_date': '13-03-2023', 'comment': 'Большой саб дня'}))
