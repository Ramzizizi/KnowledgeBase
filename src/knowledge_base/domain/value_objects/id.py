from typing import Any

from knowledge_base.domain.errors import InvalidValue


class Id:
    __slots__ = ("_value",)

    def __init__(self, value: Any):
        if not isinstance(value, int):
            raise InvalidValue("Id must be an integer.")

        if value <= 0:
            raise InvalidValue("Id must be greater than 0.")

        self._value: int = value

    def __int__(self) -> int:
        return self._value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Id) and self._value == other._value
