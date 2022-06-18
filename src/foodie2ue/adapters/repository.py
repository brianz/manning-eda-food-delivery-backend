import abc
from typing import List, Optional

from ..domain import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def fetch_or_create_addon(self, addon: model.AddOn) -> model.AddOn:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_addon_by_name(self, name: str) -> Optional[model.AddOn]:
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

    def fetch_or_create_addon(self, addon: model.AddOn) -> model.AddOn:
        """Create a new AddOn item for a given MenuItem"""
        _addon = self.session.query(model.AddOn).filter_by(name=addon.name).one_or_none()
        if _addon:
            return _addon

        self.session.add(addon)
        self.session.commit()
        self.session.refresh(addon)
        return addon

    def add_addon_to_menu_item(self, item: model.MenuItem, addon: model.AddOn):
        item.addons.append(addon)
        self.session.add(item)

    def fetch_addon_by_name(self, name: str) -> Optional[model.AddOn]:
        """Fetch a single AddOn"""
        return self.session.query(model.AddOn).filter_by(name=name).one_or_none()

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
        """Fetch all menu items"""
        return self.session.query(model.MenuItem).all()
