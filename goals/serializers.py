from rest_framework import serializers
from .models import GoalCategory, Goal, GoalComment
from core.serializers import UserUpdateGetSerializer
from .container import goal_service

CATEGORY_READONLY_FIELDS = ("id", "created", "updated", "user", "is_deleted")

class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = CATEGORY_READONLY_FIELDS
        fields = '__all__'

class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserUpdateGetSerializer(read_only=True)

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