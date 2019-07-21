from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.ImageField(upload_to='customer_avatar/', blank=True)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    fip = models.CharField(max_length=10)

    def __str__(self):
        return self.user.get_full_name()


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    avatar = models.ImageField(upload_to='driver_avatar/', blank=True)
    phone = models.CharField(max_length=45, blank=True)
    address = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=150, blank=True)
    fip = models.CharField(max_length=10)

