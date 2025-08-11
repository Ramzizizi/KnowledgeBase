import asyncio

from knowledge_base.domain.repository.question_repository import QuestionRepository
from knowledge_base.domain.repository.source_repository import SourceRepository
from knowledge_base.domain.repository.task_repository import TaskRepository
from knowledge_base.domain.value_objects.id import Id


class SubCategoryDeletionPolicy:
    def __init__(self, task: TaskRepository, source: SourceRepository, question: QuestionRepository):
        self.task: TaskRepository = task
        self.source: SourceRepository = source
        self.question: QuestionRepository = question

    async def can_delete(self, id_subcategory: Id) -> bool:
        task_exists, source_exists, question_exists = await asyncio.gather(
            self.task.exists_by_subcategory(id_subcategory),
            self.source.exists_by_subcategory(id_subcategory),
            self.question.exists_by_subcategory(id_subcategory),
        )

        return not any((task_exists, source_exists, question_exists))
