"""
Модуль описывает репозиторий, работающий в оперативной памяти
"""

from itertools import count
from typing import Any

from core.repository.abstract_repository import AbstractRepository, T


# эта хрень работает с готовыми экземплярами классов и ничего не создает
# так что конструкторы можно менять на свое усмотрение спокойно
class MemoryRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в оперативной памяти. Хранит данные в словаре.
    """

    def __init__(self) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        pk = next(self._counter)
        self._container[pk] = obj
        obj.pk = pk
        return pk

    def get(self, pk: int) -> T | None:
        # просто используем метод словаря, возвращаем объект или ничего
        return self._container.get(pk)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        if where is None:
            """
            where - условие в виде словаря {'название_поля': значение}
            если условие не задано (по умолчанию), вернуть все записи
            """
            return list(self._container.values())
        return [obj for obj in self._container.values()
                if all(getattr(obj, attr) == value for attr, value in where.items())]

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        self._container.pop(pk)
        # то есть ключи не меняем при удавлении, так как не факт,
        # что удаляем из конца, и необязательно они у нас
        # идут непрерывно, какие-то значения могут быть пропущены
