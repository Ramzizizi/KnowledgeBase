from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from knowledge_base.domain.entities.question import NewQuestion, Question
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title
from knowledge_base.infrastructure.db.database import Base


class QuestionModel(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str | None]

    id_subcategory: Mapped[int] = mapped_column(ForeignKey("subcategories.id", ondelete="RESTRICT"), nullable=False)

    @staticmethod
    def from_new_entity(question: NewQuestion) -> "QuestionModel":
        return QuestionModel(title=question.title, answer=question.answer, id_subcategory=question.id_subcategory)

    @staticmethod
    def from_entity(question: Question) -> "QuestionModel":
        return QuestionModel(
            id=question.id, title=question.title, answer=question.answer, id_subcategory=question.id_subcategory
        )

    def to_entity(self) -> Question:
        return Question(
            id=Id(self.id), title=Title(self.title), answer=self.answer, id_subcategory=Id(self.id_subcategory)
        )
