from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt

from knowledge_base.application.services.category_service import CategoryService
from knowledge_base.application.services.question_service import QuestionService
from knowledge_base.application.services.source_service import SourceService
from knowledge_base.application.services.subcategory_service import SubCategoryService
from knowledge_base.application.services.task_service import TaskService
from knowledge_base.interface.api.schemas.category import CreateCategory, DetailedOutCategory, OutCategory
from knowledge_base.interface.api.schemas.question import OutQuestion
from knowledge_base.interface.api.schemas.source import OutSource
from knowledge_base.interface.api.schemas.subcategory import DetailedOutSubCategory
from knowledge_base.interface.api.schemas.task import OutTask
from knowledge_base.interface.dependencies import (
    get_category_service,
    get_question_service,
    get_source_service,
    get_subcategory_service,
    get_task_service,
)

router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error."},
    },
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[OutCategory],
)
async def get_categories(
    service: Annotated[CategoryService, Depends(get_category_service)],
) -> list[OutCategory]:
    categories = await service.list()
    return [OutCategory.from_entity(category) for category in categories]


@router.get(
    path="/{id_category}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedOutCategory,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Object not found."},
    },
)
async def get_category(
    id_category: PositiveInt,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    subcategory_service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    source_service: Annotated[SourceService, Depends(get_source_service)],
) -> DetailedOutCategory:
    category = await category_service.get(id_category)

    schema_category = DetailedOutCategory.from_entity(category)
    subcategories = [
        DetailedOutSubCategory.from_entity(subcategory)
        for subcategory in await subcategory_service.list_by_category(id_category)
    ]

    for subcategory in subcategories:
        tasks = await task_service.list_by_subcategory(subcategory.id)
        questions = await question_service.list_by_subcategory(subcategory.id)
        sources = await source_service.list_by_subcategory(subcategory.id)

        subcategory.tasks = [OutTask.from_entity(task) for task in tasks]
        subcategory.questions = [OutQuestion.from_entity(question) for question in questions]
        subcategory.sources = [OutSource.from_entity(source) for source in sources]

        schema_category.subcategories.append(subcategory)

    return schema_category


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=OutCategory,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Incorrect values."},
    },
)
async def create_category(
    data_to_create: CreateCategory,
    service: Annotated[CategoryService, Depends(get_category_service)],
) -> OutCategory:
    category = await service.create(**data_to_create.model_dump())
    return OutCategory.from_entity(category)


@router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Object not found."},
    },
)
async def delete_category(
    id_category: PositiveInt,
    service: Annotated[CategoryService, Depends(get_category_service)],
) -> None:
    return await service.delete(id_category)
