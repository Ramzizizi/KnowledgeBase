from abc import ABC, abstractmethod

from knowledge_base.domain.entities.subcategory import NewSubCategory, SubCategory
from knowledge_base.domain.value_objects.id import Id


class SubCategoryRepository(ABC):
    @abstractmethod
    async def get(self, id_category: Id, id_subcategory: Id) -> SubCategory | None: ...

    @abstractmethod
    async def save(self, subcategory: NewSubCategory | SubCategory) -> SubCategory: ...

    @abstractmethod
    async def delete(self, id_category: Id, id_subcategory: Id) -> None: ...

    @abstractmethod
    async def exists_by_category(self, id_category: Id) -> bool: ...
