from django.db import models
from django.contrib.auth.models import User
from store.models import Product, Customer
from django.conf import settings

# Create your models here.


# Order is the summary of the items, along with a transaction id, more or less means cart
# Foreign key means a customer can have multiple orders
# There can be only one of these per customer, i.e the same order is not shared between customers

class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()
        return shipping

# get_cart_total tells the project to add up all the $£ for the items in the cart

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

# get_cart_items tells the project to add up all the cart items, e.g. total items=33
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


# OrderItem translates the Product into the cart/Order.
# So, in the cart/order, there will be order items, which relate to the Products
# Naturally, there can be multiple OrderItems
# get_total calculates its price by the number of instances of itself, e.g. (beefburger*3)*9.99
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

# this tells us where to send the burger.
# this will get connected/linked to a customer, so they don't have to fill it in again
# in the profile, this will be editable (CRUD!)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    county = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
