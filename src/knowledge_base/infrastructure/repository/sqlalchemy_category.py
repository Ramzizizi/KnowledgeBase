from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.services.category_queries import CategoryListingPort
from knowledge_base.domain.entities.category import Category, NewCategory
from knowledge_base.domain.repository.category_repository import CategoryRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.category import CategoryModel
from knowledge_base.infrastructure.paginator import SqlAlchemyPaginator


class SqlAlchemyCategoryListing(CategoryListingPort):
    def __init__(self, paginator: SqlAlchemyPaginator[CategoryModel]):
        self.paginator: SqlAlchemyPaginator[CategoryModel] = paginator

    async def list(self, pagination_options: PaginationOptions) -> PaginationResult[Category]:
        stmt = select(CategoryModel)
        result = await self.paginator.paginate(stmt, pagination_options)

        return PaginationResult(total=result["total"], items=list(map(lambda m: m.to_entity(), result["items"])))


class SqlAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_category: Id) -> Category | None:
        stmt = select(CategoryModel).where(CategoryModel.id == id_category)
        category = (await self.session.execute(stmt)).scalar_one_or_none()

        if category:
            return category.to_entity()

        return None

    async def save(self, category: NewCategory | Category) -> Category:
        if isinstance(category, NewCategory):
            model_category = CategoryModel.from_new_entity(category)
            self.session.add(model_category)
            await self.session.flush([model_category])
        else:
            model_category = await self.session.get_one(CategoryModel, int(category.id))
            model_category.title = str(category.title)
            model_category.description = category.description

        return model_category.to_entity()

    async def delete(self, id_category: Id) -> None:
        stmt = select(CategoryModel).where(CategoryModel.id == id_category)
        category = (await self.session.execute(stmt)).scalar_one_or_none()

        if category:
            await self.session.delete(category)
