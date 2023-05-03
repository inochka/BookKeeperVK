from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any, Callable, Type
from core.models.expense import Expense
from core.models.category import Category
from core.models.budget import Budget
import core.view.widgets

# нужно, по-хорошему, написать класс-обработчик событий, чтобы и для тг, и для графона было норм

class AbstractView(Protocol):
    # Вывод общего окна

    @abstractmethod
    def init_window(self):
        """общее окно и то, какая вкладка открыта"""

    # Category_framework

    @abstractmethod
    def set_category_list(self, l: list[Category]) -> None:
        """ вывести список категорий """

    @abstractmethod
    def register_cat_modifier(self,
                              handler: Callable[[Category], None]):
        """зарегистрировать графический модификатор категорий"""

    @abstractmethod
    def register_cat_adder(self, handler):
        """ #self.cat_adder = handler"""

    @abstractmethod
    def add_category(self):
        """# получение данных из формочки
        #name = ...
        #parent = ..."""

    # Expense_framework

    @abstractmethod
    def set_expense_list(self, l: list[Expense]) -> None:
        """ вывести список расходов """

    @abstractmethod
    def register_expense_modifier(self,
                              handler: Callable[[Category], None]):
        """зарегистрировать графический модификатор расходов"""

    @abstractmethod
    def register_expense_adder(self, handler):
        """ регистрация обработчика событий добавления расходов """
        # в тг-боте мы просто через декоратор его подвесим, видимо

    @abstractmethod
    def add_expense(self):
        """добавить расход"""

    # budget_framework

    @abstractmethod
    def set_budget_list(self, l: list[Budget]) -> None:
        """ вывести список бюджетов """

    @abstractmethod
    def register_budget_modifier(self,
                              handler: Callable[[Category], None]):
        """зарегистрировать графический модификатор бюджета"""

    @abstractmethod
    def register_budget_adder(self, handler):
        """ регистрация граф обработчика событий добавления бюджета """

    @abstractmethod
    def add_budget(self):
        """добавить бюджет"""

