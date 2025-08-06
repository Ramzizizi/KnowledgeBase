from fastapi import Depends

from knowledge_base.application.services.category_service import CategoryService
from knowledge_base.application.services.question_service import QuestionService
from knowledge_base.application.services.source_service import SourceService
from knowledge_base.application.services.subcategory_service import SubCategoryService
from knowledge_base.application.services.task_service import TaskService
from knowledge_base.infrastructure.uow import SqlAlchemyUoW


def get_uow() -> SqlAlchemyUoW:
    return SqlAlchemyUoW()


def get_category_service(uow: SqlAlchemyUoW = Depends(get_uow)) -> CategoryService:
    return CategoryService(uow)


def get_subcategory_service(uow: SqlAlchemyUoW = Depends(get_uow)) -> SubCategoryService:
    return SubCategoryService(uow)


def get_question_service(uow: SqlAlchemyUoW = Depends(get_uow)) -> QuestionService:
    return QuestionService(uow)


def get_task_service(uow: SqlAlchemyUoW = Depends(get_uow)) -> TaskService:
    return TaskService(uow)


def get_source_service(uow: SqlAlchemyUoW = Depends(get_uow)) -> SourceService:
    return SourceService(uow)
