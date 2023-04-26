from django.urls import path
from .api import ProfileAPI, ChangePasswordAPI

urlpatterns = [
    path('profile', ProfileAPI.as_view()),
    path('update_password', ChangePasswordAPI.as_view()),
]
