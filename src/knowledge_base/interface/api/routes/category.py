from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from pydantic import PositiveInt

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.services.category_service import CategoryService
from knowledge_base.interface.api.schemas.category import (
    CreateCategory,
    DetailedOutCategory,
    OutCategory,
    UpdateCategory,
)
from knowledge_base.interface.api.schemas.utils import DetailedResponse
from knowledge_base.interface.dependencies import (
    get_category_service,
    get_pagination,
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
    response_model=PaginationResult[OutCategory],
)
async def get_categories(
    pagination_options: Annotated[PaginationOptions, Depends(get_pagination)],
    service: Annotated[CategoryService, Depends(get_category_service)],
) -> PaginationResult[OutCategory]:
    categories = await service.list(pagination_options)

    return PaginationResult(  # noqa
        total=categories["total"], items=[OutCategory.from_entity(category) for category in categories["items"]]
    )


@router.get(
    path="/{idCategory}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[DetailedOutCategory],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Object not found."},
    },
)
async def get_category(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> DetailedResponse[DetailedOutCategory]:
    category = await category_service.get(id_category)
    schema_category = DetailedOutCategory.from_entity(category)

    return DetailedResponse(data=schema_category)


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=DetailedResponse[OutCategory],
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Incorrect values."},
    },
)
async def create_category(
    data_to_create: CreateCategory,
    service: Annotated[CategoryService, Depends(get_category_service)],
) -> DetailedResponse[OutCategory]:
    category = await service.create(**data_to_create.model_dump())

    return DetailedResponse(data=OutCategory.from_entity(category))


@router.patch(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutCategory],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Object not found."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Incorrect values."},
    },
)
async def update_category(
    data_to_update: UpdateCategory,
    service: Annotated[CategoryService, Depends(get_category_service)],
) -> DetailedResponse[OutCategory]:
    category = await service.update(**data_to_update.model_dump())

    return DetailedResponse(data=OutCategory.from_entity(category))


@router.delete(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Object not found."},
        status.HTTP_409_CONFLICT: {"description": "Object has related data."},
    },
)
async def delete_category(
    id_category: PositiveInt,
    service: Annotated[CategoryService, Depends(get_category_service)],
) -> None:
    return await service.delete(id_category)
