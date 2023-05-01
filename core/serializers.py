from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.validators import UniqueValidator
from django.core.validators import validate_email
from core.models import User
from .container import user_dao
from .message import VALIDATION_UNIQUE_USERNAME, VALIDATION_OLD_PASSWORD, VALIDAITON_NEW_PASSWORD, VALIDATION_PASSWORD_DONT_MATCH
from core.classes.fields import PasswordField
from django.contrib.auth import authenticate
from core.classes.exceptions import FormatValidationException

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

class UserUpdateGetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=user_dao.get_all(), message=VALIDATION_UNIQUE_USERNAME)],
        required=False
    )

    email = serializers.EmailField(validators=[validate_email])
 
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
    

class UpatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    old_password = PasswordField(
        required=True
    )

    new_password = PasswordField(
        required=True
    )

    def validate(self, attrs):
        if not (user := attrs['user']):
            raise NotAuthenticated
        
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({'new_password':[VALIDAITON_NEW_PASSWORD]})
        
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({'old_password':[VALIDATION_OLD_PASSWORD]})
        
        return attrs

    def create(self, validated_data: dict):
        raise NotImplementedError

    def update(self, instance: User, validated_data: dict):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance

