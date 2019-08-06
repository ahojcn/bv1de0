from django.urls import path

from .views import user

urlpatterns = [
    path('userRegister/', user.UserRegisterView.as_view(), name="user-register")
]
