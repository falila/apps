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


@action(detail=False, methods=['get'])
def driver_get_ready_orders(self, request):
    order = OrderSerializer(
        Order.objects.filter(status=Order.READY, driver=None).order_by("-id"),
        many=True).data
    return JsonResponse({"orders": order})


@csrf_exempt
# POST params: access_token, order_id
@action(detail=False, methods=['post'])
def driver_pick_orders(request):
    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token=request.POST.get("access_token"),
                                               expires__gt=timezone.now())

        # Get Driver based on token
        driver = access_token.user.driver

        # Check if the driver can only pick up one order at the same timezone
        if Order.objects.filter(driver=driver).exclude(status=Order.ONTHEWAY):
            return JsonResponse({"status": "failed", "error": "You can only pick up one order at a time."})

        try:
            order = Order.objects.get(
                id=request.POST["order_id"],
                driver=None,
                status=Order.READY

            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another driver."})


# GET params: access_token
@action(detail=False, methods=['post'])
def driver_get_latest_orders(self, request):
    access_token = AccessToken.objects.get(token=request.GET.get("access_token"),
                                           expires__gt=timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.get.filter(driver=driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})


# GET params: access_token
@action(detail=False, methods=['get'])
def driver_get_latest_orders(self, request):
    access_token = AccessToken.objects.get(token=request.GET.get("access_token"),
                                           expires__gt=timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.get.filter(driver=driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})


# POST params: access_token, order_id
@action(detail=False, methods=['post'])
def driver_complete_orders(self, request):
    access_token = AccessToken.objects.get(token=request.POST.get("access_token"),
                                           expires__gt=timezone.now())

    driver = access_token.user.driver
    order = Order.objects.get(id=request.POST["order_id"], driver=driver)
    order.status = order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})


# GET params: access_token
@action(detail=False, methods=['get'])
def driver_get_revenue(self, request):
    access_token = AccessToken.objects.get(token=request.GET.get("access_token"),
                                           expires__gt=timezone.now())

    driver = access_token.user.driver

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver=driver,
            status=Order.DELIVERED,
            created_at__year=day.year,
            created_at__month=day.month,
            created_at__day=day.day
        )

        revenue[day.strtime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})


# POST params: access_token, "lat, long"
@csrf_exempt
@action(detail=False, methods=['post'])
def driver_update_location(self, request):
    if request.method == "POST":
        access_token = AccessToken.objects.get(token=request.POST.get("access_token"),
                                               expires__gt=timezone.now())

        driver = access_token.user.driver

        # SET location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})


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
