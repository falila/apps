from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from main.serializers import MealSerializer
from restaurant.models import Meal, Restaurant

MEALS_URL = reverse('api:meal-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publically available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(MEALS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test meal can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        restaurant = Restaurant(name="TimeH", user=self.user,
                                address="kingstone road",
                                phone="478512dfds")
        restaurant.save()
        self.assertEqual(len(Restaurant.objects.all()), 1)

    def tearDown(self):
        self.user.delete()

    def test_retrieve_restau_list(self):
        """Test retrieving a list of meals"""
        self.assertEqual(len(Restaurant.objects.all()), 1)
        Meal.objects.create(name='Gombo', short_description="Plat Gombo")
        Meal.objects.create(name='Fried K', short_description="fried kkk")

        res = self.client.get(MEALS_URL)

        meals = Meal.objects.all().order_by('-name').distinct()
        serializer = MealSerializer(meals, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_restau(self):
        pass
    def test_update_restau(self):
        pass
    def test_restau_details(self):
        pass

