from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from knowledge_base.domain.entities.category import Category, NewCategory
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title
from knowledge_base.infrastructure.db.database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None]

    @staticmethod
    def from_new_entity(category: NewCategory) -> "CategoryModel":
        return CategoryModel(title=str(category.title), description=category.description)

    @staticmethod
    def from_entity(category: Category) -> "CategoryModel":
        return CategoryModel(id=int(category.id), title=str(category.title), description=category.description)

    def to_entity(self) -> Category:
        return Category(id=Id(self.id), title=Title(self.title), description=self.description)
