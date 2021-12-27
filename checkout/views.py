from django.shortcuts import render
from checkout.models import Order
from .models import *
from store.views import updateItem
import stripe

# Create your views here.

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        # this is because the template will loop through the whole list, so there needs to be something here
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    stripe.api_key = 'sk_test_51K8jexEE3VLVHzWcHSDIRoXnm3cGSze1zo4WDrHeSMwLQjO269ds452ALbYGlliIeTcdqzW7qEc82cOtrKUILdq100uvmXF6cq'

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        customer='{{customer}}',
        currency="usd",
        amount=2000,
        payment_method_types=["card"],
        setup_future_usage="on_session",
        )

    context = {
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        'stripe_public_key':stripe_public_key,
        'client_secret': intent.client_secret,
         }
    return render(request, 'checkout/checkout.html', context)

