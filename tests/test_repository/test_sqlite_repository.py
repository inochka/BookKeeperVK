#@pytest.mark.parametrize("repo", MemoryRepository(), SQLiteRepository(...))
from core.repository.sqlite_repository import SQLiteRepository
from core.models.expense import Expense
from core.models.category import Category
from core.models.budget import Budget
import os
from pathlib import Path
import pytest

DB_PATH = "../../db/bookkeeper.db"

"""path = Path(os.path.abspath("test_sqlite_repository.py"))
DB_PATH = str(path.parent.parent.parent.absolute()) + '\\db\\bookkeeper.db'
#CLASS_NAMES = ["expense", "budget", "category"]
print(DB_PATH)"""

"""    objects = [
        [
            Expense(**{'pk': 1, 'amount': 500.0,
                    'category': 0, 'expense_date': '13-03-2023',
                    'added_date': '13-03-2023', 'comment': 'Большой саб дня'}),
            Expense(**{'pk': pk_e, 'amount': 500.0,
                    'category': 0, 'expense_date': '14-03-2023',
                    'added_date': '15-03-2023', 'comment': 'Большой 1 саб дня'})
         ],
        [
            Budget(**{'name': "Бюджет до конца марта", "amount": 10000, "category": 1, "term": "31-03-2023"}),
            Budget(**{'pk': pk_b, 'name': "Развлечения до конца марта",
                        "amount": 10000, "category": 1, "term": "31-03-2023"})
        ],
        [Category(**{'name': "Хозтовары"}),
            Category(**{'name': "Хозтовары", "parent": 0})
        ]
        
    ]
"""

# создаем подключения к каждой из таблиц
sql_e = SQLiteRepository(DB_PATH, Expense)
sql_c = SQLiteRepository(DB_PATH, Category)
sql_b = SQLiteRepository(DB_PATH, Budget)

# создаем объекты, которые будем добавлять, pk здесь не имеет значения все равно бд свой выдаст
obj_e = Expense(**{'pk': 1, 'amount': 500.0,
                    'category': 0, 'expense_date': '13-03-2023',
                    'added_date': '13-03-2023', 'comment': 'Большой саб дня'})
obj_c = Category(**{'name': "Хозтовары"})
obj_b = Budget(**{'name': "Бюджет до конца марта", "amount": 10000, "category": 1, "term": "31-03-2023"})


"""
@pytest.fixture
def repo():
    return SQLiteRepository(DB_PATH, Expense)

"""
def test_crud():

    #print(objE.get_all({"pk" : 0}))


    # проверяем create
    pk_e = sql_e.add(obj_e)
    pk_c = sql_c.add(obj_c)
    pk_b = sql_b.add(obj_b)

    # проверяем read
    # считываем объекты, чтобы сохранить pk
    obj_e_r = sql_e.get(pk_e)
    obj_c_r = sql_c.get(pk_c)
    obj_b_r = sql_b.get(pk_b)

    # проверяем, что считали именно то, что вносили
    assert obj_e_r == obj_e
    assert obj_c_r == obj_c
    assert obj_b_r == obj_b

    # проверяем udpate

    # создаем объекты, которыми будем обновлять

    obj_e_upd = Expense(**{'pk': pk_e, 'amount': 500.0,
                            'category': 0, 'expense_date': '14-03-2023',
                            'added_date': '15-03-2023', 'comment': 'Большой 1 саб дня'})

    obj_b_upd = Budget(**{'pk': pk_b, 'name': "Развлечения до конца марта",
                              "amount": 10000, "category": 1, "term": "31-03-2023"})

    obj_c_upd = Category(**{"pk": pk_c, 'name': "Хозтовары", "parent": 0})

    sql_e.update(obj_e_upd)
    sql_b.update(obj_b_upd)
    sql_c.update(obj_c_upd)

    assert sql_e.get(pk_e) == obj_e_upd
    assert sql_b.get(pk_b) == obj_b_upd
    assert sql_c.get(pk_c) == obj_c_upd


    # проверяем delete

    sql_e.delete(pk_e)
    sql_b.delete(pk_b)
    sql_c.delete(pk_c)

    # проверяем, что запись действительно исчезла
    assert sql_e.get(pk_e) is None
    assert sql_b.get(pk_b) is None
    assert sql_c.get(pk_c) is None


"""
видимо, для скл это уже не надо
def test_cannot_add_without_pk():
    with pytest.raises(ValueError):
        repo.add(0)
"""
def test_cannot_delete_unexistent():
    with pytest.raises(KeyError):
        sql_e.delete(9999999999)


def test_cannot_update_without_pk():
    with pytest.raises(ValueError):
        obj_e_m = obj_e
        obj_e_m.pk = None
        sql_e.update(obj_e_m)


"""def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects"""

"""
def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        o.test = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'}) == [objects[0]]
    assert repo.get_all({'test': 'test'}) == objects
"""

test_crud()
