from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE, null=True)

    def total(self):
        return self.quantity * self.product.price

    def name(self):
        return self.product.name
    
    def price(self):
        return self.product.price

    def augment_quantity(self, quantity):
        self.quantity = self.quantity + int(quantity)
        self.save