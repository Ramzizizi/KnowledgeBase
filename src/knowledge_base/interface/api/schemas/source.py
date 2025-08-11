from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, HttpUrl, PositiveInt

from knowledge_base.domain.entities.source import Source


class CreateSource(BaseModel):
    link: Annotated[HttpUrl, AfterValidator(str)]


class UpdateSource(BaseModel):
    link: HttpUrl | None


class OutSource(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

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
