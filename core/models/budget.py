from dataclasses import dataclass, field
from datetime import datetime, date
#from core.models.category import Category


@dataclass
class Budget():
    # в бюджете должны быть: срок, категория расходов, сумма
    # он ни от кого не наследуется, видимо

    amount: float
    category: int
    # как и в Expense, передаем не объект катгории
    # а ее номер pk
    term: datetime.date
    name: str
    # на всякий случай, дадим ему еще и имя
    pk: int
    # также добавляем порядковый номер для хранения в бд

    def __init__(self, **kwargs):

        self.pk = 0
        self.name = ""
        self.category = 0

        # если передали, то переопределяем значения по умолчанию
        # если делать инит, то почему-то значения по умолчанию
        # в аннотациях не определяются, так что приходится здесь

        for key, value in kwargs.items():
            setattr(self, key, value)
