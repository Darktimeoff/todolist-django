from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from . import user_dao
from .serializers import UserUpdateGetSerializer, UpatePasswordSerializer
from django.contrib.auth import logout
from django.http import HttpResponse


class ProfileAPI(RetrieveUpdateDestroyAPIView):
    queryset = user_dao.get_all()
    serializer_class = UserUpdateGetSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        logout(request)

        return  HttpResponse(status=204)


class ChangePasswordAPI(UpdateAPIView):
    serializer_class = UpatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user