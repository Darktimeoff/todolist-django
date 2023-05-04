from .dao import GoalDAO, GoalCategoryDAO, BoardParticipantDAO, BoardDAO
from rest_framework.serializers import ValidationError
from .message import VALIDATION_CATEGORY_OWNER,VALIDATION_GOAL_OWNER, VALIDATION_NOT_ALLOWED_FOR_DELETED_CATEGORY, VALIDATION_NOT_ALLOWED_FOR_DELETED_GOAL
from core.models import User
from .models import Board, BoardParticipant
from rest_framework.exceptions import ValidationError
from typing import List
class GoalService:
    dao: GoalDAO
    category_dao: GoalCategoryDAO

    def __init__(self, dao: GoalDAO, category_dao: GoalCategoryDAO):
        self.dao = dao
        self.category_dao = category_dao

    def validate_category(self, category_id: int, user: User):
        """raise ValidationError if category is not found, user not owner, category is deleted"""
        category = self.category_dao.get_by_id(category_id) if type(category_id) is int else category_id

        if category.is_deleted:
            raise ValidationError({"category": [VALIDATION_NOT_ALLOWED_FOR_DELETED_CATEGORY]})
        
        if category.user_id != user.pk:
            raise ValidationError({"category": [VALIDATION_CATEGORY_OWNER]})
        
        return category
    
    def validate_comment(self, goal_id: int, user: User):
        goal = self.dao.get_by_id(goal_id) if type(goal_id) is int else goal_id


        if goal.is_deleted or goal.status == goal.Status.archived:
            raise ValidationError({"comment": [VALIDATION_NOT_ALLOWED_FOR_DELETED_GOAL]})
        
        if goal.user_id != user.pk:
            raise ValidationError({"comment": [VALIDATION_GOAL_OWNER]})
        
        return goal

class BoardService:
    dao: BoardDAO
    board_participant_dao: BoardParticipantDAO

    def __init__(self, dao: BoardDAO, board_participiant_dao: BoardParticipantDAO):
        self.dao = dao
        self.board_participant_dao = board_participiant_dao

    def update_board_participants(self, user: User, board: Board, participants: List[BoardParticipant]):
        participants_by_id = {p['user'].id: p for p in participants}

        board_participiant = self.board_participant_dao.get_participant(user, board)
        is_owner = board_participiant.role == board_participiant.Role.owner

        old_participants = board.participants

        if is_owner:
            old_participants = board.participants.exclude(user=user)

        for p in old_participants:
            if p.user_id not in participants_by_id:
                self.board_participant_dao.delete_participant(p)
            else:
                if p.role != participants_by_id[p.user_id]['role']:
                    self.board_participant_dao.change_role(p, participants_by_id[p.user_id]['role'])
                
                participants_by_id.pop(p.user_id)

        for p in participants_by_id.values():
            self.board_participant_dao.add_participant(p['user'], board, role=p['role'])