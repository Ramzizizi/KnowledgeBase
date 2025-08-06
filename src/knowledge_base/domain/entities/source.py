from dataclasses import dataclass

from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.link import Link


@dataclass
class SourceBase:
    link: Link
    id_subcategory: Id

    def change_link(self, link: Link) -> None:
        self.link = link

    def change_subcategory(self, new_id_subcategory: Id) -> None:
        self.id_subcategory = new_id_subcategory


@dataclass
class NewSource(SourceBase): ...


@dataclass
class Source(SourceBase):
    id: Id
