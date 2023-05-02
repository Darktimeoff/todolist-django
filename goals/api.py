from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .container import goal_category_dao, goal_comment_dao, goal_dao
from .filters import GoalDateFilter
from .serializers import (GoalCategoryCreateSerializer, GoalCategorySerializer,
                          GoalCommentCreateSerializer, GoalCommentSerializer,
                          GoalCreateSerializer, GoalSerializer)


class CategoryCreateAPI(CreateAPIView):
    queryset = goal_category_dao.get_all()
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [IsAuthenticated]


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
        # type: ignore
        return goal_category_dao.get_all_by_user(self.request.user)


class CategoryAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = goal_category_dao.get_all()

    def get_queryset(self):
        return goal_category_dao.get_all_by_user(self.request.user)


class GoalCreateAPI(CreateAPIView):
    queryset = goal_dao.get_all()
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    queryset = goal_dao.get_all()

    def get_queryset(self):
        return goal_dao.get_all_by_user(self.request.user)


class GoalListAPI(ListAPIView):
    queryset = goal_dao.get_all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_class = GoalDateFilter
    search_fields = ('title', 'description',)
    ordering_fields = ('due_date', 'priority', )
    ordering = ('priority', 'due_date', )

    def get_queryset(self):
        return goal_dao.get_all_by_user(self.request.user)  # type: ignore


class GoalCommentCreateAPI(CreateAPIView):
    queryset = goal_comment_dao.get_all()
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalListCommentAPI(ListAPIView):
    queryset = goal_comment_dao.get_all()
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ('goal',)
    ordering_fields = ('id', )
    ordering = "-id"

    def get_queryset(self):
        # type: ignore
        return goal_comment_dao.get_all_by_user(self.request.user)


class GoalCommentAPI(RetrieveUpdateDestroyAPIView):
    queryset = goal_comment_dao.get_all()
    serializer_class = GoalCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # type: ignore
        return goal_comment_dao.get_all_by_user(self.request.user)
