from django.utils import timezone

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from main.factories import DriverFactory, CustomerFactory, RestaurantFactory
from main.models import Customer, Driver
from order.models import Order
from restaurant.models import Restaurant


class DriverTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser12', 'test@example12.com', 'testpassword')
        self.test_user2 = User.objects.create_user('testuser02', 'test@example.com', 'testpassword')

        Token.objects.create(user=self.test_user)
        Token.objects.create(user=self.test_user2)
        token = Token.objects.get(user__username='testuser12')

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        RestaurantFactory()
        CustomerFactory()
        DriverFactory()
        self.test_customer = Customer.objects.all().first()
        self.test_driver = Driver.objects.all().first()
        self.test_resto = Restaurant.objects.all().first()
        # create an order
        self.test_order = Order.objects.create(customer=self.test_customer, restaurant=self.test_resto,
                                               address="78 bvd lakeshore", status=Order.ONTHEWAY)
        self.test_driver.user = self.test_user
        self.test_driver.save()

    def test_get_all_driver_restricted_to_admin(self):
        response = self.client.get(reverse("api:driver-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_driver_detail(self):
        response = self.client.get(reverse("api:driver-list"), data={'id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_driver_complete_orders_no_matching_order_found(self):
        """The driver cant complete an fake order."""
        self.test_driver.user = None
        response = self.client.post(reverse("api:driver-driver-complete-orders"), data={"order_id": 12})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_driver_get_latest_orders(self):
        """ Getting the latest order."""
        order = Order.objects.create(customer=self.test_customer, restaurant=self.test_resto,
                                     address="78 bvd lakeshore", status=Order.DELIVERED)

        order.driver = self.test_driver
        order.picked_at = timezone.now()
        order.save()

        response = self.client.get(reverse("api:driver-driver-get-latest-orders"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)

    def test_driver_get_latest_orders_(self):
        response = self.client.get(reverse("api:driver-driver-get-latest-orders"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_test_complete_orders_success(self):
        self.assertIsNotNone(self.test_driver.user)
        self.test_order.driver = self.test_driver
        self.test_order.save()

        response = self.client.post(reverse("api:driver-driver-complete-orders"), data={"order_id": self.test_order.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_driver_picked_order_already_assignTo(self):
        """ A driver can picked more than one order at the same time."""
        order = Order.objects.create(customer=self.test_customer, restaurant=self.test_resto,
                                     address="78 bvd lakeshore", status=Order.READY)

        order.driver = self.test_driver
        order.save()

        response = self.client.post(reverse("api:driver-driver-pick-orders"), data={"order_id": order.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_driver_picked_order_No_driver_assignTo(self):
        """ An order can be picked up when its status shows ready"""
        order = Order.objects.create(customer=self.test_customer, restaurant=self.test_resto,
                                     address="78 bvd lakeshore", status=Order.READY)

        order.driver = None
        order.save()

        response = self.client.post(reverse("api:driver-driver-pick-orders"), data={"order_id": order.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
