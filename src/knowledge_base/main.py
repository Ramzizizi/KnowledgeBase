from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from knowledge_base.domain.errors import DomainError
from knowledge_base.interface.api import router as interface_router
from knowledge_base.interface.api.handlers import domain_error_handler

app = FastAPI(
    title="Knowledge Base",
    default_response_class=ORJSONResponse,
    exception_handlers={DomainError: domain_error_handler},
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interface_router)
