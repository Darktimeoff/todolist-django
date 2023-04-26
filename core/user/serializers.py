from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import validate_email
from core.models import User
from . import user_dao
from .message import VALIDATION_UNIQUE_USERNAME


class UserUpdateGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=user_dao.get_all(), message=VALIDATION_UNIQUE_USERNAME)],
        required=False
    )

    email = serializers.EmailField(validators=[validate_email], required=False)

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
    
