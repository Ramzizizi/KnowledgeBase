from typing import Protocol

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.domain.entities.category import Category


class CategoryListingPort(Protocol):
    async def list(self, pagination_options: PaginationOptions) -> PaginationResult[Category]:
        raise NotImplementedError
