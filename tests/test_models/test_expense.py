# type: ignore

from core.models.expense import Expense
from datetime import datetime
from core.repository.memory_repository import MemoryRepository
import pytest

@pytest.fixture
def repo():
    return MemoryRepository()
# функция, которая возвращает репозиторий, который мы хотим тестировать

def test_create_with_full_args_list():
    e = Expense(amount=100, category=1, expense_date=datetime.now(),
                added_date=datetime.now(), comment='test', pk=1)
    assert e.amount == 100
    assert e.category == 1


def test_create_brief():
    e = Expense(amount=100, category=1)
    assert e.amount == 100
    assert e.category == 1


def test_can_add_to_repo(repo):
    e = Expense(amount=100, category=1)
    pk = repo.add(e)
    assert e.pk == pk
