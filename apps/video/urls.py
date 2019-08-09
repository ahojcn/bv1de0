from django.urls import path

from apps.video.views import VideoViewSet

urlpatterns = [
    path('all/', VideoViewSet.as_view({
        "get": "list",
    })),
    path('all/<int:pk>/', VideoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),
]
