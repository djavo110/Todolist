from django.urls import path
from todolist.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)
urlpatterns = [
    path('login/', LoginUser.as_view()),
    path('todolist/', TodolistView.as_view()),
    path('todolist/<int:pk>/', TodolistView.as_view()),
    path('staffregister/', StaffRegister.as_view()),
    path('api/token/', LoginUser.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

