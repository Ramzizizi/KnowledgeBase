from abc import ABC, abstractmethod
from typing import Any

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult


class AbstractPaginator[MappingDomain](ABC):
    @abstractmethod
    async def paginate(self, query: Any, pagination_options: PaginationOptions) -> PaginationResult[MappingDomain]: ...
