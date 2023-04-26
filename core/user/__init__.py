from .dao import UserDao
from .service import UserService

user_dao = UserDao()
user_service = UserService(user_dao)