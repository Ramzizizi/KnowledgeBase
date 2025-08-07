from fastapi import Request, status
from fastapi.responses import ORJSONResponse

from knowledge_base.domain.errors import DomainError, HasRelatedData, InvalidValue, NotFound

domain_to_api_errors_mapping: dict[type[DomainError | ValueError], int] = {
    NotFound: status.HTTP_404_NOT_FOUND,
    HasRelatedData: status.HTTP_409_CONFLICT,
    InvalidValue: status.HTTP_422_UNPROCESSABLE_ENTITY,
}


async def domain_error_handler(request: Request, exc: DomainError) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=domain_to_api_errors_mapping.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={"detail": exc.args[0]},
    )
