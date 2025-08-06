from dataclasses import dataclass

from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


@dataclass
class CategoryBase:
    title: Title
    description: str | None

    def change_title(
        self,
        new_title: Title,
    ) -> None:
        self.title = new_title

    def change_description(
        self,
        new_description: str | None,
    ) -> None:
        self.description = new_description


@dataclass
class NewCategory(CategoryBase): ...


@dataclass
class Category(CategoryBase):
    id: Id
