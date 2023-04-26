from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import user_dao, user_service
from .serializers import UserUpdateGetSerializer, UpatePasswordSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from todolist.settings import SIMPLE_JWT

@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProfileAPI(RetrieveUpdateDestroyAPIView):
    queryset = user_dao.get_all()
    serializer_class = UserUpdateGetSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.request.user.pk
        return user_dao.get_by_id(id)
    
    def delete(self, request):
        logout(request)
        response: HttpResponse = HttpResponse(status=204)
        response.delete_cookie(SIMPLE_JWT['AUTH_COOKIE'])

        return response

@method_decorator(ensure_csrf_cookie, name='dispatch')
class ChangePasswordAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.request.user.pk
        return user_dao.get_by_id(id)
    
    def change_password(self, request, *args, **kwargs):
        serializer = UpatePasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        
        id = self.request.user.pk

        user_service.change_password(id, **serializer.data)

        return JsonResponse(serializer.data)
    
    def put(self, request, *args, **kwargs):
        return self.change_password(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.change_password(request, *args, **kwargs)