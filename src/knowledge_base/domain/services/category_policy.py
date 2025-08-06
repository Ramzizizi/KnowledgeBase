from knowledge_base.domain.repository.subcategory_repository import SubCategoryRepository
from knowledge_base.domain.value_objects.id import Id


class CategoryDeletionPolicy:
    def __init__(
        self,
        subcategory: SubCategoryRepository,
    ):
        self.subcategory = subcategory

    def can_delete(
        self,
        id_category: Id,
    ) -> bool:
        return not self.subcategory.exists_by_category(id_category)
