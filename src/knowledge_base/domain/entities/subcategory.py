from dataclasses import dataclass

from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


@dataclass
class SubCategoryBase:
    title: Title
    id_category: Id

    def change_title(self, new_title: Title) -> None:
        self.title = new_title


@dataclass
class NewSubCategory(SubCategoryBase): ...


@dataclass
class SubCategory(SubCategoryBase):
    id: Id
