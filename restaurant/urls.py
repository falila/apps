from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from restaurant import views as views_restau

router = DefaultRouter()

router.register('restaurants', views_restau.RestaurantViewSet)
# Restaurant
urlpatterns = [
    url(r'^restaurant/sign-in/$', auth_views.login, name='restaurant-sign-in'),
    url(r'^restaurant/sign-out', auth_views.logout, {'next_page': '/'}, name='restaurant-sign-out'),
    url(r'^restaurant/sign-up', views_restau.restaurant_sign_up, name='restaurant-sign-up'),
    url(r'^restaurant/$', views_restau.restaurant_home, name='restaurant-home'),
    url(r'^restaurant/account/$', views_restau.restaurant_account, name='restaurant-account'),
    url(r'^restaurant/meal/$', views_restau.restaurant_meal, name='restaurant-meal'),
    url(r'^restaurant/meal/add/$', views_restau.restaurant_add_meal, name='restaurant-add-meal'),
    url(r'^restaurant/meal/edit/(?P<meal_id>\d+)/$', views_restau.restaurant_edit_meal, name='restaurant-edit-meal'),
    url(r'^restaurant/order/$', views_restau.restaurant_order, name='restaurant-order'),
    url(r'^restaurant/customer/(?P<restaurant_id>\d+)/$', views_restau.restaurant_customer, name='restaurant-customer'),
    url(r'^restaurant/report/$', views_restau.restaurant_report, name='restaurant-report'),
]
