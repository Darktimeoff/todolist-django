from django.db.models.manager import BaseManager
from core.classes.dao import Dao
from django.db.models import Q
from .models import GoalCategory, Goal,GoalComment, Board, BoardParticipant
from core.models import User
class GoalCategoryDAO(Dao[GoalCategory]):
    EXCLUDE_FILTER = Q(is_deleted=True)

    def __init__(self, ordering=None):
        super().__init__(GoalCategory, ordering)

    def get_all(self) -> BaseManager[GoalCategory]:
        return super().get_all().exclude(self.EXCLUDE_FILTER).select_related('user')

    def get_all_by_user(self, user: User) -> BaseManager[GoalCategory]:
        return self.get_all().filter(Q(user=user) | Q(board__participants__user=user))
    
    def delete(self, category: int | GoalCategory) -> GoalCategory:
        id = category if type(category) is int else category.pk

        return  super().delete(id)
    
class GoalDAO(Dao[Goal]):
    EXCLUDE_FILTER = Q(is_deleted=True) | Q(status=Goal.Status.archived)

    def __init__(self, ordering=None):
        super().__init__(Goal, ordering)

    def get_all(self) -> BaseManager[Goal]:
        return super().get_all().exclude(self.EXCLUDE_FILTER).select_related('user', 'category')
    
    def get_all_by_user(self, user: User) -> BaseManager[Goal]:
        return self.get_all().filter(user=user)
    
class GoalCommentDAO(Dao[GoalComment]):
    def __init__(self, ordering=None):
        super().__init__(GoalComment, ordering)

    def get_all(self) -> BaseManager[GoalComment]:
        return super().get_all().select_related('user', 'goal')
    
    def get_all_by_user(self, user: User) -> BaseManager[GoalComment]:
        return self.get_all().filter(user=user)
    
class BoardDAO(Dao[Board]):
    EXCLUDE_FILTER = Q(is_deleted=True)

    def __init__(self, ordering=None):
        super().__init__(Board, ordering)

    def get_all(self) -> BaseManager[Board]:
        return super().get_all().exclude(self.EXCLUDE_FILTER)
    
    def get_all_by_user(self, user: User) -> BaseManager[Board]:
        return self.get_all().filter(participants__user=user)
    
class BoardParticipantDAO(Dao[BoardParticipant]):
    def __init__(self, ordering=None):
        super().__init__(BoardParticipant, ordering)

    def get_all(self) -> BaseManager[BoardParticipant]:
        return super().get_all().select_related('user', 'board')
    
    def get_all_by_user(self, user: User) -> BaseManager[BoardParticipant]:
        return self.get_all().filter(user=user)
    
    def get_all_by_board(self, board: Board) -> BaseManager[BoardParticipant]:
        return self.get_all().filter(board=board)
    
    def get_participant(self, user: User, board: Board) -> BoardParticipant | None:
        return self.get_all().filter(user=user, board=board).first()
    
    def change_role(self, participant_id: int | BoardParticipant, role: BoardParticipant.Role) -> BoardParticipant:
        return super().update(participant_id if type(participant_id) is int else participant_id.pk, {
            "role": role
        })
    
    def delete_participant(self, participant_id: int | BoardParticipant) -> BoardParticipant:
        return super().delete(participant_id if type(participant_id) is int else participant_id.pk)
    
    def is_user_participant(self, user: User, board: Board) -> bool:
        return bool(self.get_participant(user, board))
    
    def add_participant(self, user: User, board: Board, role: BoardParticipant.Role = BoardParticipant.Role.owner) -> BoardParticipant:
        return super().create({
            "user": user,
            "board": board,
            "role": role
        })