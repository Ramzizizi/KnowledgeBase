from knowledge_base.application.uow import AbstractUoW
from knowledge_base.infrastructure.db.database import AsyncSessionLocal
from knowledge_base.infrastructure.repository.sqlalchemy_category import SqlAlchemyCategoryRepository
from knowledge_base.infrastructure.repository.sqlalchemy_question import SqlAlchemyQuestionRepository
from knowledge_base.infrastructure.repository.sqlalchemy_source import SqlAlchemySourceRepository
from knowledge_base.infrastructure.repository.sqlalchemy_subcategory import SqlAlchemySubCategoryRepository
from knowledge_base.infrastructure.repository.sqlalchemy_task import SqlAlchemyTaskRepository


class SqlAlchemyUoW(AbstractUoW):
    async def __aenter__(self) -> "SqlAlchemyUoW":
        self.session = AsyncSessionLocal()
        self.categories = SqlAlchemyCategoryRepository(self.session)
        self.subcategories = SqlAlchemySubCategoryRepository(self.session)
        self.questions = SqlAlchemyQuestionRepository(self.session)
        self.tasks = SqlAlchemyTaskRepository(self.session)
        self.sources = SqlAlchemySourceRepository(self.session)
        return self

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
