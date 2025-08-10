from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.subcategory import NewSubCategory, SubCategory
from knowledge_base.domain.errors import HasRelatedData, NotFound
from knowledge_base.domain.services.subcategory_policy import SubCategoryDeletionPolicy
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


class SubCategoryService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_category: int, id_subcategory: int) -> SubCategory:
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            subcategory = await uow.subcategories.get(id_object_category, id_object_subcategory)
            if subcategory is None:
                raise NotFound("Subcategory not found.")

        return subcategory

    async def create(self, id_category: int, title: str) -> SubCategory:
        id_object = Id(id_category)
        title_object = Title(title)

        async with self.uow as uow:
            if await uow.categories.get(id_object) is None:
                raise NotFound("Category not found.")

            new_subcategory = NewSubCategory(id_category=id_object, title=title_object)

            return await uow.subcategories.save(new_subcategory)

    async def update(self, id_category: int, id_subcategory: int, changes: dict[str, str | int]) -> SubCategory:
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            subcategory = await uow.subcategories.get(id_object_category, id_object_subcategory)
            if subcategory is None:
                raise NotFound("Subcategory not found.")

            if "title" in changes:
                title_object = Title(changes["title"])
                subcategory.change_title(title_object)

            return await uow.subcategories.save(subcategory)

    async def delete(self, id_category: int, id_subcategory: int) -> None:
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            subcategory = await uow.subcategories.get(id_object_category, id_object_subcategory)
            if subcategory is None:
                raise NotFound("Subcategory not found.")

            policy = SubCategoryDeletionPolicy(uow.tasks, uow.sources, uow.questions)
            if not policy.can_delete(id_object_subcategory):
                raise HasRelatedData("The subcategory has related data.")

            await uow.subcategories.delete(id_object_category, id_object_subcategory)

    async def list_by_category(
        self, id_category: int, pagination_options: PaginationOptions
    ) -> PaginationResult[SubCategory]:
        id_object_category = Id(id_category)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            return await uow.subcategory_queries.list_by_category(id_object_category, pagination_options)
