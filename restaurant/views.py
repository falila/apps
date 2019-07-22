from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser

from .models import Meal
from main.models import Driver, Customer
from main.serializers import *


# Create your views here.
def obtain_auth_token(request):
    return redirect(restaurant_home)


@login_required
def restaurant_home(request):
    return redirect(restaurant_order)


@login_required(login_url='/restaurant/sign-in/')
def restaurant_account(request):
    pass


@login_required
def restaurant_meal(request):
    pass


@login_required
def restaurant_add_meal(request):
    pass


@login_required(login_url='/restaurant/sign-in/')
def restaurant_edit_meal(request, meal_id):
    pass


@login_required
@api_view()
def restaurant_order(request):
    pass


@login_required
def restaurant_customer(request):
    pass


class RestaurantViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
