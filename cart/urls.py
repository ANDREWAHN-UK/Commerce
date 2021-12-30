from django.urls import path
from . import views
import json
from django.http import JsonResponse


# urlpatterns = [
#     path('', views.cart, name='cart'),
#     path('update_item/', views.updateItem, name="update_item"),
# ]

urlpatterns = [
    path('', views.cart, name='cart'),
    # path('', views.view_cart, name='view_cart'),
    # path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    # path('update/<item_id>/', views.update_cart, name='update_cart'),
    # path('remove/<item_id>/', views.remove_from_cart, name='remove_from_cart'),

]