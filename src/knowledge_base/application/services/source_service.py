from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.source import NewSource, Source
from knowledge_base.domain.errors import NotFound
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.link import Link


class SourceService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_category: int, id_subcategory: int, id_source: int) -> Source:
        id_object_source = Id(id_source)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            source = await uow.sources.get(id_object_subcategory, id_object_source)
            if source is None:
                raise NotFound("Source not found.")

        return source

    async def create(self, id_category: int, id_subcategory: int, link: str) -> Source:
        link_object = Link(link)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            new_source = NewSource(link=link_object, id_subcategory=id_object_subcategory)

            return await uow.sources.save(new_source)

    async def update(
        self, id_category: int, id_subcategory: int, id_source: int, changes: dict[str, str | int]
    ) -> Source:
        id_object = Id(id_source)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            source = await uow.sources.get(id_object_subcategory, id_object)
            if source is None:
                raise NotFound("Source not found.")

            if "link" in changes:
                link = Link(str(changes["link"]))
                source.change_link(link)

            return await uow.sources.save(source)

    async def delete(self, id_category: int, id_subcategory: int, id_source: int) -> None:
        id_object_source = Id(id_source)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            source = await uow.sources.get(id_object_subcategory, id_object_source)
            if source is None:
                raise NotFound("Source not found.")

            await uow.sources.delete(id_object_subcategory, id_object_source)

    async def list_by_subcategory(
        self, id_category: int, id_subcategory: int, pagination_options: PaginationOptions
    ) -> PaginationResult[Source]:
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            return await uow.source_queries.list_by_subcategory(id_object_subcategory, pagination_options)
