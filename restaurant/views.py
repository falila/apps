from datetime import timedelta

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.models import AccessToken
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.serializers import *
from .models import Meal


# Create your views here.
def obtain_auth_token(self, request):
    return redirect(self.restaurant_home)


@action(detail=False, methods=['get'])
def restaurant_home(request):
    return redirect(restaurant_order)


@api_view(['GET'])
def restaurant_account(request):
    user = request.user

    restaurant = user.restaurant
    serializer = RestaurantSerializer().to_representation(instance=restaurant)
    return Response(status=status.HTTP_200_OK, data=dict(serializer))


@api_view(['GET', 'POST'])
def restaurant_meal(request):
    if request.method == 'POST':
        # cree meal
        incoming_data = MealSerializer(data=request.POST)
        if incoming_data.is_valid():
            meal = incoming_data.save()
            return Response(status=status.HTTP_200_OK, data=meal)
    if request.method == 'GET':
        # return meal
        pass

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def restaurant_add_meal(request, restaurant_id=None, meal_id=None):
    incoming_data = MealSerializer(data=request.POST)
    if incoming_data.is_valid():
        meal = incoming_data.save()
        return Response(status=status.HTTP_200_OK, data=meal)


@api_view(['GET', 'POST'])
def restaurant_edit_meal(request, restaurant_id=None, meal_id=None):
    pass


@api_view()
def restaurant_order(request):
    pass


@action(detail=False, methods=['post', 'get'])
def restaurant_customer(self, request):
    pass


@action(detail=False, methods=['get'])
def restaurant_order_notification(request, last_request_time):
    notification = Order.objects.filter(restaurant=request.user.restaurant,
                                        created_at__gt=last_request_time).count()

    return JsonResponse({"notification": notification})


@action(detail=False, methods=['get'])
def logout(self, request):
    access_token = AccessToken.objects.get(token=request.POST.get("access_token"),
                                           expires__gt=timezone.now()).delete()
    logout(request)




class MealViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant', 'short_description']

    def get_queryset(self):
        queryset = Meal.objects.all()
        rest_id = self.request.query_params.get('restaurant_id', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant_id=rest_id)
        return queryset

    def perform_create(self, serializer):
        """Create a new meal"""
        # if self.request.user.restaurant and self.request.user.restaurant != None:
        #   serializer.save(restaurant=self.request.user.restaurant)
        serializer.save()


class RestaurantViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Restaurant.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'fip', 'account_ref']

    def perform_create(self, serializer):
        """Create a new meal"""
        if self.request.user.is_staff:
            serializer.save()
