from .dao import GoalCategoryDAO, GoalDAO, GoalCommentDAO
from .services import GoalService

goal_category_dao = GoalCategoryDAO()
goal_comment_dao = GoalCommentDAO()
goal_dao = GoalDAO()
goal_service = GoalService(goal_dao, goal_category_dao)