from core.models.budget import Budget
from datetime import datetime, date

import pytest

from datetime import date
today = str(date.today())
print(today)   # '2017-12-26'


def test_create_with_full_args_list():
    b = Budget(amount=100, category=1, term=date.today(), pk=1, name="test")
    assert b.amount == 100
    assert b.category == 1
    assert b.pk == 1
    assert b.name == "test"


def test_create_brief():
    e = Budget(100, 1, date.today(), )
    assert e.amount == 100
    assert e.category == 1

