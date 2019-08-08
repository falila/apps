from django.contrib.auth import logout
from django.db.models import Sum, Count, Case, When
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.serializers import *
from .models import Meal


class RestaurantViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Restaurant.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def perform_create(self, serializer):
        """Create a new meal"""
        if self.request.user:
            serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def order(self, request):
        pass

    @action(detail=False, methods=['get'])
    def customer(self, request):
        pass

    @action(detail=False, methods=['get'])
    def order_notification(request, last_request_time):
        notification = Order.objects.filter(restaurant=request.user.restaurant,
                                            created_at__gt=last_request_time).count()

        return JsonResponse({"notification": notification})

    @action(detail=False, methods=['get'])
    def report(request):
        # Calculate revenue and number of orders by current week
        from datetime import datetime, timedelta

        revenue = []
        orders = []

        # Calculate weekdays
        today = datetime.now()
        current_weekdays = [today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]

        for day in current_weekdays:
            delivered_orders = Order.objects.filter(
                restaurant=request.user.restaurant,
                status=Order.DELIVERED,
                created_at__year=day.year,
                created_at__month=day.month,
                created_at__day=day.day
            )
            revenue.append(sum(order.total for order in delivered_orders))
            orders.append(delivered_orders.count())

        # Top 3 Meals
        top3_meals = Meal.objects.filter(restaurant=request.user.restaurant).annotate(
            total_order=Sum('orderdetails__quantity')).order_by("-total_order")[:3]

        meal = {
            "labels": [meal.name for meal in top3_meals],
            "data": [meal.total_order or 0 for meal in top3_meals]
        }

        # Top 3 DRIVERS
        top3_drivers = Driver.objects.annotate(
            total_order=Count(
                Case(
                    When(order__restaurant=request.user.restaurant, then=1)
                )
            )
        ).order_by("-total_order")[:3]

        driver = {
            "labels": [driver.user.get_full_name() for driver in top3_drivers],
            "data": [driver.total_order for driver in top3_drivers]
        }

        return Response(data={'revenue': revenue, 'orders': orders, 'meal': meal, 'driver': driver},
                        status=status.HTTP_200_OK)


@action(detail=False, methods=['get'])
def logout(self, request):
    logout(request)


class MealViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant', 'id', 'name']

    def get_queryset(self):
        queryset = Meal.objects.all()
        rest_id = self.request.query_params.get('restaurant', None)
        if rest_id is not None:
            queryset = queryset.filter(restaurant_id=rest_id)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.restaurant:
            serializer.save(restaurant=self.request.user.restaurant)
