from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.domain.entities.source import NewSource, Source
from knowledge_base.domain.repository.source_repository import SourceRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.source import SourceModel


class SqlAlchemySourceRepository(SourceRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_source: Id) -> Source | None:
        stmt = select(SourceModel).where(SourceModel.id == id_source)
        source = (await self.session.execute(stmt)).scalar_one_or_none()

        if source:
            return source.to_entity()

        return None

    async def save(self, source: NewSource | Source) -> Source:
        if isinstance(source, NewSource):
            model_source = SourceModel.from_new_entity(source)
        else:
            model_source = SourceModel.from_entity(source)

        self.session.add(model_source)
        await self.session.flush([model_source])

        return model_source.to_entity()

    async def delete(self, id_source: Id) -> None:
        stmt = select(SourceModel).where(SourceModel.id == id_source)
        source = (await self.session.execute(stmt)).scalar_one_or_none()

        if source:
            await self.session.delete(source)

    async def list_by_subcategory(self, id_subcategory: Id) -> list[Source]:
        stmt = select(SourceModel).where(SourceModel.id_subcategory == id_subcategory)
        sources = (await self.session.execute(stmt)).scalars()

        return [source.to_entity() for source in sources]

    async def exists_by_subcategory(self, id_subcategory: Id) -> bool:
        stmt = select(SourceModel).where(SourceModel.id_subcategory == id_subcategory)
        source = (await self.session.execute(stmt)).scalar_one_or_none()

        return bool(source)
