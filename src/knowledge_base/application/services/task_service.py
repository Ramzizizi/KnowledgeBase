from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.task import NewTask, Task
from knowledge_base.domain.errors import NotFound
from knowledge_base.domain.value_objects.id import Id


class TaskService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_task: int) -> Task:
        id_object = Id(id_task)

        async with self.uow as uow:
            task = await uow.tasks.get(id_object)

        if task is None:
            raise NotFound("Task not found.")

        return task

    async def create(self, id_task: int, description: str) -> Task:
        id_object = Id(id_task)

        async with self.uow as uow:
            if await uow.tasks.get(id_object) is None:
                raise NotFound("Task not found.")

            new_task = NewTask(id_subcategory=id_object, description=description)

            return await uow.tasks.save(new_task)

    async def update(self, id_task: int, changes: dict[str, str | int]) -> Task:
        id_object = Id(id_task)

        async with self.uow as uow:
            task = await uow.tasks.get(id_object)

            if task is None:
                raise NotFound("Task not found.")

            if "description" in changes:
                task.change_description(str(changes["description"]))

            if "id_subcategory" in changes:
                id_subcategory = Id(changes["id_subcategory"])

                if await uow.subcategories.get(id_subcategory) is None:
                    raise NotFound("Subcategory not found.")

                task.change_subcategory(id_subcategory)

            return await uow.tasks.save(task)

    async def delete(self, id_task: int) -> None:
        id_object = Id(id_task)

        async with self.uow as uow:
            task = await uow.tasks.get(id_object)

            if task is None:
                raise NotFound("Task not found.")

            await uow.tasks.delete(id_object)

    async def list_by_subcategory(self, id_subcategory: int) -> list[Task]:
        id_object = Id(id_subcategory)

        async with self.uow as uow:
            return await uow.tasks.list_by_subcategory(id_object)
