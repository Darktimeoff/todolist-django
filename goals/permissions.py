from rest_framework.permissions import BasePermission, SAFE_METHODS
from .container import board_participant_dao
from .models import Board, GoalCategory, Goal, GoalComment
class BoardPermissions(BasePermission):
    message = "You are not allowed to modify a board"

    def has_object_permission(self, request, view, obj: Board):
        if not request.user.is_authenticated:
            return False
        
        participant = board_participant_dao.get_participant(request.user, obj)

        if not participant:
            return False
        
        if request.method in SAFE_METHODS:
            return  True
       
        return participant.role == participant.Role.owner
    
class CategoryPermissions(BasePermission):
    message = "You are not allowed to modify a category"

    def has_object_permission(self, request, view, obj: GoalCategory):
        if not request.user.is_authenticated:
            return False
        
        participant = board_participant_dao.get_participant(request.user, obj.board)

        if not participant:
            return False
        
        if request.method in SAFE_METHODS:
            return  True
       
        return participant.role in [participant.Role.owner, participant.Role.writer]
    
class CategoryCreatePermissions(BasePermission):
    message = "You are not allowed to create a category"

    def has_object_permission(self, request, view, obj: GoalCategory):
        if not request.user.is_authenticated:
            return False
        
        participant = board_participant_dao.get_participant(request.user, obj.board)

        if not participant:
            return False
        
        if request.method in SAFE_METHODS:
            return  True
       
        return participant.role == participant.Role.owner
    
class GoalPermissions(BasePermission):
    message = "You are not allowed to modify a goal"

    def has_object_permission(self, request, view, obj: Goal):
        if not request.user.is_authenticated:
            return False
        
        participant = board_participant_dao.get_participant(request.user, obj.category.board)

        if not participant:
            return False
        
        if request.method in SAFE_METHODS:
            return  True
       
        return participant.role in [participant.Role.owner, participant.Role.writer]
    
class CommentCreatePermissions(BasePermission):
    message = "You are not allowed to create a comment"

    def has_object_permission(self, request, view, obj: GoalComment):
        if not request.user.is_authenticated:
            return False
        
        participant = board_participant_dao.get_participant(request.user, obj.goal.category.board)

        if not participant:
            return False
        
        if request.method in SAFE_METHODS:
            return  True
       
        return participant.role in [participant.Role.owner, participant.Role.writer]