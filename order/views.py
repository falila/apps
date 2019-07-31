# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from main.serializers import OrderSerializer, OrderDetailsSerializer
from order.models import Order, OrderDetails


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'restaurant', 'driver', 'status', 'created_at']


class OrderDetailsViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = OrderDetails.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']
