from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.domain.entities.subcategory import NewSubCategory, SubCategory
from knowledge_base.domain.repository.subcategory_repository import SubCategoryRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.subcategory import SubCategoryModel


class SqlAlchemySubCategoryRepository(SubCategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_subcategory: Id) -> SubCategory | None:
        stmt = select(SubCategoryModel).where(SubCategoryModel.id == id_subcategory)
        subcategory = (await self.session.execute(stmt)).scalar_one_or_none()

        if subcategory:
            return subcategory.to_entity()

        return None

    async def save(self, subcategory: NewSubCategory | SubCategory) -> SubCategory:
        if isinstance(subcategory, NewSubCategory):
            model_subcategory = SubCategoryModel.from_new_entity(subcategory)
        else:
            model_subcategory = SubCategoryModel.from_entity(subcategory)

        self.session.add(model_subcategory)
        await self.session.flush([model_subcategory])

        return model_subcategory.to_entity()

    async def delete(self, id_subcategory: Id) -> None:
        stmt = select(SubCategoryModel).where(SubCategoryModel.id == id_subcategory)
        subcategory = (await self.session.execute(stmt)).scalar_one_or_none()

        if subcategory:
            await self.session.delete(subcategory)

    async def list_by_category(self, id_category: Id) -> list[SubCategory]:
        stmt = select(SubCategoryModel).where(SubCategoryModel.id_category == id_category)
        subcategories = (await self.session.execute(stmt)).scalars()

        return [subcategory.to_entity() for subcategory in subcategories]

    async def exists_by_category(self, id_category: Id) -> bool:
        stmt = select(SubCategoryModel).where(SubCategoryModel.id_category == id_category)
        subcategory = (await self.session.execute(stmt)).scalar_one_or_none()

        return bool(subcategory)
