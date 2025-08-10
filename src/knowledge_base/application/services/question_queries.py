from knowledge_base.application.paginator import AbstractPaginator
from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.domain.entities.question import Question
from knowledge_base.domain.value_objects.id import Id


class QuestionListingPort[MappingQuestion]:
    def __init__(self, paginator: AbstractPaginator[MappingQuestion]):
        self.paginator: AbstractPaginator[MappingQuestion] = paginator

    async def list_by_subcategory(
        self, id_subcategory: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[Question]:
        raise NotImplementedError
