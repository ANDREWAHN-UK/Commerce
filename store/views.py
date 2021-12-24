from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from store.models import Product
from checkout.models import Order, OrderItem
from django.http import JsonResponse
import json


# Create your views here.

# refer to cart for the logic
def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		# Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'store/store.html', context)


# below to update items once the relevant buttons are clicked
def updateItem(request):

	# retrieve relevant info
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	# link info to the classes in models.py
	# get or create here to allow the editing of a cart item 
	# without having to reload the page. 
	# get or create documentation (requires lots of tea to understand)
	#  - https://www.kite.com/python/docs/django.db.models.QuerySet.get_or_create
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	# set the logic of what the buttons do, which links to the up/down arrows.
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	# instead of using a specific remove function,
	#  this just tells the cart that if an item is at 0,
	#  to delete that item entirely
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)
