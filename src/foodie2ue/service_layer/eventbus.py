import abc
import json

from typing import Protocol
# from ..powertools import logger, tracer, metrics


class AbstractMessageBus(Protocol):

    def __init__(self):
        pass

    @abc.abstractmethod
    def publish_event(self, event_type: str, payload: dict):
        raise NotImplementedError


class EventBridge(AbstractMessageBus):

    def __init__(self, client, eventbus_name: str):
        super().__init__()
        self._client = client
        self._eventbus_name = eventbus_name

    def publish_event(self, event_type: str, payload: dict):
        # payload['correlation_id'] = logger.get_correlation_id()
        response = self._client.put_events(Entries=[
            {
                'Source': 'OrderService',
                'DetailType': event_type,
                'Detail': json.dumps(payload),
                'EventBusName': self._eventbus_name,
            },
        ])
        print(response)
        return response
