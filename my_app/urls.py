from django.urls import path
from .views import Items

urlpatterns = [
    path('items/', Items.as_view(), name='items'),
    path('items/<int:item_id>', Items.as_view(), name='items'),
]
