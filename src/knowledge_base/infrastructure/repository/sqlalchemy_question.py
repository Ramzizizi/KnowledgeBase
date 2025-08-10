from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.services.question_queries import QuestionListingPort
from knowledge_base.domain.entities.question import NewQuestion, Question
from knowledge_base.domain.repository.question_repository import QuestionRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.question import QuestionModel
from knowledge_base.infrastructure.paginator import SqlAlchemyPaginator


class SqlAlchemyQuestionListing(QuestionListingPort):
    def __init__(self, paginator: SqlAlchemyPaginator[QuestionModel]):
        self.paginator: SqlAlchemyPaginator[QuestionModel] = paginator

    async def list_by_subcategory(
        self, id_subcategory: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[Question]:
        stmt = select(QuestionModel).where(QuestionModel.id_subcategory == id_subcategory)
        result = await self.paginator.paginate(stmt, pagination_options)

        return PaginationResult(total=result["total"], items=list(map(lambda m: m.to_entity(), result["items"])))


class SqlAlchemyQuestionRepository(QuestionRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_subcategory: Id, id_question: Id) -> Question | None:
        stmt = select(QuestionModel).where(
            and_(
                QuestionModel.id == id_question,
                QuestionModel.id_subcategory == id_subcategory,
            )
        )
        question = (await self.session.execute(stmt)).scalar_one_or_none()

        if question:
            return question.to_entity()

        return None

    async def save(self, question: NewQuestion | Question) -> Question:
        if isinstance(question, NewQuestion):
            model_question = QuestionModel.from_new_entity(question)
        else:
            model_question = QuestionModel.from_entity(question)

        self.session.add(model_question)
        await self.session.flush([model_question])

        return model_question.to_entity()

    async def delete(self, id_subcategory: Id, id_question: Id) -> None:
        stmt = select(QuestionModel).where(
            and_(
                QuestionModel.id == id_question,
                QuestionModel.id_subcategory == id_subcategory,
            )
        )
        question = (await self.session.execute(stmt)).scalar_one_or_none()

        if question:
            await self.session.delete(question)

    async def exists_by_subcategory(self, id_subcategory: Id) -> bool:
        stmt = select(QuestionModel).where(QuestionModel.id_subcategory == id_subcategory)
        question = (await self.session.execute(stmt)).scalar_one_or_none()

        return bool(question)
