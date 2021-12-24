from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('update_item/', views.updateItem, name="update_item"),
]
