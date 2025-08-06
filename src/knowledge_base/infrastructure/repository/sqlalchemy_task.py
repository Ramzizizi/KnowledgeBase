from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.domain.entities.task import NewTask, Task
from knowledge_base.domain.repository.task_repository import TaskRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.task import TaskModel


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_task: Id) -> Task | None:
        stmt = select(TaskModel).where(TaskModel.id == id_task)
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

    async def delete(self, id_task: Id) -> None:
        stmt = select(TaskModel).where(TaskModel.id == id_task)
        task = (await self.session.execute(stmt)).scalar_one_or_none()

        if task:
            await self.session.delete(task)

    async def list_by_subcategory(self, id_subcategory: Id) -> list[Task]:
        stmt = select(TaskModel).where(TaskModel.id_subcategory == id_subcategory)
        tasks = (await self.session.execute(stmt)).scalars()

        return [task.to_entity() for task in tasks]

    async def exists_by_subcategory(self, id_subcategory: Id) -> bool:
        stmt = select(TaskModel).where(TaskModel.id_subcategory == id_subcategory)
        task = (await self.session.execute(stmt)).scalar_one_or_none()

        return bool(task)
