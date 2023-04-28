import factory
from core.models import User
from django.contrib.auth.hashers import make_password

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'test@ssss@3434'
    _password = 'test@ssss@3434'
    
    password = make_password(_password)