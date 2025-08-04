from typing import Any


class InvalidTitle(ValueError):
    pass


class Title:
    __slots__ = ("_value",)

    def __init__(self, raw: str):
        clean = raw.strip()
        if not (1 <= len(clean) <= 50):
            raise InvalidTitle("Title length must be between 1 and 50.")

        self._value: str = clean

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Title) and self._value == other._value
