from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from knowledge_base.application.schemas.pagination import PaginationOptions, PaginationResult
from knowledge_base.application.services.question_service import QuestionService
from knowledge_base.application.services.source_service import SourceService
from knowledge_base.application.services.subcategory_service import SubCategoryService
from knowledge_base.application.services.task_service import TaskService
from knowledge_base.interface.api.schemas.question import CreateQuestion, OutQuestion, UpdateQuestion
from knowledge_base.interface.api.schemas.source import CreateSource, OutSource, UpdateSource
from knowledge_base.interface.api.schemas.subcategory import (
    CreateSubCategory,
    OutSubCategory,
    UpdateSubCategory,
)
from knowledge_base.interface.api.schemas.task import CreateTask, OutTask, UpdateTask
from knowledge_base.interface.api.schemas.utils import DetailedResponse
from knowledge_base.interface.dependencies import (
    get_pagination,
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
    response_model=PaginationResult[OutSubCategory],
    tags=["Subcategories"],
)
async def get_subcategories(
    pagination_options: Annotated[PaginationOptions, Depends(get_pagination)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
) -> PaginationResult[OutSubCategory]:
    subcategories = await service.list_by_category(id_category, pagination_options)

    return PaginationResult(  # noqa
        total=subcategories["total"],
        items=[OutSubCategory.from_entity(subcategory) for subcategory in subcategories["items"]],
    )


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutSubCategory],
    tags=["Subcategories"],
)
async def get_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
) -> DetailedResponse[OutSubCategory]:
    subcategory = await service.get(id_category, id_subcategory)
    schema_subcategory = OutSubCategory.from_entity(subcategory)

    return DetailedResponse(data=schema_subcategory)


@router.post(
    path="/{idCategory}/subcategories",
    status_code=status.HTTP_201_CREATED,
    response_model=DetailedResponse[OutSubCategory],
    tags=["Subcategories"],
)
async def create_subcategory(
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    data_to_create: CreateSubCategory,
    service: Annotated[SubCategoryService, Depends(get_subcategory_service)],
) -> DetailedResponse[OutSubCategory]:
    subcategory = await service.create(id_category, **data_to_create.model_dump())

    return DetailedResponse(data=OutSubCategory.from_entity(subcategory))


