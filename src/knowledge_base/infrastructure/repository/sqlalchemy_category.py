from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from knowledge_base.domain.entities.category import Category, NewCategory
from knowledge_base.domain.repository.category_repository import CategoryRepository
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.orm.category import CategoryModel


class SqlAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get(self, id_category: Id) -> Category | None:
        stmt = select(CategoryModel).where(CategoryModel.id == id_category)
        category = (await self.session.execute(stmt)).scalar_one_or_none()

        if category:
            return category.to_entity()

        return None

    async def list(self) -> list[Category]:
        stmt = select(CategoryModel)
        categories = (await self.session.execute(stmt)).scalars()

        return [category.to_entity() for category in categories]

    async def save(self, category: NewCategory | Category) -> Category:
        if isinstance(category, NewCategory):
            model_category = CategoryModel.from_new_entity(category)
        else:
            model_category = CategoryModel.from_entity(category)

        self.session.add(model_category)
        await self.session.flush([model_category])

        return model_category.to_entity()

    async def delete(self, id_category: Id) -> None:
        stmt = select(CategoryModel).where(CategoryModel.id == id_category)
        category = (await self.session.execute(stmt)).scalar_one_or_none()

        if category:
            await self.session.delete(category)
