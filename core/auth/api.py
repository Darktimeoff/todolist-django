from rest_framework.generics import CreateAPIView
from .serializers import SignupSerializer
from core.user import user_dao

class SignupAPI(CreateAPIView):
    serializer_class = SignupSerializer
    queryset = user_dao.get_all()
