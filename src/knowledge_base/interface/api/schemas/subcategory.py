from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from knowledge_base.domain.entities.subcategory import SubCategory


class CreateSubCategory(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]


class UpdateSubCategory(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]


class OutSubCategory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PositiveInt
    title: Annotated[str, Field(min_length=1, max_length=50)]
    id_category: Annotated[PositiveInt, Field(alias="idCategory")]

    @staticmethod
    def from_entity(subcategory: SubCategory) -> "OutSubCategory":
        return OutSubCategory(
            id=int(subcategory.id), title=str(subcategory.title), id_category=int(subcategory.id_category)
        )
