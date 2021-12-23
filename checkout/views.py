from django.shortcuts import render
from .models import Order, OrderItem, ShippingAddress

# Create your views here.

def checkout(request):
    context = {}
    return render(request, 'checkout/checkout.html', context)