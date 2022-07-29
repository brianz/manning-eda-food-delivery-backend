import abc

from typing import List, Optional

from sqlalchemy.exc import (
    DataError,
    IntegrityError,    # InvalidTextRepresentation,
    MultipleResultsFound,
)

# sqlalchemy.exc.DataError: (psycopg2.errors.InvalidTextRepresentation)

from ..constants import (
    ORDER_STATUS_NEW,
    ORDER_STATUS_READY_FOR_PICKUP,
)
from ..domain import model
from ..exceptions import (
    DuplicateItemException,
    MultipleItemsFoundException,
    InvalidOrderStateException,
)


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

    def fetch_addon_by(self, name: Optional[str]) -> Optional[model.AddOn]:
        raise NotImplementedError

    @abc.abstractmethod
    def update_addon(self, addon: model.AddOn, data: dict) -> Optional[model.AddOn]:
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

    @abc.abstractmethod
    def fetch_menu_item_by(self, name: Optional[str]) -> Optional[model.MenuItem]:
        raise NotImplementedError

    @abc.abstractmethod
    def update_menu_item(self, menu_item: model.MenuItem, data: dict) -> Optional[model.MenuItem]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_order(self, order: model.Order) -> Optional[model.Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_new_orders(self) -> List[model.Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_ready_for_pickup_orders(self) -> List[model.Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_order(self, item_id: int) -> model.Order:
        raise NotImplementedError

    @abc.abstractmethod
    def update_order_status(self, order: model.Order, status: str) -> Optional[model.Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_drivers(self) -> List[model.Driver]:
        raise NotImplementedError

    @abc.abstractmethod
    def create_driver(self, driver: model.Driver) -> Optional[model.Driver]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def __create_and_refesh_model(self, model):
        self.session.add(model)
        return self.__refesh_model(model)

    def __refesh_model(self, model):
        self.session.commit()
        self.session.refresh(model)
        return model

    def fetch_or_create_addon(self, addon: model.AddOn) -> model.AddOn:
        """Create a new AddOn item for a given MenuItem"""
        _addon = self.fetch_addon_by(name=addon.name)
        if _addon:
            return _addon
        return self.__create_and_refesh_model(addon)

    def fetch_addon(self, item_id: int) -> Optional[model.AddOn]:
        """Fetch a single AddOn"""
        return self.session.query(model.AddOn).get(item_id)

    def fetch_addons(self) -> List[model.AddOn]:
        """Fetch all AddOns"""
        return self.session.query(model.AddOn).all()

    def fetch_addon_by(self, name: Optional[str]) -> Optional[model.AddOn]:
        if name:
            return self.session.query(model.AddOn).filter_by(name=name).one_or_none()

        return None

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
            raise DuplicateItemException(error)

    def create_menu_item(self, menu_item: model.MenuItem) -> model.MenuItem:
        """Create a new menu item"""
        try:
            return self.__create_and_refesh_model(menu_item)
        except IntegrityError as error:
            raise DuplicateItemException(error)

    def fetch_menu_item(self, item_id: int) -> model.MenuItem:
        """Fetch a single menu item by primary key"""
        return self.session.query(model.MenuItem).get(item_id)

    def fetch_menu_items(self) -> List[model.MenuItem]:
        """Fetch all menu items"""
        return self.session.query(model.MenuItem).all()

    def fetch_menu_item_by(self,
                           name: Optional[str] = '',
                           size: Optional[str] = '') -> Optional[model.MenuItem]:
        if not (name or size):
            return None

        filters = {}
        if name:
            filters['name'] = name
        if size:
            filters['size'] = size.lower()

        try:
            return self.session.query(model.MenuItem).filter_by(**filters).one_or_none()
        except MultipleResultsFound as error:
            # For menu items, when there are multiple items with the same name but different sizes,
            # querying for just the name will result in multiple items being returned. In that case
            # we'll error out.
            raise MultipleItemsFoundException(error)

    def update_menu_item(self, menu_item: model.MenuItem, data: dict) -> Optional[model.MenuItem]:
        try:
            self.session.query(model.MenuItem).filter(model.MenuItem.id == menu_item.id).update(
                data,
                synchronize_session="fetch",
            )
            self.session.commit()
            self.session.refresh(menu_item)
            return menu_item
        except IntegrityError as error:
            raise DuplicateItemException(error)

    def create_order(self, order: model.Order) -> model.Order:
        return self.__create_and_refesh_model(order)

    def fetch_new_orders(self) -> List[model.Order]:
        return self.session.query(model.Order).filter(model.Order.status == ORDER_STATUS_NEW).all()

    def fetch_ready_for_pickup_orders(self) -> List[model.Order]:
        return self.session.query(
            model.Order).filter(model.Order.status == ORDER_STATUS_READY_FOR_PICKUP).all()

    def fetch_order(self, item_id: int) -> model.Order:
        return self.session.query(model.Order).get(item_id)

    def update_order_status(self, order: model.Order, status: str) -> Optional[model.Order]:
        try:
            self.session.query(model.Order).filter(model.Order.id == order.id).update(
                {'status': status},
                synchronize_session="fetch",
            )
            return self.__refesh_model(order)
        except DataError as error:
            raise InvalidOrderStateException(error)

    def fetch_drivers(self) -> List[model.Driver]:
        return self.session.query(model.Driver).all()

    def create_driver(self, driver: model.Driver) -> Optional[model.Driver]:
        try:
            return self.__create_and_refesh_model(driver)
        except IntegrityError as error:
            raise DuplicateItemException(error)
