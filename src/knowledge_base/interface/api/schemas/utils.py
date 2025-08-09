from typing import TypedDict

from pydantic import BaseModel


class DetailedResponse[Item: BaseModel](TypedDict):
    data: Item
