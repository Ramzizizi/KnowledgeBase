from abc import ABC, abstractmethod

from knowledge_base.domain.entities.task import NewTask, Task
from knowledge_base.domain.value_objects.id import Id


class TaskRepository(ABC):
    @abstractmethod
    async def get(self, id_subcategory: Id, id_task: Id) -> Task | None: ...

    @abstractmethod
    async def save(self, task: NewTask | Task) -> Task: ...

    @abstractmethod
    async def delete(self, id_subcategory: Id, id_task: Id) -> None: ...

    @abstractmethod
    async def list_by_subcategory(self, id_subcategory: Id) -> list[Task]: ...

    @abstractmethod
    async def exists_by_subcategory(self, id_subcategory: Id) -> bool: ...
