from django.db import models
from django.contrib.auth.models import User
from store.models import Customer, Product
from django.conf import settings
import decimal
import uuid
# Create your models here.


# Order is the summary of the items, along with a transaction id, more or less means cart
# Foreign key means a customer can have multiple orders
# There can be only one of these per customer, i.e the same order is not shared between customers

class Order(models.Model):
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4

    ORDER_STATUSES = (
        (SUBMITTED, 'Submitted'),
        (PROCESSED, 'Processed'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
    )

    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    order_number = models.CharField(max_length=32, null=False, editable=False, default='111')

    name = models.CharField(max_length=50, null=False, blank=False, default='name')
    email = models.EmailField(max_length=254, null=False, blank=False, default='email')
    address = models.CharField(max_length=80, null=False, blank=False, default='address')
    street = models.CharField(max_length=80, null=False, blank=False, default='street')
    city = models.CharField(max_length=80, null=False, blank=False, default='city')
    county = models.CharField(max_length=80, null=False, blank=True, default='county')
    postcode = models.CharField(max_length=20, null=True, blank=False, default='postcode')
    number = models.CharField(max_length=20, null=False, blank=False, default='number')

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def _generate_order_number(self):
        # UUID to generate a random number    
        return uuid.uuid4().hex.upper()

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()
        return shipping

# get_cart_total tells the project to add up all the $?? for the items in the cart

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
# this will get linked to a customer, so they don't have to fill it in again
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
