from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt


class CreateQuestion(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    answer: str | None
    id_subcategory: PositiveInt


class UpdateQuestion(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]
    answer: str | None
    id_subcategory: PositiveInt | None


class OutQuestion(CreateQuestion):
    id: PositiveInt
