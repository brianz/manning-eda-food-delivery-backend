class F2UException(Exception):

    MESSAGE = "Foodie2ue Exception"

    def __init__(self, error, details=None) -> None:
        self._message = self.MESSAGE
        self._details = details or {}

        # some exceptions that we reraise has a params attribute, which we can reuse
        if hasattr(error, 'params'):
            self._details = error.params

    def __str__(self) -> str:
        return self._message

    def __repr__(self) -> str:
        return str(self)

    @property
    def details(self):
        return self._details


class MultipleItemsFoundException(F2UException):
    MESSAGE = "Multiple items were found when one or none was required"


class DoesNotExistException(F2UException):
    MESSAGE = "The item requested does not exist"

    # def __init__(self, message) -> None:
    #     self._message = message


class DuplicateItemException(F2UException):
    MESSAGE = "An item like this already exists"

    # def __init__(self, message) -> None:
    #     self._message = "Duplicate item"