@router.patch(
    path="/{idCategory}/subcategories/{idSubcategory}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutSubCategory],
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
) -> DetailedResponse[OutSubCategory]:
    subcategory = await service.update(id_category, id_subcategory, **data_to_update.model_dump())

    return DetailedResponse(data=OutSubCategory.from_entity(subcategory))


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
    response_model=PaginationResult[OutTask],
    tags=["Task"],
)
async def get_tasks_subcategory(
    pagination_options: Annotated[PaginationOptions, Depends(get_pagination)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> PaginationResult[OutTask]:
    tasks = await service.list_by_subcategory(id_category, id_subcategory, pagination_options)

    return PaginationResult(total=tasks["total"], items=[OutTask.from_entity(task) for task in tasks["items"]])  # noqa


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/tasks/{idTask}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutTask],
    tags=["Task"],
)
async def get_task_subcategory(
    id_task: Annotated[int, Path(alias="idTask", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> DetailedResponse[OutTask]:
    task = await service.get(id_category, id_subcategory, id_task)

    return DetailedResponse(data=OutTask.from_entity(task))


@router.post(
    path="/{idCategory}/subcategories/{idSubcategory}/tasks/",
    status_code=status.HTTP_201_CREATED,
    response_model=DetailedResponse[OutTask],
    tags=["Task"],
)
async def create_task_subcategory(
    data_to_create: CreateTask,
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> DetailedResponse[OutTask]:
    task = await service.create(id_category, id_subcategory, **data_to_create.model_dump())

    return DetailedResponse(data=OutTask.from_entity(task))


@router.patch(
    path="/{idCategory}/subcategories/{idSubcategory}/tasks/{idTask}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutTask],
    tags=["Task"],
)
async def update_task_subcategory(
    data_to_update: UpdateTask,
    id_task: Annotated[int, Path(alias="idTask", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> DetailedResponse[OutTask]:
    task = await service.update(id_category, id_subcategory, id_task, **data_to_update.model_dump())

    return DetailedResponse(data=OutTask.from_entity(task))


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
    response_model=PaginationResult[OutQuestion],
    tags=["Question"],
)
async def get_questions_subcategory(
    pagination_options: Annotated[PaginationOptions, Depends(get_pagination)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> PaginationResult[OutQuestion]:
    questions = await service.list_by_subcategory(id_category, id_subcategory, pagination_options)

    return PaginationResult(  # noqa
        total=questions["total"], items=[OutQuestion.from_entity(question) for question in questions["items"]]
    )


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/questions/{idQuestions}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutQuestion],
    tags=["Question"],
)
async def get_question_subcategory(
    id_questions: Annotated[int, Path(alias="idQuestions", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> DetailedResponse[OutQuestion]:
    question = await service.get(id_category, id_subcategory, id_questions)

    return DetailedResponse(data=OutQuestion.from_entity(question))


@router.post(
    path="/{idCategory}/subcategories/{idSubcategory}/questions/",
    status_code=status.HTTP_201_CREATED,
    response_model=DetailedResponse[OutQuestion],
    tags=["Question"],
)
async def create_question_subcategory(
    data_to_create: CreateQuestion,
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> DetailedResponse[OutQuestion]:
    question = await service.create(id_category, id_subcategory, **data_to_create.model_dump())

    return DetailedResponse(data=OutQuestion.from_entity(question))


@router.patch(
    path="/{idCategory}/subcategories/{idSubcategory}/questions/{idQuestions}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutQuestion],
    tags=["Question"],
)
async def update_question_subcategory(
    data_to_update: UpdateQuestion,
    id_questions: Annotated[int, Path(alias="idQuestions", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> DetailedResponse[OutQuestion]:
    task = await service.update(id_category, id_subcategory, id_questions, **data_to_update.model_dump())

    return DetailedResponse(data=OutQuestion.from_entity(task))


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
    response_model=PaginationResult[OutSource],
    tags=["Source"],
)
async def get_sources_subcategory(
    pagination_options: Annotated[PaginationOptions, Depends(get_pagination)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> PaginationResult[OutSource]:
    sources = await service.list_by_subcategory(id_category, id_subcategory, pagination_options)

    return PaginationResult(  # noqa
        total=sources["total"], items=[OutSource.from_entity(source) for source in sources["items"]]
    )


@router.get(
    path="/{idCategory}/subcategories/{idSubcategory}/sources/{idSource}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutSource],
    tags=["Source"],
)
async def get_source_subcategory(
    id_source: Annotated[int, Path(alias="idSources", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> DetailedResponse[OutSource]:
    source = await service.get(id_category, id_subcategory, id_source)

    return DetailedResponse(data=OutSource.from_entity(source))


@router.post(
    path="/{idCategory}/subcategories/{idSubcategory}/sources/",
    status_code=status.HTTP_201_CREATED,
    response_model=DetailedResponse[OutSource],
    tags=["Source"],
)
async def create_source_subcategory(
    data_to_create: CreateSource,
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> DetailedResponse[OutSource]:
    question = await service.create(id_category, id_subcategory, **data_to_create.model_dump())

    return DetailedResponse(data=OutSource.from_entity(question))


@router.patch(
    path="/{idCategory}/subcategories/{idSubcategory}/sources/{idSource}",
    status_code=status.HTTP_200_OK,
    response_model=DetailedResponse[OutSource],
    tags=["Source"],
)
async def update_source_subcategory(
    data_to_update: UpdateSource,
    id_source: Annotated[int, Path(alias="idSource", gt=0)],
    id_category: Annotated[int, Path(alias="idCategory", gt=0)],
    id_subcategory: Annotated[int, Path(alias="idSubcategory", gt=0)],
    service: Annotated[SourceService, Depends(get_source_service)],
) -> DetailedResponse[OutSource]:
    source = await service.update(id_category, id_subcategory, id_source, **data_to_update.model_dump())

    return DetailedResponse(data=OutSource.from_entity(source))


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
