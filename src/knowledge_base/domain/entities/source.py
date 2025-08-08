from dataclasses import dataclass

from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.link import Link


@dataclass
class SourceBase:
    link: Link
    id_subcategory: Id

    def change_link(self, link: Link) -> None:
        self.link = link


@dataclass
class NewSource(SourceBase): ...


@dataclass
class Source(SourceBase):
    id: Id
