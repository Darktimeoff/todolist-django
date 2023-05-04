from rest_framework import serializers
from .models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from core.serializers import UserUpdateGetSerializer
from .container import goal_service, board_participant_dao, board_service
from core.container import user_dao

CATEGORY_READONLY_FIELDS = ("id", "created", "updated", "user", "is_deleted")

BOARD_READONLY_FIELDS = ('id', 'created', 'updated', 'is_deleted')

class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = BOARD_READONLY_FIELDS
        fields = '__all__'

    
    def create(self, validated_data):
        user  = validated_data.pop("user")
        board = super().create(validated_data)

        board_participant_dao.add_participant(user, board)

        return board
    
BOARD_PARTICIPANT_READONLY_FIELDS = CATEGORY_READONLY_FIELDS
class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True,
        choices=BoardParticipant.Role.choices
    )

    user = serializers.SlugRelatedField(slug_field='username', queryset=user_dao.get_all())

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = BOARD_PARTICIPANT_READONLY_FIELDS

class BoardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participants = BoardParticipantSerializer(many=True)

    class Meta:
        model = Board
        read_only_fields = BOARD_READONLY_FIELDS
        fields = '__all__'

    def update(self, instance, validated_data):
        user = validated_data.pop("user")
        participants = validated_data.pop("participants")
        board  = instance

        board_service.update_board_participants(user, board, participants)

        return super().update(instance, validated_data)
    

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = BOARD_READONLY_FIELDS
        fields = '__all__'
    
    
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = CATEGORY_READONLY_FIELDS
        fields = '__all__'

class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserUpdateGetSerializer(read_only=True)
    board = BoardSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        read_only_fields = CATEGORY_READONLY_FIELDS
        fields = '__all__'

GOAL_READONLY_FIELDS = CATEGORY_READONLY_FIELDS

class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = GOAL_READONLY_FIELDS
        fields = '__all__'

    def validate(self, attrs):
        category: int = attrs.get("category")
        user = attrs.get("user")

        goal_service.validate_category(category, user)
        
        return attrs
    
class GoalSerializer(serializers.ModelSerializer):
    user = UserUpdateGetSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = GOAL_READONLY_FIELDS
        fields = '__all__'

    def validate(self, attrs):
        category: int = attrs.get("category")
        user = self.context['request'].user

        goal_service.validate_category(category, user)
        
        return attrs
    
GOAL_COMMENT_READONLY_FIELDS = CATEGORY_READONLY_FIELDS
class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = GOAL_COMMENT_READONLY_FIELDS
        fields = '__all__'

    def validate(self, attrs):
        goal: int = attrs.get("goal")
        user = self.context['request'].user

        goal_service.validate_comment(goal, user)
        
        return attrs
    
class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserUpdateGetSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = GOAL_READONLY_FIELDS
        fields = '__all__'

    def validate(self, attrs):
        goal: int = attrs.get("goal")
        user = self.context['request'].user

        goal_service.validate_comment(goal, user)
        
        return attrs