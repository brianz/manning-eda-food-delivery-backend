import abc
from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from ..domain import model
from ..exceptions import UOWDuplicateException


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def fetch_or_create_addon(self, addon: model.AddOn) -> model.AddOn:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_addon(self, item_id: int) -> Optional[model.AddOn]:
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

    def fetch_addon(self, item_id: int) -> Optional[model.AddOn]:
        """Fetch a single AddOn"""
        return self.session.query(model.AddOn).get(item_id)

    def fetch_addons(self) -> List[model.AddOn]:
        """Fetch all AddOns"""
        return self.session.query(model.AddOn).all()

    def add_addon_to_menu_item(self, item: model.MenuItem, addon: model.AddOn):
        """Add an AddOn item to an existing MenuItem"""
        item.addons.append(addon)
        self.session.add(item)

    def update_addon(self, addon: model.AddOn, data: dict) -> Optional[model.AddOn]:
        """Update an AddOn"""
        try:
            self.session.query(model.AddOn).filter(model.AddOn.id == addon.id).update(
                data,
                synchronize_session="fetch",
            )
            self.session.commit()
            self.session.refresh(addon)
            return addon
        except IntegrityError as error:
            raise UOWDuplicateException(error)

    def create_menu_item(self, menu_item: model.MenuItem) -> model.MenuItem:
        """Create a new menu item"""
        self.session.add(menu_item)
        self.session.commit()
        self.session.refresh(menu_item)
        return menu_item

    def fetch_menu_item(self, item_id: int) -> model.MenuItem:
        """Fetch a single menu item by primary key"""
        return self.session.query(model.MenuItem).get(item_id)

    def fetch_menu_items(self) -> List[model.MenuItem]:
        """Fetch all menu items"""
        return self.session.query(model.MenuItem).all()
