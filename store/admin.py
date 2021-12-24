from django.contrib import admin
from .models import Product, Customer
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'image',
        'description',
    )


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
