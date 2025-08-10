from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from knowledge_base.domain.entities.category import Category


class CreateCategory(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: str | None


class UpdateCategory(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]
    description: str | None


class OutCategory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PositiveInt
    title: Annotated[str, Field(min_length=1, max_length=50)]

    @staticmethod
    def from_entity(category: Category) -> "OutCategory":
        return OutCategory(id=int(category.id), title=str(category.title))


class DetailedOutCategory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PositiveInt
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: str | None

    @staticmethod
    def from_entity(category: Category) -> "DetailedOutCategory":
        return DetailedOutCategory(
            id=int(category.id),
            title=str(category.title),
            description=category.description,
        )
