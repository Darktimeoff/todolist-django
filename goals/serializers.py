from rest_framework import serializers
from .models import GoalCategory
from core.serializers import UserUpdateGetSerializer

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
    