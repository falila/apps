import uuid

from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant', null= True)
    name = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    address = models.CharField(max_length=500, blank=True)
    logo = models.ImageField(upload_to='restaurant_logo/', default='restaurant_logo/pie.jpeg',null=True)
    fip = models.CharField(max_length=10, blank=True)  # field identification point
    account_ref = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url


class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='meal_images/', null=True)
    price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


