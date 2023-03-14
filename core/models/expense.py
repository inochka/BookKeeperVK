"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime
from inspect import get_annotations
"""
Используя декоратор @dataclass мы автоматически получаем класс,
с реализованными методами __init__, __repr__, __str__ и __eq__
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
    expense_date: datetime
    added_date: datetime
    comment: str
    pk: int

    def __init__(self, **kwargs):
        """self.pk = pk
        self.amount = amount
        self.expense_date = expense_date
        self.added_date = added_date
        self.comment = comment"""

        self.expense_date = field(default_factory=datetime.now)
        self.added_date = field(default_factory=datetime.now)
        self.comment = ''
        self.pk = 0

        # если передали, то переопределяем значения по умолчанию
        # если делать инит, то почему-то значения по умолчанию
        # в аннотациях не определяются, так что приходится здесь

        for key, value in kwargs.items():
            setattr(self, key, value)

    # также реализуем метод сравнения для удобства

    def __eq__(self, other):
        if not isinstance(other, Expense):
            # don't attempt to compare against unrelated types
            return NotImplemented

        attrs = get_annotations(Expense, eval_str=True)
        attrs.pop("pk")
        for f in attrs:
            if getattr(self, f) != getattr(other, f):
                return False

        return True

"""
exp = Expense(**{'pk': 0, 'amount': 200.0, 'category': 0, 'expense_date': '13-03-2023', 'added_date': '13-03-2023', 'comment': 'Кофе в столовке'})
exp1 = Expense(**{'pk': 0, 'amount': 300.0, 'category': 0, 'expense_date': '13-03-2023', 'added_date': '13-03-2023', 'comment': 'Кофе в столовке'})
print(exp == exp1)
"""
