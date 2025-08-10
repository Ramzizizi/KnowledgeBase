from knowledge_base.application.paginator import AbstractPaginator
from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.domain.entities.subcategory import SubCategory
from knowledge_base.domain.value_objects.id import Id


class SubCategoryListingPort[MappingSubCategory]:
    def __init__(self, paginator: AbstractPaginator[MappingSubCategory]):
        self.paginator: AbstractPaginator[MappingSubCategory] = paginator

    async def list_by_category(
        self, id_category: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[SubCategory]:
        raise NotImplementedError
