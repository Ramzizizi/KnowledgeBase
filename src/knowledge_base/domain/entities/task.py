from dataclasses import dataclass

from knowledge_base.domain.value_objects.id import Id


@dataclass
class TaskBase:
    description: str
    id_subcategory: Id

    def change_description(
        self,
        new_description: str,
    ) -> None:
        self.description = new_description

    def change_subcategory(
        self,
        new_id_subcategory: Id,
    ) -> None:
        self.id_subcategory = new_id_subcategory


@dataclass
class NewTask(TaskBase): ...


@dataclass
class Task(TaskBase):
    id: Id
