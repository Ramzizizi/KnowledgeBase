from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from knowledge_base.domain.entities.task import Task


class CreateTask(BaseModel):
    description: str
    id_subcategory: Annotated[PositiveInt, Field(alias="idSubcategory")]


class UpdateTask(BaseModel):
    description: str | None = None
    id_subcategory: Annotated[PositiveInt | None, Field(default=None, alias="idSubcategory")]


class OutTask(BaseModel):
    id: PositiveInt
    description: str
    id_subcategory: Annotated[PositiveInt, Field(alias="idSubcategory")]

    @staticmethod
    def from_entity(task: Task) -> "OutTask":
        return OutTask(
            id=int(task.id),
            description=task.description,
            id_subcategory=int(task.id_subcategory),
        )
