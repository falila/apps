from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from restaurant.models import Restaurant


class RestaurantTest(APITestCase):

    def setUp(self):
        self.create_url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'foobar@example.com',
            'password': 'testpassword'
        }

        self.client.post(self.create_url, data, format='json')

        restaurant_data = {
            'name': 'foobar',
            'phone': 'foobarbaz@example.com',
            'address': 'foo',
            'logo': '',
            'fip': 'fip124785'
        }
        # create a new restaurant
        self.test_user = User.objects.filter(username='testuser').first()
        self.restaurant_test = Restaurant.objects.create(**restaurant_data, user=self.test_user)

        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data, format='json')
        access_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
        # self.client.login(username=self.test_user.username, password='testpassword')

    def test_restaurant_home(self):
        """
                Go to restaurant home page.
        """
        self.assertEqual(Restaurant.objects.count(), 1)
        self.restaurant_home_url = reverse('restaurant-home')

        response = self.client.get(self.restaurant_home_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_restaurant_account(self):
        """
                Can acces to a restaurant account info.
        """
        self.assertEqual(Restaurant.objects.count(), 1)
        self.restaurant_account_url = reverse('restaurant-account')

        response = self.client.get(self.restaurant_account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, "foobar")
        print(response.data)

    def test_restaurant_acces_home(self):
        """
                try to  acces to a restaurant account info.
        """
        # self.client.logout()
        self.assertEqual(Restaurant.objects.count(), 1)
        self.restaurant_account_url = reverse('restaurant-account')

        response = self.client.get(self.restaurant_account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_add_meal(self):
        """
             add meal
        """
        self.add_meal = reverse('meal:meal-list')

        data = {
            "name": "meal",
            "short_description": " pizza",
            "price": "7.52",
            "restaurant_id": self.restaurant_test.id
        }

        response = self.client.post(self.add_meal, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
