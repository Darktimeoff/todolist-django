from .dao import GoalDAO, GoalCategoryDAO
from rest_framework.serializers import ValidationError
from .message import VALIDATION_CATEGORY_OWNER,VALIDATION_GOAL_OWNER, VALIDATION_NOT_ALLOWED_FOR_DELETED_CATEGORY, VALIDATION_NOT_ALLOWED_FOR_DELETED_GOAL
from core.models import User
from rest_framework.exceptions import ValidationError

class GoalService:
    dao: GoalDAO
    category_dao: GoalCategoryDAO

    def __init__(self, dao: GoalDAO, category_dao: GoalCategoryDAO):
        self.dao = dao
        self.category_dao = category_dao

    def validate_category(self, category_id: int, user: User):
        """raise ValidationError if category is not found, user not owner, category is deleted"""
        category = self.category_dao.get_by_id(category_id) if type(category_id) is int else category_id

        if category.is_deleted:
            raise ValidationError({"category": [VALIDATION_NOT_ALLOWED_FOR_DELETED_CATEGORY]})
        
        if category.user_id != user.pk:
            raise ValidationError({"category": [VALIDATION_CATEGORY_OWNER]})
        
        return category
    
    def validate_comment(self, goal_id: int, user: User):
        goal = self.dao.get_by_id(goal_id) if type(goal_id) is int else goal_id


        if goal.is_deleted or goal.status == goal.Status.archived:
            raise ValidationError({"comment": [VALIDATION_NOT_ALLOWED_FOR_DELETED_GOAL]})
        
        if goal.user_id != user.pk:
            raise ValidationError({"comment": [VALIDATION_GOAL_OWNER]})
        
        return goal
