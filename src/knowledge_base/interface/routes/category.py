from typing import Annotated

from fastapi import APIRouter, Depends, status

from knowledge_base.application.services.category_service import CategoryService
from knowledge_base.interface.dependencies import get_category_service
from knowledge_base.interface.schemas.category import CreateCategory, OutCategory

router = APIRouter(prefix="/category", tags=["Category"])


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


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=OutCategory,
    responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid title."}},
)
async def create_category(
    data_to_create: CreateCategory,
    service: Annotated[CategoryService, Depends(get_category_service)],
) -> OutCategory:
    category = await service.create(**data_to_create.model_dump())
    return OutCategory.from_entity(category)
