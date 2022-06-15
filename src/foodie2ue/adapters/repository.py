import abc
from typing import List

from ..domain import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def create_addon(self, addon: model.AddOn):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_addon(self, item_id: int) -> model.AddOn:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_addons(self) -> List[model.AddOn]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_menu_item(self, menu_item: model.MenuItem):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_menu_item(self, item_id: int) -> model.MenuItem:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_menu_items(self) -> List[model.MenuItem]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def create_addon(self, addon: model.AddOn):
        """Create a new AddOn item for a given MenuItem"""
        self.session.add(addon)

    def fetch_addon(self, item_id: int) -> model.AddOn:
        """Fetch a single AddOn"""
        return self.session.query(model.AddOn).get(item_id)

    def fetch_addons(self) -> List[model.AddOn]:
        """Fetch all AddOns"""
        return self.session.query(model.AddOn).all()

    def create_menu_item(self, menu_item: model.MenuItem):
        """Create a new menu item"""
        self.session.add(menu_item)

    def fetch_menu_item(self, item_id: int) -> model.MenuItem:
        """Fetch a single menu item by primary key"""
        return self.session.query(model.MenuItem).get(item_id)

    def fetch_menu_items(self) -> List[model.MenuItem]:
        """Fetch all meanu items"""
        q = self.session.query(model.MenuItem).outerjoin(model.AddOn)
        return q.all()
