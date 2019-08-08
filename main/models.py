import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', null=True)


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver', null=True)
    lon = models.FloatField(default=0, blank=True)
    lat = models.FloatField(default=0, blank=True)
    location = models.TextField(max_length=100, blank=True)


class Tag(models.Model):
    """Tag to be used """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Profile(models.Model):
    customer = 0
    driver = 1
    restaurant = 2
    anonymous = 3

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='profile_avatar/', blank=True)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    fip = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    type = models.IntegerField(blank=True, default=anonymous)
    account_ref = models.UUIDField(default=uuid.uuid4, editable=True, blank=True)
    rank = models.IntegerField(default=0, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
