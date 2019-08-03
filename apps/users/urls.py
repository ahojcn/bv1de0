from django.urls import path, include
from . import views

urlpatterns = [
    path('user/', views.StudentList.as_view(), name='student-list'),
    path('user/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
]
