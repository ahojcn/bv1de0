from django.urls import path
from apps.user.views import (
    UserLoginView,
    UserRegisterView,
    UserActiveView,
    UserHomeView
)
from django.conf import settings

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('active/', UserActiveView.as_view(), name="active"),

    path('home/', UserHomeView.as_view({
        "get": "list",
    }), name="home"),
    path('home/<int:pk>/', UserHomeView.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),
]
