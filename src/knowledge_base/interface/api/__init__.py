from fastapi import APIRouter

from knowledge_base.interface.api.routes.category import router as category_router
from knowledge_base.interface.api.routes.subcategory import router as subcategory_router

router = APIRouter(prefix="/api")

router.include_router(category_router)
router.include_router(subcategory_router)
