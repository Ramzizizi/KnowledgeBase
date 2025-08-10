from pydantic import BaseModel, PositiveInt


class PaginationOptionsSchema(BaseModel):
    limit: PositiveInt = 20
    page_number: PositiveInt = 1
