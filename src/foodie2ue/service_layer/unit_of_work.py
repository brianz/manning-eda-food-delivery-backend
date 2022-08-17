# pylint: disable=attribute-defined-outside-init
import abc
import os

import boto3

from typing import List

from sqlalchemy.exc import IntegrityError

from ..adapters import eventbus, repository
from ..adapters.orm import get_session
from ..domain import events
from ..exceptions import DuplicateItemException

EVENTBRIDGE_ARN = os.environ['EVENTBRIDGE_ARN']


def get_eventbridge():
    return boto3.client('events')


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository
    messagebus: eventbus.AbstractMessageBus

    def __init__(self) -> None:
        super().__init__()
        self._events: List[events.Event] = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for event in self._events:
            self.messagebus.publish_event(
                event_type=event.__class__.__name__,
                payload=event.asdict(),
            )

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self, instance, **kwargs):
        raise NotImplementedError

    def add_event(self, event: events.Event) -> None:
        self._events.append(event)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, close_on_exit=True):
        super().__init__()
        self.repo: repository.SqlAlchemyRepository = None
        self.messagebus: eventbus.AbstractMessageBus = None
        self.__close_on_exit = close_on_exit

    def __enter__(self):
        self.session = get_session()
        self.repo = repository.SqlAlchemyRepository(self.session)

        self.eventbridge = get_eventbridge()
        self.messagebus = eventbus.EventBridge(self.eventbridge, EVENTBRIDGE_ARN)

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
