from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from knowledge_base.infrastructure.db.database import Base


class SourceModel(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    link: Mapped[str]

    id_category: Mapped[int] = mapped_column(
        ForeignKey(
            "subcategories.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
