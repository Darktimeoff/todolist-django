from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from . import user_dao
from .serializers import UserUpdateGetSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.http import HttpResponse
from todolist.settings import SIMPLE_JWT
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserAPI(RetrieveUpdateDestroyAPIView):
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

