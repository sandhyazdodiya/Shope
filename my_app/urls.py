from django.urls import path
from .views import Items, ItemsUsingSerializer, csrf_token_api, session_login_api, session_logout_api,token_login_api, token_logout_api
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('items/', Items.as_view(), name='items'),
    path('items/<int:item_id>', Items.as_view(), name='items'),
    path('items_using_serializer/', ItemsUsingSerializer.as_view(), name='items_using_serializer'),
    path('items_using_serializer/<int:item_id>', ItemsUsingSerializer.as_view(), name='items_using_serializer'),
    path('csrf_token', csrf_token_api, name='csrf_token'),
    path('session_login_api', session_login_api, name='session_login_api'), # need to use csrf
    path('session_logout_api', session_logout_api, name='session_logout_api'), # need to use csrf
    path('token_login_api', token_login_api, name='token_login_api'),
    path('token_logout_api', token_logout_api, name='token_logout_api')


    # path('login_jwt_token/', TokenObtainPairView.as_view()),
    # path('login_jwt_token/refresh/', TokenRefreshView.as_view()),
]
