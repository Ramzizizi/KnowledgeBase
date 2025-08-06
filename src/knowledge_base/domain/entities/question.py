from dataclasses import dataclass

from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


@dataclass
class QuestionBase:
    title: Title
    answer: str | None
    id_subcategory: Id

    def change_title(
        self,
        new_title: Title,
    ) -> None:
        self.title = new_title

    def change_answer(
        self,
        new_answer: str | None,
    ) -> None:
        self.answer = new_answer

    def change_subcategory(
        self,
        new_id_subcategory: Id,
    ) -> None:
        self.id_subcategory = new_id_subcategory


@dataclass
class NewQuestion(QuestionBase): ...


@dataclass
class Question(QuestionBase):
    id: Id
