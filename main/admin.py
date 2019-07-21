from django.contrib import admin

from .models import Customer, Driver

admin.site.register(Customer)
admin.site.register(Driver)