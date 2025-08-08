import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from knowledge_base.domain.errors import DomainError
from knowledge_base.interface.api.handlers import domain_error_handler
from knowledge_base.interface.api.routes.category import router as category_router
from knowledge_base.interface.api.routes.subcategory import router as subcategory_router

app = FastAPI(
    default_response_class=ORJSONResponse,
    exception_handlers={DomainError: domain_error_handler},
)
app.include_router(category_router)
app.include_router(subcategory_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
