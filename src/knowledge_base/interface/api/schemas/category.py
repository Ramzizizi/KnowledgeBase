from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from knowledge_base.domain.entities.category import Category
from knowledge_base.interface.api.schemas.subcategory import DetailedOutSubCategory


class CreateCategory(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: str | None


class UpdateCategory(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]
    description: str | None


class OutCategory(BaseModel):
    id: PositiveInt
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: str | None

    @staticmethod
    def from_entity(category: Category) -> "OutCategory":
        return OutCategory(id=int(category.id), title=str(category.title), description=category.description)


class DetailedOutCategory(BaseModel):
    id: PositiveInt
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: str | None

    subcategories: Annotated[
        list[DetailedOutSubCategory],
        Field(
            examples=[
                {
                    "subcategories": [
                        {
                            "id": 1,
                            "title": "Test subcategory",
                            "id_category": 1,
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
                    ],
                }
            ],
        ),
    ] = []

    @staticmethod
    def from_entity(category: Category) -> "DetailedOutCategory":
        return DetailedOutCategory(
            id=int(category.id),
            title=str(category.title),
            description=category.description,
        )
