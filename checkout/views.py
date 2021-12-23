from django.shortcuts import render

# Create your views here.

def checkout(request):
    context = {}
    return render(request, 'checkout/checkout.html', context)