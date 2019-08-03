from django.urls import path, include
from . import views

urlpatterns = [
    # path('student/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    # path('', views.StudentList.as_view(), name='student-list'),
    path('student/', views.StudentLC.as_view(), name='student-list-create'),
]
