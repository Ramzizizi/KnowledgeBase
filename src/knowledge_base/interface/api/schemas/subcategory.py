from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from knowledge_base.domain.entities.subcategory import SubCategory
from knowledge_base.interface.api.schemas.question import OutQuestion
from knowledge_base.interface.api.schemas.source import OutSource
from knowledge_base.interface.api.schemas.task import OutTask


class CreateSubCategory(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    id_category: Annotated[PositiveInt, Field(alias="idSubcategory")]


class UpdateSubCategory(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]
    id_category: Annotated[PositiveInt | None, Field(default=None, alias="idSubcategory")]


class OutSubCategory(BaseModel):
    id: PositiveInt
    title: Annotated[str, Field(min_length=1, max_length=50)]
    id_category: Annotated[PositiveInt, Field(alias="idSubcategory")]

    @staticmethod
    def from_entity(subcategory: SubCategory) -> "OutSubCategory":
        return OutSubCategory(
            id=int(subcategory.id), title=str(subcategory.title), id_category=int(subcategory.id_category)
        )


class DetailedOutSubCategory(BaseModel):
    id: PositiveInt
    title: Annotated[str, Field(min_length=1, max_length=50)]
    id_category: Annotated[PositiveInt, Field(alias="idSubcategory")]

    questions: Annotated[
        list[OutQuestion],
        Field(
            examples=[
                {
                    "questions": [
                        {
                            "id": 1,
                            "title": "Test question one",
                            "answer": "Test question one",
                            "idSubcategory": 1,
                        },
                        {
                            "id": 2,
                            "title": "Test question two",
                            "answer": "Test question two",
                            "idSubcategory": 1,
                        },
                    ],
                }
            ]
        ),
    ] = []
    tasks: Annotated[
        list[OutTask],
        Field(
            examples=[
                {
                    "tasks": [
                        {
                            "id": 1,
                            "description": "Test description one.",
                            "idSubcategory": 1,
                        },
                        {
                            "id": 2,
                            "description": "Test description two.",
                            "idSubcategory": 1,
                        },
                    ],
                }
            ]
        ),
    ] = []
    sources: Annotated[
        list[OutSource],
        Field(
            examples=[
                {
                    "sources": [
                        {
                            "id": 1,
                            "source": "https://example.com",
                            "idSubcategory": 1,
                        },
                        {
                            "id": 2,
                            "source": "https://example.com",
                            "idSubcategory": 1,
                        },
                    ],
                }
            ]
        ),
    ] = []

    @staticmethod
    def from_entity(subcategory: SubCategory) -> "DetailedOutSubCategory":
        return DetailedOutSubCategory(
            id=int(subcategory.id), title=str(subcategory.title), id_category=int(subcategory.id_category)
        )
