from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.uow import AbstractUoW
from knowledge_base.domain.entities.question import NewQuestion, Question
from knowledge_base.domain.errors import NotFound
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


class QuestionService:
    def __init__(self, uow: AbstractUoW):
        self.uow: AbstractUoW = uow

    async def get(self, id_category: int, id_subcategory: int, id_question: int) -> Question:
        id_object_question = Id(id_question)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            question = await uow.questions.get(id_object_subcategory, id_object_question)
            if question is None:
                raise NotFound("Question not found.")

            return question

    async def create(self, id_category: int, id_subcategory: int, title: str, answer: str | None) -> Question:
        title_object = Title(title)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            new_question = NewQuestion(id_subcategory=id_object_subcategory, title=title_object, answer=answer)

            return await uow.questions.save(new_question)

    async def update(
        self, id_category: int, id_subcategory: int, id_question: int, changes: dict[str, str | None | int]
    ) -> Question:
        id_object_question = Id(id_question)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            question = await uow.questions.get(id_object_subcategory, id_object_question)
            if question is None:
                raise NotFound("Question not found.")

            if "title" in changes:
                title_object = Title(changes["title"])
                question.change_title(title_object)

            if "answer" in changes:
                answer = changes["answer"]
                question.change_answer(str(answer) if answer else None)

            return await uow.questions.save(question)

    async def delete(self, id_category: int, id_subcategory: int, id_question: int) -> None:
        id_object_question = Id(id_question)
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            question = await uow.questions.get(id_object_subcategory, id_object_question)
            if question is None:
                raise NotFound("Question not found.")

            await uow.questions.delete(id_object_subcategory, id_object_question)

    async def list_by_subcategory(
        self, id_category: int, id_subcategory: int, pagination_options: PaginationOptions
    ) -> PaginationResult[Question]:
        id_object_category = Id(id_category)
        id_object_subcategory = Id(id_subcategory)

        async with self.uow as uow:
            if await uow.categories.get(id_object_category) is None:
                raise NotFound("Category not found.")

            if await uow.subcategories.get(id_object_category, id_object_subcategory) is None:
                raise NotFound("Subcategory not found.")

            return await uow.question_queries.list_by_subcategory(id_object_subcategory, pagination_options)
