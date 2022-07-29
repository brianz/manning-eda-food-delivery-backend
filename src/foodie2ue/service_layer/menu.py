from typing import List, Optional, Tuple

from . import ServiceError
from ..domain.model import AddOn, MenuItem
from ..exceptions import DuplicateItemException
from .unit_of_work import AbstractUnitOfWork


def get_addon(item_id: int, uow: AbstractUnitOfWork) -> AddOn:
    return uow.repo.fetch_addon(item_id=item_id)


def update_addon(add_on: AddOn, data: dict,
                 uow: AbstractUnitOfWork) -> Tuple[Optional[AddOn], Optional[ServiceError]]:
    # This is needed b/c trying to run an update when the name is the same results in a duplicate
    # key exception
    if data.get('name') == add_on.name:
        data.pop('name')

    try:
        uow.repo.update_addon(add_on, data=data)
        return add_on, None
    except DuplicateItemException as error:
        msg = 'There is already an addon with this name'
        return (None, ServiceError(msg, error.details))


def list_addons(uow: AbstractUnitOfWork) -> List[AddOn]:
    """Return all AddOns"""
    return uow.repo.fetch_addons()


def create_new_addon(addon: AddOn, uow: AbstractUnitOfWork) -> AddOn:
    return uow.repo.fetch_or_create_addon(addon)


def add_addon_to_menu_item(item: MenuItem, addon: AddOn, uow: AbstractUnitOfWork) -> MenuItem:
    uow.repo.add_addon_to_menu_item(item, addon)
    return item


def get_menu_item(item_id: int, uow: AbstractUnitOfWork) -> MenuItem:
    return uow.repo.fetch_menu_item(item_id=item_id)


def update_menu_item(menu_item: MenuItem, data: dict,
                     uow: AbstractUnitOfWork) -> Tuple[Optional[AddOn], Optional[ServiceError]]:
    if data.get('name') == menu_item.name:
        data.pop('name')

    try:
        uow.repo.update_menu_item(menu_item, data=data)
        return menu_item, None
    except DuplicateItemException as error:
        msg = 'A menu item like this already exists. Make sure the name and size are unique.'
        return (None, ServiceError(msg, error.details))


def list_menu_items(uow: AbstractUnitOfWork) -> List[MenuItem]:
    return uow.repo.fetch_menu_items()


def create_new_menu_item(
        menu_item: MenuItem,
        uow: AbstractUnitOfWork) -> Tuple[Optional[MenuItem], Optional[ServiceError]]:
    try:
        uow.repo.create_menu_item(menu_item)
        return menu_item, None
    except DuplicateItemException as error:
        msg = 'A menu item like this already exists. Make sure the name and size are unique.'
        return (None, ServiceError(msg, error.details))