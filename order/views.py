# Create your views here.
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import mixins, status
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if self.request.user.customer:
                customer = self.request.user.customer
                # Check whether customer has any order that is not delivered
                if Order.objects.filter(customer=customer).exclude(status=Order.DELIVERED):
                    return JsonResponse({"status": "failed", "error": "Your last order must be completed."})
        except Exception as e:
            return JsonResponse({"status": "failed", "error": "Only a customer can submit an order."})

        self.perform_create(serializer)
        headers = self.getget_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)
