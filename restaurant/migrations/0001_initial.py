# Generated by Django 2.2.3 on 2019-07-31 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=500)),
                ('phone', models.CharField(blank=True, max_length=25)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('logo', models.ImageField(default='restaurant_logo/pie.jpeg', null=True, upload_to='restaurant_logo/')),
                ('fip', models.CharField(blank=True, max_length=10)),
                ('account_ref', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('short_description', models.CharField(blank=True, max_length=500)),
                ('image', models.ImageField(null=True, upload_to='meal_images/')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurant')),
            ],
        ),
    ]