from dataclasses import dataclass


class Event:

    def asdict(self) -> dict:
        return self.__dict__


@dataclass
class OrderUpdated(Event):
    id: str
    start_time: int


@dataclass
class AddPlayerToGame(Event):
    player_id: str
    player_name: int


@dataclass
class CreatePlayer(AddPlayerToGame):
    player_id: str
    player_name: int
