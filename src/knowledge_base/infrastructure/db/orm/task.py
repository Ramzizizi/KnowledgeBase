from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from knowledge_base.infrastructure.db.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    description: Mapped[str]

    id_category: Mapped[int] = mapped_column(
        ForeignKey(
            "subcategories.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
