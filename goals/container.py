from .dao import GoalCategoryDAO, GoalDAO, GoalCommentDAO, BoardDAO, BoardParticipantDAO
from .services import GoalService, BoardService

goal_category_dao = GoalCategoryDAO()
goal_comment_dao = GoalCommentDAO()
goal_dao = GoalDAO()
goal_service = GoalService(goal_dao, goal_category_dao)
board_dao = BoardDAO()
board_participant_dao = BoardParticipantDAO()
board_service = BoardService(board_dao, board_participant_dao)
