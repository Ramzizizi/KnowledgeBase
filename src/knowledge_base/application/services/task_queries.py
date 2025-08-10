from knowledge_base.application.paginator import AbstractPaginator
from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.domain.entities.task import Task
from knowledge_base.domain.value_objects.id import Id


class TaskListingPort[MappingTask]:
    def __init__(self, paginator: AbstractPaginator[MappingTask]):
        self.paginator: AbstractPaginator[MappingTask] = paginator

    async def list_by_subcategory(
        self, id_subcategory: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[Task]:
        raise NotImplementedError
