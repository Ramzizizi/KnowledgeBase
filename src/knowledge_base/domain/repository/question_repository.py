from abc import ABC, abstractmethod

from knowledge_base.domain.entities.question import NewQuestion, Question
from knowledge_base.domain.value_objects.id import Id


class QuestionRepository(ABC):
    @abstractmethod
    async def get(self, id_question: Id) -> Question | None: ...

    @abstractmethod
    async def save(self, question: NewQuestion | Question) -> Question: ...

    @abstractmethod
    async def delete(self, id_question: Id) -> None: ...

    @abstractmethod
    async def list_by_subcategory(self, id_subcategory: Id) -> list[Question]: ...

    @abstractmethod
    async def exists_by_subcategory(self, id_subcategory: Id) -> bool: ...
