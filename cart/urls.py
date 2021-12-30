from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_cart, name='cart'),
    path('update_item/', views.updateItem, name="update_item"),
]