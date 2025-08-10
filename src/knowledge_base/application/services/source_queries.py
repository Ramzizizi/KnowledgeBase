from typing import Protocol

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.domain.entities.source import Source
from knowledge_base.domain.value_objects.id import Id


class SourceListingPort(Protocol):
    async def list_by_subcategory(
        self, id_subcategory: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[Source]:
        raise NotImplementedError
