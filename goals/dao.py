from django.db.models.manager import BaseManager
from core.classes.dao import Dao
from django.db.models import Q
from .models import GoalCategory
from core.models import User

class GoalCategoryDAO(Dao[GoalCategory]):
    SHOW_FILTER = Q(is_deleted=False)

    def __init__(self, ordering=None):
        super().__init__(GoalCategory, ordering)

    def get_all(self) -> BaseManager[GoalCategory]:
        return super().get_all().filter(self.SHOW_FILTER)

    def get_all_by_user(self, user: User) -> BaseManager[GoalCategory]:
        return super().get_all().filter(user=user)
    
    def delete(self, category: int | GoalCategory) -> GoalCategory:
        category: GoalCategory = self.get_by_id(category) if type(category) is int else category

        category.is_deleted = True

        category.save()

        return category