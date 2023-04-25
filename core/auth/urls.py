from django.urls import path
from .api import SignupAPI, LoginAPI

urlpatterns = [
    path('signup', SignupAPI.as_view(), name='signup'),
    path('login', LoginAPI.as_view(), name='login')
]