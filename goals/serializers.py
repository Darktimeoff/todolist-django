from rest_framework import serializers
from .models import GoalCategory, Goal
from core.serializers import UserUpdateGetSerializer
from .message import VALIDATION_CATEGORY_OWNER, VALIDATION_NOT_ALLOWED_FOR_DELETED_CATEGORY
from .container import goal_category_dao, goal_service

CATEGORY_READONLY_FIELDS = ("id", "created_at", "updated_at", "user")

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
    category = GoalCategorySerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = GOAL_READONLY_FIELDS
        fields = '__all__'

    def validate(self, attrs):
        category: int = attrs.get("category")
        user = attrs.get("user")

        goal_service.validate_category(category, user)
        
        return attrs