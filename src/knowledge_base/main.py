import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from knowledge_base.domain.errors import DomainError
from knowledge_base.interface.api.handlers import domain_error_handler
from knowledge_base.interface.api.routes.category import router

app = FastAPI(
    default_response_class=ORJSONResponse,
    exception_handlers={DomainError: domain_error_handler},
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
