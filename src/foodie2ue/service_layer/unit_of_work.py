# pylint: disable=attribute-defined-outside-init
import abc
import os

from sqlalchemy.exc import IntegrityError

from . import eventbus
from ..adapters import repository
from ..adapters.orm import get_session
from ..exceptions import DuplicateItemException

EVENTBUS_ARN = os.environ['EVENTBUS_ARN']


def get_eventbridge():
    return boto3.client('events')


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository
    messagebus: eventbus.AbstractMessageBus

    def __init__(self) -> None:
        # self.events: List[events.Event] = []
        self.events = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for event in self.events:
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


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, close_on_exit=True):
        self.repo: repository.SqlAlchemyRepository = None
        self.__close_on_exit = close_on_exit

    def __enter__(self):
        self.session = get_session()
        self.eventbridge = get_eventbridge()
        self.repo = repository.SqlAlchemyRepository(self.session)
        self.messagebus = eventbus.EventBridge(self.eventbridge, EVENTBUS_ARN)
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
