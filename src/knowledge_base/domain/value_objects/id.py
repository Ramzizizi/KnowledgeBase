from typing import Any

from knowledge_base.domain.errors import InvalidId


class Id:
    __slots__ = ("_value",)

    def __init__(
        self,
        value: Any,
    ):
        if not isinstance(
            value,
            int,
        ):
            raise InvalidId("Id must be an integer.")

        if value <= 0:
            raise InvalidId("Id must be greater than 0.")

        self._value: int = value

    def __get__(
        self,
        instance,
        owner,
    ):  # type: ignore
        return instance.id

    def __str__(
        self,
    ) -> str:
        return str(self._value)

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        return (
            isinstance(
                other,
                Id,
            )
            and self._value == other._value
        )
