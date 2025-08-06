from pydantic import BaseModel, PositiveInt


class CreateTask(BaseModel):
    description: str
    id_subcategory: PositiveInt


class UpdateTask(BaseModel):
    description: str | None
    id_subcategory: PositiveInt | None


class OutTask(CreateTask):
    id: PositiveInt
