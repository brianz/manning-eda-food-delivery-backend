import abc
import simplejson as json

from typing import List

from ..domain import events


class AbstractEventBroker(abc.ABC):

    def __init__(self):
        self._events: List[events.Event] = []

    @abc.abstractmethod
    def _publish_event(self, source_name: str, event_type: str, payload: dict) -> None:
        raise NotImplementedError

    def add_event(self, event: events.Event) -> None:
        self._events.append(event)

    def publish(self):
        for event in self._events:
            self._publish_event(
                source_name=event.event_source,
                event_type=event.__class__.__name__,
                payload=event.asdict(),
            )


class EventBridgeBroker(AbstractEventBroker):

    def __init__(self, client, eventbus_name: str):
        super().__init__()
        self._client = client
        self._eventbus_name = eventbus_name

    def _publish_event(self, source_name: str, event_type: str, payload: dict) -> None:
        self._client.put_events(Entries=[
            {
                'Source': source_name,
                'DetailType': event_type,
                'Detail': json.dumps(payload),
                'EventBusName': self._eventbus_name,
            },
        ])
