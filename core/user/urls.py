from django.urls import path
from .api import UserAPI

urlpatterns = [
    path('profile', UserAPI.as_view()),
]
