from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.services.subcategory_queries import SubCategoryListingPort
from knowledge_base.domain.entities.subcategory import NewSubCategory, SubCategory
from knowledge_base.domain.repository.subcategory_repository import SubCategoryRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.subcategory import SubCategoryModel
from knowledge_base.infrastructure.paginator import SqlAlchemyPaginator


class SqlAlchemySubCategoryListing(SubCategoryListingPort):
    def __init__(self, paginator: SqlAlchemyPaginator[SubCategoryModel]):
        self.paginator: SqlAlchemyPaginator[SubCategoryModel] = paginator

    async def list_by_category(
        self, id_category: Id, pagination_options: PaginationOptions
    ) -> PaginationResult[SubCategory]:
        stmt = select(SubCategoryModel).where(SubCategoryModel.id_category == id_category)
        result = await self.paginator.paginate(stmt, pagination_options)

        return PaginationResult(total=result["total"], items=list(map(lambda m: m.to_entity(), result["items"])))


class SqlAlchemySubCategoryRepository(SubCategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_category: Id, id_subcategory: Id) -> SubCategory | None:
        stmt = select(SubCategoryModel).where(
            and_(SubCategoryModel.id == id_subcategory, SubCategoryModel.id_category == id_category)
        )
        subcategory = (await self.session.execute(stmt)).scalar_one_or_none()

        if subcategory:
            return subcategory.to_entity()

        return None

    async def save(self, subcategory: NewSubCategory | SubCategory) -> SubCategory:
        if isinstance(subcategory, NewSubCategory):
            model_subcategory = SubCategoryModel.from_new_entity(subcategory)
            self.session.add(model_subcategory)
            await self.session.flush([model_subcategory])
        else:
            model_subcategory = await self.session.get_one(SubCategoryModel, int(subcategory.id))
            model_subcategory.title = str(subcategory.title)

        return model_subcategory.to_entity()

    async def delete(self, id_category: Id, id_subcategory: Id) -> None:
        stmt = select(SubCategoryModel).where(
            and_(SubCategoryModel.id == id_subcategory, SubCategoryModel.id_category == id_category)
        )
        subcategory = (await self.session.execute(stmt)).scalar_one_or_none()

        if subcategory:
            await self.session.delete(subcategory)

    async def exists_by_category(self, id_category: Id) -> bool:
        stmt = select(SubCategoryModel).where(SubCategoryModel.id_category == id_category)
        subcategory = (await self.session.execute(stmt)).scalar_one_or_none()

        return bool(subcategory)
