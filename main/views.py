from datetime import timedelta

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from oauth2_provider.models import AccessToken
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from main import serializers
from main.models import Tag, Driver, Customer, Profile
from main.serializers import UserSerializer, OrderSerializer
from order.models import Order


def index(request):
    return JsonResponse({"home": "welcome"})


class UserCreate(APIView):
    """
    Create the user
    """
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                if user:
                    access_token = Token.objects.create(user=user)
                    # from datetime import datetime, timedelta

                    # exp = timezone.now() + timedelta(hours=24)
                    # access_token = AccessToken.objects.create(user=user, expires=exp)
                    json = serializer.data
                    json['token'] = access_token.key
                    return Response(json, status=status.HTTP_201_CREATED)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = AccessToken.objects.get_or_create(user=user)
        return Response({
            'token': token.token,
            'user_id': user.pk,
            'email': user.email,
            'profile': user.profile.id
        })


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class DriverViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    # authentication_classes = (TokenAuthentication,)
    queryset = Driver.objects.all()
    serializer_class = serializers.DriverSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_permissions(self):

        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsAuthenticatedOrTokenHasScope]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.order_by('-id')

    # POST params: access_token, order_id
    @action(detail=False, methods=['post'])
    def driver_pick_orders(self, request):
        if request.method == "POST":
            # Get token
            if request.user:
                driver = request.user.driver

            # Check if the driver can only pick up one order at the same timezone
            if Order.objects.filter(driver=driver).exclude(status=Order.ONTHEWAY):
                return JsonResponse({"status": "failed", "error": "You can only pick up one order at a time."},
                                    status=status.HTTP_400_BAD_REQUEST)

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
    @action(detail=False, methods=['get'])
    def driver_get_latest_orders(self, request):
        if request.method == "GET" and request.user:
            try:
                driver = request.user.driver
                if not driver:
                    raise Exception
                order = OrderSerializer(
                    Order.objects.filter(driver=driver).order_by("picked_at").last()
                ).data
            except Exception as e:
                return JsonResponse({"status": "failed", "error": e.args},
                                    status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"order": order})

    # POST params: access_token, order_id
    @action(detail=False, methods=['post'])
    def driver_complete_orders(self, request):
        if request.method == "POST" and request.user:
            try:
                driver = request.user.driver
                if not driver:
                    raise Exception
            except Exception as e:
                return JsonResponse({"status": "failed", "error": "No driver found."},
                                    status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=request.POST["order_id"], driver=driver)
            order.status = order.DELIVERED
            order.save()
        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "No order found."},
                                status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"status": "success"})

    # GET params: access_token
    @action(detail=False, methods=['get'])
    def driver_get_revenue(self, request):
        if request.user:
            try:
                driver = request.user.driver
                if not driver:
                    raise Exception
            except Exception as e:
                return JsonResponse({"status": "failed", "error": "No driver found."},
                                    status=status.HTTP_400_BAD_REQUEST)
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
    @action(detail=False, methods=['post'])
    def driver_update_location(self, request):
        if request.method == "POST":
            try:
                driver = request.user.driver
                if not driver:
                    raise Exception
            except Exception as e:
                return JsonResponse({"status": "failed", "error": "No driver found."},
                                    status=status.HTTP_400_BAD_REQUEST)

            # SET location string => database
            driver.location = request.POST["location"]
            driver.save()
            return JsonResponse({"status": "success"})

    @action(detail=False, methods=['get'])
    def get_ready_orders(self, request):
        order = OrderSerializer(
            Order.objects.filter(status=Order.READY, driver=None).order_by("-id"),
            many=True).data
        return JsonResponse({"orders": order})


class CustomerViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin):
    """Manage  customers."""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', ]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.order_by('-id')

    @action(detail=False, methods=['get'])
    def latest_order(self, request):
        customer = self.request.user.customer
        order = OrderSerializer(Order.objects.filter(customer=customer).last()).data

        return JsonResponse({"order": order})

    @action(detail=True, methods=['get'])
    def driver_location(self, request):
        customer = self.request.user.customer
        # Get drivers location realted to this customer current order
        current_order = Order.objects.filter(customer=customer, status=Order.ONTHEWAY).last()
        location = current_order.driver.location

        return JsonResponse({"location": location})


class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    """Manage  customers."""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'phone', 'fip', 'user', 'type', 'account_ref', 'rank']
