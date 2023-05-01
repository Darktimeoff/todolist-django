from django.urls import path
from .api import CategoryCreateAPI, CategoryListAPI

urlpatterns = [
    path('goal_category/create', CategoryCreateAPI.as_view(), name='goal_category_create'),
    path('goal_category/list', CategoryListAPI.as_view(), name='goal_category_list'),
    path('goal_category/<int:pk>', CategoryListAPI.as_view(), name='goal_category'),
]
