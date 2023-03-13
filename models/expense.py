"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime

"""
Используя декоратор @dataclass мы автоматически получаем класс, с реализованными методами __init__, __repr__, __str__ и __eq__

объявление анотации добавляет в __init__ строку типа self.amount = amount
"""

@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0
