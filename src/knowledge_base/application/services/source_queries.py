from knowledge_base.application.paginator import AbstractPaginator
from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.domain.entities.source import Source
from knowledge_base.domain.value_objects.id import Id


class SourceListingPort[MappingSource]:
    def __init__(self, paginator: AbstractPaginator[MappingSource]):
        self.paginator: AbstractPaginator[MappingSource] = paginator

    async def list_by_subcategory(
        self, id_subcategory: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[Source]:
        raise NotImplementedError
