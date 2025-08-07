from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.category import Category, NewCategory
from knowledge_base.domain.errors import HasRelatedData, NotFound
from knowledge_base.domain.services.category_policy import CategoryDeletionPolicy
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


class CategoryService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_category: int) -> Category:
        async with self.uow as uow:
            id_object = Id(id_category)
            category = await uow.categories.get(id_object)

            if category is None:
                raise NotFound("Category not found.")

        return category

    async def list(self) -> list[Category]:
        async with self.uow as uow:
            return await uow.categories.list()

    async def create(self, title: str, description: str) -> Category:
        async with self.uow as uow:
            title_object = Title(title)
            new_category = NewCategory(title=title_object, description=description)
            return await uow.categories.save(new_category)

    async def update(self, id_subcategory: int, changes: dict[str, str]) -> Category:
        async with self.uow as uow:
            id_object = Id(id_subcategory)
            title_object = Title(changes["title"])
            category = await uow.categories.get(id_object)

            if category is None:
                raise NotFound("Category not found.")

            if "title" in changes:
                category.change_title(title_object)
            if "description" in changes:
                category.change_description(changes["description"])

            return await uow.categories.save(category)

    async def delete(self, id_category: int) -> None:
        async with self.uow as uow:
            policy = CategoryDeletionPolicy(uow.subcategories)
            id_object = Id(id_category)
            category = await uow.categories.get(id_object)

            if category is None:
                raise NotFound("Category not found.")

            if not policy.can_delete(id_object):
                raise HasRelatedData("The category has related data.")

            await uow.categories.delete(id_object)
