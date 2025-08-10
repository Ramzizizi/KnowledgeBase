from typing import Protocol

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.domain.entities.subcategory import SubCategory
from knowledge_base.domain.value_objects.id import Id


class SubCategoryListingPort(Protocol):
    async def list_by_category(
        self, id_category: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[SubCategory]:
        raise NotImplementedError
