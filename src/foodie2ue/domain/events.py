from dataclasses import dataclass


class Event:

    def asdict(self) -> dict:
        return self.__dict__


@dataclass
class OrderCreatedEvent(Event):
    id: str
    recipient: str
    first_name: str
    order_id: str
    order_total: float


@dataclass
class OrderUpdatedEvent(Event):
    id: str
    status: str


# @dataclass
# class AddPlayerToGame(Event):
#     player_id: str
#     player_name: int

# @dataclass
# class CreatePlayer(AddPlayerToGame):
#     player_id: str
#     player_name: int
