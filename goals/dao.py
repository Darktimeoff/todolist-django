from django.db.models.manager import BaseManager
from core.classes.dao import Dao
from django.db.models import Q
from .models import GoalCategory, Goal,GoalComment
from core.models import User
class GoalCategoryDAO(Dao[GoalCategory]):
    EXCLUDE_FILTER = Q(is_deleted=True)

    def __init__(self, ordering=None):
        super().__init__(GoalCategory, ordering)

    def get_all(self) -> BaseManager[GoalCategory]:
        return super().get_all().exclude(self.EXCLUDE_FILTER).select_related('user')

    def get_all_by_user(self, user: User) -> BaseManager[GoalCategory]:
        return self.get_all().filter(user=user)
    
    def delete(self, category: int | GoalCategory) -> GoalCategory:
        id = category if type(category) is int else category.pk

        return  super().delete(id)
    
class GoalDAO(Dao[Goal]):
    EXCLUDE_FILTER = Q(is_deleted=True) | Q(status=Goal.Status.archived)

    def __init__(self, ordering=None):
        super().__init__(Goal, ordering)

    def get_all(self) -> BaseManager[Goal]:
        return super().get_all().exclude(self.EXCLUDE_FILTER).select_related('user', 'category')
    
    def get_all_by_user(self, user: User) -> BaseManager[Goal]:
        return self.get_all().filter(user=user)
    
class GoalCommentDAO(Dao[GoalComment]):
    def __init__(self, ordering=None):
        super().__init__(GoalComment, ordering)

    def get_all(self) -> BaseManager[GoalComment]:
        return super().get_all().select_related('user', 'goal')
    
    def get_all_by_user(self, user: User) -> BaseManager[GoalComment]:
        return self.get_all().filter(user=user)