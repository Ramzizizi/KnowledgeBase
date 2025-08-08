from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from knowledge_base.application.services.question_service import QuestionService
from knowledge_base.application.services.source_service import SourceService
from knowledge_base.application.services.subcategory_service import SubCategoryService
from knowledge_base.application.services.task_service import TaskService
from knowledge_base.interface.api.schemas.question import CreateQuestion, OutQuestion, UpdateQuestion
from knowledge_base.interface.api.schemas.source import CreateSource, OutSource, UpdateSource
from knowledge_base.interface.api.schemas.subcategory import (
    CreateSubCategory,
    DetailedOutSubCategory,
    OutSubCategory,
    UpdateSubCategory,
)
from knowledge_base.interface.api.schemas.task import CreateTask, OutTask, UpdateTask
from knowledge_base.interface.dependencies import (
    get_question_service,
    get_source_service,
    get_subcategory_service,
    get_task_service,
)

router = APIRouter(
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Object not found."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error."},
    },
)


################################################## SUBCATEGORY ROUTE ###################################################


@router.get(
    path="/{idCategory}/subcategories",
    status_code=status.HTTP_200_OK,
    response_model=list[OutSubCategory],
    tags=["Subcategories"],
)
async def get_subcategories(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
) -> list[OutSubCategory]:
    subcategories = await service.list_by_category(id_category)

    return [OutSubCategory.from_entity(subcategory) for subcategory in subcategories]


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedOutSubCategory,
    tags=["Subcategories"],
)
async def get_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    subcategory_service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    question_service: Annotated[QuestionService, Depends(get_question_service)],
    source_service: Annotated[SourceService, Depends(get_source_service)],
) -> DetailedOutSubCategory:
    subcategory = await subcategory_service.get(id_category, id_subcategory)
    tasks = await task_service.list_by_subcategory(id_category, id_subcategory)
    questions = await question_service.list_by_subcategory(id_category, id_subcategory)
    sources = await source_service.list_by_subcategory(id_category, id_subcategory)

    schema_subcategory = DetailedOutSubCategory.from_entity(subcategory)
    schema_subcategory.tasks = [OutTask.from_entity(task) for task in tasks]
    schema_subcategory.questions = [OutQuestion.from_entity(question) for question in questions]
    schema_subcategory.sources = [OutSource.from_entity(source) for source in sources]

    return schema_subcategory


@router.post(
    path="/{idCategory}/subcategories",
    status_code=status.HTTP_201_CREATED,
    response_model=OutSubCategory,
    tags=["Subcategories"],
)
async def create_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    data_to_create: CreateSubCategory,
    service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
) -> OutSubCategory:
    subcategory = await service.create(id_category, **data_to_create.model_dump())

    return OutSubCategory.from_entity(subcategory)


@router.patch(
    path="/{idCategory}/subcategories/{idSubcategory}",
    status_code=status.HTTP_200_OK,
    response_model=OutSubCategory,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Incorrect values."},
    },
    tags=["Subcategories"],
)
async def update_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    data_to_update: UpdateSubCategory,
    service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
) -> OutSubCategory:
    subcategory = await service.update(id_category, id_subcategory, **data_to_update.model_dump())

    return OutSubCategory.from_entity(subcategory)


@router.delete(
    path="/{idCategory}/subcategories/{idSubcategory}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Incorrect values."},
        status.HTTP_409_CONFLICT: {"description": "Object has related data."},
    },
    tags=["Subcategories"],
)
async def delete_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
) -> None:
    await service.delete(id_category, id_subcategory)


