class Foodie2ueException(Exception):

    def __init__(self, *args: object) -> None:
        self._message = "Foodie2ue Exception"
        self._details = {}

    def __str__(self) -> str:
        return self._message

    def __repr__(self) -> str:
        return str(self)

    @property
    def details(self):
        return self._details


class UOWDuplicateException(Foodie2ueException):

    def __init__(self, message) -> None:
        self._message = "Duplicate item"

        if hasattr(message, 'params'):
            self._message = "An item like this already exists"
            self._details = message.params
