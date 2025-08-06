from pydantic import BaseModel, HttpUrl, PositiveInt


class CreateSource(BaseModel):
    link: HttpUrl
    id_subcategory: PositiveInt


class UpdateSource(BaseModel):
    link: HttpUrl | None
    id_subcategory: PositiveInt | None


class OutSource(CreateSource):
    id: PositiveInt
