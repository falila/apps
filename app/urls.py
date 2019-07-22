from django.urls import path
from app import views
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main import views as main_view
from rest_framework.authtoken import views as rest_auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^api-token-auth/', rest_auth_views.obtain_auth_token, name='login'),
    url(r'^api/register/', main_view.UserCreate.as_view(), name="register"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
