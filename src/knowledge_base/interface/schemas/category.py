from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from knowledge_base.domain.entities.category import Category


class CreateCategory(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: str | None


class UpdateCategory(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]
    description: str | None


class OutCategory(CreateCategory):
    id: PositiveInt

    @staticmethod
    def from_entity(category: Category) -> "OutCategory":
        return OutCategory(id=int(category.id), title=str(category.title), description=category.description)
