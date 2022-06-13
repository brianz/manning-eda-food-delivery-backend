# pylint: disable=attribute-defined-outside-init
import abc

from ..adapters import repository

from ..orm import get_session


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository

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


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, close_on_exit=True):
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
        self.session.commit()

    def rollback(self):
        self.session.rollback()
