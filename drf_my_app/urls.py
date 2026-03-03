from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, ItemAPIView, ItemModelSerializerView, ItemModelViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'item', ItemViewSet, basename='list-post')
router.register(r'item_using_model_view_set', ItemViewSet, basename='model-view-set')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('item_using_apiview', ItemAPIView.as_view(), name='item_apiview'),
    path('item_using_apiview/<int:item_id>', ItemAPIView.as_view(), name='item_apiview'),
    path('item_using_model_serializer', ItemModelSerializerView.as_view(), name='item_apiview'),
    path('item_using_model_serializer/<int:item_id>', ItemModelSerializerView.as_view(), name='item_apiview'),
]