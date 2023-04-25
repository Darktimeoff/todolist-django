from django.urls import path
from .api import SignupAPI

urlpatterns = [
    path('signup/', SignupAPI.as_view())
]