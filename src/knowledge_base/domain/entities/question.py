from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


class Question:
    def __init__(self, id_question: Id, title: Title, answer: str | None):
        self._id: Id = id_question
        self._title: Title = title
        self._answer: str | None = answer

    @property
    def id(self) -> Id:
        return self._id

    @property
    def title(self) -> Title:
        return self._title

    @property
    def answer(self) -> str | None:
        return self._answer

    def change_title(self, new_title: Title) -> None:
        self._title = new_title

    def change_answer(self, new_answer: str | None) -> None:
        self._answer = new_answer
