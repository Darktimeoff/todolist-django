from .dao import UserDao
from .services import UserService

user_dao = UserDao()
user_service = UserService(user_dao)