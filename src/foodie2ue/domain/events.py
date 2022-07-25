from dataclasses import dataclass


class Event:

    def asdict(self) -> dict:
        return self.__dict__


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
