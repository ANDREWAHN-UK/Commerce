from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Product, Customer

# Create your views here.


def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/store.html', context)