import re
from typing import Any

from knowledge_base.domain.errors import InvalidLink


class Link:
    __slots__ = ("_value",)

    __PATTERN = re.compile(
        "^https?://(?:www\\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$"
    )

    def __init__(self, raw: str):
        if re.match(self.__PATTERN, raw) is None:
            raise InvalidLink("Invalid link.")

        self._value: str = raw

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Link) and self._value == other._value
