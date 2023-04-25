import factory
from core.models import User
from django.contrib.auth.hashers import make_password

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'test'
    _password = 'test'
    
    password = make_password(_password)