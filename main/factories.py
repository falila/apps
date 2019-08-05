import factory.fuzzy
import uuid
from order.models import Order
from restaurant.models import Restaurant
from .models import Customer, Driver
from django.utils import timezone


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver

    phone = factory.Sequence(lambda n: '641785425{0}'.format(n))
    address = factory.fuzzy.FuzzyText(length=95)
    location = factory.fuzzy.FuzzyText(length=85)
    fip = factory.Sequence(lambda n: '000dfde{0}'.format(n))
    lon = factory.Sequence(lambda n: '9854{0}'.format(n))
    lat = factory.Sequence(lambda n: '33695{0}'.format(n))


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    phone = factory.fuzzy.FuzzyText(length=12)
    address = factory.fuzzy.FuzzyText(length=45)
    fip = factory.Sequence(lambda n: 'fip4d4s{0}'.format(n))


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    phone = factory.fuzzy.FuzzyText(length=10)
    address = factory.fuzzy.FuzzyText(length=45)
    fip = factory.Sequence(lambda n: 'fip4d4s{0}'.format(n))
    account_ref = uuid.uuid4()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    restaurant = factory.SubFactory(RestaurantFactory)
    driver = None
    address = factory.fuzzy.FuzzyText(length=89)
    total = factory.fuzzy.FuzzyDecimal(low=56, precision=2, high=456333)
    status = Order.PLACED
    created_at = factory.fuzzy.FuzzyDateTime(timezone.now())
    picked_at = ''
