from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.task import NewTask, Task
from knowledge_base.domain.errors import NotFound
from knowledge_base.domain.value_objects.id import Id


class TaskService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_category: int, id_subcategory: int, id_task: int) -> Task:
        id_object_task = Id(id_task)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            task = await uow.tasks.get(id_object_subcategory, id_object_task)
            if task is None:
                raise NotFound("Task not found.")

            return task

    async def create(self, id_category: int, id_subcategory: int, description: str) -> Task:
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            new_task = NewTask(id_subcategory=id_object_subcategory, description=description)

            return await uow.tasks.save(new_task)

    async def update(self, id_category: int, id_subcategory: int, id_task: int, changes: dict[str, str]) -> Task:
        id_object_task = Id(id_task)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            task = await uow.tasks.get(id_object_subcategory, id_object_task)
            if task is None:
                raise NotFound("Task not found.")

            if "description" in changes:
                task.change_description(str(changes["description"]))

            return await uow.tasks.save(task)

    async def delete(self, id_category: int, id_subcategory: int, id_task: int) -> None:
        id_object_task = Id(id_task)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            task = await uow.tasks.get(id_object_subcategory, id_object_task)
            if task is None:
                raise NotFound("Task not found.")

            await uow.tasks.delete(id_object_subcategory, id_object_task)

    async def list_by_subcategory(
        self, id_category: int, id_subcategory: int, pagination_options: PaginationOptions
    ) -> PaginationResult[Task]:
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            return await uow.task_queries.list_by_subcategory(id_object_subcategory, pagination_options)
