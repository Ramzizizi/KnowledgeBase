from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.subcategory import NewSubCategory, SubCategory
from knowledge_base.domain.errors import CategoryNotFound, SubCategoryHasRelatedData, SubCategoryNotFound
from knowledge_base.domain.services.subcategory_policy import SubCategoryDeletionPolicy
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


class SubCategoryService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_subcategory: int) -> SubCategory:
        async with self.uow as uow:
            id_object = Id(id_subcategory)
            subcategory = await uow.subcategories.get(id_object)

            if subcategory is None:
                raise SubCategoryNotFound("Subcategory not found")

        return subcategory

    async def create(self, id_category: int, title: str) -> SubCategory:
        async with self.uow as uow:
            id_object = Id(id_category)
            title_object = Title(title)

            if await uow.categories.get(id_object) is None:
                raise CategoryNotFound("Category not found")

            new_subcategory = NewSubCategory(id_category=id_object, title=title_object)
            return await uow.subcategories.create(new_subcategory)

    async def update(self, id_subcategory: int, changes: dict[str, str | int]) -> SubCategory:
        async with self.uow as uow:
            id_object = Id(id_subcategory)
            title_object = Title(changes["title"])
            subcategory = await uow.subcategories.get(id_object)

            if subcategory is None:
                raise SubCategoryNotFound("Subcategory not found")

            if "title" in changes:
                subcategory.change_title(title_object)

            if "id_category" in changes:
                id_category = Id(changes["id_category"])

                if await uow.categories.get(id_category) is None:
                    raise CategoryNotFound("Category not found")

                subcategory.change_category(id_category)
        return subcategory

    async def delete(self, id_subcategory: int) -> None:
        async with self.uow as uow:
            policy = SubCategoryDeletionPolicy(uow.tasks, uow.sources, uow.questions)
            id_object = Id(id_subcategory)
            subcategory = await uow.subcategories.get(id_object)

            if subcategory is None:
                raise SubCategoryNotFound("Subcategory not found")

            if not policy.can_delete(id_object):
                raise SubCategoryHasRelatedData("The subcategory has related data.")

            await uow.subcategories.delete(id_object)
