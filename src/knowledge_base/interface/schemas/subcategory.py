from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt


class CreateSubCategory(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    id_category: PositiveInt


class UpdateSubCategory(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]
    id_category: PositiveInt | None


class OutSubCategory(CreateSubCategory):
    id: PositiveInt
