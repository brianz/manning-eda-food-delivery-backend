from typing import List
from .unit_of_work import AbstractUnitOfWork
from ..domain.model import MenuItem


class InvalidMenuItem(Exception):
    pass


def list_menu_items(uow: AbstractUnitOfWork) -> List[MenuItem]:
    with uow:
        return uow.repo.fetch_menu_items()


def create_new_menu_item(menu_item: MenuItem, uow: AbstractUnitOfWork) -> MenuItem:
    with uow:
        uow.repo.create_menu_item(menu_item)
        uow.commit()

    return menu_item
