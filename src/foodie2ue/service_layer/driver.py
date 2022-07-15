from typing import List

from . import ServiceError
from .unit_of_work import AbstractUnitOfWork
from ..domain.model import Driver
from ..exceptions import DuplicateItemException


def list_drivers(uow: AbstractUnitOfWork) -> List[Driver]:
    return uow.repo.fetch_drivers()


def create_driver(driver: Driver, uow: AbstractUnitOfWork) -> Driver:
    try:
        driver = uow.repo.create_driver(driver)
        return driver, None
    except DuplicateItemException as error:
        msg = 'A driver like this already exists. Make sure the phone number is unique.'
        return (None, ServiceError(msg, error.details))