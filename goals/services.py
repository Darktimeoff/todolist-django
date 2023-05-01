from .dao import GoalDAO, GoalCategoryDAO
from rest_framework.serializers import ValidationError
from .message import VALIDATION_CATEGORY_NOT_FOUND, VALIDATION_CATEGORY_OWNER, VALIDATION_NOT_ALLOWED_FOR_DELETED_CATEGORY
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
        category = self.category_dao.get_by_id(category_id)

        if category is None:
            raise ValidationError({"category": [VALIDATION_CATEGORY_NOT_FOUND]})
        
        if category.is_deleted:
            raise ValidationError({"category": [VALIDATION_NOT_ALLOWED_FOR_DELETED_CATEGORY]})
        
        if category.user_id != user.pk:
            raise ValidationError({"category": [VALIDATION_CATEGORY_OWNER]})
        
        return category
        