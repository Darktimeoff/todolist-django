from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from core.models import User
from . import user_dao
from .message import VALIDATION_UNIQUE_USERNAME, VALIDAITON_NEW_PASSWORD, VALIDAITON_REQUIRED_FIELD
from django.core.exceptions import ValidationError

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
    
class UpatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True
    )

    new_password = serializers.CharField(
        required=True
    )


    def is_valid(self, *, raise_exception=False):
        result = super().is_valid(raise_exception=raise_exception)

        self._old_passord = self.initial_data.get('old_password', None)
        self._new_password = self.initial_data.get('new_password', None)
        
        if not self._old_passord:
            self._errors['old_password'] = [VALIDAITON_REQUIRED_FIELD]
            result = False

        if not self._new_password:
            self._errors['new_password'] = [VALIDAITON_REQUIRED_FIELD]
            result = False

        if  self._old_passord == self._new_password:
            self._errors['new_password'] = [VALIDAITON_NEW_PASSWORD]
            result = False

        try:
            validate_password(self._new_password)
        except ValidationError as e:
            self._errors['new_password'] = list(e)
        
        if raise_exception and not result:
            raise serializers.ValidationError(self.errors)
       
        return result


