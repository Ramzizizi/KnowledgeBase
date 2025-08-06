from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from knowledge_base.domain.entities.task import NewTask, Task
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.infrastructure.db.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str]

    id_subcategory: Mapped[int] = mapped_column(ForeignKey("subcategories.id", ondelete="RESTRICT"), nullable=False)

    @staticmethod
    def from_new_entity(task: NewTask) -> "TaskModel":
        return TaskModel(description=task.description, id_subcategory=int(task.id_subcategory))

    @staticmethod
    def from_entity(task: Task) -> "TaskModel":
        return TaskModel(id=int(task.id), description=task.description, id_subcategory=int(task.id_subcategory))

    def to_entity(self) -> Task:
        return Task(id=Id(self.id), description=self.description, id_subcategory=Id(self.id_subcategory))
