from django.http import JsonResponse, HttpResponse, HttpRequest
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer
from core.user import user_dao
from django.contrib.auth import authenticate
from .message import VALIDATION_LOGIN
import json
from todolist import settings
from django.middleware import csrf

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignupAPI(CreateAPIView):
    serializer_class = SignupSerializer
    queryset = user_dao.get_all()

class LoginAPI(APIView):
    def post(self, request: HttpRequest):
       
        data = json.loads(request.body)

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password, request=request)

        if user is None:
            return JsonResponse({
                "username": [VALIDATION_LOGIN],
                "password": [VALIDATION_LOGIN]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        tokens_data = get_tokens_for_user(user)

        response: HttpResponse = JsonResponse(LoginSerializer(user).data, status=status.HTTP_200_OK)

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens_data['access'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )

        csrf.get_token(request)
        
        return response

      
        
