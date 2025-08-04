from typing import Any


class InvalidId(ValueError):
    pass


class Id:
    __slots__ = ("_value",)

    def __init__(self, value: int):
        if value <= 0:
            raise InvalidId("Id must be greater than 0.")

        if not isinstance(value, int):
            raise InvalidId("Id must be an integer.")

        self._value: int = value

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Id) and self._value == other._value
