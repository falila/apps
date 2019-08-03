from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', null=True)
    name = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='customer_avatar/', blank=True)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    fip = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver', null=True)
    name = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='driver_avatar/', blank=True)
    phone = models.CharField(max_length=45, blank=True)
    address = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=150, blank=True)
    fip = models.CharField(max_length=10, blank=True)
    lon = models.FloatField(blank=True, default=0)
    lat = models.FloatField(blank=True, default=0)


class Tag(models.Model):
    """Tag to be used """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
