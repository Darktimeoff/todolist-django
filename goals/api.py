from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from .container import goal_category_dao
from rest_framework.permissions import IsAuthenticated
from .serializers import GoalCategoryCreateSerializer, GoalCategorySerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django.http import HttpResponse

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CategoryCreateAPI(CreateAPIView):
    queryset = goal_category_dao.get_all()
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [IsAuthenticated]

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CategoryListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = (
        OrderingFilter,
        SearchFilter,
    )
    serializer_class = GoalCategorySerializer
    queryset = goal_category_dao.get_all()
    ordering_fields = ('title', "created_at",)
    search_fields = ('title',)

    def get_queryset(self):
        return goal_category_dao.get_all_by_user(self.request.user) # type: ignore
    
class CategoryAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = goal_category_dao.get_all()

    def get_queryset(self):
        return goal_category_dao.get_all_by_user(self.request.user)
    
    def perform_destroy(self, instance):
        instance = goal_category_dao.delete(instance)

        return instance