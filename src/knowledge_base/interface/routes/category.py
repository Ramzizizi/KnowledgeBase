from typing import Annotated

from fastapi import APIRouter, Depends

from knowledge_base.application.services.category_service import CategoryService
from knowledge_base.interface.dependencies import get_category_service
from knowledge_base.interface.schemas.category import OutCategory

router = APIRouter(prefix="/category", tags=["Category"])


@router.get("")
async def get_categories(service: Annotated[CategoryService, Depends(get_category_service)]) -> list[OutCategory]:
    categories = await service.list()
    return categories
