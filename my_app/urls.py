from django.urls import path
from .views import Items, ItemsUsingSerializer, csrf_token_api

urlpatterns = [
    path('items/', Items.as_view(), name='items'),
    path('items/<int:item_id>', Items.as_view(), name='items'),
    path('items_using_serializer/', ItemsUsingSerializer.as_view(), name='items_using_serializer'),
    path('items_using_serializer/<int:item_id>', ItemsUsingSerializer.as_view(), name='items_using_serializer'),
    path('csrf_token', csrf_token_api, name='csrf_token'),


]
