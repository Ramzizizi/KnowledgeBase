from knowledge_base.application.paginator import AbstractPaginator
from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.domain.entities.category import Category


class CategoryListingPort[MappingCategory]:
    def __init__(self, paginator: AbstractPaginator[MappingCategory]):
        self.paginator: AbstractPaginator[MappingCategory] = paginator

    async def list(self, pagination_options: PaginationOptions) -> PaginationResult[Category]:
        raise NotImplementedError
