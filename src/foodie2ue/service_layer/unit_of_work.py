# pylint: disable=attribute-defined-outside-init
import abc
from typing import Optional

from sqlalchemy.exc import IntegrityError

from ..adapters import repository
from ..adapters.orm import get_session
from ..exceptions import DuplicateItemException


class AbstractUnitOfWork(abc.ABC):

    def __init__(self) -> None:
        self.repo: Optional[repository.AbstractRepository] = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self, instance, **kwargs):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, close_on_exit=True):
        self.repo: Optional[repository.SqlAlchemyRepository] = None
        self.__close_on_exit = close_on_exit

    def __enter__(self):
        self.session = get_session()
        self.repo = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        if self.__close_on_exit:
            self.session.close()

    def close(self):
        self.session.close()

    def commit(self):
        try:
            return self.session.commit()
        except IntegrityError as error:
            raise DuplicateItemException(error)

    def rollback(self):
        self.session.rollback()

    def refresh(self, instance, **kwargs):
        self.session.refresh(instance, **kwargs)
