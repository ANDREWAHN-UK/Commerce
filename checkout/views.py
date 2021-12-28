from django.shortcuts import render
from checkout.models import Order
from .models import *
from store.views import updateItem
import stripe
from bestburger import settings
import datetime
import json
from django.http import JsonResponse

# Create your views here.

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        # this is because the template will loop through the whole list,
        #  so there needs to be something here
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    stripe.api_key = 'sk_test_51K8jexEE3VLVHzWcHSDIRoXnm3cGSze1zo4WDrHeSMwLQjO269ds452ALbYGlliIeTcdqzW7qEc82cOtrKUILdq100uvmXF6cq'

    # public key needs to be displayed here so stripe_elements can access it
    stripe_public_key = 'pk_test_51K8jexEE3VLVHzWc8ckIVJpmSWAhlhOnT7nz8ioOry3z0atx9lyoXk3K2njUw23ZsTs21nofTig1QnoY31ni4H0s00njCJPUBc'
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    # the'amount' variable  is also displayed in the cart and checkout apps
    # it needs to be a number like 1234 instead of 12.34, for stripe reasons
    amount = round(order.get_cart_total*100)

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=settings.STRIPE_CURRENCY,
        payment_method_types=["card"],
        setup_future_usage="on_session",
        )

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
         }
    return render(request, 'checkout/checkout.html', context)


# below to process order once may payment button is clicked
# date time generates order id
def processOrder(request):
	
    transaction_id = datetime.datetime.now().timestamp()
    # below used to parse a valid JSON string
    # and convert it into a Python Dictionary, so the views can read it
    data = json.loads(request.body)
    # below is some logic to get info from logged in users
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        # make sure the total received matches the cart total, and if so, save the order
    if total == order.get_cart_total:
        order.complete = True
        order.save()
    
    # create an instance of the shipping data
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            county=data['shipping']['county'],
            postcode=data['shipping']['postcode'],
            )
    
    return JsonResponse('Payment submitted...', safe=False)
