from core.models import User
from core.classes.dao import Dao

class UserDao(Dao[User]):
    def __init__(self):
        super().__init__(User)