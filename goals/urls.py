from django.urls import path
from .api import CategoryCreateAPI, CategoryListAPI,GoalCreateAPI, GoalListAPI, GoalAPI

category = [
    path('goal_category/create', CategoryCreateAPI.as_view(), name='goal_category_create'),
    path('goal_category/list', CategoryListAPI.as_view(), name='goal_category_list'),
    path('goal_category/<int:pk>', CategoryListAPI.as_view(), name='goal_category'),
]

goal = [
    path('goal/create', GoalCreateAPI.as_view(), name='goal_create'),
    path('goal/list', GoalListAPI.as_view(), name='goal_list'),
    path('goal/<int:pk>', GoalAPI.as_view(), name='goal'),
]

urlpatterns = category + goal