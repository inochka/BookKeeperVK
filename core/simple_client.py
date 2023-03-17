"""
Простой тестовый скрипт для терминала
"""

from core.models.category import Category
from core.models.expense import Expense
from core.repository.memory_repository import MemoryRepository
from core.repository.sqlite_repository import SQLiteRepository
from core.utils import read_tree

'''"cat_repo = MemoryRepository[Category]
exp_repo = MemoryRepository[Expense]"'''

cat_repo = SQLiteRepository(Category, "../db/bookkeeper.db")
exp_repo = SQLiteRepository(Expense, "../db/bookkeeper.db")

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

#Category.create_from_tree(read_tree(cats), cat_repo)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    elif cmd == "exit":
        break
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(amount=int(amount), category=cat.pk)
        exp_repo.add(exp)
        print(exp)

# нужно добавить уникальность каждой категории по имени в бд
