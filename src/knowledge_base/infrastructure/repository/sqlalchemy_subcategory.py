from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.domain.entities.category import Category, NewCategory
from knowledge_base.domain.repository.subcategory_repository import SubCategoryRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.category import CategoryModel


class SqlAlchemySubCategoryRepository(SubCategoryRepository):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session: AsyncSession = session

    async def get(
        self,
        id_category: Id,
    ) -> Category | None:
        stmt = select(CategoryModel).where(CategoryModel.id == id_category)
        category = (await self.session.execute(stmt)).scalar_one_or_none()

        if category:
            return category.to_entity()

        return None

    async def create(
        self,
        category: NewCategory,
    ) -> Category:
        new_category = CategoryModel.from_entity(category)
        self.session.add(new_category)
        await self.session.flush([new_category])

        return new_category.to_entity()

    async def delete(
        self,
        id_category: Id,
    ) -> None:
        stmt = select(CategoryModel).where(CategoryModel.id == id_category)
        category = (await self.session.execute(stmt)).scalar_one_or_none()

        if category:
            await self.session.delete(category)

    async def list_by_category(
        self,
        id_category: Id,
    ) -> list[SubCategory]: ...

    async def exists_by_category(
        self,
        id_category: Id,
    ) -> bool: ...
