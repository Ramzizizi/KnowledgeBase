from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from knowledge_base.domain.entities.subcategory import NewSubCategory, SubCategory
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title
from knowledge_base.infrastructure.db.database import Base


class SubCategoryModel(Base):
    __tablename__ = "subcategories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    id_category: Mapped[int] = mapped_column(
        ForeignKey(
            "categories.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    @staticmethod
    def from_entity(
        category: NewSubCategory,
    ) -> "SubCategoryModel":
        return SubCategoryModel(
            title=category.title,
        )

    def to_entity(
        self,
    ) -> SubCategory:
        return SubCategory(
            id=Id(self.id),
            title=Title(self.title),
            id_category=Id(self.id_category),
        )
