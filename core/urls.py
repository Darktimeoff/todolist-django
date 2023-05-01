from django.urls import path
from .api import ProfileAPI, ChangePasswordAPI, SignupAPI, LoginAPI

user_urls = [
    path('profile', ProfileAPI.as_view(), name='profile'),
    path('update_password', ChangePasswordAPI.as_view(), name='update_password')
]

auth_urls = [
     path('signup', SignupAPI.as_view(), name='signup'),
    path('login', LoginAPI.as_view(), name='login')
]

urlpatterns = auth_urls + user_urls