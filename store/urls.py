from django.urls import path
from . import views
from cart.views import *
import json
from django.http import JsonResponse

urlpatterns = [
    path('', views.store, name='store'),
    path('update_item/', views.updateItem, name="update_item"),
]
