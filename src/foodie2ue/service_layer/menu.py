from typing import List
from .unit_of_work import AbstractUnitOfWork, UOWDuplicateException
from ..domain.model import AddOn, MenuItem


class InvalidMenuItem(Exception):
    pass


def get_addon(item_id: int, uow: AbstractUnitOfWork) -> AddOn:
    return uow.repo.fetch_addon(item_id=item_id)


def list_addons(menu_item: MenuItem, uow: AbstractUnitOfWork) -> List[AddOn]:
    return uow.repo.fetch_addons()


def create_new_addon(menu_item: MenuItem, addon: AddOn, uow: AbstractUnitOfWork) -> AddOn:
    uow.repo.create_addon(addon)

    try:
        return (uow.commit(), None)
    except UOWDuplicateException as error:
        return (None, str(error))


def get_menu_item(item_id: int, uow: AbstractUnitOfWork) -> MenuItem:
    return uow.repo.fetch_menu_item(item_id=item_id)


def list_menu_items(uow: AbstractUnitOfWork) -> List[MenuItem]:
    return uow.repo.fetch_menu_items()


def create_new_menu_item(menu_item: MenuItem, uow: AbstractUnitOfWork) -> MenuItem:
    uow.repo.create_menu_item(menu_item)

    try:
        return (uow.commit(), None)
    except UOWDuplicateException as error:
        return (None, str(error))
