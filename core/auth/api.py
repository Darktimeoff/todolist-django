from rest_framework.generics import CreateAPIView
from .serializers import SignupSerializer, LoginSerializer
from core.user import user_dao
from django.contrib.auth import login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

class SignupAPI(CreateAPIView):
    serializer_class = SignupSerializer
    queryset = user_dao.get_all()

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginAPI(CreateAPIView):
    serializer_class = LoginSerializer
    queryset = user_dao.get_all()
    
    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())

      
        
