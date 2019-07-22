import factory.django

from .models import Customer, Driver
from django.contrib.auth import get_user_model


class DriverFactory(factory.Factory):
    class Meta:
        model = Driver

    phone = factory.Sequence(lambda n: '641785425{0}'.format(n))
    address = factory.Faker('address')
    location = "loaocoait oaiodoiadfodsfdf "
    fip = factory.Sequence(lambda n: '000dfde{0}'.format(n))
    lon = factory.Sequence(lambda n: '9854{0}'.format(n))
    lat = factory.Sequence(lambda n: '33695{0}'.format(n))


class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer

    phone = factory.Faker('phone')
    address = factory.Faker('address')
    location = "jjfaofjfa saifdsof saf"
    fip = factory.Sequence(lambda n: 'fip4d4s{0}'.format(n))
