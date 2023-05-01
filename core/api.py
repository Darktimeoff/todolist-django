from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .container import user_dao
from .serializers import UserUpdateGetSerializer, UpatePasswordSerializer, SignupSerializer, LoginSerializer
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import login

class SignupAPI(CreateAPIView):
    serializer_class = SignupSerializer
    queryset = user_dao.get_all()


class LoginAPI(CreateAPIView):
    serializer_class = LoginSerializer
    queryset = user_dao.get_all()
    
    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())

      


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