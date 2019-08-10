from django.urls import path

from apps.comment.views import CommentViewSet

urlpatterns = [
    path('<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),
    path('', CommentViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
]
