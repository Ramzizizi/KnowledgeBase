from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.title import Title


class SubCategory:
    def __init__(self, id_subcategory: Id, title: Title):
        self._id: Id = id_subcategory
        self._title: Title = title

    @property
    def id(self) -> Id:
        return self._id

    @property
    def title(self) -> Title:
        return self._title

    def change_title(self, new_title: Title) -> None:
        self._title = new_title
