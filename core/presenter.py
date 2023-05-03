# взаимодействие со вьювером и бд

from view.abstract_view import AbstractView
from core.models.expense import Expense
from core.models.category import Category
from core.models.budget import Budget

class Bookkeeper:   # presenter
    def __init__(self,
                 view: AbstractView,
                 repository_factory):

        self.view = view

        # repository_factory - штука, которая возвращает объект бд нужного типа
        self.category_repository = repository_factory.get(Category)
        self.expenses_repository = repository_factory.get(Expense)

        self.cats = self.category_repository.get_all()

        self.view.set_category_list(self.cats)
        self.view.register_cat_modifier(self.modify_cat)

    def modify_cat(self, cat: Category) -> None:
        self.category_repository.update(cat)
        self.view.set_category_list(self.cats)

    def add_category(self, name, parent) -> None:
        if name in [c.name for c in self.cats]:
            raise ValueError(f'Категория {name} уже существует')
        cat = Category(**{"name": name, "parent": parent})
        self.category_repository.add(cat)
        self.cats.append(cat)
        self.view.set_category_list(self.cats)

    def delete_category(self, name, parent, delete_expenses=False):
        pass
        # нужно категорию удалить, а все записи из нее перенести в родительскую категорию
        # или удалить, в зависимости от опции из условия

    def add_expense(self, exp: Expense):
        # категория есть уже в самом объекте Expense
        pass

    def modify_expense(self, exp: Expense):
        pass

    def delete_expense(self, exp: Expense):
        # категория есть уже в самом объекте Expense
        pass

    def add_budget(self, budget: Budget):
        pass

    def modify_budget(self, budget: Budget):
        pass

    def delete_budget(self, budget: Expense):
        pass

    def show_expenses(self, start_date, end_date, cat_list=None):
        if cat_list is None:
            cat_list = []
            pass
        else:
            pass

    def show_categories(self):
        pass

    def show_budgets(self):
        pass


