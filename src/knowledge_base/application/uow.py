from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from types import TracebackType

from knowledge_base.application.services.category_queries import CategoryListingPort
from knowledge_base.application.services.question_queries import QuestionListingPort
from knowledge_base.application.services.source_queries import SourceListingPort
from knowledge_base.application.services.subcategory_queries import SubCategoryListingPort
from knowledge_base.application.services.task_queries import TaskListingPort
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

    category_queries: CategoryListingPort
    question_queries: QuestionListingPort
    source_queries: SourceListingPort
    subcategory_queries: SubCategoryListingPort
    task_queries: TaskListingPort

    async def __aenter__(
        self,
    ) -> "AbstractUoW":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.rollback() if exc_type else await self.commit()

    @abstractmethod
    async def commit(self) -> None: ...
    @abstractmethod
    async def rollback(self) -> None: ...
