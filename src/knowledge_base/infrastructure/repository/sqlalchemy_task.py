from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.services.task_queries import TaskListingPort
from knowledge_base.domain.entities.task import NewTask, Task
from knowledge_base.domain.repository.task_repository import TaskRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.task import TaskModel
from knowledge_base.infrastructure.paginator import SqlAlchemyPaginator


class SqlAlchemyTaskListing(TaskListingPort):
    def __init__(self, paginator: SqlAlchemyPaginator[TaskModel]):
        self.paginator: SqlAlchemyPaginator[TaskModel] = paginator

    async def list_by_subcategory(
        self, id_subcategory: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[Task]:
        stmt = select(TaskModel).where(TaskModel.id_subcategory == id_subcategory)
        result = await self.paginator.paginate(stmt, pagination_options)

        return PaginationResult(total=result["total"], items=list(map(lambda m: m.to_entity(), result["items"])))


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_subcategory: Id, id_task: Id) -> Task | None:
        stmt = select(TaskModel).where(
            and_(
                TaskModel.id == id_task,
                TaskModel.id_subcategory == id_subcategory,
            )
        )
        task = (await self.session.execute(stmt)).scalar_one_or_none()

        if task:
            return task.to_entity()

        return None

    async def save(self, task: NewTask | Task) -> Task:
        # ruff: noqa: SIM108
        if isinstance(task, NewTask):
            model_task = TaskModel.from_new_entity(task)
        else:
            model_task = TaskModel.from_entity(task)

        self.session.add(model_task)
        await self.session.flush([model_task])

        return model_task.to_entity()

    async def delete(self, id_subcategory: Id, id_task: Id) -> None:
        stmt = select(TaskModel).where(
            and_(
                TaskModel.id == id_task,
                TaskModel.id_subcategory == id_subcategory,
            )
        )
        task = (await self.session.execute(stmt)).scalar_one_or_none()

        if task:
            await self.session.delete(task)

    async def exists_by_subcategory(self, id_subcategory: Id) -> bool:
        stmt = select(TaskModel).where(TaskModel.id_subcategory == id_subcategory)
        task = (await self.session.execute(stmt)).scalar_one_or_none()

        return bool(task)
