from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.models import AccessToken
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main import serializers
from main.models import Tag, Driver, Customer
from main.serializers import UserSerializer


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
            'email': user.email
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
    """Manage tags in the database"""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Driver.objects.all()
    serializer_class = serializers.DriverSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'phone', 'fip', 'user']

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.order_by('-name')


class CustomerViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin):
    """Manage tags in the database"""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'phone', 'fip', 'user']

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.order_by('-name')
