from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl, PositiveInt

from knowledge_base.domain.entities.source import Source


class CreateSource(BaseModel):
    link: HttpUrl
    id_subcategory: Annotated[PositiveInt, Field(alias="idSubcategory")]


class UpdateSource(BaseModel):
    link: HttpUrl | None
    id_subcategory: Annotated[PositiveInt | None, Field(default=None, alias="idSubcategory")]


class OutSource(BaseModel):
    id: PositiveInt
    link: HttpUrl
    id_subcategory: Annotated[PositiveInt, Field(alias="idSubcategory")]

    @staticmethod
    def from_entity(source: Source) -> "OutSource":
        return OutSource(
            id=int(source.id),
            link=HttpUrl(str(source.link)),
            id_subcategory=int(source.id_subcategory),
        )
