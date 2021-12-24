from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Product, Customer
from django.http import JsonResponse

# Create your views here.


def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/store.html', context)


def updateItem(request):
	return JsonResponse('Item was added', safe=False)