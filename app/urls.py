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
    # url(r'^api/', include(restaurant.urls)),
    url(r'^api/v1/restaurant/sign-in/$', rest_auth_views.obtain_auth_token, name='restaurant-sign-in'),
    url(r'^api/v1/restaurant/sign-out', views_restau.logout, {'next_page': '/'}, name='restaurant-sign-out'),
    # url(r'^restaurant/sign-up', views_restau.restaurant_sign_up, name='restaurant-sign-up'),
    url(r'^api/v1/restaurants/$', views_restau.restaurant_home, name='restaurant-home'),
    url(r'^api/v1/restaurants/account/$', views_restau.restaurant_account, name='restaurant-account'),
    url(r'^api/v1/restaurants/(?P<restaurant_id>\d+)/meals/$', views_restau.restaurant_meal, name='restaurant-meal'),
    url(r'^api/v1/restaurants/meals/add/$', views_restau.restaurant_add_meal, name='restaurant-add-meal'),
    url(r'^api/v1/restaurants/(?P<restaurant_id>\d+)/meals/edit/(?P<meal_id>\d+)/$', views_restau.restaurant_edit_meal,
    name='restaurant-edit-meal'),
    url(r'^api/v1/restaurants/order/$', views_restau.restaurant_order, name='restaurant-order'),
    url(r'^api/v1/restaurants/customer/(?P<restaurant_id>\d+)/$', views_restau.restaurant_customer,
    name='restaurant-customer'),
    url(r'^api/v1/', include((router.urls, 'api'),namespace="api")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
