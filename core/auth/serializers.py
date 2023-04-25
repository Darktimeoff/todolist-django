from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core.models import User
from django.contrib.auth.password_validation import validate_password
from core.user import user_dao
from core.classes.exceptions import FormatValidationException
from .message import VALIDATION_PASSWORD_DONT_MATCH, VALIDATION_REQUIRED_FIELD, VALIDATION_UNIQUE_USERNAME
from django.core.exceptions import ValidationError

class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=user_dao.get_all(), message=VALIDATION_UNIQUE_USERNAME)]
    )
    password_repeat = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password", "password_repeat"]

    def is_valid(self, *, raise_exception=False):
        if 'password_repeat' not in self.initial_data:
            raise FormatValidationException('password_repeat', VALIDATION_REQUIRED_FIELD)
        
        result = super().is_valid(raise_exception=raise_exception)

        password = self.initial_data.get("password")
     
        password_repeat = self.initial_data.get("password_repeat")
       
        if password !=  password_repeat:
            raise FormatValidationException('password_repeat', VALIDATION_PASSWORD_DONT_MATCH)
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise FormatValidationException('password', list(e))

    
        return result
    
    def get_password_repeat(self, *args, **kwargs):
        return self._password_repeat

    def create(self, validated_data):
        user: User = super().create(validated_data)
        user.set_password(validated_data["password"])

        user.save()

        self._password_repeat = user.password

        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
    