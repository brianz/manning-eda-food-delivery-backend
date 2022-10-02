# pylint: disable=attribute-defined-outside-init
import abc
import os

import boto3

from sqlalchemy.exc import IntegrityError

from ..adapters import eventbus, repository
from ..adapters.orm import get_session
from ..exceptions import DuplicateItemException

EVENTBRIDGE_ARN = os.environ['EVENTBRIDGE_ARN']


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository
    broker: eventbus.AbstractEventBroker

    def __init__(self) -> None:
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.broker.publish()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self, instance, **kwargs):
        raise NotImplementedError


def get_eventbridge():
    return boto3.client('events')


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, close_on_exit=True):
        super().__init__()
        self.repo: repository.SqlAlchemyRepository = None
        self.broker: eventbus.AbstractEventBroker = None
        self.__close_on_exit = close_on_exit

    def __enter__(self):
        self.session = get_session()
        self.repo = repository.SqlAlchemyRepository(self.session)

        eventbridge_client = get_eventbridge()
        self.broker = eventbus.EventBridgeBroker(eventbridge_client, EVENTBRIDGE_ARN)

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
