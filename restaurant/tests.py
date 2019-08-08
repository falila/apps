from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from main.factories import OrderFactory, MealFactory
from restaurant.models import Restaurant, Meal


class RestaurantTest(APITestCase):

    def setUp(self):
        self.create_url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'foobar@example.com',
            'password': 'testpassword'
        }

        self.client.post(self.create_url, data, format='json')

        restaurant_data = {}
        # create a new restaurant
        self.test_user = User.objects.filter(username='testuser').first()
        self.test_restaurant = Restaurant.objects.create(**restaurant_data)
        self.test_restaurant.user = self.test_user
        self.test_restaurant.save()

        data_login = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data_login, format='json')
        access_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)

    def test_restaurant_add_meal(self):
        """
             add meal
        """
        self.add_meal = reverse('api:meal-list')

        data = {
            "name": "meal",
            "short_description": " pizza",
            "price": "7.52",
        }

        response = self.client.post(self.add_meal, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        meal = Meal.objects.filter(name='meal').first()
        self.assertIsNotNone(meal)

        response = self.client.get(reverse('api:meal-list'))
        self.assertTrue(len(response.content) > 10)

    def test_restaurant_get_meal_by_restaurant(self):
        for cpt in range(10):
            OrderFactory()
            MealFactory()
        count = Meal.objects.all().count()
        response = self.client.get(reverse('api:meal-list'))
        self.assertEqual(len(json.loads(response.content)), count)

        for meal in Meal.objects.all():
            meal.restaurant = self.test_restaurant
            meal.save()

        response = self.client.get(reverse('api:meal-list'), data={"restaurant": self.test_restaurant.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
