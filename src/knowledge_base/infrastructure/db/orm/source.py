from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from knowledge_base.domain.entities.source import NewSource, Source
from knowledge_base.domain.value_objects.id import Id
from knowledge_base.domain.value_objects.link import Link
from knowledge_base.infrastructure.db.database import Base


class SourceModel(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str]

    id_subcategory: Mapped[int] = mapped_column(ForeignKey("subcategories.id", ondelete="RESTRICT"), nullable=False)

    @staticmethod
    def from_new_entity(source: NewSource) -> "SourceModel":
        return SourceModel(link=source.link, id_subcategory=source.id_subcategory)

    @staticmethod
    def from_entity(source: Source) -> "SourceModel":
        return SourceModel(id=source.id, link=source.link, id_subcategory=source.id_subcategory)

    def to_entity(self) -> Source:
        return Source(id=Id(self.id), link=Link(self.link), id_subcategory=Id(self.id_subcategory))
