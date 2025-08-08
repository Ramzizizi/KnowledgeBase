from abc import ABC, abstractmethod

from knowledge_base.domain.entities.source import NewSource, Source
from knowledge_base.domain.value_objects.id import Id


class SourceRepository(ABC):
    @abstractmethod
    async def get(self, id_subcategory: Id, id_source: Id) -> Source | None: ...

    @abstractmethod
    async def save(self, source: NewSource | Source) -> Source: ...

    @abstractmethod
    async def delete(self, id_subcategory: Id, id_source: Id) -> None: ...

    @abstractmethod
    async def list_by_subcategory(self, id_subcategory: Id) -> list[Source]: ...

    @abstractmethod
    async def exists_by_subcategory(self, id_subcategory: Id) -> bool: ...
