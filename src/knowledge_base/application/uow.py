from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from types import TracebackType

from knowledge_base.domain.repository.category_repository import CategoryRepository
from knowledge_base.domain.repository.question_repository import QuestionRepository
from knowledge_base.domain.repository.source_repository import SourceRepository
from knowledge_base.domain.repository.subcategory_repository import SubCategoryRepository
from knowledge_base.domain.repository.task_repository import TaskRepository


class AbstractUoW(AbstractAsyncContextManager["AbstractUoW"]):
    categories: CategoryRepository
    subcategories: SubCategoryRepository
    questions: QuestionRepository
    tasks: TaskRepository
    sources: SourceRepository

    @abstractmethod
    async def __aenter__(
        self,
    ) -> "AbstractUoW":
        return self

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    @abstractmethod
    async def commit(
        self,
    ) -> None: ...
    @abstractmethod
    async def rollback(
        self,
    ) -> None: ...
