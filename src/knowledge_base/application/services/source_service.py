from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.source import NewSource, Source
from knowledge_base.domain.errors import NotFound
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.link import Link


class SourceService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_source: int) -> Source:
        async with self.uow as uow:
            id_object = Id(id_source)
            source = await uow.sources.get(id_object)

        if source is None:
            raise NotFound("Source not found.")

        return source

    async def create(self, link: str, id_subcategory: int) -> Source:
        link_object = Link(link)
        id_object = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.subcategories.get(id_object) is None:
                raise NotFound("Subcategory not found.")

            new_source = NewSource(link=link_object, id_subcategory=id_object)

            return await uow.sources.save(new_source)

    async def update(self, id_source: int, changes: dict[str, str | int]) -> Source:
        id_object = Id(id_source)

        async with self.uow as uow:
            source = await uow.sources.get(id_object)

            if source is None:
                raise NotFound("Source not found.")

            if "link" in changes:
                link = Link(str(changes["link"]))
                source.change_link(link)

            if "id_subcategory" in changes:
                id_subcategory = Id(changes["id_subcategory"])

                if await uow.subcategories.get(id_subcategory) is None:
                    raise NotFound("Subcategory not found.")

                source.change_subcategory(id_subcategory)

            return await uow.sources.save(source)

    async def delete(self, id_source: int) -> None:
        async with self.uow as uow:
            id_object = Id(id_source)
            source = await uow.sources.get(id_object)

            if source is None:
                raise NotFound("Source not found.")

            await uow.sources.delete(id_object)

    async def list_by_subcategory(self, id_subcategory: int) -> list[Source]:
        id_object = Id(id_subcategory)

        async with self.uow as uow:
            return await uow.sources.list_by_subcategory(id_object)
