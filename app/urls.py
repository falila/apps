from django.urls import path, include
from rest_framework import routers

from app import views
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main import views as main_view
from restaurant import views as views_restau
from rest_framework.authtoken import views as rest_auth_views
from restaurant.views import MealViewSet,RestaurantViewSet
from order.views import OrderDetailsViewSet, OrderViewSet
from main.views import CustomerViewSet, DriverViewSet

router = routers.DefaultRouter()
router.register(r'meals', MealViewSet, basename='meal')
router.register(r'restos', RestaurantViewSet, basename='resto')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'customers',CustomerViewSet, basename='customer')
router.register(r'tags', main_view.TagViewSet)
router.register(r'orderDetails', OrderDetailsViewSet, basename='orderdetails')
router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^api-token-auth/', rest_auth_views.obtain_auth_token, name='login'),
    # url(r'^api-token-auth/', custo_auth.as_view(), name='login'),
    url(r'^api/register/', main_view.UserCreate.as_view(), name="register"),
    url(r'^api/v1/', include((router.urls, 'api'),namespace="api")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
