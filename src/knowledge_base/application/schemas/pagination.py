from collections.abc import Sequence
from typing import TypedDict


class PaginationOptions(TypedDict):
    limit: int
    page_number: int


class PaginationResult[MappingDomain](TypedDict):
    total: int
    items: Sequence[MappingDomain]