##################################################### TASKS ROUTER #####################################################


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/tasks",
    status_code=status.HTTP_200_OK,
    response_model=list[OutTask],
    tags=["Task"],
)
async def get_tasks_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> list[OutTask]:
    tasks = await service.list_by_subcategory(id_category, id_subcategory)

    return [OutTask.from_entity(task) for task in tasks]


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/tasks/{idTask}",
    status_code=status.HTTP_200_OK,
    response_model=OutTask,
    tags=["Task"],
)
async def get_task_subcategory(
    id_task: Annotated[int, Path(alias="idTask", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> OutTask:
    task = await service.get(id_category, id_subcategory, id_task)

    return OutTask.from_entity(task)


@router.post(
    path="/{idCategory}/subcategories/{idSubcategory}/tasks/",
    status_code=status.HTTP_201_CREATED,
    response_model=OutTask,
    tags=["Task"],
)
async def create_task_subcategory(
    data_to_create: CreateTask,
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> OutTask:
    task = await service.create(id_category, id_subcategory, **data_to_create.model_dump())

    return OutTask.from_entity(task)


@router.patch(
    path="/{idCategory}/subcategories/{idSubcategory}/tasks/{idTask}",
    status_code=status.HTTP_200_OK,
    response_model=OutTask,
    tags=["Task"],
)
async def update_task_subcategory(
    data_to_update: UpdateTask,
    id_task: Annotated[int, Path(alias="idTask", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> OutTask:
    task = await service.update(id_category, id_subcategory, id_task, **data_to_update.model_dump())

    return OutTask.from_entity(task)


@router.delete(
    path="/{idCategory}/subcategories/{idSubcategory}/tasks/{idTask}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Task"],
)
async def delete_task_subcategory(
    id_task: Annotated[int, Path(alias="idTask", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> None:
    await service.delete(id_category, id_subcategory, id_task)


################################################### QUESTIONS ROUTER ###################################################


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/questions",
    status_code=status.HTTP_200_OK,
    response_model=list[OutQuestion],
    tags=["Question"],
)
async def get_questions_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> list[OutQuestion]:
    questions = await service.list_by_subcategory(id_category, id_subcategory)

    return [OutQuestion.from_entity(question) for question in questions]


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/questions/{idQuestions}",
    status_code=status.HTTP_200_OK,
    response_model=OutQuestion,
    tags=["Question"],
)
async def get_question_subcategory(
    id_questions: Annotated[int, Path(alias="idQuestions", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> OutQuestion:
    question = await service.get(id_category, id_subcategory, id_questions)

    return OutQuestion.from_entity(question)


@router.post(
    path="/{idCategory}/subcategories/{idSubcategory}/questions/",
    status_code=status.HTTP_201_CREATED,
    response_model=OutQuestion,
    tags=["Question"],
)
async def create_question_subcategory(
    data_to_create: CreateQuestion,
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> OutQuestion:
    question = await service.create(id_category, id_subcategory, **data_to_create.model_dump())

    return OutQuestion.from_entity(question)


@router.patch(
    path="/{idCategory}/subcategories/{idSubcategory}/questions/{idQuestions}",
    status_code=status.HTTP_200_OK,
    response_model=OutQuestion,
    tags=["Question"],
)
async def update_question_subcategory(
    data_to_update: UpdateQuestion,
    id_questions: Annotated[int, Path(alias="idQuestions", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> OutQuestion:
    task = await service.update(id_category, id_subcategory, id_questions, **data_to_update.model_dump())

    return OutQuestion.from_entity(task)


@router.delete(
    path="/{idCategory}/subcategories/{idSubcategory}/questions/{idQuestions}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Question"],
)
async def delete_question_subcategory(
    id_questions: Annotated[int, Path(alias="idQuestions", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> None:
    await service.delete(id_category, id_subcategory, id_questions)


##################################################### SOURCES ROUTER ###################################################


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/sources",
    status_code=status.HTTP_200_OK,
    response_model=list[OutSource],
    tags=["Source"],
)
async def get_sources_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> list[OutSource]:
    sources = await service.list_by_subcategory(id_category, id_subcategory)

    return [OutSource.from_entity(source) for source in sources]


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/sources/{idSource}",
    status_code=status.HTTP_200_OK,
    response_model=OutSource,
    tags=["Source"],
)
async def get_source_subcategory(
    id_source: Annotated[int, Path(alias="idSources", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> OutSource:
    source = await service.get(id_category, id_subcategory, id_source)

    return OutSource.from_entity(source)


@router.post(
    path="/{idCategory}/subcategories/{idSubcategory}/sources/",
    status_code=status.HTTP_201_CREATED,
    response_model=OutSource,
    tags=["Source"],
)
async def create_source_subcategory(
    data_to_create: CreateSource,
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> OutSource:
    question = await service.create(id_category, id_subcategory, **data_to_create.model_dump())

    return OutSource.from_entity(question)


@router.patch(
    path="/{idCategory}/subcategories/{idSubcategory}/sources/{idSource}",
    status_code=status.HTTP_200_OK,
    response_model=OutSource,
    tags=["Source"],
)
async def update_source_subcategory(
    data_to_update: UpdateSource,
    id_source: Annotated[int, Path(alias="idSource", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> OutSource:
    source = await service.update(id_category, id_subcategory, id_source, **data_to_update.model_dump())

    return OutSource.from_entity(source)


@router.delete(
    path="/{idCategory}/subcategories/{idSubcategory}/sources/{idQuestions}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Source"],
)
async def delete_source_subcategory(
    id_source: Annotated[int, Path(alias="idSource", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> None:
    await service.delete(id_category, id_subcategory, id_source)
