from .dao import UserDao
from rest_framework.serializers import ValidationError
from .message import VALIDATION_OLD_PASSWORD

class UserService:
    dao: UserDao

    def __init__(self, user_dao: UserDao):
        self.dao = user_dao

    def change_password(self, id: int, old_password: str, new_password: str):
        user = self.dao.get_by_id(id)

        if not user.check_password(old_password):
            raise ValidationError({
                "old_password": [VALIDATION_OLD_PASSWORD]
            })

        user.set_password(new_password)

        user.save()

        return user
