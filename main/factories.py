import uuid

import factory.fuzzy
from django.contrib.auth.models import User
from django.utils import timezone

from order.models import Order
from restaurant.models import Restaurant, Meal
from .models import Customer, Driver, Profile


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver

    lon = factory.Sequence(lambda n: '9854{0}'.format(n))
    lat = factory.Sequence(lambda n: '33695{0}'.format(n))
    location = factory.fuzzy.FuzzyText(length=100)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.fuzzy.FuzzyText(length=15)
    password = factory.fuzzy.FuzzyText(length=10)
    email = factory.Sequence(lambda n: 'falisof@fali{0}.com'.format(n))


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    phone = factory.Sequence(lambda n: '641785425{0}'.format(n))
    address = factory.fuzzy.FuzzyText(length=95)
    fip = factory.Sequence(lambda n: '000dfde{0}'.format(n))
    bio = factory.fuzzy.FuzzyText(length=500)
    birth_date = factory.fuzzy.FuzzyDateTime(start_dt=timezone.now())
    type = factory.fuzzy.FuzzyInteger(low=0, high=4)
    rank = factory.fuzzy.FuzzyInteger(low=0, high=5)
    account_ref = uuid.uuid4()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    restaurant = factory.SubFactory(RestaurantFactory)
    driver = None
    address = factory.fuzzy.FuzzyText(length=89)
    total = factory.fuzzy.FuzzyDecimal(low=1, precision=2)
    status = Order.PLACED
    created_at = factory.fuzzy.FuzzyDateTime(timezone.now())
    picked_at = timezone.now()


class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meal

    restaurant = factory.SubFactory(RestaurantFactory)
    name = factory.fuzzy.FuzzyText(length=12)
    short_description = factory.fuzzy.FuzzyText(length=12)
    image = None
    price = factory.fuzzy.FuzzyDecimal(low=1, precision=2)
