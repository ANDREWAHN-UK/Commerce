from django.contrib import admin
from .models import Product, Customer
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)