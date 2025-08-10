from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.services.source_queries import SourceListingPort
from knowledge_base.domain.entities.source import NewSource, Source
from knowledge_base.domain.repository.source_repository import SourceRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.source import SourceModel


class SqlAlchemySourceListing[MappingSource: SourceModel](SourceListingPort[MappingSource]):
    async def list_by_subcategory(
        self, id_subcategory: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[Source]:
        stmt = select(SourceModel).where(SourceModel.id_subcategory == id_subcategory)
        result = await self.paginator.paginate(stmt, pagination_options)

        return PaginationResult(total=result["total"], items=list(map(lambda m: m.to_entity(), result["items"])))


class SqlAlchemySourceRepository(SourceRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_subcategory: Id, id_source: Id) -> Source | None:
        stmt = select(SourceModel).where(
            and_(
                SourceModel.id == id_source,
                SourceModel.id_subcategory == id_subcategory,
            )
        )
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

    async def delete(self, id_subcategory: Id, id_source: Id) -> None:
        stmt = select(SourceModel).where(
            and_(
                SourceModel.id == id_source,
                SourceModel.id_subcategory == id_subcategory,
            )
        )
        source = (await self.session.execute(stmt)).scalar_one_or_none()

        if source:
            await self.session.delete(source)

    async def exists_by_subcategory(self, id_subcategory: Id) -> bool:
        stmt = select(SourceModel).where(SourceModel.id_subcategory == id_subcategory)
        source = (await self.session.execute(stmt)).scalar_one_or_none()

        return bool(source)
