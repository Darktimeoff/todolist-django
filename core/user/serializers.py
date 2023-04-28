from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated
from rest_framework.validators import UniqueValidator
from django.core.validators import validate_email
from core.models import User
from . import user_dao
from .message import VALIDATION_UNIQUE_USERNAME, VALIDATION_OLD_PASSWORD, VALIDAITON_NEW_PASSWORD
from . import user_service
from core.classes.fields import PasswordField
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

