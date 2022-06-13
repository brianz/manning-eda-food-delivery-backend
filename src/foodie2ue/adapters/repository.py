import abc
from typing import List

from ..domain import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def create_menu_item(self, menu_item: model.MenuItem):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_menu_items(self) -> List[model.MenuItem]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def create_menu_item(self, menu_item: model.MenuItem):
        self.session.add(menu_item)

    def fetch_menu_items(self) -> List[model.MenuItem]:
        return self.session.query(model.MenuItem).all()
