from django.urls import path

from apps.video.views import (
    VideoViewSet,
    VideoCategoryViewSet
)

urlpatterns = [
    path('all/', VideoViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path('all/<int:pk>/', VideoViewSet.as_view({
        'get': 'retrieve',
        # 'put': 'update',
    })),

    path('category/', VideoCategoryViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path('category/<int:pk>/', VideoCategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),
]
