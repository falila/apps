from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from order.models import Order, OrderDetails
from restaurant.models import Restaurant, Meal
from .models import Customer, Driver, Tag

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    name = serializers.CharField(allow_blank=True, allow_null=True)
    phone = serializers.CharField(allow_blank=True, allow_null=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)
    fip = serializers.CharField(allow_blank=True, allow_null=True, read_only=True)
    account_ref = serializers.CharField(allow_blank=True, allow_null=True, read_only=True)
    bio = serializers.CharField(max_length=500, allow_blank=True)
    avatar = serializers.ImageField(allow_null=True)
    birth_date = serializers.DateField(allow_null=True)
    type = serializers.IntegerField(allow_null=True)
    rank = serializers.IntegerField(default=0, allow_null=True, read_only=True)

    def get_logo(self, profile):
        request = self.context.get('request')
        logo_url = profile.avatar_url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Restaurant
        fields = (
        "id", "name", "phone", "address", "fip", "account_ref", "bio", "avatar", "birth_date", "rank", "type", 'user')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True, max_length=100,
                                   validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(max_length=32, required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())]
                                     )
    profile = ProfileSerializer(source='Profile', required=False)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields
        fields = ("id", "username", "password", "email", "profile")


class RestaurantSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    user = UserSerializer()

    class Meta:
        model = Restaurant
        fields = ("id", "user")


class MealSerializer(serializers.ModelSerializer):
    """
    def get_image(self, meal):
        request = self.context.get('request')
        image_url = meal.image.url
        return request.build_absolute_uri(image_url)
        """

    class Meta:
        model = Meal
        fields = ('id', 'name', 'short_description', 'price')
        read_only_Fields = ('id',)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ("id", "user")


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ("id", "user",)


class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id",)


class OrderMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ("id", "name", "price")


class OrderDetailsSerializer(serializers.ModelSerializer):
    meal = OrderMealSerializer()

    class Meta:
        model = OrderDetails
        fields = ("id", "meal", "quantity", "sub_total")


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    driver = DriverSerializer()
    restaurant = OrderRestaurantSerializer()
    order_details = OrderDetailsSerializer(many=True)
    status = serializers.ReadOnlyField(source="get_status_display")

    class Meta:
        model = Order
        fields = ("id", "customer", "restaurant", "driver", "order_details", "total", "status", "address")


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name',)
        read_only_Fields = ('id',)
