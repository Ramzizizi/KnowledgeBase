from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


class Category:
    def __init__(self, id_category: Id, title: Title, description: str | None):
        self._id: Id = id_category
        self._title: Title = title
        self._description: str | None = description

    @property
    def id(self) -> Id:
        return self._id

    @property
    def title(self) -> Title:
        return self._title

    @property
    def description(self) -> str | None:
        return self._description

    def change_title(self, new_title: Title) -> None:
        self._title = new_title

    def change_description(self, new_description: str | None) -> None:
        self._description = new_description
