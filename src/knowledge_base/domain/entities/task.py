from knowledge_base.domain.value_objects.id import Id


class Task:
    def __init__(self, id_task: Id, description: str):
        self._id: Id = id_task
        self._description: str = description

    @property
    def id(self) -> Id:
        return self._id

    @property
    def description(self) -> str:
        return self._description

    def change_description(self, new_description: str) -> None:
        self._description = new_description
