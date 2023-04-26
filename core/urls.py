from core.auth import urls as auth_urls
from core.user import urls as user_urls

urlpatterns = auth_urls.urlpatterns + user_urls.urlpatterns