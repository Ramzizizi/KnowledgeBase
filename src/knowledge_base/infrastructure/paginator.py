from collections.abc import Sequence

from sqlalchemy import Select, literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from knowledge_base.application.paginator import AbstractPaginator
from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.infrastructure.db.database import Base


class SqlAlchemyPaginator[Model: Base](AbstractPaginator[Model]):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def paginate(
        self, query: Select[tuple[Model]], pagination_options: PaginationOptions
    ) -> PaginationResult[Model]:
        return {
            "total": await self._get_total_elements(query),
            "items": await self._get_page(query, pagination_options),
        }

    async def _get_total_elements(self, query: Select[tuple[Model]]) -> int:
        total_elements = await self._session.execute(select(count(literal_column("*"))).select_from(query.subquery()))
        return total_elements.scalar_one()

    async def _get_page(self, query: Select[tuple[Model]], pagination_options: PaginationOptions) -> Sequence[Model]:
        stmt = query.limit(pagination_options["limit"]).offset(
            (pagination_options["page_number"] - 1) * pagination_options["limit"]
        )
        items = await self._session.execute(stmt)
        return items.scalars().all()
