from django.shortcuts import render, get_object_or_404, reverse
from store.models import  Product
from checkout.models import Order

# Create your views here.


# see documentation on get or create https://docs.djangoproject.com/en/4.0/ref/models/querysets/#get-or-create

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        # this is because the template will loop through the whole list, so 
        # there needs to be something here
        items = []	
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart/cart.html', context)

