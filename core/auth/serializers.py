from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core.models import User
from core.user import user_dao
from core.classes.exceptions import FormatValidationException
from .message import VALIDATION_PASSWORD_DONT_MATCH, VALIDATION_UNIQUE_USERNAME
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from core.classes.fields import PasswordField


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=user_dao.get_all(), message=VALIDATION_UNIQUE_USERNAME)]
    )
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", 'password_repeat')

    def validate(self, attrs: dict):
        if attrs.get("password") != attrs.get("password_repeat"):
            raise FormatValidationException('password_repeat', VALIDATION_PASSWORD_DONT_MATCH)
        
        return attrs


    def create(self, validated_data):
        del validated_data['password_repeat']

        user: User = super().create(validated_data)
        user.set_password(validated_data["password"])

        user.save()

        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[]
    )
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def create(self, validated_data: dict):
        if not (user := authenticate(
            username=validated_data['username'], 
            password=validated_data['password']
        )):
            raise AuthenticationFailed

        return user