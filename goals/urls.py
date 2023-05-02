from django.urls import path

from .api import (CategoryAPI, CategoryCreateAPI, CategoryListAPI, GoalAPI,
                  GoalCommentAPI, GoalCommentCreateAPI, GoalCreateAPI,
                  GoalListAPI, GoalListCommentAPI)

category = [
    path('goal_category/create', CategoryCreateAPI.as_view(), name='goal_category_create'),
    path('goal_category/list', CategoryListAPI.as_view(), name='goal_category_list'),
    path('goal_category/<int:pk>', CategoryAPI.as_view(), name='goal_category'),
]

goal = [
    path('goal/create', GoalCreateAPI.as_view(), name='goal_create'),
    path('goal/list', GoalListAPI.as_view(), name='goal_list'),
    path('goal/<int:pk>', GoalAPI.as_view(), name='goal'),
]

comment = [
    path('goal_comment/create', GoalCommentCreateAPI.as_view(), name='comment_create'),
    path('goal_comment/list', GoalListCommentAPI.as_view(), name='comment_list'),
    path('goal_comment/<int:pk>', GoalCommentAPI.as_view(), name='comment'),
]

urlpatterns = category + goal + comment