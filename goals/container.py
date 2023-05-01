from .dao import GoalCategoryDAO, GoalDAO
from .services import GoalService

goal_category_dao = GoalCategoryDAO()
goal_dao = GoalDAO()
goal_service = GoalService(goal_dao, goal_category_dao)