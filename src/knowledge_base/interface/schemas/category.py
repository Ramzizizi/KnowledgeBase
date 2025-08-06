from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt


class CreateCategory(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: str | None


class UpdateCategory(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]
    description: str | None


class OutCategory(CreateCategory):
    id: PositiveInt
