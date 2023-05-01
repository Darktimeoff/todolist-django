from .dao import UserDao
from rest_framework.serializers import ValidationError
from .message import VALIDATION_OLD_PASSWORD
from core.models import User

class UserService:
    dao: UserDao

    def __init__(self, user_dao: UserDao):
        self.dao = user_dao

    def change_password(self, user: int | User, old_password: str, new_password: str):
        user: User = self.dao.get_by_id(user) if type(user) is int else user

        if not user.check_password(old_password):
            raise ValidationError({
                "old_password": [VALIDATION_OLD_PASSWORD]
            })

        user.set_password(new_password)

        user.save()

        return user
