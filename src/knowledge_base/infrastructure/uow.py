from types import TracebackType

from knowledge_base.application.uow import AbstractUoW
from knowledge_base.infrastructure.db.database import AsyncSessionLocal
from knowledge_base.infrastructure.db.orm.category import CategoryModel
from knowledge_base.infrastructure.db.orm.question import QuestionModel
from knowledge_base.infrastructure.db.orm.source import SourceModel
from knowledge_base.infrastructure.db.orm.subcategory import SubCategoryModel
from knowledge_base.infrastructure.db.orm.task import TaskModel
from knowledge_base.infrastructure.paginator import SqlAlchemyPaginator
from knowledge_base.infrastructure.repository.sqlalchemy_category import (
    SqlAlchemyCategoryListing,
    SqlAlchemyCategoryRepository,
)
from knowledge_base.infrastructure.repository.sqlalchemy_question import (
    SqlAlchemyQuestionListing,
    SqlAlchemyQuestionRepository,
)
from knowledge_base.infrastructure.repository.sqlalchemy_source import (
    SqlAlchemySourceListing,
    SqlAlchemySourceRepository,
)
from knowledge_base.infrastructure.repository.sqlalchemy_subcategory import (
    SqlAlchemySubCategoryListing,
    SqlAlchemySubCategoryRepository,
)
from knowledge_base.infrastructure.repository.sqlalchemy_task import SqlAlchemyTaskListing, SqlAlchemyTaskRepository


class SqlAlchemyUoW(AbstractUoW):
    async def __aenter__(self) -> "SqlAlchemyUoW":
        self.session = AsyncSessionLocal()
        self.categories = SqlAlchemyCategoryRepository(self.session)
        self.subcategories = SqlAlchemySubCategoryRepository(self.session)
        self.questions = SqlAlchemyQuestionRepository(self.session)
        self.tasks = SqlAlchemyTaskRepository(self.session)
        self.sources = SqlAlchemySourceRepository(self.session)

        self.category_queries = SqlAlchemyCategoryListing(SqlAlchemyPaginator[CategoryModel](self.session))
        self.subcategory_queries = SqlAlchemySubCategoryListing(SqlAlchemyPaginator[SubCategoryModel](self.session))
        self.question_queries = SqlAlchemyQuestionListing(SqlAlchemyPaginator[QuestionModel](self.session))
        self.task_queries = SqlAlchemyTaskListing(SqlAlchemyPaginator[TaskModel](self.session))
        self.source_queries = SqlAlchemySourceListing(SqlAlchemyPaginator[SourceModel](self.session))

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
