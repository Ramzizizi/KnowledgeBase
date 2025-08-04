from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.link import Link


class Source:
    def __init__(self, id_source: Id, link: Link):
        self._id: Id = id_source
        self._link: Link = link

    @property
    def id(self) -> Id:
        return self._id

    @property
    def link(self) -> Link:
        return self._link

    def change_link(self, link: Link) -> None:
        self._link = link
