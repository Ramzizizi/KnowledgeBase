from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from knowledge_base.infrastructure.db.database import Base


class QuestionModel(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str]

    id_category: Mapped[int] = mapped_column(ForeignKey("subcategories.id", ondelete="RESTRICT"), nullable=False)
