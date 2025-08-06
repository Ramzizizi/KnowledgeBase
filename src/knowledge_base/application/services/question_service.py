from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.question import NewQuestion, Question
from knowledge_base.domain.errors import QuestionNotFound, SubCategoryNotFound
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


class QuestionService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_question: int) -> Question:
        id_object = Id(id_question)

        async with self.uow as uow:
            question = await uow.questions.get(id_object)

        if question is None:
            raise QuestionNotFound("Question not found.")

        return question

    async def create(self, id_subcategory: int, title: str, answer: str | None) -> Question:
        id_object = Id(id_subcategory)
        title_object = Title(title)

        async with self.uow as uow:
            if await uow.subcategories.get(id_object) is None:
                raise SubCategoryNotFound("Subcategory not found.")

            new_question = NewQuestion(id_subcategory=id_object, title=title_object, answer=answer)

            return await uow.questions.save(new_question)

    async def update(self, id_question: int, changes: dict[str, str | None | int]) -> Question:
        id_object = Id(id_question)

        async with self.uow as uow:
            question = await uow.questions.get(id_object)

            if question is None:
                raise QuestionNotFound("Question not found.")

            if "title" in changes:
                title_object = Title(changes["title"])
                question.change_title(title_object)

            if "answer" in changes:
                answer = changes["answer"]
                question.change_answer(str(answer) if answer else None)

            if "id_subcategory" in changes:
                id_subcategory = Id(changes["id_subcategory"])

                if await uow.subcategories.get(id_subcategory) is None:
                    raise SubCategoryNotFound("Subcategory not found.")

                question.change_subcategory(id_subcategory)

            return await uow.questions.save(question)

    async def delete(self, id_question: int) -> None:
        id_object = Id(id_question)

        async with self.uow as uow:
            question = await uow.questions.get(id_object)

            if question is None:
                raise QuestionNotFound("Question not found.")

            await uow.questions.delete(id_object)
