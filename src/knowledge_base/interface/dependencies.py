from typing import Annotated

from fastapi import Depends
from pydantic import TypeAdapter

from knowledge_base.application.schemas.pagination import PaginationOptions
from knowledge_base.application.services.category_service import CategoryService
from knowledge_base.application.services.question_service import QuestionService
from knowledge_base.application.services.source_service import SourceService
from knowledge_base.application.services.subcategory_service import SubCategoryService
from knowledge_base.application.services.task_service import TaskService
from knowledge_base.infrastructure.uow import SqlAlchemyUoW
from knowledge_base.interface.api.schemas.pagination import PaginationOptionsSchema


def get_pagination(pagination_options: Annotated[PaginationOptionsSchema, Depends()]) -> PaginationOptions:
    return TypeAdapter(PaginationOptions).validate_python(pagination_options.model_dump())


async def get_uow() -> SqlAlchemyUoW:
    return SqlAlchemyUoW()


async def get_category_service(uow: Annotated[SqlAlchemyUoW, Depends(get_uow)]) -> CategoryService:
    return CategoryService(uow)


async def get_subcategory_service(uow: Annotated[SqlAlchemyUoW, Depends(get_uow)]) -> SubCategoryService:
    return SubCategoryService(uow)


async def get_question_service(uow: Annotated[SqlAlchemyUoW, Depends(get_uow)]) -> QuestionService:
    return QuestionService(uow)


async def get_task_service(uow: Annotated[SqlAlchemyUoW, Depends(get_uow)]) -> TaskService:
    return TaskService(uow)


async def get_source_service(uow: Annotated[SqlAlchemyUoW, Depends(get_uow)]) -> SourceService:
    return SourceService(uow)
