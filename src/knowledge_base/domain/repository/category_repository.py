from abc import ABC, abstractmethod

from knowledge_base.domain.entities.category import Category, NewCategory
from knowledge_base.domain.value_objects.id import Id


class CategoryRepository(ABC):
    @abstractmethod
    async def get(
        self,
        id_category: Id,
    ) -> Category | None: ...

    @abstractmethod
    async def create(
        self,
        category: NewCategory,
    ) -> Category: ...

    @abstractmethod
    async def delete(
        self,
        id_category: Id,
    ) -> None: ...
