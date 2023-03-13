import pytest

from repository.abstract_repository import AbstractRepository

# видимо, эту щтуку корректно запускать только из консоли непосредственно через pytest


def test_cannot_create_abstract_repository():
    with pytest.raises(TypeError):
        AbstractRepository()


def test_can_create_subclass():
    class Test(AbstractRepository):
        def add(self, obj): pass
        def get(self, pk): pass
        def get_all(self, where=None): pass
        def update(self, obj): pass
        def delete(self, pk): pass

    t = Test()
    assert isinstance(t, AbstractRepository)
