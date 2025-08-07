from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from knowledge_base.domain.entities.question import Question


class CreateQuestion(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    answer: str | None
    id_subcategory: Annotated[PositiveInt, Field(alias="idSubcategory")]


class UpdateQuestion(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=50)]
    answer: str | None
    id_subcategory: Annotated[PositiveInt | None, Field(default=None, alias="idSubcategory")]


class OutQuestion(BaseModel):
    id: PositiveInt
    title: Annotated[str, Field(min_length=1, max_length=50)]
    answer: str | None
    id_subcategory: Annotated[PositiveInt, Field(alias="idSubcategory")]

    @staticmethod
    def from_entity(question: Question) -> "OutQuestion":
        return OutQuestion(
            id=int(question.id),
            title=str(question.title),
            answer=question.answer,
            id_subcategory=int(question.id_subcategory),
        )
