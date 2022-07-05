from typing import List, Optional, Tuple

from .unit_of_work import AbstractUnitOfWork
from ..domain.model import AddOn, MenuItem
from ..exceptions import UOWDuplicateException, Foodie2ueException


def get_addon(item_id: int, uow: AbstractUnitOfWork) -> AddOn:
    return uow.repo.fetch_addon(item_id=item_id)


def update_addon(add_on: AddOn, data: dict,
                 uow: AbstractUnitOfWork) -> Tuple[Optional[AddOn], Optional[Foodie2ueException]]:
    # This is needed b/c trying to run an update when the name is the same results in a duplicate
    # key exception
    if data.get('name') == add_on.name:
        data.pop('name')

    try:
        uow.repo.update_addon(add_on, data=data)
        return add_on, None
    except UOWDuplicateException as error:
        return (None, error)


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


def list_menu_items(uow: AbstractUnitOfWork) -> List[MenuItem]:
    return uow.repo.fetch_menu_items()


def create_new_menu_item(
        menu_item: MenuItem,
        uow: AbstractUnitOfWork) -> Tuple[Optional[MenuItem], Optional[Foodie2ueException]]:

    try:
        uow.repo.create_menu_item(menu_item)
        return menu_item, None
    except UOWDuplicateException as error:
        return (None, error)
